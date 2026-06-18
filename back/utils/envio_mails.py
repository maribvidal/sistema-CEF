import smtplib
from email.mime.text import MIMEText
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_id

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

def enviar_mail_confirmacion_asistencia(id_usuario: int, cursor):
    """Función que envía un correo electrónico al usuario para avisarle que
        puede tener una reserva para una clase en la cual estaba esperando."""
    consulta = consultar_usuario_por_id(id_usuario, cursor)
    correo = consulta["data"]["correo"]

    enviar_mail(correo, "Buenos días, tiene la posibilidad de reservar si lo desea.")
