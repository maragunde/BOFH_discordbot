import requests
import discord
from discord import Embed
from datetime import datetime
import json
from ratelimit import limits
import os
from dotenv import load_dotenv

quince_minutos = 900
load_dotenv()

# Limitamos las API calls por las dudas. Esta libreria es medio negra. Lo dejamos asi por ahora, Mariano del futuro lo va a hacer manual
@limits(calls=15, period=quince_minutos)
async def criptofun(interaction):
    FechaActual = datetime.now()
  
    try:
        #Llama a la API
        COIN_key = os.getenv('COIN_key')

        url = 'https://api.coinranking.com/v2/coins'
        response = requests.get(url, headers={'Authorization': f'Bearer {COIN_key}'})
            
        if response.status_code == 200:
            
            # Carga el JSON en Python dictionaro
            json_cripto = json.loads(response.text)          
            preciomoneda = []
                    
            # Recorre el JSON y trate la info de las monedas que elegimos. Appendea en una lista para mostrar
            for coin in json_cripto['data']['coins']:
                if coin['symbol'] in ["BTC", "ETH", "LTC", "USDT", "SHIB", "DOGE", "SOL", "BSV", "BCH"]:
                    nombre = coin["name"],
                    precio = coin["price"],
                    simbolo = coin["symbol"],
                    moneda = {"nombre": nombre, "precio": precio, "simbolo": simbolo}
                    preciomoneda.append(moneda)

            # Log
            print(FechaActual)
            print(f"Se ha ejecutado el comando cripto por {interaction.user}")

            # Se crea el embed con los precios de cripto
            embed = Embed(title=f"La timba! 🚀 🌕", description=f"A pedido de {interaction.user}", color = discord.Color.green())
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/en/d/d0/Dogecoin_Logo.png")              
            for moneda in preciomoneda:
                embed.add_field(name =f"{moneda['nombre'][0]}  ({moneda['simbolo'][0]})", value =f"USD {round(float(moneda['precio'][0]),3)}", inline=False)
            return embed

        else:
            print(f"Error: {response.status_code}. Pincho la API.")
            print(f"Error en la API {response.status_code}")

    except Exception as e:
        print(f"Error en la API: {e}")