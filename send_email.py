import smtplib
import streamlit as st
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

##FUNCION ENVIAR MAIL
def send(email, nombre, fecha, hora, pista, notas):
    
    #Credenciales
    user = st.secrets["emails"]["smtp_user"]
    password = st.secrets["emails"]["smtp_password"]
    sender_email = "Diporto Club"
    
    #Configuración servidor
    msg = MIMEMultipart() 
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    
    #Parámetros del mensaje
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = "Reserva de pista en Diporto Club"
    
    #Cuerpo del mensaje
    message = f"""
    Hola {nombre},
    Su reserva ha sido realizada con éxito.
    El día {fecha} a las {hora} tiene reservada la {pista}.
    Detalles: {notas}
    
    Gracias por confiar en nosotros.
    Saludos cordiales.
    """
    #Atachear mensaje
    msg.attach(MIMEText(message, "plain"))
    
    #Conexión al servidor
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(user, password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()
    except smtplib.SMTPException as e:
        st.exception("Error al enviar el email")     