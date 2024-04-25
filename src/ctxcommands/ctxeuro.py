import requests
import discord
from datetime import datetime
from ratelimit import limits

quince_minutos = 900
# Limitamos las API calls por las dudas. Esta libreria es medio negra. Lo dejamos asi por ahora, Mariano del futuro lo va a hacer manual
@limits(calls=15, period=quince_minutos)
async def eurofunctx(ctx):
    FechaActual = datetime.now()

    # Llama a las APIs
    responseEuro = requests.get("https://dolarapi.com/v1/cotizaciones/eur")
    if responseEuro.status_code  == 200:
      
      # Carga el JSON en un diccionario de Python
      responseEuro = responseEuro.json()
      
      print(responseEuro)   
        
      # Traemos el precio del Euro al valor oficial
      EuroOficialcompra = responseEuro['compra']
      EuroOficialventa = responseEuro['venta']
      print("Valor de euro compra (Oficial):", EuroOficialcompra)
      print("Valor de euro venta (Oficial):", EuroOficialventa)

      # Log
      print(FechaActual)
      print(f"Se ha ejecutado el comando euro")

      # Crea el mensaje con los precios del Euro
      message = (f"El precio del Euro 💸\n"
                  f"Cotización oficial --> Compra = {EuroOficialcompra} USD   |   Venta = {EuroOficialventa} USD")
      await ctx.send(message)

    else:
       print(f"Error en la API {responseEuro.status_code}")
      
       # Respuesta de error
       await ctx.send(f"Error en la API: {responseEuro.status_code}. Por favor avisar a algun root ")
