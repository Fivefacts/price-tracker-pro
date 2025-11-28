# 🚀 DÉMARRAGE RAPIDE - Price Tracker Pro

## Lancement en 3 minutes

### Étape 1 : Installation
```bash
cd price-tracker-pro
pip install -r requirements.txt
```

### Étape 2 : Configuration (optionnelle pour tester)
```bash
cp .env.example .env
```

### Étape 3 : Lancement
```bash
cd app
python app.py
```

✅ **L'application est maintenant accessible sur : http://localhost:5000**

---

## 🎯 Prochaines étapes pour générer des revenus

### 1. Tester l'application (5 minutes)
- Créez un compte
- Ajoutez un produit Amazon
- Vérifiez que le prix est bien récupéré
- Testez la limite de 3 produits (version gratuite)

### 2. Configurer les emails (10 minutes)
Éditez `.env` :
```
SENDER_EMAIL=votre-email@gmail.com
SENDER_PASSWORD=votre-mot-de-passe-application
```

**Comment obtenir un mot de passe d'application Gmail :**
1. Allez dans votre compte Google
2. Sécurité → Validation en 2 étapes (activez-la)
3. Mots de passe d'application → Générer
4. Copiez le mot de passe dans `.env`

### 3. Déployer en ligne (15 minutes)

**Option A : Railway.app (Recommandé - GRATUIT)**
1. Créez un compte sur https://railway.app
2. "New Project" → "Deploy from GitHub repo"
3. Sélectionnez votre repo
4. Ajoutez les variables d'environnement :
   - `SECRET_KEY` : générez une clé aléatoire
   - `SENDER_EMAIL` : votre email
   - `SENDER_PASSWORD` : votre mot de passe d'application
5. Deploy !

**Option B : Render.com (GRATUIT aussi)**
1. Compte sur https://render.com
2. New → Web Service
3. Connectez votre repo
4. Build : `pip install -r requirements.txt`
5. Start : `gunicorn app.app:app`
6. Ajoutez les variables d'environnement
7. Create Web Service

### 4. Configurer Stripe pour les paiements (20 minutes)

1. **Créez un compte Stripe** : https://stripe.com
2. **Récupérez vos clés** : Dashboard → Developers → API keys
3. **Créez un produit Premium** :
   - Dashboard → Products → Add product
   - Nom : "Price Tracker Premium"
   - Prix : 4,99€/mois (récurrent)
4. **Ajoutez les clés dans `.env`** :
   ```
   STRIPE_PUBLIC_KEY=pk_test_...
   STRIPE_SECRET_KEY=sk_test_...
   ```
5. **Configurez les webhooks** (pour gérer les abonnements) :
   - Dashboard → Developers → Webhooks
   - Add endpoint : `https://votre-app.railway.app/webhook/stripe`
   - Événements : `checkout.session.completed`, `customer.subscription.deleted`

---

## 💰 Générer vos premiers revenus

### Semaine 1 : Acquisition gratuite
- Partagez sur Reddit : r/deals, r/frugal, r/beermoney
- Groupes Facebook de bons plans
- Forums de discussions économies

### Semaine 2-4 : Optimisation
- Postez sur Product Hunt
- Améliorez la page d'accueil
- Ajoutez des témoignages
- Créez du contenu SEO ("comment suivre prix Amazon")

### Mois 2+ : Croissance
- Email marketing aux utilisateurs gratuits
- A/B testing du pricing
- Ajoutez plus de sites supportés
- Créez une extension Chrome

---

## 📊 Objectifs réalistes

**Mois 1-3 (Bootstrap):**
- 100-300 utilisateurs gratuits
- 5-10 utilisateurs premium
- **50-100€/mois** 💰

**Mois 4-6 (Croissance):**
- 500-1000 utilisateurs gratuits
- 25-50 utilisateurs premium
- **125-250€/mois** 💰

**Mois 7-12 (Scale):**
- 2000+ utilisateurs gratuits
- 100+ utilisateurs premium
- **500€+/mois** 💰

---

## ⚡ Checklist de lancement

- [ ] Application testée en local
- [ ] Emails configurés et testés
- [ ] Déployée en ligne (Railway/Render)
- [ ] Stripe configuré
- [ ] Compte créé et testé
- [ ] 1er produit surveillé avec succès
- [ ] Partagé sur 3+ communautés
- [ ] Analytics ajouté (Google Analytics)

---

## 🆘 Besoin d'aide ?

**Problèmes courants :**

1. **"Module not found"** → `pip install -r requirements.txt`
2. **Email ne fonctionne pas** → Vérifiez le mot de passe d'application Gmail
3. **Scraping ne marche pas** → Certains sites bloquent, commencez par Amazon
4. **Stripe ne fonctionne pas** → Utilisez les clés de TEST d'abord

---

**Vous êtes prêt ! Lancez-vous et générez vos premiers revenus ! 🚀💰**
