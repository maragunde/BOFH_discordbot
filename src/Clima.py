import discord
from discord import Embed
from datetime import datetime
import aiohttp
from ratelimit import limits
import os
from dotenv import load_dotenv

quince_minutos = 900
load_dotenv()

# Limitamos las API calls por las dudas. Esta libreria es medio negra. Lo dejamos asi por ahora, Mariano del futuro lo va a hacer manual
@limits(calls=15, period=quince_minutos)
async def climafun(interaction, city):

    FechaActual = datetime.now()
    
    
    try:
        url = "http://api.weatherapi.com/v1/current.json" 
        CLIMA_key = os.getenv('WEATHER_key')
        params = {"key": f"{CLIMA_key}","q": city} 
        
        # Llama a la API y trae la data
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as res: # <-- Necesitamos la ciudad para checkear el clima en la API. Este es un parametro obligatorio.
                data = await res.json()
                if res.status == 200:
                    
                    if("error" in data):
                        await interaction.response.send_message("Ubicación no encontrada/invalida", ephemeral=True)
                    location = data["location"]["name"]
                    country = data["location"]["country"]
                    temp_c = data["current"]["temp_c"]
                    feelslike_c = data["current"]["feelslike_c"]
                    humidity = data["current"]["humidity"]
                    vis_km = data["current"]["vis_km"]
                    condition = data["current"]["condition"]["text"]
                    image_url = "http:" + data["current"]["condition"]["icon"]

                    # Log
                    print(FechaActual)
                    print(f"Se ha ejecutado el comando clima por {interaction.user}")

                    # Se crea el embed con los campos del clima
                    embed = Embed(title=f"El clima en {location}, {country}", description=f"A pedido de {interaction.user}", color = discord.Color.green())   
                    embed.add_field(name = "Estado", value =f"{condition}",inline=True)
                    embed.add_field(name = "Temperatura", value =f"C: {temp_c} | ST: {feelslike_c}",inline=True)
                    embed.add_field(name = "Humedad", value =f"   {humidity}%",inline=True)
                    embed.add_field(name = "Visibilidad", value =f"{vis_km}KM",inline=True)
                    embed.set_thumbnail(url=image_url)

                    return embed
    except:
        
        # En caso de error en la API, se imprime el mensaje
        embed = Embed(title=f"Error en la API", description=f"Se ha producido un error", color = discord.Color.green())   
        embed.add_field(name = "Error", value =f"Avisar a algun root",inline=True)
        print("Error en la API")