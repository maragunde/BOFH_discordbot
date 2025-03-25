import os
import json
import pandas as pd

#########################################################################################################
##########Este Script convierte bulk request de XLS a JSON que vienen de recruiters autorizados##########
#########################################################################################################

# Directorio donde van a parar todos los nuevos spreadsheets con requests
JOBS_FOLDER = os.path.abspath("src/discordjobs/bulk")
OUTPUT_JSON_JOB = os.path.join(JOBS_FOLDER, "job.json")
LOG = os.path.join(JOBS_FOLDER, "DiscordJobsBulk_log.txt")

# Carga y guardado en log de requests ya procesados
def log_requests_procesados():
    if os.path.exists(LOG):
        with open(LOG, "r", encoding="utf-8") as f:
            logged_files = set(f.read().splitlines())
            return logged_files
    return set()

def save_log_requests_procesados(file_name):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(file_name + "\n")

# Hay que definir las columnas que espera el JSON porque sino pincha feo
EXPECTED_COLUMNS = [
    'job_title',      # Cargo/Título
    'company',        # Empresa
    'salary_range',   # Rango salarial
    'job_link',       # Link
    'discord_id',     # Discord ID
    'tags',           # Tags
    'job_description',# Descripción
    'job_scheme',     # Esquema
    'location',       # Ubicación
    'experiencia'     # Experiencia
]

# Convertimos a JSON y appendeamos los jobs
def process_excel(file_path):
    try:
        df = pd.read_excel(file_path, header=None)
        
        print(f"Discord Jobs - ✅ Leyendo nuevo bulk request: {file_path}")
        
        # Asignamos solamente las columnas que necesitamos para que lea bien el file
        columns_to_use = min(len(EXPECTED_COLUMNS), df.shape[1])
        column_mapping = {i: EXPECTED_COLUMNS[i] for i in range(columns_to_use)}
        df = df.rename(columns=column_mapping)
        
        df = df.iloc[1:].reset_index(drop=True)
        
        new_jobs = []
        
        for _, row in df.iterrows():
            job_data = {}
            
            # Checkeamos que el job sea valido revisando que por lo menos tenga job title y company
            if pd.notna(row.get('job_title')) and pd.notna(row.get('company')):
 
                for field in EXPECTED_COLUMNS:
                    if field in row and pd.notna(row[field]):
                        job_data[field] = str(row[field])
                    else:
                        job_data[field] = ""
                
                new_jobs.append(job_data)
                print(f"Discord Jobs - ✅ Job Agregado al JSON: {job_data['job_title']} - {job_data['company']}")
            else:
                print(f"Discord Jobs - ❌ Job no valido - falta info: {row.to_dict()}")
        
        # Carga jobs ya existentes
        existing_jobs = []
        if os.path.exists(OUTPUT_JSON_JOB):
            try:
                with open(OUTPUT_JSON_JOB, 'r', encoding='utf-8') as f:
                    existing_jobs = json.load(f)
            except json.JSONDecodeError:
                existing_jobs = []
        
        # Combinamos todos los jobs y los metemos en un solo JSON
        all_jobs = existing_jobs + new_jobs
    
        with open(OUTPUT_JSON_JOB, "w", encoding="utf-8") as f:
            json.dump(all_jobs, f, indent=4, ensure_ascii=False)
        
        print(f"Discord Jobs - ✅ Agarre {file_path} y agregué {len(new_jobs)} jobs al JSON.")
        print(f"Discord Jobs - ✅ Total jobs in JSON: {len(all_jobs)}")
        return True
    
    except Exception as e:
        print(f"Discord Jobs - ❌ Error procesando el archivo: {file_path}: {e}")
        import traceback
        traceback.print_exc()
        return False

# Labura todos los archivos nuevos
def process_all_new_excels():
    processed_files = log_requests_procesados()
    all_excel_files = [f for f in os.listdir(JOBS_FOLDER) if f.endswith((".xls", ".xlsx"))]
    
    new_files = [f for f in all_excel_files if f not in processed_files]

    if not new_files:
        print("Discord Jobs - ⚠️ No hay nuevos archivos que procesar.")
        return False
    
    # Reseteamos el JSON para proces un nuevo batch
    with open(OUTPUT_JSON_JOB, "w", encoding="utf-8") as f:
        json.dump([], f)
    
    success = False
    for file_name in new_files:
        file_path = os.path.join(JOBS_FOLDER, file_name)
        if process_excel(file_path):
            save_log_requests_procesados(file_name)
            success = True

    print(f"Discord Jobs - ✅ Finalizado con {len(new_files)} archivos")
    return success