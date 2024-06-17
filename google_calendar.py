from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import streamlit as st
from datetime import datetime

##SE CREA UNA CLASE PARA INTERACTUAR CON LA API DE GOOGLECALENDAR
class GoogleCalendar:
    #Se inicia la clase pasandole las credenciales de google y el id del calendario con el que vamos a interactuar
    def __init__(self, credentials, idcalendar):
        #Se declaran las variables
        self.credentials = credentials
        self. idcalendar = idcalendar
        # Se construye el servicio de Google Calendar con las credenciales creadas
        self.service = build("calendar", "v3", 
                             credentials= service_account.Credentials.from_service_account_info(self.credentials, 
                             scopes= ["https://www.googleapis.com/auth/calendar"]))
        
    def create_event(self, name_event, start_time, end_time, timezone, attendes= None):
        # Define la estructura del evento con los detalles proporcionados
        event = {
            "summary" : name_event,
            "start" :{
                "dateTime" : start_time,
                "timeZone" : timezone,
            },
            
            "end" :{
                "dateTime" : end_time,
                "timeZone" : timezone,
                },
        }
        # Si hay asistentes, los agrega al evento
        if attendes:
            event["attendes"] = [{"email": email} for email in attendes]
            
        ##Creación del evento
        try:
            # Intenta crear el evento en el calendario
            created_event = self.service.events().insert(calendarId = self.idcalendar, body = event).execute()
            
        except HttpError as error:
            # Si ocurre un error HTTP, lanza una excepción con un mensaje de error
            raise Exception(f"An error has ocurred: {error}")
        
        return created_event
    
    def get_events(self, date = None):
        if not date:
            events = self.service.events().list(calendarId = self.idcalendar).execute()
        else:
            start_date = f"{date}T00:00:00Z"
            end_date = f"{date}T23:59:00Z"
            events = self.service.events().list(calendarId = self.idcalendar, timeMin = start_date, timeMax = end_date).execute()
        return events.get("items", [])
    
    def get_events_start_time(self, date):
        #Recupera los eventos del calendario de una determinada fecha
        events = self.get_events(date)
        #Crea lista vacía para incluir las horas de inicio de los eventos
        start_times =[]
        #Bucle para capturar las horas de inicio
        for event in events:
            #Toma del listado el comienzo del evento
            start_time = event["start"]["dateTime"]
            #Se le da formato al string de horas y minutos
            parsed_start_time = datetime.fromisoformat(start_time[:-6])
            hours_minutes = parsed_start_time.strftime("%H:%M")
            #Se agrega al listado las horas de inicio
            start_times.append(hours_minutes)
        #Se retorna la lista
        return start_times