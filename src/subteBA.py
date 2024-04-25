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
async def SubteBA(interaction):
    FechaActual = datetime.now()
    
    try:
        #Llama a la API y trae la data
        SUBTE_clientID = os.getenv('SUBTE_clientID')
        SUBTE_clientSecret = os.getenv('SUBTE_clientSecret')
        url = f"https://apitransporte.buenosaires.gob.ar/subtes/serviceAlerts?client_id={SUBTE_clientID}&client_secret={SUBTE_clientSecret}&json=1"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as res:
                data = await res.json()
                if res.status == 200:

                    # Log
                    print(FechaActual)
                    print(f"Se ha ejecutado el comando subteBA por {interaction.user}")

        #La API solo manda entity si hay disrupcion en el servicio en la linea. Sino, no manda nada. Aca chequeamos eso. Por default el servicio esta OK (oh, the irony), a menos que encontremos entity de la linea.
                    errores = []
                    error = data["entity"]
                    i = 0
                    while i < len(error):
                        error[i]['id']
                        errores.append([error[i]['id'],[error[i]['alert']['header_text']['translation'][0]['text']]])
                        i+=1
                    
                    #Se crea el embed con la respuesta
                    embed = Embed(title="Estado del subte", description=f"A pedido de {interaction.user}", color = discord.Color.green())
                    embed.set_thumbnail(url="https://cdn.civitatis.com/argentina/buenos-aires/galeria/mapa-subte-buenos-aires.png")
                    embed.add_field(name = "🟢 Linea A", value ="Funciona con normalidad",inline=False)
                    embed.add_field(name = "🟢 Linea B", value ="Funciona con normalidad",inline=False)
                    embed.add_field(name = "🟢 Linea C", value ="Funciona con normalidad",inline=False)
                    embed.add_field(name = "🟢 Linea D", value ="Funciona con normalidad",inline=False)
                    embed.add_field(name = "🟢 Linea E", value ="Funciona con normalidad",inline=False)
                    embed.add_field(name = "🟢 Linea H", value ="Funciona con normalidad",inline=False)
                    for j in errores:
                        if j[0] == ' Alert_LineaA':
                            embed.set_field_at(index=0,name="🔴 Linea A",value=f"{j[1][0]}",inline=False)
                        if j[0] == 'Alert_LineaB':
                            embed.set_field_at(index=1,name="🔴 Linea B",value=f"{j[1][0]}",inline=False)
                        if j[0] == 'Alert_LineaC':
                            embed.set_field_at(index=2,name="🔴 Linea C",value=f"{j[1][0]}",inline=False)
                        if j[0] == 'Alert_LineaD':
                            embed.set_field_at(index=3,name="🔴 Linea D",value=f"{j[1][0]}",inline=False)
                        if j[0] == 'Alert_LineaE':
                            embed.set_field_at(index=4,name="🔴 Linea E",value=f"{j[1][0]}",inline=False)
                        if j[0] == 'Alert_LineaH':
                            embed.set_field_at(index=5,name="🔴 Linea H",value=f"{j[1][0]}",inline=False)
                    return embed
                
    except:
        #En caso de error en la API, se imprime el mensaje y se crea el embed con la respuesta
        embed = Embed(title=f"Error en la API", description=f"Se ha producido un error", color = discord.Color.green())   
        embed.add_field(name = "Error", value =f"Avisar a algun root",inline=True)
        print("Error en la API")