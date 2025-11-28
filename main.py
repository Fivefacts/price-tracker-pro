from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os

from models import db, User, Product, PriceHistory
from scraper import PriceScraper
from email_service import EmailService

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pricetracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

scraper = PriceScraper()
email_service = EmailService()

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Routes d'authentification
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(email=email).first():
            flash('Email déjà utilisé', 'error')
            return redirect(url_for('register'))
        
        user = User(
            email=email,
            password=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        
        flash('Email ou mot de passe incorrect', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Routes principales
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    products = Product.query.filter_by(user_id=current_user.id).all()
    
    # Limites selon le plan
    max_products = 999 if current_user.is_premium else 3
    can_add_more = len(products) < max_products
    
    return render_template('dashboard.html', 
                         products=products, 
                         can_add_more=can_add_more,
                         max_products=max_products)

@app.route('/add-product', methods=['POST'])
@login_required
def add_product():
    """Ajouter un nouveau produit à surveiller"""
    url = request.form.get('url')
    target_price = request.form.get('target_price')
    product_name_manual = request.form.get('product_name')
    current_price_manual = request.form.get('current_price')
    
    # Vérifier la limite de produits
    products_count = Product.query.filter_by(user_id=current_user.id).count()
    max_products = 999 if current_user.is_premium else 3
    
    if products_count >= max_products:
        flash(f'Limite de {max_products} produits atteinte. Passez Premium pour plus !', 'error')
        return redirect(url_for('dashboard'))
    
    # MODE MANUEL : Si le nom et le prix sont fournis manuellement
    if product_name_manual and current_price_manual:
        name = product_name_manual
        try:
            price = float(current_price_manual)
        except:
            flash('Prix invalide', 'error')
            return redirect(url_for('dashboard'))
    else:
        # MODE AUTO : Essayer d'extraire automatiquement
        name, price = scraper.get_price(url)
        
        if price is None:
            flash('Impossible de récupérer le prix automatiquement. Utilisez le mode manuel ci-dessous.', 'error')
            return redirect(url_for('dashboard'))

    # Créer le produit
    product = Product(
        user_id=current_user.id,
        url=url,
        name=name,
        current_price=price,
        target_price=float(target_price) if target_price else None,
        last_checked=datetime.utcnow()
    )
    db.session.add(product)
    
    # Ajouter l'historique
    history = PriceHistory(product=product, price=price)
    db.session.add(history)
    
    db.session.commit()
    
    flash('Produit ajouté avec succès !', 'success')
    return redirect(url_for('dashboard'))

@app.route('/delete-product/<int:product_id>')
@login_required
def delete_product(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        return redirect(url_for('dashboard'))
    
    if product.user_id != current_user.id:
        flash('Accès non autorisé', 'error')
        return redirect(url_for('dashboard'))
    
    db.session.delete(product)
    db.session.commit()
    
    flash('Produit supprimé', 'success')
    return redirect(url_for('dashboard'))

@app.route('/update-target-price/<int:product_id>', methods=['POST'])
@login_required
def update_target_price(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({'success': False, 'message': 'Produit non trouvé'}), 404
    
    # Vérifier que le produit appartient bien à l'utilisateur
    if product.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Accès non autorisé'}), 403
    
    new_target_price = request.json.get('target_price')
    
    try:
        if new_target_price and new_target_price.strip():
            product.target_price = float(new_target_price)
        else:
            product.target_price = None  # Supprimer le prix cible
        
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Prix cible mis à jour !',
            'new_target_price': product.target_price
        })
    except ValueError:
        return jsonify({'success': False, 'message': 'Prix invalide'}), 400

@app.route('/upgrade')
@login_required
def upgrade():
    return render_template('upgrade.html')

@app.route('/api/check-prices')
def check_all_prices():
    """API endpoint pour vérifier tous les prix"""
    products = Product.query.filter_by(is_active=True).all()
    alerts_sent = 0
    
    for product in products:
        name, price = scraper.get_price(product.url)
        
        # Si le scraping échoue mais qu'on a déjà un prix, on utilise le prix existant
        if not price and product.current_price:
            price = product.current_price
            print(f"⚠️ Scraping échoué, utilisation du prix existant: {price}€")
        
        if price:
            product.current_price = price
            product.last_checked = datetime.utcnow()
            
            # Enregistrer l'historique
            history = PriceHistory(product_id=product.id, price=price)
            db.session.add(history)
            
            # Envoyer email si prix cible atteint
            if product.target_price and price <= product.target_price:
    		user = db.session.get(User, product.user_id)
                print(f"📧 Envoi d'email à {user.email} pour {product.name} (prix: {price}€, cible: {product.target_price}€)")
                email_service.send_price_alert(user.email, product.name, price, product.url)
                alerts_sent += 1
    
    db.session.commit()
    return jsonify({
        'status': 'success', 
        'checked': len(products),
        'alerts_sent': alerts_sent
    })

# Scheduler pour vérifier les prix régulièrement
def init_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=lambda: app.test_client().get('/api/check-prices'),
        trigger='interval',
        hours=6,
        id='price_check_job'
    )
    scheduler.start()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    init_scheduler()
    app.run(debug=True, host='0.0.0.0', port=5000)
