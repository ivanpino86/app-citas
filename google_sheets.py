import gspread
 
class GoogleSheets:
    def __init__(self, credentials, document, sheet_name):
        #Autenticación
        self.gc = gspread.service_account_from_dict(credentials)
        #Abre documento Excel
        self.sh = self.gc.open(document)
        #Activa hoja Excel
        self.sheet = self.sh.worksheet(sheet_name)
    
    def write_data(self, range, data):
        #Escribe la información en un rango dado
        self.sheet.update(range, data)
        
    def get_last_row_range(self):
        #Obtiene la última fila con datos y le suma uno
        last_row = len(self.sheet.get_all_values()) + 1
        #Obtiene datos del Excel
        deta = self.sheet.get_values()
        #Rango Inicio A + última fila
        range_start = f"A{last_row}"
        #Rango Fin última columna + última fila
        range_end = f"{chr(ord('A') + len(deta[0]) -1 )}{last_row}"
        #Retorna el rango de la última fila
        return f"{range_start}:{range_end}"
        