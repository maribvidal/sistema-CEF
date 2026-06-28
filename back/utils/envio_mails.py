import smtplib
from email.mime.text import MIMEText
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_id

def enviar_mail(correo: str, sujeto: str, mensaje: str):
    """Función que envía un correo electrónico al usuario para restablecer su contraseña."""
    servidor_smtp = "smtp.gmail.com"
    puerto = 587

    msg = MIMEText(mensaje, 'html')
    msg['Subject'] = sujeto
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

    enviar_mail(correo, "Confirmación de asistencia", "Buenos días, tiene la posibilidad de reservar si lo desea.\nHaga click en este enlace para confirmar.")

def enviar_mail_confirmacion_nuevo_correo(id_usuario: int, enlace: str, cursor):
    """Función que envía un correo electrónico al usuario para avisarle que
        su correo ha sido cambiado exitosamente."""
    consulta = consultar_usuario_por_id(id_usuario, cursor)
    correo = consulta["data"]["correo"]

    html = f"Le contactamos desde el equipo del Sistema CEF para que confirme su nuevo correo \ntocando <a href=\"{enlace}\">este enlace.</a>\nSi no fue usted quien realizó este cambio, por favor contacte con el soporte técnico."
    enviar_mail(correo, "Confirmación de cambio de correo", html)
