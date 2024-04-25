import discord
from datetime import datetime
import aiohttp
from ratelimit import limits
import os
from dotenv import load_dotenv

quince_minutos = 900
load_dotenv()

# Limitamos las API calls por las dudas. Esta libreria es medio negra. Lo dejamos asi por ahora, Mariano del futuro lo va a hacer manual
@limits(calls=15, period=quince_minutos)
async def subtefunctx(ctx):
    FechaActual = datetime.now()
    
    try:
        # Llama a la API y trae la data
        SUBTE_clientID = os.getenv('SUBTE_clientID')
        SUBTE_clientSecret = os.getenv('SUBTE_clientSecret')
        url = f"https://apitransporte.buenosaires.gob.ar/subtes/serviceAlerts?client_id={SUBTE_clientID}&client_secret={SUBTE_clientSecret}&json=1"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as res:
                data = await res.json()
                if res.status == 200:

                    # Log
                    print(FechaActual)
                    print(f"Se ha ejecutado el comando subteBA")

                    # La API solo manda entity si hay disrupcion en el servicio en la linea. Sino, no manda nada. Aca chequeamos eso.
                    # Por default el servicio esta OK, a menos que encontremos entity de la linea.
                    errores = []
                    error = data.get("entity", [])
                    for item in error:
                        linea_id = item.get('id')
                        alert_text = item['alert']['header_text']['translation'][0]['text']
                        errores.append((linea_id, alert_text))

                    # Se crea el mensaje ctx para mandar (titulo)
                    mensaje = "Estado del subte en Buenos Aires\n"
                    
                    # Creamos las variables para los mensajes de estado de cada linea
                    mensaje_linea_a = "🟢 Linea A funciona con normalidad\n"
                    mensaje_linea_b = "🟢 Linea B funciona con normalidad\n"
                    mensaje_linea_c = "🟢 Linea C funciona con normalidad\n"
                    mensaje_linea_d = "🟢 Linea D funciona con normalidad\n"
                    mensaje_linea_e = "🟢 Linea E funciona con normalidad\n"
                    mensaje_linea_h = "🟢 Linea H funciona con normalidad\n"

                    # Si aplica la alerta, la mandamos a las variables de mensaje
                    for linea, alert_text in errores:
                        if linea == 'Alert_LineaA':
                            mensaje_linea_a = f"🔴 Linea A - {alert_text}\n"
                        elif linea == 'Alert_LineaB':
                            mensaje_linea_b = f"🔴 Linea B - {alert_text}\n"
                        elif linea == 'Alert_LineaC':
                            mensaje_linea_c = f"🔴 Linea C - {alert_text}\n"
                        elif linea == 'Alert_LineaD':
                            mensaje_linea_d = f"🔴 Linea D - {alert_text}\n"
                        elif linea == 'Alert_LineaE':
                            mensaje_linea_e = f"🔴 Linea E - {alert_text}\n"
                        elif linea == 'Alert_LineaH':
                            mensaje_linea_h = f"🔴 Linea H - {alert_text}\n"

                    mensaje += mensaje_linea_a + mensaje_linea_b + mensaje_linea_c + mensaje_linea_d + mensaje_linea_e + mensaje_linea_h

                    # Se mande el mensaje CTX
                    await ctx.send(mensaje)
                
    except Exception as e:
        # En caso de error en la API, se imprime el mensaje y se crea el embed con la respuesta
        await ctx.send("Error en la API. Avisar a algun root")
        print("Error en la API:", str(e))
