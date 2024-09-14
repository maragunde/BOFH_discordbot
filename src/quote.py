import discord
from discord import Embed
from datetime import datetime
import sqlite3



#################### FUNCION DE QUOTE ALEATORIA
async def quotefunc(interaction):
    FechaActual = datetime.now()

    # Conectamos a la base
    databasequotes = sqlite3.connect('db/quotes.db')
    cursorquotes = databasequotes.cursor()

    # Selecciona una quote aleatoria de la DB
    SQLcount = ("SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1")
    cursorquotes.execute(SQLcount)
    historicquote = cursorquotes.fetchone()

    # Formateamos fecha
    date_str = str(historicquote[2])[:10]

    # Se crea el embedd con la respuesta
    embed = Embed(title=f"Quote historica", description=f"a pedido de {interaction.user}", color=discord.Color.green())
    embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1356823152391843844/_Eooxcxc_400x400.png")
    embed.add_field(name="Quote historica de Sysarmy", value=f"{historicquote[0]} - by {historicquote[1]} - Date: {date_str}", inline=False)


    # Log
    print(FechaActual)
    print(f"Comando /quote ejecutado por {interaction.user}")

    databasequotes.commit()
    databasequotes.close()

    return embed

#################### FUNCION DE QUOTE POR BUSQUEDA DE TEXTO
async def qsearchfunc(interaction, texto):
    FechaActual = datetime.now()

    # Conectamos a la base
    databasequotes = sqlite3.connect('db/quotes.db')
    cursorbusqueda = databasequotes.cursor()

    # Selecciona una quote de la DB en base a texto (ambos campos de usuario o de quote)
    SQLbuscaquote = ("SELECT * FROM quotes WHERE quote LIKE ? OR username LIKE ? ORDER BY RANDOM()")
    cursorbusqueda.execute(SQLbuscaquote, ('%' + texto + '%', '%' + texto + '%'))
    quotesencontrados = cursorbusqueda.fetchall()

    # Si el texto no se encuentra quoteado, devuelve la respuesta
    if len(quotesencontrados) == 0:
        embed = Embed(title=f"Quote historica cortesia de {interaction.user}", description=f"{str(len(quotesencontrados))} quotes encontradas para {texto}", color = discord.Color.green())
        embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1356823152391843844/_Eooxcxc_400x400.png")
        embed.add_field(name="Quote historica de Sysarmy", value =f"No se han encontrado quotes para {texto}", inline=False)

        #Log
        print(FechaActual)
        print(f"Comando /quotesearch ejecutado por {interaction.user}")

    else:
        # Se crea el embed con la respuesta para cada un maximo de 4 quotes
        embed = Embed(title=f"A pedido de {interaction.user}", description=f"{str(len(quotesencontrados))} quotes encontradas para {texto}. Aca hay algunas:", color = discord.Color.green())
        embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1356823152391843844/_Eooxcxc_400x400.png")
        for i, quote in enumerate(quotesencontrados[:4], start=1):
            embed.add_field(name=f"Quote de {quote[1]} - Fecha: {quote[2][0:10]}", value =f"{quote[0]}", inline=False)
            
            # Limita la cantidad de quotes a 4
            if i == 4:
                break
             
        #Log
        print(FechaActual)
        print(f"Comando /quotesearch ejecutado por {interaction.user}")

    databasequotes.commit()
    databasequotes.close()

    return embed