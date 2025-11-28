# Database initialization script
"""Script pour initialiser la base de données"""
from main import app, db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Base de données créée avec succès !")