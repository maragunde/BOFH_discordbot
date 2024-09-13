import discord
from discord import Embed
from datetime import datetime
import random, sqlite3



#################### FUNCION DE AGREGAR QUOTE 
async def quoteaddfunctx(ctx, quote):
    FechaActual = datetime.now()

    # Conectamos a la base de datos
    databasequotes = sqlite3.connect('db/quotes.db')
    cursorquotes = databasequotes.cursor()

    SQLbuscar = ("SELECT quote FROM quotes WHERE quote = ? AND username = ?")
    cursorquotes.execute(SQLbuscar, (quote, str(ctx.author)))
    quotesencontradas = cursorquotes.fetchall()

    

    if len(quotesencontradas) == 0:
        
        # Log
        print(FechaActual)
        print("Mensaje quoteado via !qadd")
        print(f"Quote: {quote}")
        print(f"Author: {ctx.author}")
        print(f"Date: {FechaActual}")

        # Inserta la quote con los valores y manda mensaje de confirmacion
        SQLquote = ("INSERT INTO quotes (quote, username, date) VALUES (?, ?, ?)")
        cursorquotes.execute(SQLquote, (quote, str(ctx.author), str(FechaActual)))
        await ctx.send(f"Quote agregado: {quote} - cortesia de: {ctx.author}")

    else:
        await ctx.send("Error de capa 8. Este quote ya fue agregado anteriormente")

    databasequotes.commit()
    databasequotes.close()

#################### FUNCION DE QUOTE ALEATORIA
async def quotefunctx(ctx):
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
            
    # Se crea el CTX con la respuesta
    await ctx.send("Quote random de sysarmy")
    await ctx.send(f"{historicquote[0]} - by {historicquote[1]} - Date: {date_str}")

    # Log 
    print(FechaActual)
    print("Comando !q ejecutado")

    databasequotes.commit()
    databasequotes.close()

#################### FUNCION DE QUOTE POR BUSQUEDA DE TEXTO
async def qsearchfunctx(ctx, texto):
    FechaActual = datetime.now()

    # Conectamos a la base de datos
    databasequotes = sqlite3.connect('db/quotes.db')
    cursorbusqueda = databasequotes.cursor()

    # Selecciona una quote de la DB en base a texto (ambos campos de usuario o de quote)
    SQLbuscaquote = ("SELECT * FROM quotes WHERE quote LIKE ? OR username LIKE ? ORDER BY RANDOM()")
    cursorbusqueda.execute(SQLbuscaquote, ('%' + texto + '%', '%' + texto + '%'))
    quotesencontrados = cursorbusqueda.fetchall()
    
    # Si el texto no se encuentra quoteado, devuelve la respuesta
    if len(quotesencontrados) == 0:
        await ctx.send(f"No se han encontrado quotes historicas de sysarmy para {texto}")
    else:

        # Log 
        print(FechaActual)
        print("Comando !qsearch search ejecutado")

        # Se crea el CTX con la respuesta para cada un maximo de 4 quotes
        await ctx.send(f"{str(len(quotesencontrados))} quotes encontradas para {texto}. Aca hay algunas:")
        for i, quote in enumerate(quotesencontrados[:4], start=1):
            await ctx.send(f"Quote de {quote[1]} - Fecha: {quote[2][0:10]} - {quote[0]}")
            
            # Limita la cantidad de quotes a 4
            if i == 4:
                break

    databasequotes.commit()
    databasequotes.close()
