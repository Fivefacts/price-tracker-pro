import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class EmailService:
    def __init__(self):
        self.smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.environ.get('SMTP_PORT', 587))
        self.sender_email = os.environ.get('SENDER_EMAIL', '')
        self.sender_password = os.environ.get('SENDER_PASSWORD', '')
    
    def send_price_alert(self, recipient_email, product_name, current_price, product_url):
        """Envoyer une alerte de prix"""
        if not self.sender_email or not self.sender_password:
            print("Email credentials not configured")
            return False
        
        subject = f"🔥 Alerte Prix : {product_name}"
        
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
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = self.sender_email
            message['To'] = recipient_email
            
            html_part = MIMEText(html_body, 'html')
            message.attach(html_part)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            print(f"Email sent to {recipient_email}")
            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False
