import requests
import discord
from discord import Embed
from datetime import datetime
import json
from ratelimit import limits

# Ojala algun dia no haga falta mas este comando

quince_minutos = 900

# Limitamos las API calls por las dudas. Esta libreria es medio negra. Lo dejamos asi por ahora, Mariano del futuro lo va a hacer manual
@limits(calls=15, period=quince_minutos)
async def pesosfunctx(ctx, monto):

    FechaActual = datetime.now()

    try:
        # Llama a la API
        response = requests.get("https://dolarapi.com/v1/dolares")

        if response.status_code == 200:

            # Carga el JSON en Python dictionary
            json_dolar = json.loads(response.text)          
            preciosdolares = response.json()
            dolaresconvertidos = []

            # Log
            print(FechaActual)
            print(f"Se ha ejecutado el comando !pesos")
            
            # Parsea el Json, convierte los precios, y appendea a la lista
            for casa in preciosdolares:
                nombre = casa["nombre"]
                preciocompra = casa["compra"]
                precioventa = casa["venta"]
                
                montoendolares = monto / preciocompra
                dolaresconvertidos.append({"nombre": nombre, "montoendolares": montoendolares})

             # Se crea el mensaje ctx para mandar
            mensaje = f'Calculo de {monto} pesos a USD 💸\n'
            for conversion in dolaresconvertidos:
                mensaje += f"{conversion['nombre']} --> Compra = {conversion['montoendolares']:.2f}\n"

            await ctx.send(mensaje)        
    
    except Exception as e:
        print(f"Error en la API: {e}")
        await ctx.send(f"Error. Pincho la API. Error {response.status_code}")


