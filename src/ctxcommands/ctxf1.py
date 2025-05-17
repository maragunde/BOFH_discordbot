import discord
from discord.ext import commands
import fastf1
import datetime
import os
from collections import defaultdict
import logging


# Funcion principal usando la API de FastF1 para traer posiciones de la F1.
# Es la unica que encontre gratis que anda masomenos bien, hay que instalarla como requerimiento

# Sacamos todos los logs molestos de la api
logging.getLogger('fastf1').setLevel(logging.WARNING)
logging.getLogger('fastf1').setLevel(logging.ERROR)

os.makedirs('cache', exist_ok=True)
fastf1.Cache.enable_cache('cache')  # Le tenemos que cachear porque la API es un poco lerda

FechaActual = datetime.datetime.now()

# Comando principal para ambas opciones
@commands.command(name='f1')
async def formula1ctxfunc(ctx, texto):
    try:
        async with ctx.typing():
            texto = texto.lower()

            if texto == "temporada":
                await resultados_temporada(ctx)
            elif texto == "carrera":
                await resultados_ultima_carrera(ctx)
            else:
                await ctx.send("Usaste mal el comando. Usa `!f1 temporada` o `!f1 carrera`.")

    except Exception as e:
        await ctx.send(f"Error en el comando de F1: {str(e)}")


# Funcion para los resultados de la temporada
async def resultados_temporada(ctx):
    anio = datetime.datetime.now().year
    schedule = fastf1.get_event_schedule(anio)

    carreras = schedule[schedule['Session5Date'] < datetime.datetime.now(datetime.timezone.utc)]
    if carreras.empty:
        await ctx.send("No hay carreras completadas aún en esta temporada.")
        return

    # Creamos los diccionarios
    driver_points = defaultdict(float)
    driver_teams = {}
    driver_names = {}

    # Scrapea los resultados y los trae para todas las carreras de la temporada
    for _, race in carreras.iterrows():
        try:
            session = fastf1.get_session(anio, race['RoundNumber'], 'RACE')
            session.load(telemetry=False, weather=False, messages=False)
            results = session.results

            if results is None or results.empty:
                continue

            for _, row in results.iterrows():
                driver_id = row['DriverNumber']
                points = row['Points']
                full_name = f"{row['FirstName']} {row['LastName']}"
                team = row['TeamName']

                driver_points[driver_id] += points
                driver_teams[driver_id] = team
                driver_names[driver_id] = full_name

        except Exception as e:
            print(f"Error cargando carrera {race['EventName']}: {e}")
            continue

    standings = sorted(driver_points.items(), key=lambda x: x[1], reverse=True)

    # Creamos el mensaje y lo mandamos
    lines = [f"🏁 **Formula 1 - Clasificación de la temporada {anio}** 🏁\n"]
    for position, (driver_id, total_points) in enumerate(standings, start=1):
        nombre = driver_names[driver_id]
        equipo = driver_teams[driver_id]
        lines.append(f"{position}. {nombre} — {equipo} — {total_points:.0f} pts")

    mensaje = "\n".join(lines)

    # Chequeo en caso de que se pase el limite de 2000 caracteres
    if len(mensaje) > 2000:
        partes = [mensaje[i:i+1990] for i in range(0, len(mensaje), 1990)]
        for parte in partes:
            await ctx.send(f"```{parte}```")
    else:
        await ctx.send(f"```{mensaje}```")

    print(FechaActual)
    print("Comando !f1 ejecutado")


# Funcion para los resultados de la ultima carrera

async def resultados_ultima_carrera(ctx):
    anio = datetime.datetime.now().year
    schedule = fastf1.get_event_schedule(anio)
    past_races = schedule[schedule['Session5Date'] < datetime.datetime.now(datetime.timezone.utc)]

    if past_races.empty:
        await ctx.send("No hay carreras completadas aún en esta temporada.")
        return

    # Traemos los datos de la ultima carrera
    last_race = past_races.iloc[-1]
    session = fastf1.get_session(anio, last_race['RoundNumber'], 'RACE')
    session.load(telemetry=False, weather=False, messages=False)

    resultados = session.results
    if resultados is None or resultados.empty:
        await ctx.send("No se encontraron resultados para la última carrera.")
        return

    # Creamos el mensaje y lo mandamos
    lines = [f"🏁 **Resultados del GP de {last_race['EventName']}** 🏁\n"]

    for _, row in resultados.iterrows():

        pos = row['Position']
        nombre = f"{row['FirstName']} {row['LastName']}"
        equipo = row['TeamName']
        puntos = row['Points']
        status = row['Status']
        lines.append(f"{pos}. {nombre} — {equipo} — {puntos:.0f} pts ({status})")

    mensaje = "\n".join(lines)

    # Chequeo en caso de que se pase el limite de 2000 caracteres
    if len(mensaje) > 2000:
        partes = [mensaje[i:i+1990] for i in range(0, len(mensaje), 1990)]
        for parte in partes:
            await ctx.send(f"```{parte}```")
    else:
        await ctx.send(f"```{mensaje}```")

    # Log
    print(FechaActual)
    print("Comando !f1 ejecutado")