import discord
import datetime, sqlite3
from datetime import datetime

################### FUNCION DE RANKING
async def karmarankfunctx(ctx):
    FechaActual = datetime.now()
    
    # Conectamos a la base
    database = sqlite3.connect('db/karma.db')
    cursor = database.cursor()
    
    # Campos que necesitamos en la base: Username, Uy karma, ya presorteados
    SQL = ("SELECT karmavalue, palabra FROM karma ORDER BY karmavalue DESC LIMIT 10") 

    cursor.execute(SQL)
    rows = cursor.fetchall()

    # Se crea el mensaje
    message = "Sysarmy karma ranking:\n"
    j = 1
    for i in rows:
        message += f"Puesto {j}:  **{i[1]}**   -  Karma:  {i[0]}\n"
        j += 1
    await ctx.send(message)
    
    # Log
    print (FechaActual)
    print("Se ha ejecutado el comando de Karma Rank")  
    
    database.commit()
    database.close()
    
################### FUNCION DE KARMA PALABRA
async def karmawordfunctx(ctx, text):
    FechaActual = datetime.now()

    # Conectamos a la base
    database = sqlite3.connect('db/karma.db')
    cursor = database.cursor()
    
    # Chequea si la palabra esta en la base
    SQL_check = "SELECT EXISTS(SELECT 1 FROM karma WHERE palabra = ?)"
    cursor.execute(SQL_check, (text,))
    palabra_existe = cursor.fetchone()[0]
    
    if not palabra_existe:
        await ctx.send(f"**{text}** no tiene karma.")
    else:
        
        # Se manda mensaje
        SQL = "SELECT karmavalue FROM karma WHERE palabra = ?"
        cursor.execute(SQL, (text,))
        karma_value = cursor.fetchone()[0]
        await ctx.send(f"**{text}** tiene {karma_value} karma.")
    
    # Log
    print(FechaActual)
    print("Se ha ejecutado el comando karma")

    database.commit()
    database.close()

################### FUNCION DE KARMA GIVERS USUARIO
async def karmagiversuserfunctx(ctx, text):
    FechaActual = datetime.now()

    # Conectamos a la base
    database = sqlite3.connect('db/karma.db')
    cursor = database.cursor()
    
    # Chequea si la palabra esta en la base
    SQL_check = "SELECT EXISTS(SELECT 1 FROM karma WHERE palabra = ? AND isuser = 'YES')"
    cursor.execute(SQL_check, (text,))
    palabra_existe = cursor.fetchone()[0]
    
    if not palabra_existe:
        await ctx.send(f"**{text}** no tiene karmagiven.")
    else:
        
        # Se manda mensaje
        SQL = "SELECT karmagiven FROM karma WHERE palabra = ?"
        cursor.execute(SQL, (text,))
        karma_value = cursor.fetchone()[0]
        await ctx.send(f"**{text}** tiene {karma_value} karmagiven.")
    
    # Log
    print(FechaActual)
    print("Se ha ejecutado el comando givers")

    database.commit()
    database.close()

################### FUNCION DE RANKING KARMAGIVERS
async def karmagiversfunctx(ctx):
    FechaActual = datetime.now()

    # Conectamos a las bases
    database = sqlite3.connect('db/discordusrs.db')
    cursor = database.cursor()
    databasectx = sqlite3.connect('db/karma.db')
    cursorctx = databasectx.cursor()

    # Campos que necesitamos en la base de discord: Username, y karmagiven, ya presorteados
    SQLDiscord = ("SELECT karmagiven, username FROM usuarios ORDER BY karmagiven DESC LIMIT 5") 
    cursor.execute(SQLDiscord)
    rowsusersdiscord = cursor.fetchall()

    # Se crea el mensaje para usuarios de Discord
    messageDiscord = "Ususarios de Discord con mas constribuciones de Karma:\n"
    j = 1
    for i in rowsusersdiscord:
        messageDiscord += f"Puesto {j}:  **{i[1]}**   -  Karma dado:  {i[0]}\n"
        j += 1
    await ctx.send(messageDiscord)

   # Campos que necesitamos en la base de karma: Username, y karmagiven, ya presorteados
    SQLKarma = ("SELECT karmagiven, palabra, isuser FROM karma WHERE isuser = 'YES' ORDER BY karmagiven DESC LIMIT 5") 
    cursorctx.execute(SQLKarma)
    rowsctx = cursorctx.fetchall()
    
    # Se crea el mensaje para usuarios externos
    messageCTX = "Ususarios externos con mas constribuciones de Karma:\n"
    x = 1
    for z in rowsctx:
        messageCTX += f"Puesto {x}:  **{z[1]}**   -  Karma dado:  {z[0]}\n"
        x += 1
    await ctx.send(messageCTX)

    # Log
    print (FechaActual)
    print("Se ha ejecutado el comando de Karma Givers")

    database.commit()
    database.close()