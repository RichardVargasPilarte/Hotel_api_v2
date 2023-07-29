import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def enviar_correo_zoho(para, asunto, cuerpo):
    # Configuración del servidor SMTP de Zoho
    servidor_smtp = 'smtp.zoho.com'
    puerto_smtp = 587
    correo_emisor = 'ricardo.pilarte@zohomail.com'  # Reemplaza con tu dirección de correo Zoho
    contraseña = 'TFj55S$bswYv4xb'  # Reemplaza con tu contraseña de Zoho

    # Crear el objeto de mensaje MIME
    mensaje = MIMEMultipart()
    mensaje['From'] = correo_emisor
    mensaje['To'] = para
    mensaje['Subject'] = asunto

    # Agregar el cuerpo del mensaje al objeto MIME
    mensaje.attach(MIMEText(cuerpo, 'plain'))

    # Configurar la conexión SMTP
    servidor = smtplib.SMTP(servidor_smtp, puerto_smtp)
    servidor.starttls()  # Habilitar el modo de encriptación TLS
    servidor.login(correo_emisor, contraseña)

    # Enviar el correo
    servidor.sendmail(correo_emisor, para, mensaje.as_string())

    # Cerrar la conexión SMTP
    servidor.quit()

# Ejemplo de uso
para = 'ricardo.pilarte94@gmail.com'
asunto = 'Prueba de correo desde Zoho y Django'
cuerpo = '¡Hola! Este es un correo de prueba enviado desde Zoho y Django.'
enviar_correo_zoho(para, asunto, cuerpo)
