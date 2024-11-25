import discord
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

async def jobsearchfunctx(ctx, texto):
    FechaActual = datetime.now()

    # Traemos el canal de job board
    JobsChannel = int(os.getenv('JobsChannel'))
    forum_channel = discord.utils.get(ctx.guild.channels, id=JobsChannel)

    # Fetching de threads posteados en el canal
    matching_threads = []
    
    for thread in forum_channel.threads:
        if texto.lower() in thread.name.lower():
            matching_threads.append(thread)
    
    matching_threads = matching_threads[:5] # <-- limitamos a un maximo de 5 

    # Si matchea, se manda respuesta
    if matching_threads:
        response = f"Encontré las siguientes posiciones para [{texto}] : (5 max)\n"
        for thread in matching_threads:
            response += f"• [{thread.name}](https://discord.com/channels/{ctx.guild.id}/{thread.id})\n"
        await ctx.send(response)
    else:
        # Se crea el embed con la respuesta si no hay match
        await ctx.send(f"No encontré trabajos con '{texto}' en el título.")
    
    # Log
    print(FechaActual)
    print(f"Se ha ejecutado el comando !jobs")