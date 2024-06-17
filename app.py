import streamlit as st
from streamlit_option_menu import option_menu
import base64
from send_email import send
import re
from google_sheets import GoogleSheets
import uuid
from google_calendar import GoogleCalendar
import numpy as np
import datetime as dt

## FUNCIONES
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def validate_email(email):  #Valida el mail con expresiones regulares
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return True
    else:
        return False

def generate_uid():    #Genera un ID único
    return str(uuid.uuid4())

def add_hour_and_half(time):    #Agrega una hora y media a la hora que se le pase
    parsed_time = dt.datetime.strptime(time, "%H:%M").time()
    new_time = (dt.datetime.combine(dt.date.today(), parsed_time) + dt.timedelta(hours=1, minutes=30)).time()
    return new_time.strftime("%H:%M")
    
##############################################################################
###                            FRONTEND                                    ###
##############################################################################

##VARIABLES############################################################################################
#Datos WEB-APP
page_title = "Diporto Club"
page_icon = "🎾"
layout = "centered"
telefono = "543515926145"
short_tel = "351-5926145"
whatsapp_link = f"https://api.whatsapp.com/send/?phone={telefono}&text&type=phone_number&app_absent=0"
whatsapp_image_path = "assets/wa.png"
instagram_image_path = "assets/insta.png"
instagram_link = "https://www.instagram.com/diporto.club/"
horario = ["08:00", "09:30", "11:00", "12:30", "14:00", "15:30", "17:00", "18:30", "20:00", "21.30"]
#horario2 = ["08:30", "10:00", "11:30", "13:00", "14:30", "16:00", "17:30", "19:00", "20:30", "22.00"]
pistas = ["Pista 1", "Pista 2", "Pista 3", "Pista 4"]

#Datos GoogleSheet BD
document = "app-citas"
sheet_name = "reservas"

#Datos GoogleCalendar
idcalendar1 = "18d7ff1017a3b9639f2ea26953d3add34c176b72a21caaa493a45d3ebd7c3cb6@group.calendar.google.com"
idcalendar2 ="5f7a6c267ba81df73ce577cffa64a255a6ce522a30edc20f086fd836c678b96a@group.calendar.google.com"
time_zone = "America/Argentina/Buenos_Aires"
hora_time_zone = -3
#Credenciales API Google
credentials = st.secrets["google"]["credentials_google"]

########################################################################################################

#CONFIGURACIÓN PÁGINA
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)

#IMAGEN PRINCIPAL
st.image("assets/main.jpg", use_column_width=True)

#TÍTULO Y DIRECCIÓN
st.title("Diporto Club")
st.text("Calle Agustín Piaggio 1150 - Córdoba - CP:5014")

###TABS
selected = option_menu(
    menu_title=None, 
    options=["Reservar", "Pistas", "Detalles"], 
    icons=["calendar-date", "building", "clipboard-minus"],
    orientation="horizontal"
)

###TABS - DETALLES
if selected == "Detalles":
    #Pinta Ubicación Maps
    st.subheader("📍 Ubicación")
    st.markdown("""<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3402.0504538573646!2d-64.18415402452779!3d-31.49529697422551!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x9432a32fb807b679%3A0xef0c6cae4ee3e5ad!2sDiporto%20Club!5e0!3m2!1sen!2sar!4v1718483790877!5m2!1sen!2sar" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>""", unsafe_allow_html=True)
    #Horarios
    st.text("")
    st.subheader("Horarios")
    st.text("Lunes             08:00 a 00:00")
    st.text("Martes            08:00 a 00:00")
    st.text("Miércoles         08:00 a 00:00")
    st.text("Jueves            08:00 a 00:00")
    st.text("Viernes           08:00 a 00:00")
    st.text("Sábado            08:00 a 00:00")
    st.text("Domingo           08:00 a 00:00")
    
    # Contacto
    st.subheader("Contacto")
    # Convierte image en base64
    whatsapp_image_base64 = get_base64_image(whatsapp_image_path)
    # Usa HTML para mostrar la imagen con el link
    st.markdown(f'''
    <a href="{whatsapp_link}" target="_blank">
        <img src="data:image/png;base64,{whatsapp_image_base64}" style="width:50px; height:50px;">
    </a>
    ''', unsafe_allow_html=True)
    st.markdown(f"[{short_tel}]({whatsapp_link})")
 
    #SOCIAL MEDIA
    st.subheader("Instagram")
    # Convierte image en base64
    instagram_image_base64 = get_base64_image(instagram_image_path)
    # Usa HTML para mostrar la imagen con el link
    st.markdown(f'''
    <a href="{instagram_link}" target="_blank">
        <img src="data:image/png;base64,{instagram_image_base64}" style="width:50px; height:50px;">
    </a>
    ''', unsafe_allow_html=True)
    
