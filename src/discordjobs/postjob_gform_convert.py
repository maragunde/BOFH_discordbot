import os
import json
from datetime import datetime
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

load_dotenv()

################# SETUP #################
jobs_gdrive_service = os.getenv('jobs_gdrive_service')
jobs_sheetid = os.getenv('jobs_sheetid')
jobs_sheetname = os.getenv('jobs_sheetname', 'Respuestas')
output_json = "src/discordjobs/gform_job.json"
row_log = "src/discordjobs/DiscordJobsGform_log.txt"

# Conecta a la API de Google Sheet
def setup_sheets_service():
    try:
        # Esto es para forzar las credenciales cada vez que se conecta a la API de Google, que es muy hinchapelotas
        if os.path.exists(jobs_gdrive_service) and jobs_gdrive_service.endswith('.json'):
            # En el caso de file path
            with open(jobs_gdrive_service, 'r') as f:
                service_account_info = json.load(f)
            
            credentials = service_account.Credentials.from_service_account_info(
                service_account_info,
                scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
            )
        else:
            # En el caso de JSON string
            credentials = service_account.Credentials.from_service_account_info(
                json.loads(jobs_gdrive_service),
                scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
            )
        
        # Crea un servicio de conexion nuevo
        return build('sheets', 'v4', credentials=credentials, cache_discovery=False)
    except Exception as e:
        print(f"Discord Jobs (Gform) - ❌ Error de autenticacion con Google Sheet: {e}")
        return None

################# LABURO DE SPREADSHEET #################

# Fetcheamos la data de la sheet
def get_sheet_data(service, spreadsheet_id, sheet_name):
    try:
        # Esto es para traer la sheet por el nombre, pero no me estaria andando

        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=f"'{sheet_name}'!B:L"  # Trae solo las columnas que sirven del form. Modificar si se modifica el form
        ).execute()
        return result.get('values', [])
    except Exception as e:
        
        # Por si pincha, trae la sheet por index
        print(f"Discord Jobs (Gform) - ⚠️ Error accediendo a la sheet por nombre: {e}")
        print(f"Discord Jobs (Gform) - 🔍 Trayendo sheets.")
        
        try:
            # Trae metadata
            sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
            sheets = sheet_metadata.get('sheets', [])
            
            # En caso de que algo pinche, usa siempre la primera sheet del spreadsheet
            if sheets:
                first_sheet = sheets[0]['properties']['title']
                print(f"Discord Jobs (Gform) - 🔹 Usando sheet: {first_sheet}")
                
                result = service.spreadsheets().values().get(
                    spreadsheetId=spreadsheet_id,
                    range=f"'{first_sheet}'"
                ).execute()
                return result.get('values', [])
        except Exception as inner_e:
            print(f"Discord Jobs (Gform) - ❌ Error obteniendo sheets: {inner_e}")
        
        raise e

# Traemos del log para chequear lo ulitmo procesado
def ultimo_index_procesado(verbose=True):
    try:
        if os.path.exists(row_log):
            with open(row_log, 'r') as f:
                content = f.read().strip()
                if content:
                    index = int(content)
                    if verbose:
                        print(f"Discord Jobs (Gform) - 📃 Última row procesada: {index}")
                    return index
                else:
                    print(f"Discord Jobs (Gform) - ⚠️ Fuck el log esta vacío! ya fue, arranco desde la row 1")
                    return 1
        else:
            print(f"Discord Jobs (Gform) - 🔧 No encontre el archivo de log. Creando archivo")
            with open(row_log, 'w') as f:
                f.write("1")  # Saltea el header
            return 1
    except Exception as e:
        print(f"Discord Jobs (Gform) - ⚠️ Error leyendo log: {e}. Ya fue, arranco desde la row 1")
        return 1


# Guardamos la ultima row procesada en el log
def guardaultimarow(index):
    try:
        with open(row_log, 'w') as f:
            f.write(str(index))
        print(f"Discord Jobs (Gform) - 💾 Loggeando row #{index} en el log")
    except Exception as e:
        print(f"Discord Jobs (Gform) - ❌ Error guardando log: {e}")

# Funcion para convertir la data de la sheet a JSON
def convierte_json(headers, new_row):
    new_row.extend([''] * (len(headers) - len(new_row)))
    try:
        # Formateo JSON
        job_data = {
            "job_title": new_row[0],
            "company": new_row[1],
            "salary_range": new_row[2],
            "job_link": new_row[3],
            "discord_id": int(new_row[4]) if new_row[4].isdigit() else None,
            "tags": new_row[5],
            "job_description": new_row[6],
            "job_scheme": new_row[7],
            "location": new_row[8],
            "experiencia": new_row[9],
            "ingles": new_row[10]
        }
    except IndexError:
        print("Discord Jobs (Gform) -❌ Error: El job tiene campos incompletos")
        return None
    return job_data

# Guarda JSON
def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

################# MONITOREO DE NUEVAS ROWS EN GOOGLE SHEET #################
# La ejecutamos con Asyncio

async def checkforjobs(verbose=True):
    if verbose:
        print(f"Discord Jobs (Gform) - ✅ Buscando nuevos jobs en la sheet {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create un servicio nuevo de
    service = setup_sheets_service()
    last_processed_index = ultimo_index_procesado(verbose=verbose)
    new_jobs = []
    
    try:
        data = get_sheet_data(service, jobs_sheetid, jobs_sheetname)
        if not data:
            print("Discord Jobs (Gform) - ⚠️ No se encontraron datos en la sheet")
            return new_jobs
                
        if len(data) <= 1:
            print("Discord Jobs (Gform) - ℹ️ Solamente encontre los headers")
            return new_jobs
        
        headers = data[0]  # Salteamos los headers
        current_row_count = len(data)
        
        if verbose:
            print(f"Discord Jobs (Gform) - 📊 Filas totales: {current_row_count}, Última fila procesada: {last_processed_index}")
        
        # Verifica las ultimas rows para encontrar jobs nuevos
        if current_row_count > last_processed_index:
            print(f"Discord Jobs (Gform) - 🆕 {current_row_count - last_processed_index} nuevos jobs encontrados")
            
            for row_index in range(last_processed_index, current_row_count):
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"Discord Jobs (Gform) - 🔹 {timestamp} - Nuevo job! Procesando row {row_index}...")
                
                new_row = data[row_index]
                json_data = convierte_json(headers, new_row)
                
                if json_data:
                    save_json(json_data, output_json)
                    print(f"Discord Jobs (Gform) - ✅ Job guardado en {output_json}")
                    new_jobs.append(json_data)
            
            # Actualiza las ultimas filas procesadas solamente despues de haber procesado todas las nuevas
            guardaultimarow(current_row_count)
        else:
            if verbose:
                print(f"Discord Jobs (Gform) - ℹ️ No hay nuevos jobs para procesar")
    
    except Exception as e:
        print(f"Discord Jobs (Gform) - ❌ Error: {e}")
    
    return new_jobs