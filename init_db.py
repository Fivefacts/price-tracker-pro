"""Script pour initialiser la base de données"""
import sys
import os

# Ajouter le dossier app au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import app, db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Base de données créée avec succès !")