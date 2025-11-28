#!/bin/bash

echo "🚀 Lancement de Price Tracker Pro..."
echo ""

# Vérifier si .env existe
if [ ! -f .env ]; then
    echo "⚠️  Fichier .env manquant. Création depuis .env.example..."
    cp .env.example .env
    echo "✅ Fichier .env créé. Pensez à le configurer avec vos vraies clés !"
    echo ""
fi

# Installer les dépendances si nécessaire
if [ ! -d "venv" ]; then
    echo "📦 Installation des dépendances..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    echo "✅ Dépendances installées !"
    echo ""
fi

# Lancer l'application
echo "🌟 Application disponible sur : http://localhost:5000"
echo "📧 Pensez à configurer vos emails dans .env pour les alertes"
echo "💳 Configurez Stripe dans .env pour accepter les paiements"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter l'application"
echo ""

cd app && python app.py
