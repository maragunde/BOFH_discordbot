import requests
import discord
from datetime import datetime
from ratelimit import limits
import os
from dotenv import load_dotenv

quince_minutos = 900
load_dotenv()


# Limitamos las API calls por las dudas. Esta libreria es medio negra. Lo dejamos asi por ahora, Mariano del futuro lo va a hacer manual
# Para cehquear estado: http://cloud.tfl.gov.uk/TrackerNet/LineStatus
@limits(calls=15, period=quince_minutos)
def get_tfl_status(api_key):

    # Conectamos a la API
    api_key = os.getenv('TFL_key')
    url = f"https://api.tfl.gov.uk/Line/Mode/tube/Status?app_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve data.")
        return None

async def undergroundfunctx(ctx):
    FechaActual = datetime.now()

    # Log
    print(FechaActual)
    print("Se ha ejecutado el comando londonUnderground")

    # Creamos un mensaje para cada linea
    message = "Estado del subte en Londres:\n"
    lines_status = {
        "Bakerloo": "Good Service",
        "Central": "Good Service",
        "Circle": "Good Service",
        "District": "Good Service",
        "Hammersmith & City": "Good Service",
        "Jubilee": "Good Service",
        "Metropolitan": "Good Service",
        "Northern": "Good Service",
        "Piccadilly": "Good Service",
        "Victoria": "Good Service",
        "Waterloo & City": "Good Service"
    }

    # Hacemos el API call y traemos los estados de cada linea
    api_key = '8847defd8a9c48578339178623f278ea'
    tube_status = get_tfl_status(api_key)
    if tube_status:
        for line in tube_status:
            line_name = line['name']
            if line['lineStatuses'][0]['statusSeverityDescription'] != 'Good Service':
                lines_status[line_name] = line['lineStatuses'][0]['statusSeverityDescription']

    # Concatenamos el mensaje para cada linea y se manda el mensaje al canal
        for line_name, status in lines_status.items():
            if status == 'Good Service':
                message += f"🟢 {line_name}: {status}\n"
            else:
                message += f"🔴 {line_name}: {status}\n"   
        await ctx.send(message)
    else:
        print("Error en el request")
        await ctx.send(f"Error en el request. Por favor avisar a algun root.")
