import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
import time
import random

class PriceScraper:
    """Classe pour extraire les prix des sites e-commerce"""
    
    def __init__(self):
        # En-têtes HTTP plus complets pour mieux simuler un navigateur
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        }
    
    def get_price(self, url):
        """Extraire le prix et le nom d'un produit depuis son URL"""
        try:
            # Ajouter un petit délai aléatoire pour paraître plus humain
            time.sleep(random.uniform(1, 3))
            
            domain = urlparse(url).netloc
            
            # Choisir la méthode selon le site
            if 'amazon' in domain:
                return self._scrape_amazon(url)
            else:
                return self._scrape_generic(url)
        except Exception as e:
            print(f"Erreur lors de l'extraction de {url}: {str(e)}")
            return None, None
    
    def _scrape_amazon(self, url):
        """Extraire le prix d'une page Amazon - Version améliorée"""
        try:
            # Session pour conserver les cookies
            session = requests.Session()
            response = session.get(url, headers=self.headers, timeout=15)
            
            print(f"Status code Amazon: {response.status_code}")  # Debug
            
            if response.status_code != 200:
                print(f"Amazon a bloqué la requête (code {response.status_code})")
                return None, None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraire le nom du produit
            title = soup.find('span', {'id': 'productTitle'})
            if not title:
                title = soup.find('h1', {'id': 'title'})
            
            product_name = title.get_text().strip() if title else "Produit Amazon"
            print(f"Nom trouvé: {product_name}")  # Debug
            
            # Chercher le prix - PLUSIEURS méthodes
            price = None
            
            # Méthode 1: Prix principal
            price_whole = soup.find('span', {'class': 'a-price-whole'})
            price_fraction = soup.find('span', {'class': 'a-price-fraction'})
            if price_whole:
                whole = price_whole.get_text().strip().replace(',', '').replace('.', '')
                fraction = price_fraction.get_text().strip() if price_fraction else '00'
                try:
                    price = float(f"{whole}.{fraction}")
                    print(f"Prix trouvé (méthode 1): {price}")  # Debug
                except:
                    pass
            
            # Méthode 2: Prix dans a-offscreen
            if not price:
                price_offscreen = soup.find('span', {'class': 'a-offscreen'})
                if price_offscreen:
                    price_text = price_offscreen.get_text()
                    price_clean = re.sub(r'[^\d,.]', '', price_text)
                    price_clean = price_clean.replace(',', '.')
                    try:
                        price = float(price_clean)
                        print(f"Prix trouvé (méthode 2): {price}")  # Debug
                    except:
                        pass
            
            # Méthode 3: Ancien format
            if not price:
                for price_id in ['priceblock_ourprice', 'priceblock_dealprice', 'price']:
                    price_elem = soup.find('span', {'id': price_id})
                    if price_elem:
                        price_text = price_elem.get_text()
                        price_clean = re.sub(r'[^\d,.]', '', price_text)
                        price_clean = price_clean.replace(',', '.')
                        try:
                            price = float(price_clean)
                            print(f"Prix trouvé (méthode 3): {price}")  # Debug
                            break
                        except:
                            continue
            
            # Méthode 4: Recherche dans tout le texte (dernier recours)
            if not price:
                text = soup.get_text()
                matches = re.findall(r'(\d+)[,.](\d{2})\s*€', text)
                if matches:
                    try:
                        price = float(f"{matches[0][0]}.{matches[0][1]}")
                        print(f"Prix trouvé (méthode 4): {price}")  # Debug
                    except:
                        pass
            
            if not price:
                print("Aucun prix trouvé avec toutes les méthodes")
            
            return product_name, price
            
        except Exception as e:
            print(f"Erreur Amazon détaillée: {str(e)}")
            import traceback
            traceback.print_exc()
            return None, None
    
    def _scrape_generic(self, url):
        """Extraire le prix d'un site générique"""
        try:
            session = requests.Session()
            response = session.get(url, headers=self.headers, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Chercher le titre
            title = None
            for selector in ['h1', 'title', {'class': 'product-title'}]:
                elem = soup.find(selector)
                if elem:
                    title = elem.get_text().strip()[:100]
                    break
            
            # Chercher le prix avec des expressions régulières
            price = None
            price_patterns = [
                r'€\s*(\d+[.,]\d{2})',
                r'(\d+[.,]\d{2})\s*€',
                r'\$\s*(\d+[.,]\d{2})',
                r'(\d+[.,]\d{2})\s*\$',
            ]
            
            page_text = soup.get_text()
            for pattern in price_patterns:
                match = re.search(pattern, page_text)
                if match:
                    price_str = match.group(1).replace(',', '.')
                    try:
                        price = float(price_str)
                        break
                    except:
                        continue
            
            return title or "Produit", price
        except Exception as e:
            print(f"Erreur générique: {str(e)}")
            return None, None