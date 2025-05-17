import fastf1
import datetime
from collections import defaultdict
import logging
import os
import discord

# Funcion principal usando la API de FastF1 para traer posiciones de la F1.
# Es la unica que encontre gratis que anda masomenos bien, hay que instalarla como requerimiento

# Sacamos todos los logs molestos de la api
logging.getLogger('fastf1').setLevel(logging.WARNING)
logging.getLogger('fastf1').setLevel(logging.ERROR)

os.makedirs('cache', exist_ok=True)
fastf1.Cache.enable_cache('cache')  # Le tenemos que cachear porque la API es un poco lerda

FechaActual = datetime.datetime.now()

# Comando principal para ambas opciones de resultado (carrea o temporada)
async def f1func(interaction: discord.Interaction, opcion: str):
    opcion = opcion.lower()
    
    if opcion == "temporada":
        return await resultados_temporada()
    elif opcion == "carrera":
        return await resultados_ultima_carrera()
    else:
        return "Usa una opción válida: `temporada` o `carrera`."

################################################################################
################################################################################

# Funcion para los resultados de la temporada
async def resultados_temporada():

    anio = datetime.datetime.now().year
    schedule = fastf1.get_event_schedule(anio)
    past_races = schedule[schedule['Session5Date'] < datetime.datetime.now(datetime.timezone.utc)]
    if past_races.empty:
        return "No hay carreras completadas aún en esta temporada."
    
    # Creamos los diccionarios
    pilotos_puntos = defaultdict(float)
    pilotos_equipos = {}
    pilotos_nombres = {}

        # Scrapea los resultados y los trae para todas las carreras de la temporada
    for _, race in past_races.iterrows():
        try:
            session = fastf1.get_session(anio, race['RoundNumber'], 'RACE')
            session.load(telemetry=False, weather=False, messages=False)
            results = session.results

            if results is None or results.empty:
                continue

            for _, row in results.iterrows():
                driver_id = row['DriverNumber']
                puntos = row['Points']
                nombres = f"{row['FirstName']} {row['LastName']}"
                equipos = row['TeamName']

                # Sumamos todo
                pilotos_puntos[driver_id] += puntos
                pilotos_equipos[driver_id] = equipos
                pilotos_nombres[driver_id] = nombres

        except Exception:
            continue

    standings = sorted(pilotos_puntos.items(), key=lambda x: x[1], reverse=True)

    # Creamos el mensaje y lo mandamos
    lines = [f"🏁 **Formula 1 - Clasificación de la temporada {anio}** 🏁\n"]
    for posicion, (driver_id, total_points) in enumerate(standings, start=1):
        nombre = pilotos_nombres[driver_id]
        equipo = pilotos_equipos[driver_id]
        lines.append(f"{posicion}. {nombre} — {equipo} — {total_points:.0f} pts")

    message = "\n".join(lines)
    return message

# Funcion para los resultados de la ultima carrera
async def resultados_ultima_carrera():
    anio = datetime.datetime.now().year
    schedule = fastf1.get_event_schedule(anio)
    carreras = schedule[schedule['Session5Date'] < datetime.datetime.now(datetime.timezone.utc)]
    if carreras.empty:
        return "No hay carreras completadas aún en esta temporada."

    # Traemos los ultimos resultados de la ultima carrera
    ultima_carrera = carreras.iloc[-1]
    session = fastf1.get_session(anio, ultima_carrera['RoundNumber'], 'RACE')
    session.load(telemetry=False, weather=False, messages=False)

    results = session.results
    if results is None or results.empty:
        return "No se encontraron resultados para la última carrera."

    # Creamos el mensaje y lo mandamos
    lines = [f"🏁 **Resultados del último GP: {ultima_carrera['EventName']}** 🏁\n"]
    for _, row in results.iterrows():
        pos = int(row['Position'])
        nombre = f"{row['FirstName']} {row['LastName']}"
        equipo = row['TeamName']
        puntos = row['Points']
        status = row['Status']
        lines.append(f"{pos}. {nombre} — {equipo} — {puntos:.0f} pts ({status})")

    mensaje = "\n".join(lines)
    
    # Log
    print(FechaActual)
    print("Comando Formula 1 ejecutado")

    return mensaje

