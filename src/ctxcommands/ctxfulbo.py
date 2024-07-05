import discord
import json
import http.client
import datetime
from ratelimit import limits
from discord.ext import commands

quince_minutos = 900

# Limitamos las API calls por las dudas. Esta libreria es medio negra. Lo dejamos asi por ahora, Mariano del futuro lo va a hacer manual
@limits(calls=5, period=quince_minutos)
async def fulbofunctx(ctx, liga):
    try:
        
        # Bloque de calculo de fechas
        out_format = "%Y-%m-%d"
        FechaActual = datetime.datetime.now() # <-- Para el log
        fechapedida = datetime.date.today() # <-- Para calcular la fecha
        fechapedida_string = fechapedida.strftime(out_format)
        fechadesde = datetime.date.today() - datetime.timedelta(days=7)
        fechadesde_string = fechadesde.strftime(out_format)

        # Si el usuario no mando la liga correcta, se imprime el mensaje
        if liga not in ["PL", "BL1", "PD", "FL1", "SA"]:
            await ctx.send("Por favor selecciona una liga: PL = Premiere League, BL1 = Bundesliga, PD = La Liga España, FL1 = Liga Francia, SA = Serie A Italia")
        else:

            # Llama a la API - pasamos parametro de la fecha de hoy, y trae siempre los resultados de la ultima semana
            connection = http.client.HTTPConnection('api.football-data.org')
            headers = { 'X-Auth-Token': f'{FULBO_token}' }
            connection.request('GET', f'/v4/competitions/{liga}/matches?dateFrom={fechadesde_string}&dateTo={fechapedida_string}', None, headers )
            response = json.loads(connection.getresponse().read().decode())
            ligacompleta = response["competition"]["name"]
            partidos = []

            # Recorre el Json para traer los resultados de la ultima fecha   
            todospartidos = f"Ultimos resultados de {ligacompleta}\n"

            # Mensaje en caso de que no haya partidos recientes (response viene vacio)
            if len(response["matches"]) == 0:
                print (FechaActual)
                print(f"Se ha ejecutado el comando fulbo")
                print("Independiente sos amargo")
                await ctx.send("No hay partidos recientes para la liga seleccionada")

            else:

                for partido in response["matches"]:
                    nombrelocal = partido["homeTeam"]["name"]
                    nombrevisitante = partido["awayTeam"]["name"]
                    scorelocal = partido["score"]["fullTime"]["home"]
                    scorevisitante = partido["score"]["fullTime"]["away"]
                    fecha = partido["matchday"]
                    partido_info = f"Partido por fecha {fecha}: {nombrelocal} {scorelocal} - {scorevisitante} {nombrevisitante}\n"
                    todospartidos += partido_info
                
                # Log de ejecucion y se manda el mensaje
                print (FechaActual)
                print(f"Se ha ejecutado el comando fulbo")
                print("Independiente sos amargo")
                await ctx.send(todospartidos)       
    
    except Exception as e:
        print(f"Error en la API: {e}")
        await ctx.send("Error en la API, o limite de API calls excedido")
