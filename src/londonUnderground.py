import requests
import discord
from discord import Embed
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

def Lines():
    FechaActual = datetime.now()
    api_key = os.getenv('TFL_key')

    # Log
    print(FechaActual)
    print("Se ha ejecutado el comando londonUnderground")

    # Se crea el embed con la respuesta para cada linea
    embed = Embed(title="Estado del subte en Londres", color = discord.Color.green())
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

    
    tube_status = get_tfl_status(api_key)
    if tube_status:
        for line in tube_status:
            line_name = line['name']
            if line['lineStatuses'][0]['statusSeverityDescription'] != 'Good Service':
                lines_status[line_name] = line['lineStatuses'][0]['statusSeverityDescription']

        for line_name, status in lines_status.items():
            if status == 'Good Service':
                embed.add_field(name=f"🟢 {line_name}:", value=status, inline=False)
            else:
                embed.add_field(name=f"🔴 {line_name}:", value=status, inline=False)

        return embed
    else:
        print("Error en el request")
        embed = Embed(title="Estado del subte en Londres", color = discord.Color.green())
        embed.add_field(name="Error en el request. Por favor avisar a algun root.", inline=False)
    
