import requests
import discord
from discord import Embed
from datetime import datetime
import json
from ratelimit import limits

#Ojala algun dia no haga falta mas este comando

quince_minutos = 900

# Limitamos las API calls por las dudas. Esta libreria es medio negra. Lo dejamos asi por ahora, Mariano del futuro lo va a hacer manual
@limits(calls=15, period=quince_minutos)
async def dolarfun(interaction):

    FechaActual = datetime.now()

    try:
    #Llama a la API
        response = requests.get("https://dolarapi.com/v1/dolares")

        if response.status_code == 200:

        #Carga el JSON en Python dictionary
            json_dolar = json.loads(response.text)          
            preciosdolares = response.json()
            dolares = []

            # Log
            print(FechaActual)
            print(f"Se ha ejecutado el comando dolar por {interaction.user}")
            
        #Trae datos del precio del dolar para meter en el embed 
            for casa in preciosdolares:
                nombre = casa["nombre"]
                preciocompra = casa["compra"]
                precioventa = casa["venta"]
                dolar = {"nombre": nombre, "preciocompra": preciocompra, "precioventa": precioventa}
                dolares.append(dolar)

            #Se crea el embed con los precios del dolar
                embed = Embed(title=f"El precio del dolar 💸 ", description=f"A pedido de {interaction.user}", color = discord.Color.green())
                embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/US_one_dollar_bill%2C_obverse%2C_series_2009.jpg/1200px-US_one_dollar_bill%2C_obverse%2C_series_2009.jpg")
                for dolar in dolares:
                    embed.add_field(name =f"{dolar['nombre']}", value =f"Compra = {dolar['preciocompra']}   |   Venta = {dolar['precioventa']}", inline=False)              
            return embed
        else:
            print(f"Error: {response.status_code}. Pincho la API.")
            print(f"Error en la API {response.status_code}")
    
    except Exception as e:
        print(f"Error en la API: {e}")
    
    

