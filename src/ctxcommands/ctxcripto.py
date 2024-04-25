import requests
import discord
from datetime import datetime
import json
from ratelimit import limits
import os
from dotenv import load_dotenv

quince_minutos = 900
load_dotenv()

# Limitamos las API calls por las dudas. Esta libreria es medio negra. Lo dejamos asi por ahora, Mariano del futuro lo va a hacer manual
@limits(calls=15, period=quince_minutos)
async def criptofunctx(ctx):
    FechaActual = datetime.now()
  
    try:
        #Llama a la API
        COIN_key = os.getenv('COIN_key')

        url = 'https://api.coinranking.com/v2/coins'
        response = requests.get(url, headers={'Authorization': f'Bearer {COIN_key}'})
            
        if response.status_code == 200:
            #Carga el JSON en Python dictionaro
            json_cripto = json.loads(response.text)          
            preciomoneda = []
                    
            #Recorre el JSON y trate la info de las monedas que elegimos. Appendea en una lista para mostrar
            for coin in json_cripto['data']['coins']:
                if coin['symbol'] in ["BTC", "ETH", "LTC", "USDT", "SHIB", "DOGE", "SOL", "BSV", "BCH"]:
                    nombre = coin["name"],
                    precio = coin["price"],
                    simbolo = coin["symbol"],
                    moneda = {"nombre": nombre, "precio": precio, "simbolo": simbolo}
                    preciomoneda.append(moneda)

            # Log
            print(FechaActual)
            print(f"Se ha ejecutado el comando cripto")

            #Se crea el mensaje ctx para mandar

            mensaje = 'La timba! 🚀 🌕\n'
            for moneda in preciomoneda:
                mensaje += f"{moneda['nombre'][0]} -  ({moneda['simbolo'][0]}) USD = {round(float(moneda['precio'][0]),3)}\n"

            await ctx.send(mensaje)      

    except Exception as e:
        print(f"Error en la API: {e}")
        await ctx.send(f"Error. Pincho la API. Error {response.status_code}")