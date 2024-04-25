import discord
from discord import Embed
import datetime, sqlite3
from datetime import datetime


# Conectamos a la base
database = sqlite3.connect('db/discordusrs.db')
cursor = database.cursor()

# Campos que necesitamos en la base: Username, UserId de discord, Karma, y el budget de karma
SQL = ("SELECT karmabudget, karma, username FROM usuarios") 


################### FUNCION DE RANKING
async def karmarankfunc(interaction):
    FechaActual = datetime.now()
    
    # Conectamos a la base
    database = sqlite3.connect('db/discordusrs.db')
    cursor = database.cursor()
    
    # Campos que necesitamos en la base: Username, Uy karma, ya presorteados
    SQL = ("SELECT karma, username FROM usuarios ORDER BY karma DESC LIMIT 10") 

    cursor.execute(SQL)
    rows = cursor.fetchall()
        
    # Se crea el embed con la respuesta
    embed = Embed(title=f"Karma ranking", description=f"A pedido de {interaction.user}", color = discord.Color.green(), )
    embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1356823152391843844/_Eooxcxc_400x400.png")
    j= 1
    for i in rows:
        embed.add_field(name =f"Puesto {j}", value =f"{i[1]}   -  Karma:  {i[0]}", inline=False)
        j+=1
    database.commit()
    database.close()
    
    # Log
    print (FechaActual)
    print("Se ha ejecutado el comando de Karma Rank")
    return embed

################### FUNCION DE RANKING KARMAGIVERS
async def karmagiversfunc(interaction):
    FechaActual = datetime.now()

    # Conectamos a las bases
    database = sqlite3.connect('db/discordusrs.db')
    cursor = database.cursor()
    databasekarma = sqlite3.connect('db/karma.db')
    cursorkarma = databasekarma.cursor()

    # Campos que necesitamos en la base: Username, y karmagiven, ya presorteados
    SQLDiscord = ("SELECT karmagiven, username FROM usuarios ORDER BY karmagiven DESC LIMIT 5") 
    cursor.execute(SQLDiscord)
    rowsDiscord = cursor.fetchall()
        
    # Se crea el embed con la respuesta de ususarios de discord
    embed_discord = Embed(title=f"Mayores contribuidores de Karma", description=f"En Discord", color=discord.Color.green())
    embed_discord.set_thumbnail(url="https://pbs.twimg.com/profile_images/1356823152391843844/_Eooxcxc_400x400.png")
    j = 1
    for i in rowsDiscord:
        embed_discord.add_field(name=f"Puesto {j}", value=f"{i[1]}   -  Karma dado:  {i[0]}", inline=False)
        j += 1

    # Campos que necesitamos en la base: palabra, y karmagiven, ya presorteados
    SQLkarma = ("SELECT karmagiven, palabra FROM karma ORDER BY karmagiven DESC LIMIT 5") 
    cursorkarma.execute(SQLkarma)
    rowsCTX = cursorkarma.fetchall()
        
    # Se crea el embed con la respuesta de usuarios externos
    embed_karma = Embed(title=f"Mayores contribuidores de Karma", description=f"Usuarios Externos", color=discord.Color.red())
    embed_karma.set_thumbnail(url="https://pbs.twimg.com/profile_images/1356823152391843844/_Eooxcxc_400x400.png")
    x = 1
    for z in rowsCTX:
        embed_karma.add_field(name=f"Puesto {x}", value=f"{z[1]}   -  Karma dado:  {z[0]}", inline=False)
        x += 1

    # Log
    print(FechaActual)
    print("Se ha ejecutado el comando de Karma Givers")

    database.commit()
    database.close()
    databasekarma.commit()
    databasekarma.close()

    return [embed_discord, embed_karma]

################### FUNCION DE KARMAUSER
async def karmauserfunc(interaction, user):
    FechaActual = datetime.now()

    # Conectamos a la base
    database = sqlite3.connect('db/discordusrs.db')
    cursor = database.cursor()
    
    # Campos que necesitamos en la base: Username, y karmagiven, ya presorteados
    SQL = ("SELECT karma, username FROM usuarios WHERE username = ?") 
    cursor.execute(SQL, (str(user),))
    karmauser = cursor.fetchall()
    
    # Log
    print (FechaActual)
    print("Se ha ejecutado el comando karmauser")

    # Se crea el embed con la respuesta
    embed = Embed(title=f"Karma Status ", description=f"A pedido de {interaction.user}", color = discord.Color.green(), )
    embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1356823152391843844/_Eooxcxc_400x400.png")
    embed.add_field(name =f"{str(user)}", value =f"Karma = {karmauser[0][0]}", inline=False)
   
    return embed
