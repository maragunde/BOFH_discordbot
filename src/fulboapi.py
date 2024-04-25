import discord
from discord import Embed
import json
import http.client
import datetime
from ratelimit import limits
import os
from dotenv import load_dotenv

#Funcion principal con la data de la fecha para calcular

load_dotenv()
quince_minutos = 900

# Limitamos las API calls por las dudas. Esta libreria es medio negra. Lo dejamos asi por ahora, Mariano del futuro lo va a hacer manual
@limits(calls=2, period=quince_minutos)
async def fulboapicall(liga, interaction, emojiliga):
    try:
        out_format = "%Y-%m-%d"
        FechaActual = datetime.datetime.now() # <-- Para el log
        fechapedida = datetime.date.today() # <-- Para calcular la fecha
        fechapedida_string = fechapedida.strftime(out_format)
        fechadesde = datetime.date.today() - datetime.timedelta(days=7)
        fechadesde_string = fechadesde.strftime(out_format)

    #Llama a la API - pasamos parametro de la fecha de hoy, y trae siempre los resultados de la ultima semana
        FULBO_token = os.getenv('FULBO_token')
        connection = http.client.HTTPConnection('api.football-data.org')
        headers = { 'X-Auth-Token': f'{FULBO_token}' }
        connection.request('GET', f'/v4/competitions/{liga}/matches?dateFrom={fechadesde_string}&dateTo={fechapedida_string}', None, headers )
        response = json.loads(connection.getresponse().read().decode())
        ligacompleta = response["competition"]["name"]
        partidos = []

        #Recorre el Json para traer los resultados de la ultima fecha   
        for partido in response["matches"]:
            nombrelocal = partido["homeTeam"]["name"]
            nombrevisitante = partido["awayTeam"]["name"]
            scorelocal = partido["score"]["fullTime"]["home"]
            scorevisitante = partido["score"]["fullTime"]["away"]
            fecha = partido["matchday"]
            partido = {"nombrelocal": nombrelocal, "nombrevisitante": nombrevisitante, "scorelocal": scorelocal, "scorevisitante": scorevisitante, "fecha": fecha}
            partidos.append(partido)

        # Log
        print (FechaActual)
        print(f"Se ha ejecutado el comando fulbo por {interaction.user}")
        print("Independiente sos amargo")

        #Se crea el embed con la info y se manda a fulbo.py
        embed = Embed(title=f"Ultimos resultados {ligacompleta} {emojiliga}", description=f"A pedido de {interaction.user}", color = discord.Color.green())
        for i in partidos:
            embed.add_field(name =f"Partido por fecha {i['fecha']}", value =f"{i['nombrelocal']} {i['scorelocal']}   -   {i['scorevisitante']} {i['nombrevisitante']}")         
        return embed
    
    except Exception as e:
        print(f"Error en la API: {e}")