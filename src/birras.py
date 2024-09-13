from datetime import datetime, timezone
import requests
import discord
from discord import Embed
from ics import Calendar
import re
import os
from dotenv import load_dotenv

async def birrasfunc(interaction):
    FechaActual = datetime.now(timezone.utc)

    # Traemos los eventos del Google Calendar publico de Sysarmy
    response = requests.get(os.getenv('calendar_birras'))
    calendar = Calendar(response.text)

    # Creamos la lista para los embeds de eventos
    embed_fields = []

    eventosformateados = False
    for event in calendar.events:

        # Convertimos las timezones para poder compararlas
        evento_UTC = event.begin.datetime.astimezone(timezone.utc)

        if evento_UTC > FechaActual:
            eventosformateados = True 
            
            # Formateo de fecha
            fechaformateada = evento_UTC.strftime("%d-%m-%Y %H:%M")

            # Limpiamos el codigo feo que mete Google Calendar + sacamos la referencia del adminbirrator
            description = re.sub(r'<a href=\'(.*?)\'>.*?</a>', r'\1', event.description)
            description = re.sub(r'^Evento creado por https://github.com/sysarmy/disneyland/tree/master/adminbirrator 🍻$', '', description, flags=re.MULTILINE)

            # Busca 'birras' en el evento
            if 'birras' in event.name.lower() or 'birras' in description.lower():
                eventosformateados = True

                # Formateo de fecha
                fechaformateada = evento_UTC.strftime("%d-%m-%Y %H:%M")
                
                # Appendeamos el evento para el embed
                embed_fields.append((event.name, fechaformateada, description))

    if eventosformateados:

        # Log + Mandamos mensaje
        print(FechaActual)
        print("Se ha ejecutado el comando !birras")

        # Se crea el embed con la respuesta
        embed = Embed(title="Próximas birras / Eventos", description=f"Cortesía de {interaction.user}", color=discord.Color.green())
        embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1356823152391843844/_Eooxcxc_400x400.png")

        for name, fechaformateada, description in embed_fields:
            embed.add_field(name=f"{name} - {fechaformateada}", value=f"{description}", inline=False)

        return embed
    else:
        # Log + Mandamos mensaje
        print(FechaActual)
        print("Se ha ejecutado el comando !birras")

        embed = Embed(title="Birras", color=discord.Color.green())
        embed.add_field(name="Birras", value="No encontré Adminbirras programadas próximamente. Revisa: https://www.meetup.com/sysarmy/", inline=False)
        return embed