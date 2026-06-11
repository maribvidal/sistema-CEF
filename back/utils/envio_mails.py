import smtplib
from email.mime.text import MIMEText

def enviar_mail(correo: str, mensaje: str):
    """Función que envía un correo electrónico al usuario para restablecer su contraseña."""
    servidor_smtp = "smtp.gmail.com"
    puerto = 587

    msg = MIMEText(mensaje)
    msg['Subject'] = "Restablecer contraseña"
    msg['From'] = "sistemacef@gmail.com"
    msg['To'] = correo

    try:
        server = smtplib.SMTP(servidor_smtp, puerto)
        server.starttls() 
        server.login("sistemacef@gmail.com", "saal ixel tbum pohe")
        
        server.send_message(msg)
    except Exception as e:
        return {
            "error": str(e)
        }, 402
    finally:
        server.quit()