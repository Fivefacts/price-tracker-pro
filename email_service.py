# Email notification service - Version API SendGrid
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class EmailService:
    def __init__(self):
        # Utiliser la clé API au lieu de SMTP
        self.api_key = os.environ.get('SENDER_PASSWORD', '')
        self.sender_email = os.environ.get('SENDER_EMAIL', '')

    def send_price_alert(self, recipient_email, product_name, current_price, product_url):
        """Envoyer une alerte de prix via l'API SendGrid"""
        print(f"🔧 DEBUG - Configuration email API:")
        print(f"  API Key configured: {'Oui' if self.api_key else 'Non'}")
        print(f"  Sender: {self.sender_email}")
        
        if not self.sender_email or not self.api_key:
            print("❌ Email API credentials not configured")
            return False

        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2 style="color: #4CAF50;">Prix Target Atteint ! 🎯</h2>
                <p>Bonne nouvelle ! Le prix de votre produit surveillé a atteint votre objectif.</p>

                <div style="background-color: #f5f5f5; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <h3>{product_name}</h3>
                    <p style="font-size: 24px; color: #4CAF50; font-weight: bold;">
                        Prix actuel : {current_price}€
                    </p>
                </div>

                <a href="{product_url}"
                   style="background-color: #4CAF50; color: white; padding: 10px 20px;
                          text-decoration: none; border-radius: 5px; display: inline-block;">
                    Voir le produit
                </a>

                <p style="margin-top: 30px; color: #666; font-size: 12px;">
                    Price Tracker Pro - Votre assistant de surveillance de prix
                </p>
            </body>
        </html>
        """

        try:
            print("📧 Envoi via API SendGrid...")
            message = Mail(
                from_email=self.sender_email,
                to_emails=recipient_email,
                subject=f"🔥 Alerte Prix : {product_name}",
                html_content=html_body
            )
            
            sg = SendGridAPIClient(self.api_key)
            response = sg.send(message)
            
            print(f"✅ Email sent to {recipient_email} (status: {response.status_code})")
            return True
            
        except Exception as e:
            print(f"❌ ERREUR API SendGrid:")
            print(f"  Type: {type(e).__name__}")
            print(f"  Message: {str(e)}")
            import traceback
            traceback.print_exc()
            return False