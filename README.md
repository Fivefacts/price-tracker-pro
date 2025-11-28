# 🚀 Price Tracker Pro

**Application web de surveillance de prix pour générer des revenus**

Une application SaaS qui permet aux utilisateurs de surveiller les prix de produits en ligne et de recevoir des alertes automatiques. Modèle freemium : gratuit jusqu'à 3 produits, Premium à 4,99€/mois pour un suivi illimité.

## 💰 Potentiel de Revenus

- **Modèle Freemium** : Version gratuite limitée à 3 produits
- **Plan Premium** : 4,99€/mois pour produits illimités
- **Objectif** : 100 utilisateurs Premium = 499€/mois de revenus récurrents
- **Scalable** : Infrastructure serverless, coûts minimaux

## ✨ Fonctionnalités

### Version Gratuite
- ✅ Surveillance de jusqu'à 3 produits
- ✅ Vérification automatique des prix toutes les 6h
- ✅ Alertes email quand le prix cible est atteint
- ✅ Historique basique des prix

### Version Premium (4,99€/mois)
- ⭐ Produits illimités
- ⭐ Toutes les fonctionnalités gratuites
- ⭐ Support prioritaire
- ⭐ Historique détaillé des prix

## 🛠️ Stack Technique

- **Backend** : Flask (Python)
- **Base de données** : SQLite (facile à migrer vers PostgreSQL)
- **Scraping** : BeautifulSoup4 + Requests
- **Frontend** : Bootstrap 5
- **Paiements** : Stripe
- **Emails** : SMTP
- **Scheduler** : APScheduler

## 📦 Installation

### 1. Cloner le projet
```bash
cd price-tracker-pro
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Configuration
Copiez `.env.example` vers `.env` et configurez vos variables :

```bash
cp .env.example .env
```

Éditez `.env` avec vos informations :
- `SECRET_KEY` : Une clé secrète aléatoire
- `SENDER_EMAIL` et `SENDER_PASSWORD` : Pour les alertes email (Gmail avec mot de passe d'application)
- `STRIPE_*` : Vos clés Stripe pour les paiements

### 4. Initialiser la base de données
```bash
cd app
python app.py
```

L'application sera accessible sur `http://localhost:5000`

## 🚀 Déploiement

### Option 1 : Railway.app (Recommandé - Gratuit pour commencer)
1. Créez un compte sur [Railway.app](https://railway.app)
2. Connectez votre repo GitHub
3. Ajoutez les variables d'environnement
4. Déployez !

### Option 2 : Render.com
1. Créez un compte sur [Render.com](https://render.com)
2. Nouveau Web Service
3. Connectez le repo
4. Build Command : `pip install -r requirements.txt`
5. Start Command : `gunicorn app.app:app`

### Option 3 : Heroku
```bash
heroku create votre-app
heroku addons:create heroku-postgresql:mini
git push heroku main
```

## 💳 Configuration Stripe

1. Créez un compte sur [Stripe](https://stripe.com)
2. Récupérez vos clés API (Dashboard > Developers > API keys)
3. Créez un produit "Premium" à 4,99€/mois
4. Configurez les webhooks pour gérer les abonnements
5. Ajoutez les clés dans `.env`

## 📧 Configuration Email (Gmail)

1. Activez la validation en 2 étapes sur votre compte Gmail
2. Créez un "Mot de passe d'application" :
   - Compte Google > Sécurité > Validation en 2 étapes > Mots de passe d'application
3. Utilisez ce mot de passe dans `SENDER_PASSWORD`

## 📈 Stratégie de Croissance

### Phase 1 : MVP (Semaine 1)
- ✅ Application fonctionnelle
- ✅ Déploiement en ligne
- ✅ Page de landing attrayante

### Phase 2 : Acquisition (Semaines 2-4)
- Partager sur Reddit (r/deals, r/frugal)
- Posts sur Product Hunt
- Groupes Facebook d'économies/bons plans
- SEO pour "price tracker", "amazon price alert"

### Phase 3 : Optimisation (Mois 2-3)
- A/B testing du pricing
- Amélioration du taux de conversion free → premium
- Ajout de sites supportés
- Graphiques d'historique de prix

### Phase 4 : Scale (Mois 4+)
- Marketing par email
- Programme d'affiliation
- API pour développeurs
- Application mobile

## 💡 Améliorations Futures

- [ ] Support de plus de sites e-commerce
- [ ] Graphiques interactifs des prix
- [ ] Notifications push
- [ ] Application mobile (React Native)
- [ ] Comparateur de prix multi-sites
- [ ] Extension navigateur
- [ ] API publique
- [ ] Alertes SMS (premium++)

## 📊 Monitoring

Une fois déployé, surveillez :
- Nombre d'inscriptions quotidiennes
- Taux de conversion gratuit → premium
- Taux de rétention
- Coût d'acquisition client (CAC)
- Lifetime Value (LTV)

## 🎯 Objectifs de Revenus

**Scénario conservateur (6 mois) :**
- 500 utilisateurs gratuits
- 20 utilisateurs premium (4% conversion)
- Revenus : 20 × 4,99€ = **99,80€/mois**

**Scénario optimiste (12 mois) :**
- 2000 utilisateurs gratuits
- 100 utilisateurs premium (5% conversion)
- Revenus : 100 × 4,99€ = **499€/mois**

## 🔒 Sécurité

- Mots de passe hashés avec Werkzeug
- Protection CSRF avec Flask
- Variables d'environnement pour les secrets
- Rate limiting à ajouter pour la production

## 📞 Support

Pour toute question sur l'implémentation, référez-vous au code commenté ou créez une issue.

## 📄 Licence

Projet personnel - Tous droits réservés

---

**Prêt à générer vos premiers revenus ? C'est parti ! 🚀**