###TABS - PISTAS
if selected == "Pistas":
    st.image("assets/pista2.jpg", caption="Pista 2")
    
###TABS - RESERVAS
if selected == "Reservar":
    #RESERVAR CANCHA
    st.subheader("Reservar Cancha")
    #with st.form("formulario"):
    #SEPARAR EN COLUMNAS A LOS CAMPOS
    c1, c2 = st.columns(2)
    nombre = c1.text_input("Nombre*")
    mail = c2.text_input("Mail*")
    fecha = c1.date_input("Fecha")
    pista = c2.selectbox("Pista", pistas)
    #Busca el horario no ocupado en el calendario de cada pista
    if fecha:
        if pista == "Pista 1":
            id = idcalendar1
        elif pista == "Pista 2":
            id = idcalendar2
        calendar = GoogleCalendar(credentials, id)
        hours_blocked = calendar.get_events_start_time(str(fecha))
        #Resta la lista con el horario de las horas con eventos agendadas
        result_hours = np.setdiff1d(horario, hours_blocked)

    #Selecciona horario según pista
    hora = c1.selectbox("Hora", result_hours)
    
    notas = c2.text_area("Notas")
    
    #Enviar
    enviar = st.button("Reservar", type="primary")

##############################################################################
###                            BACKEND                                    ###
##############################################################################
    ## VALIDACIONES FORMULARIO
    if enviar:
        #Crea un spiner de carga cuando pulsa el botón enviar
        with st.spinner("Cargando..."):
            if nombre == "":
                st.warning("El nombre es obligatorio")
            elif mail == "":
                st.warning("El mail es obligatorio")
            elif not validate_email(mail):
                st.warning("El mail no es válido")
            elif fecha == "":
                st.warning("La fecha es obligatoria")
            elif hora == "":
                st.warning("La hora es obligatoria")
            elif pista == "":
                st.warning("Elija una Pista")
            else:
                ##CREAR EVENTO GOOGLECALENDAR############################
                #Fecha en formato UTC
                parsed_time = dt.datetime.strptime(hora, "%H:%M").time()
                hours1 = parsed_time.hour
                minutes1 = parsed_time.minute
                
                end_hours = add_hour_and_half(hora)
                parsed_time2 = dt.datetime.strptime(end_hours, "%H:%M").time()
                hours2 = parsed_time2.hour
                minutes2 = parsed_time2.minute
                
                
                start_time = dt.datetime(fecha.year, fecha.month, fecha.day, hours1 + hora_time_zone, minutes1).astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
                end_time = dt.datetime(fecha.year, fecha.month, fecha.day, hours2 + hora_time_zone, minutes2).astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
                
                calendar = GoogleCalendar(credentials, id)
                
                
                #Crea el evento ingresando todos los datos del mismo
                calendar.create_event(nombre, start_time, end_time, time_zone)
                
                
                #########################################################                
                
                ##CREAR REGISTRO EN GOOGLESHEET###############################
                #Crea ID único para el registro                              #
                uid = generate_uid()                                         #
                #Datos a escribir en la BD                                   #
                data = [[nombre, mail, pista, str(fecha), hora, notas, uid]] #
                #Se crea objeto GoogleSheet con nuestro Excel de BD          #
                gs = GoogleSheets(credentials, document, sheet_name)         #
                #Se obtiene el rango de la última fila                       #
                range = gs.get_last_row_range()                              #
                #Se registran los datos en el rango de la última fila        #
                gs.write_data(range, data)                                   #
                ##############################################################
                
                ##ENVIAR MAIL############################################
                send(mail, nombre, fecha, hora, pista, notas)           #
                #########################################################
                
                st.success("Su pista ha sido reservada")
                    
        
        