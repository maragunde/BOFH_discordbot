import requests
import discord
from datetime import datetime
import json
from ratelimit import limits

quince_minutos = 900

# Limitamos las API calls por las dudas. Esta libreria es medio negra. Lo dejamos asi por ahora, Mariano del futuro lo va a hacer manual
@limits(calls=15, period=quince_minutos)
async def dolarfunctx(ctx, inputpesos):

    FechaActual = datetime.now()
    print(inputpesos)

    try:

        # Convierte inputpesos para calcular
        

        # Llama a la API
        response = requests.get("https://dolarapi.com/v1/dolares")

        if response.status_code == 200:

            # Carga el JSON en Python dictionary
            json_dolar = json.loads(response.text)          
            preciosdolares = response.json()
            dolares = []

            # Log
            print(FechaActual)
            print(f"Se ha ejecutado el comando dolar")

            if inputpesos is None:
            
                # Trae datos del precio del dolar para meter en el embed 
                for casa in preciosdolares:
                    nombre = casa["nombre"]
                    preciocompra = casa["compra"]
                    precioventa = casa["venta"]
                    dolar = {"nombre": nombre, "preciocompra": preciocompra, "precioventa": precioventa}
                    dolares.append(dolar)

                # Se crea el mensaje ctx para mandar
                mensaje = 'El precio del dolar 💸\n'
                for dolar in dolares:
                    mensaje += f"{dolar['nombre']} --> Compra = {dolar['preciocompra']}   |   Venta = {dolar['precioventa']}\n"

                await ctx.send(mensaje)

            else:
                inputpesos = float(inputpesos)
                 # Trae datos del precio del dolar para meter en el embed 
                for casa in preciosdolares:
                    nombre = casa["nombre"]
                    preciocompra = casa["compra"]
                    precioventa = casa["venta"]
                    dolar = {"nombre": nombre, "preciocompra": preciocompra, "precioventa": precioventa}
                    dolares.append(dolar)
               
                # Se crea el mensaje ctx para mandar con el input del usuario
                mensaje = 'El precio del dolar 💸\n'
                for dolar in dolares:
                    mensaje += f"{dolar['nombre']} --> Compra = ${inputpesos * float(dolar['preciocompra'])}\n"

                    
                await ctx.send(mensaje)

    except Exception as e:
        print(f"Error en la API: {e}")
        await ctx.send(f"Error. Pincho la API. Error {response.status_code}")
    
    

