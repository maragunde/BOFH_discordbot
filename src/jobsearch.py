import discord
from discord import Embed
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

async def jobsearchfunc(interaction, texto):
    FechaActual = datetime.now()

    # Traemos el canal de job board
    JobsChannel = int(os.getenv('JobsChannel'))
    forum_channel = discord.utils.get(interaction.guild.channels, id=JobsChannel)

    # Fetching de threads posteados en el canal
    matching_threads = []
    
    for thread in forum_channel.threads:
        if texto.lower() in thread.name.lower():
            matching_threads.append(thread)
    
    matching_threads = matching_threads[:5] # <-- limitamos a un maximo de 5

    # Log
    print(FechaActual)
    print(f"Se ha ejecutado el comando slash /jobsearch por {interaction.user}")

    if matching_threads:

         # Se crea el embed con la respuesta para los jobs que matechan
        embed = Embed(title=f"Trabajos posteados para {texto}", description=f"Cortesía de {interaction.user}", color=discord.Color.green())
        embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1356823152391843844/_Eooxcxc_400x400.png")
        for thread in matching_threads:
            embed.add_field(name=f"{thread.name}", value=f"• [{thread.name}](https://discord.com/channels/{interaction.guild.id}/{thread.id})", inline=False)
        return embed
    else:
        # Se crea el embed con la respuesta si no hay match
        embed = Embed(title=f"Trabajos posteados para {texto}", description=f"Cortesía de {interaction.user}", color=discord.Color.green())
        embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1356823152391843844/_Eooxcxc_400x400.png")
        embed.add_field(name=f"/dev/null", value=f"No encontre trabajos posteados", inline=False)
        return embed

   