import requests
import discord
from discord import Embed
from datetime import datetime
from ratelimit import limits

quince_minutos = 900
# Limitamos las API calls por las dudas. Esta libreria es medio negra. Lo dejamos asi por ahora, Mariano del futuro lo va a hacer manual
@limits(calls=15, period=quince_minutos)
async def eurofun(interaction):
    FechaActual = datetime.now()

    # Llama a las APIs
    responseEuro = requests.get("https://dolarapi.com/v1/cotizaciones/eur")
    if responseEuro.status_code  == 200:
      
      # Carga el JSON en un diccionario de Python
      responseEuro = responseEuro.json()
        
      # Traemos el precio del Euro al valor oficial
      EuroOficialcompra = responseEuro['compra']
      EuroOficialventa = responseEuro['venta']

      # Log
      print(FechaActual)
      print(f"Se ha ejecutado el comando euro por {interaction.user}")

      #Se crea el embed con los precios del dolar
      embed = Embed(title=f"El precio del Euro 💸 ", description=f"A pedido de {interaction.user}", color = discord.Color.green())
      embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Euro_banknotes%2C_Europa_series.png/220px-Euro_banknotes%2C_Europa_series.png")
      embed.add_field(name =f"Cotizacion oficial", value =f"Compra = {EuroOficialcompra}   |   Venta = {EuroOficialventa}", inline=False)
      return embed
    else:
       print(f"Error en la API {responseEuro.status_code}")
       #Se crea el embed
       embed = Embed(title=f"Error en la API ", description=f"A pedido de {interaction.user}", color = discord.Color.green())
       embed.add_field(name ="Error:", value =f"{responseEuro.status_code}", inline=False)
       return embed
