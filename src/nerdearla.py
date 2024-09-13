import discord
from discord import Embed
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
from ratelimit import limits
from ics import Calendar
import requests

#########################################################################################
############ FUNCION PARA BUSCAR CHARLAS EN YOUTUBE Y CALENDAR DE NERDEARLA #############
#########################################################################################
quince_minutos = 900
load_dotenv()

@limits(calls=5, period=quince_minutos)
async def nerdearlacharlasfunc(interaction, texto):

    # Hacemos un defer para darle tiempo al bot y poder mandar dos respuestas de embed
    await interaction.response.defer(ephemeral=True) 

    FechaActual = datetime.now()

    ###################### Setup y llamado a la API de Google para YouTube y para el Google Calendar ######################
    YOUTUBE_API_KEY = os.getenv('google_key')
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    channel_id = 'UC1WxOSF0QFb7C0I_QGiDlrA'  # Channel ID de Nerdearla

    # Traemos los eventos del Google Calendar publico de Sysarmy
    response = requests.get(os.getenv('calendar_nerdearla'))
    calendar = Calendar(response.text)

    ###################### Bloque de busqueda en ICS Calendar ######################

    # Buscamos las charlas por titulo
    lista_charlas = []
    for event in calendar.events:
        if texto.lower() in event.name.lower():
            event_info = {
                "title": event.name,
                "start": event.begin.strftime('%Y-%m-%d %H:%M')
            }
            lista_charlas.append(event_info)

    lista_charlas = lista_charlas[:5]  # Limitamos a un maximo de 5

    # Si encontramos charlas, las mandamos como embed
    if lista_charlas:
        embedCharlas = discord.Embed(title="Próximas charlas en Nerdearla (5 max)", color=discord.Color.blue())
        for event in lista_charlas:
            embedCharlas.add_field(name=event["title"], value=f"Fecha y Hora: {event['start']}", inline=False)
        
        await interaction.followup.send(embed=embedCharlas, ephemeral=True)
    else:
        await interaction.followup.send(f"No encontré charlas próximas en Nerdearla para '{texto}'", ephemeral=True)

    ###################### Bloque de busqueda en YouTube ######################

    # Buscamos video por el titulo
    search_response = youtube.search().list(
        q=texto,
        part='snippet',
        channelId=channel_id,
        maxResults=5,  # Limitamos a un maximo de 5
        type='video',
        order='date'
    ).execute()

    videos = search_response.get('items', [])

    # Filtramos videos para que busque el keyword solamente en el titulo del video
    videos_filtrados = [video for video in videos if texto.lower() in video['snippet']['title'].lower()]

    if not videos_filtrados:
        await interaction.followup.send(f"No encontré videos en YouTube con '{texto}' en el título", ephemeral=True)
        return

    # Armamos el embed para la respuesta de los videos de YouTube
    embedYouTube = discord.Embed(
        title=f"Videos subidos a nuestro canal",
        color=discord.Color.blue()
    )

    for video in videos_filtrados:
        title = video['snippet']['title']
        video_id = video['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        video_url = video_url[:15] + '\u200B' + video_url[15:]  # Anti-embed truncation trick
        embedYouTube.add_field(name=title, value=video_url, inline=False)
    
    # Mandamos la respuesta
    await interaction.followup.send(embed=embedYouTube, ephemeral=True)

    # Log
    print(FechaActual)
    print(f"Se ha ejecutado el comando slash para '{texto}'")
