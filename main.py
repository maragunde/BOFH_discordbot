# IMPORT DE LIBRERIAS PRINCIPALES
import discord
from discord import Intents, Client, Message, app_commands, Interaction, Embed, message, reaction
from discord.ext import commands
import random, sqlite3
from datetime import datetime
from db.dbops import agregarusuario
import os
from dotenv import load_dotenv # <-- Solo para las keys storeadas en venv


# IMPORT DE COMANDOS TREE (NATIVOS DISCORD)
from src.londonUnderground import Lines
from src.subteBA import SubteBA
from src.fulbo import futbolimport
from src.Clima import climafun
from src.cripto import criptofun
from src.dolar import dolarfun
from src.euro import eurofun
from src.feriadoAR import feriadoARfun
from src.feriadoCL import feriadoCLfun
from src.feriadoES import feriadoESfun
from src.feriadoMX import feriadoMXfun
from src.feriadoUY import feriadoUYfun
from src.karma import karmagiversfunc, karmarankfunc, karmauserfunc
from src.help import helpfunc
from src.quote import quotefunc, qsearchfunc

# IMPORT DE COMANDOS VERSION SIMPLE (FUNCIONAN POR TEXTO USANDO FUNCION CTX.SEND) 
from src.ctxcommands.ctxclima import climafunctx
from src.ctxcommands.ctxcripto import criptofunctx
from src.ctxcommands.ctxdolar import dolarfunctx
from src.ctxcommands.ctxeuro import eurofunctx
from src.ctxcommands.ctxferiadoar import feriadoarfunctx
from src.ctxcommands.ctxferiadocl import feriadoclfunctx
from src.ctxcommands.ctxferiadomx import feriadomxfunctx
from src.ctxcommands.ctxferiadouy import feriadouyfunctx
from src.ctxcommands.ctxferiadoes import feriadoesfunctx
from src.ctxcommands.ctxfulbo import fulbofunctx
from src.ctxcommands.ctxhelp import helpfunctx
from src.ctxcommands.ctxkarma import karmarankfunctx, karmawordfunctx, karmagiversfunctx, karmagiversuserfunctx
from src.ctxcommands.ctxquote import quotefunctx, qsearchfunctx, quoteaddfunctx
from src.ctxcommands.ctxsubte import subtefunctx
from src.ctxcommands.ctxunderground import undergroundfunctx
                                              
                                                                    
#                @@@@@@@@@@@@@    =@@@*     @@@@    +@@@@@@@@@@@@@   
#               @@@@@@@@@@@@@@    @@@@     @@@@.    @@@@@@@@@@@@@.   
#               @@@@             =@@@-     @@@@    +@@@.             
#              @@@@@@@@@@@@@%    @@@@@@@@@@@@@.    @@@@@@@@@@@@@     
#              @@@@@@@@@@@@@    :@@@@@@@@@@@@@    =@@@@@@@@@@@@@     
#                       @@@%             +@@@:             *@@@      
#             @@@@@@@@@@@@@    :@@@@@@@@@@@@@    =@@@@@@@@@@@@@      
#            :-------------    -------------.    -------------.      
#                                                                    
#                                                                    
#           @@@@@@@@@@@@@    .@@@@@@@@@@@@@    :@@@@@@@@@@@@@        
#          @@@@@@@@@@@@@@    @@@@@@@@@@@@@=    @@@@@@@@@@@@@-        
#          @@@@     @@@@    :@@@      @@@@    :@@@@@@@@@@@@@         
#         @@@@@@@@@@@@@@    @@@# @@@@@@@@=    @@@@@@@@@@@@@-         
#         @@@@@@@@@@@@@    :@@@  @@@         :@@@@@@@@@@@@@          
#        @@@@.     @@@@    @@@@ @@@@@@@@=    @@@@@@@@@@@@@-          
#        @@@@     @@@@    .@@@  @@@@@@@@    :@@@@@@@@@@@@@           
#       :-------------    -------------.    -------------.                                                                
#                                                                    
#                                                                    
#      @@@@@@@@@@@@@     @@@@@@@@@@@@@    .@@@%     @@@@             
#     %@@@@@@@@@@@@@    @@@+-@@@%-@@@#    @@@@     #@@@=             
#     @@@@@@@@@@@@@     @@@ .@@@  @@@     @@@@@@@@@@@@@              
#    %@@@@@@@@@@@@@    @@@- @@@* @@@#    @@@@@@@@@@@@@+              
#    @@@@@@@@@@@@@     @@@  @@@  @@@              @@@@               
#  #@@@@@@@@@@@@@    @@@= @@@% @@@#    @@@@@@@@@@@@@*               
#   @@@@@@@@@@@@@    .@@@  @@@  @@@     @@@@@@@@@@@@@                
#  :-------------    -------------.    -------------.                                       

# BOFH - Discord community bot for Sysarmy
# Version 1.0 - April / May 2024
# by @Qwuor01 and @aragunde
# License GPL v2 - Ver LICENSE en repositorio                       
###########################################################################################################
########################### BOT INITIAL SETUP BEGINS ######################################################

# Definimos a bot
load_dotenv()
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

BOT_token = os.getenv('BOT_token')
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)
def main() -> None:
    bot.run(f'{BOT_token}')

################## FETCHING DE USUARIOS A LA DB CUANDO SE UNEN AL SERVER

@bot.event
async def on_member_join(member):
    
    # Traemos el nombre y ID del usuario
    username = member.name
    user_id = str(member.id)

    # Mensaje de Bienvenida privado al usuario
    await member.send("Welcome to Sysarmy. Por favor recorda pasar por la seccion de Welcome para familiarizarte con el codigo de conducta y comandos de nuestro bot. Have fun :)")
    
    # Mandamos la data a la funcion de DB Ops que la agrega a la base
    await agregarusuario(username, user_id)


@bot.event
async def on_ready():

    # BOFH starts
    FechaActual = datetime.now()
    print("Current time:", FechaActual)
    print("""
               ...........     ..  ...  ..     ............     
              @@@@@@@@@@@@    @@@     @@@@    @@@@@@@@@@@@   
             @@@@            @@@@    .@@@    %@@@            
             @@@@@@@@@@@@    @@@@@@@@@@@@    @@@@@@@@@@@@    
            @@@@@@@@@@@@    @@@@@@@@@@@@    #@@@@@@@@@@@.    
            %%%%%%%%@@@@    %%%%%%%%@@@@    %%%%%%%%@@@@     
           @@@@@@@@@@@@.   @@@@@@@@@@@@    %@@@@@@@@@@@:     
                                                             
                                                             
          @@@@@@@@@@@@    @@@@@@@@@@@@    @@@@@@@@@@@@       
         @@@@@@@@@@@@.   @@@@@@@@@@@@    #@@@@@@@@@@@:       
         @@@:    @@@@    @@@     .@@@    @@@@@@@@@@@@        
        @@@@@@@@@@@@.   @@@: @@@@@@@.   %@@@@@@@@@@@:        
        @@@@@@@@@@@@    @@@ +@@#        @@@@@@@@@@@@         
       %@@@     @@@.   @@@: @@@@@@@    #@@@@@@@@@@@:         
       @@@+    @@@@    @@@ +@@@@@@@    @@@@@@@@@@@@          
                                                             
                                                             
     #@@@@@@@@@@@.   @@@@@@@@@@@@    *@@@     @@@:           
     @@@@@@@@@@@@    @@@@@@@@@@@@    @@@+    @@@@            
    @@@@@@@@@@@@:   @@@  @@@ %@@.   #@@@@@@@@@@@=            
    @@@@@@@@@@@@    @@@ @@@. @@@    @@@@@@@@@@@@             
   #@@@@@@@@@@@.   @@@  @@@ #@@             @@@:             
   @@@@@@@@@@@@    @@@ %@@. @@@    @@@@@@@@@@@@              
   ...........     ..  ...  ..     ............     
          
          BOFH bot is ready to pwn!""") 
    try:
        synced = await bot.tree.sync()
        print(f"Se sincronizaron {len(synced)} comandos slash")
    except Exception as e:
        print(e)

########################### BOT INITIAL SETUP ENDS ######################################################
#########################################################################################################

##################################################################################################################
############################# FUNCION DE ON_REACTION PARA KARMA Y QUOTES #########################################
##################################################################################################################

# Operaciones para cuando una reaccion de Discord se agrega (Para Karma y quote)

@bot.event
async def on_reaction_add(reaction, user):
    FechaActual = datetime.now()

    # Conectamos a la base
    database = sqlite3.connect('db/discordusrs.db')
    databasequotes = sqlite3.connect('db/quotes.db')
    cursor = database.cursor()
    cursorquotes = databasequotes.cursor()

    # Esto hace que el usuario no pueda autoquotearse o darse/quitarse karma a si mismo
    if user != reaction.message.author:

        # Reaccion de Karma Up
        if "kup" in str(reaction):
            print(FechaActual)
            print("Karma +1")
            SQLkarma = ("UPDATE usuarios SET karma = karma + 1 WHERE user_id = ?")
            cursor.execute(SQLkarma, (reaction.message.author.id,))
            # Operaciones de DB
            SQLkarmagiven = ("UPDATE usuarios SET karmagiven = karmagiven + 1 WHERE user_id = ?")
            cursor.execute(SQLkarmagiven, (user.id,))
            await reaction.message.channel.send(f"+1 karma para {str(reaction.message.author)}")

        # Reaccion de Karma Down
        elif "kdown" in str(reaction):
            print("Karma -1")
            SQLkarma = ("UPDATE usuarios SET karma = karma - 1 WHERE user_id = ?")
            cursor.execute(SQLkarma, (reaction.message.author.id,))
            # Operaciones de DB
            SQLkarmagiven = ("UPDATE usuarios SET karmagiven = karmagiven + 1 WHERE user_id = ?")
            cursor.execute(SQLkarmagiven, (user.id,))
            await reaction.message.channel.send(f"-1 karma para {str(reaction.message.author)}")

    # Reaccion de Quote y agrega quote a la DB
    if "qadd" in str(reaction):
        SQLbuscar = ("SELECT quote FROM quotes WHERE quote = ? AND username = ?")
        cursorquotes.execute(SQLbuscar, (str(reaction.message.content), str(reaction.message.author)))
        quotesencontradas = cursorquotes.fetchall()
        if len(quotesencontradas) == 0:
            print(len(quotesencontradas))
            print("Mensaje quoteado")
            print(f"Message: {reaction.message.content}")
            print(f"Author: {reaction.message.author}")
            print(f"Date: {reaction.message.created_at}")
            SQLquote = ("INSERT INTO quotes (quote, username, date) VALUES (?, ?, ?)")
            cursorquotes.execute(SQLquote, (str(reaction.message.content), str(reaction.message.author), str(reaction.message.created_at)))
            await reaction.message.channel.send(f"Quote de {str(reaction.message.author)} agregado: {str(reaction.message.content)} - cortesia de: {str(user)}")
        else:
            await user.send("Error de capa 8. Este quote ya fue agregado anteriormente")
        
    database.commit()
    database.close()
    databasequotes.commit()
    databasequotes.close()

# Operaciones para cuando una reaccion de Discord se remueve (Para Karma y quote)

@bot.event
async def on_reaction_remove(reaction, user):
    FechaActual = datetime.now()

    # Conectamos a la base
    database = sqlite3.connect('db/discordusrs.db')
    databasequotes = sqlite3.connect('db/quotes.db')
    cursor = database.cursor()
    cursorquotes = databasequotes.cursor()
    
    # Esto hace que el usuario no pueda autoquotearse o darse/quitarse karma a si mismo
    if user != reaction.message.author:

        # Reaccion de Karma Up
        if "kup" in str(reaction):
            print(FechaActual)
            print("Karma -1")
            SQLkarma = ("UPDATE usuarios SET karma = karma - 1 WHERE user_id = ?")

            # Operaciones de DB
            cursor.execute(SQLkarma, (reaction.message.author.id,))
            SQLkarmagiven = ("UPDATE usuarios SET karmagiven = karmagiven - 1 WHERE user_id = ?")
            cursor.execute(SQLkarmagiven, (user.id,))
            await reaction.message.channel.send(f"karma++ removido para {str(reaction.message.author)}")
        
        # Reaccion de Karma Down
        elif "kdown" in str(reaction):
            print(FechaActual)
            print("Karma +1")
            SQLkarma = ("UPDATE usuarios SET karma = karma + 1 WHERE user_id = ?")

            # Operaciones de DB
            cursor.execute(SQLkarma, (reaction.message.author.id,))
            SQLkarmagiven = ("UPDATE usuarios SET karmagiven = karmagiven - 1 WHERE user_id = ?")
            cursor.execute(SQLkarmagiven, (user.id,))
            await reaction.message.channel.send(f"karma-- removido para {str(reaction.message.author)}")

        # Reaccion de Quote y remueve quote de la DB
        elif "qadd" in str(reaction):
            print("Quote removido")
            print(f"Message: {reaction.message.content}")
            print(f"Author: {reaction.message.author}")
            print(f"Date: {reaction.message.created_at}")
            SQLquote = ("DELETE FROM quotes WHERE quote = ? AND username = ?")
            cursorquotes.execute(SQLquote, (str(reaction.message.content), str(reaction.message.author)))
            await reaction.message.channel.send(f"Quote de {str(reaction.message.author)} removido")

    database.commit()
    database.close()
    databasequotes.commit()
    databasequotes.close()

################### MANEJO DE ERRORES Y SETUP DE ON_MESSAGE ###################

# Funcion de manejo de error cuando el argumento es None
# (usuario manda el comando sin parametros requeridos, como por ejemplo en !clima o !fulbo)
# Excepto para !help que tiene su propio mensaje si el comando va vacio

@bot.event
async def on_command_error(ctx, error):
    FechaActual = datetime.now()

    mensajeayuda_general = """Informacion general sobre los comandos del bot de Sysarmy       
                        !dolar !cripto !euro !fulbo !clima !subte !underground !feriadoAR !feriadoCL !feriadoES !feriadoMX !feriadoUY !q !qsearch !qadd !rank !kgivers !kgiven !karma
                        Mas detalles en el canal #help-bot-commands de Discord, dentro de la seccion de Welcome! - o ejecutando /help desde Discord"""

# Custom error handling - si !help se manda vacio sin especificar comando, manda un mensaje de ayuda general
    if isinstance(error, commands.MissingRequiredArgument):
        if ctx.command.name == "help":
            await ctx.send(mensajeayuda_general)

            # Log
            print(FechaActual)
            print ("Se ha ejecutado el comando !help")

        else:
            await ctx.send("Error en el comando. No pasaste argumentos.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Comando inexistente")
    else:
        await ctx.send("Error en el comando. No pasaste argumentos.")


##################################################################################################################
############################# FUNCION DE ON_MESSAGE PARA KARMA ++ y -- ###########################################
##################################################################################################################
@bot.event
async def on_message(message):
    FechaActual = datetime.now()

    # Conectamos a la base de karma
    databasekarma = sqlite3.connect('db/karma.db')
    cursorkarma = databasekarma.cursor()
    databaseusers = sqlite3.connect('db/discordusrs.db')
    cursorusers = databaseusers.cursor()

    palabra_base = None

    if message.author.bot:
        return
    else:
        botID = 483426239445598240 # <--- Aca va el usr ID del Bridge bot de Discord (Puse el de godlike por ahora para poder probar)
        BridgeBotID = await bot.fetch_user(botID)
##################################################################################################################
# Todo esto se ejecuta cuando el usuario es el bot de bridge (o sea, el mensaje viene bridgeado de IRC, Slack, Telegram, etc.)

        if message.author == BridgeBotID:
            
            # Traemos el texto del mensaje y lo buscamos en la base
            textokarma = message.content.split()
            for texto in textokarma:
                if texto.endswith("++") or texto.endswith("--"):
                    palabra_base = texto[:-2]

                    # Buscamos y traemos el username externo <--- Esto es asi porque el bot siempre empieza los mensajes con el usuario
                    # en este formato = "<usuarioexterno> Mensaje publicado al canal." 
                    start_index = message.content.find('<')
                    end_index = message.content.find('>')
                    IRCusername = message.content[start_index + 1:end_index]
                        
                    # Ejecuta query para verificar si la palabra existe en la DB
                    cursorkarma.execute("SELECT * FROM karma WHERE palabra = ?", (palabra_base,))
                    existing_word = cursorkarma.fetchone()

                    # Ejecuta query para verificar si el usuario existe en la DB
                    cursorkarma.execute("SELECT * FROM karma WHERE palabra = ? AND isuser = 'YES'", (IRCusername,))
                    existing_user = cursorkarma.fetchone()
                        
                    # Si la palabra existe, procede con las funciones de UPDATE
                    if existing_word:      
                                
                            # Update word en la DB para karma++ y se imprime confirmacion
                            if texto.endswith("++"):
                                print("This is a ++ word!")
                                cursorkarma.execute("UPDATE karma SET karmavalue = karmavalue + 1 WHERE palabra = ?", (palabra_base,))
                                databasekarma.commit()
                                cursorkarma.execute("SELECT karmavalue FROM karma WHERE palabra = ?", (palabra_base,))
                                updated_karma = cursorkarma.fetchone()[0]
                                print(FechaActual)
                                print(f"Karma++ para {palabra_base}!")
                                await message.channel.send(f"+1 karma para [{palabra_base}]. Current karma = {updated_karma}")
                                
                                # Ahora Chequeamos el autor del mensaje
                                if existing_user:
                                    # Se le da karmagiven al usuario y se imprime confirmacion
                                    cursorkarma.execute("UPDATE karma SET karmagiven = karmagiven + 1 WHERE palabra = ? AND isuser = 'YES'", (IRCusername,))
                                    databasekarma.commit()
                                    print(f"+1 Karmagiven para {IRCusername}")
                                    await message.channel.send(f"+1 karmagiven para <{IRCusername}>")

                                elif existing_user is None:
                                    # Se agrega al nuevo usuario a la DB con karmagiven inicial y se imprime confirmacion
                                    cursorkarma.execute("INSERT INTO karma (palabra, karmavalue, isuser, karmagiven) VALUES (?, 1, 'YES', 0)", (IRCusername,))
                                    cursorkarma.execute("UPDATE karma SET karmagiven = karmagiven + 1 WHERE palabra = ? AND isuser = 'YES'", (IRCusername,))
                                    databasekarma.commit()
                                    cursorkarma.execute("SELECT palabra FROM karma WHERE palabra = ? AND isuser = 'YES'", (IRCusername,))
                                    print(f"Nuevo usuario externo [{IRCusername}] agregado a la DB!.")
                                    await message.channel.send(f"+1 karmagiven para <{IRCusername}>. Welcome to the karma user list! ")
                            
                                # Update word en la DB para karma-- y se imprime confirmacion
                            elif texto.endswith("--"):
                                cursorkarma.execute("UPDATE karma SET karmavalue = karmavalue - 1 WHERE palabra = ?", (palabra_base,))
                                databasekarma.commit()
                                cursorkarma.execute("SELECT karmavalue FROM karma WHERE palabra = ?", (palabra_base,))
                                updated_karma = cursorkarma.fetchone()[0]
                                print(FechaActual)
                                print(f"Karma--  para {palabra_base}!")
                                await message.channel.send(f"-1 karma para {palabra_base}. Current karma = {updated_karma}")
        
                    # Si la palabra no existe, procede con las funciones de INSERT
                    else:
                        # Insert word en la DB para karma++ y se imprime confirmacion
                        if texto.endswith("++"):
                            initial_karma = 1 # <-- Como es una nueva palabra y es ++, el karma inicial siempe es de 1
                            cursorkarma.execute("INSERT INTO karma (palabra, karmavalue, isuser, karmagiven) VALUES (?, ?, 'NO', ?)", (palabra_base, initial_karma, 0))
                            databasekarma.commit()
                            cursorkarma.execute("SELECT karmavalue FROM karma WHERE palabra = ?", (palabra_base,))
                            updated_karma = cursorkarma.fetchone()[0]
                            print(f"Nueva palabra agregada a la DB. Karma++  para {palabra_base}")
                            await message.channel.send(f"+1 karma para {palabra_base}. Current karma = {updated_karma}")

                            # Chequeamos el autor del mensaje
                            if existing_user:
                                # Se le da karmagiven al usuario y se imprime confirmacion
                                cursorkarma.execute("UPDATE karma SET karmagiven = karmagiven + 1 WHERE palabra = ? AND isuser = 'YES'", (IRCusername,))
                                databasekarma.commit()
                                print(FechaActual)
                                print(f"Se ha dado karmagiven +1 a {IRCusername}.")
                                await message.channel.send(f"+1 karmagiven para <{IRCusername}>.")

                            elif existing_user is None:
                                # Se agrega al nuevo usuario a la DB con karmagiven inicial y se imprime confirmacion
                                cursorkarma.execute("INSERT INTO karma (palabra, karmavalue, isuser, karmagiven) VALUES (?, 1, 'YES', 0)", (IRCusername,))
                                cursorkarma.execute("UPDATE karma SET karmagiven = karmagiven + 1 WHERE palabra = ? AND isuser = 'YES'", (IRCusername,))
                                databasekarma.commit()
                                cursorkarma.execute("SELECT palabra FROM karma WHERE palabra = ? AND isuser = 'YES'", (IRCusername,))
                                print(f"Nuevo usuario externo [{IRCusername}] agregado a la DB!.")
                                await message.channel.send(f"+1 karmagiven para <{IRCusername}>. Welcome to the karma user list! ")
                        
                        # Insert palabra en la DB para karma-- y se imprime confirmacion
                        elif texto.endswith("--"):
                            initial_karma = -1 ## <-- Como es una nueva palabra y es --, el karma inicial siempe es de -1
                            cursorkarma.execute("INSERT INTO karma (palabra, karmavalue, isuser, karmagiven) VALUES (?, ?, 'NO', ?)", (palabra_base, initial_karma, 0))
                            databasekarma.commit()
                            cursorkarma.execute("SELECT karmavalue FROM karma WHERE palabra = ?", (palabra_base,))
                            updated_karma = cursorkarma.fetchone()[0]
                            print(FechaActual)
                            print(f"Nueva palabra agregada a la DB. Karma--  para {palabra_base}")
                            await message.channel.send(f"-1 karma para {palabra_base}. Current karma = {updated_karma}")

##################################################################################################################     
# Todo esto se ejecuta cuando el usuario NO es el bot (o sea, un usuario normal nativo de Discord)

        else:
            # Traemos el texto del mensaje y lo buscamos en la base
            textokarma = message.content.split()
            
            for texto in textokarma:
                if texto.endswith("++") or texto.endswith("--"):
                    palabra_base = texto[:-2]
                    cursorkarma.execute("SELECT * FROM karma WHERE palabra = ?", (palabra_base,))
                    cursorusers.execute("SELECT * FROM usuarios WHERE username = ?", (message.author.name,))
                    print(f"Palabra base detectada antes del if de existing workd: {palabra_base}")

                    # Ejecuta query para verificar si la palabra existe en la DB
                    cursorkarma.execute("SELECT * FROM karma WHERE palabra = ?", (palabra_base,))
                    existing_word = cursorkarma.fetchone()
                    

                    # Si la palabra existe, procede con las funciones de UPDATE
                    if existing_word:
                            print(f"encontre la palabra en la base de datos {palabra_base}")

                            # Update word en la DB para karma++
                            if texto.endswith("++"):
                                cursorkarma.execute("UPDATE karma SET karmavalue = karmavalue + 1 WHERE palabra = ?", (palabra_base,))
                                databasekarma.commit()
                                cursorkarma.execute("SELECT karmavalue FROM karma WHERE palabra = ?", (palabra_base,))
                                updated_karma = cursorkarma.fetchone()[0]
                                print(FechaActual)
                                print(f"Karma ++ para {palabra_base}")
                                await message.channel.send(f"+1 karma para {palabra_base}. Current karma is: {updated_karma}")

                                # Se le da karmagiven al usuario y se imprime mensaje
                                cursorusers.execute("UPDATE usuarios SET karmagiven = karmagiven + 1 WHERE username = ?", (message.author.name,))
                                databaseusers.commit()
                                cursorusers.execute("SELECT karmagiven FROM usuarios WHERE username = ?", (message.author.name,))
                                updated_karmagivenusr = cursorusers.fetchone()[0]
                                print(f"Se ha dado karmagiven +1 a {message.author.name}.")
                                await message.channel.send(f"+1 karmagiven para {message.author}. Current karmagiven is: {updated_karmagivenusr}")

                            
                            # Update palabra en la DB para karma--
                            elif texto.endswith("--"):
                                cursorkarma.execute("UPDATE karma SET karmavalue = karmavalue - 1 WHERE palabra = ?", (palabra_base,))
                                databasekarma.commit()
                                cursorkarma.execute("SELECT karmavalue FROM karma WHERE palabra = ?", (palabra_base,))
                                updated_karma = cursorkarma.fetchone()[0]
                                print(FechaActual)
                                print(f"Karma -- para {palabra_base}")
                                await message.channel.send(f"-1 karma para {palabra_base}. Current karma is: {updated_karma}")
        
                    # Si la palabra no existe, procede con las funciones de INSERT
                    else:
                        # Insert palabra en la DB para karma++
                        if texto.endswith("++"):
                            initial_karma = 1
                            cursorkarma.execute("INSERT INTO karma (palabra, karmavalue, isuser, karmagiven) VALUES (?, ?, 'NO', ?)", (palabra_base, initial_karma, 0))
                            databasekarma.commit()
                            cursorkarma.execute("SELECT karmavalue FROM karma WHERE palabra = ?", (palabra_base,))
                            updated_karma = cursorkarma.fetchone()[0]
                            print(FechaActual)
                            print(f"Nueva palabra agregada a la DB. Karma ++ para {palabra_base}")
                            await message.channel.send(f"+1 karma para {palabra_base}. Current karma is: {updated_karma}")

                            # Se le da karmagiven al usuario y se imprime mensaje
                            cursorusers.execute("UPDATE usuarios SET karmagiven = karmagiven + 1 WHERE username = ?", (message.author.name,))
                            databaseusers.commit()
                            cursorusers.execute("SELECT karmagiven FROM usuarios WHERE username = ?", (message.author.name,))
                            updated_karmagivenusr = cursorusers.fetchone()[0]
                            print(f"Se ha dado karmagiven +1 a {message.author.name}.")
                            await message.channel.send(f"+1 karmagiven para {message.author}. Current karmagiven is: {updated_karmagivenusr}")
                        
                        # Insert palabra en la DB para karma--
                        elif texto.endswith("--"):
                            initial_karma = -1
                            cursorkarma.execute("INSERT INTO karma (palabra, karmavalue, isuser, karmagiven) VALUES (?, ?, 'NO', ?)", (palabra_base, initial_karma, 0))
                            databasekarma.commit()
                            cursorkarma.execute("SELECT karmavalue FROM karma WHERE palabra = ?", (palabra_base,))
                            updated_karma = cursorkarma.fetchone()[0]
                            print(FechaActual)
                            print(f"Nueva palabra agregada a la DB. Karma -- para {palabra_base}")
                            await message.channel.send(f"-1 karma para {palabra_base}. Current karma is: {updated_karma}")

    databasekarma.commit()
    databasekarma.close()
    databaseusers.commit()
    databaseusers.close()

################### FUNCION DE ON_MESSAGE PARA YELLING ###################

#Lee el canal de Yelling
    if message.channel.id == 1209436952969879562: 

#Chequeea por lowercase. Putea solo con haber un solo caracter en lowercase. No jodan.
        if any(char.islower() for char in message.content): 
            print(FechaActual)
            print("Mensaje en lower case detectado en canal. Se ejecutara funcion de Yelling")

#Agarra frases random de un txt y las manda en respuesta al mensaje (para mas humillacion)
            with open("src/rtasyelling.txt", "r", encoding="utf8") as file: 
                lines = file.readlines()
            await message.reply(random.choice(lines).strip())

    await bot.process_commands(message) # <-- No tocar esto jamas o rompe los comandos on_message. Siempre dejar al final de la funcion on_message

#########################################################################################
################### LLAMADAS DE COMANDOS TEXT BASED (USA FUNCION CTX) ###################

# Comandos indivuduales estan en .src/ctxcommands

# COMANDO HELP
@bot.command()
async def help(ctx, texto):
    await helpfunctx(ctx, texto)

# COMANDO CLIMA   
@bot.command()
async def clima(ctx, ciudad):
    await climafunctx(ctx, ciudad)

# COMANDO CRIPTO
@bot.command()
async def cripto(ctx):
    await criptofunctx(ctx)

# COMANDO FULBO
@bot.command()
async def fulbo(ctx, liga):
    await fulbofunctx(ctx, liga)   

# COMANDO DOLAR
@bot.command()
async def dolar(ctx):
    await dolarfunctx(ctx)

# COMANDO FERIADOS
@bot.command()
async def feriadoar(ctx):
    await feriadoarfunctx(ctx)

@bot.command()
async def feriadoes(ctx):
    await feriadoesfunctx(ctx)

@bot.command()
async def feriadocl(ctx):
    await feriadoclfunctx(ctx)

@bot.command()
async def feriadouy(ctx):
    await feriadouyfunctx(ctx)    

@bot.command()
async def feriadomx(ctx):
    await feriadomxfunctx(ctx)   

# COMANDO SUBTE
@bot.command()
async def subte(ctx):
    await subtefunctx(ctx)       

# COMANDO UNDERGROUND
@bot.command()
async def underground(ctx):
    await undergroundfunctx(ctx)

# COMANDO EURO       
@bot.command()
async def euro(ctx):
    await eurofunctx(ctx)   

# COMANDO KARMA RANK
@bot.command()
async def rank(ctx):
    await karmarankfunctx(ctx)

# COMANDO KARMA PALABRA
@bot.command()
async def karma(ctx, text):
    await karmawordfunctx(ctx, text)

# COMANDO RANK GIVERS              
@bot.command()
async def kgivers(ctx):
    await karmagiversfunctx(ctx)

# COMANDO KARMA GIVERS POR USUARIO            
@bot.command()
async def kgiven(ctx, text):
    await karmagiversuserfunctx(ctx, text)

# COMANDO QUOTE ADD
@bot.command()
async def qadd(ctx, *, quote: str):
    await quoteaddfunctx(ctx, quote)

# COMANDO QUOTE RANDOM
@bot.command()
async def q(ctx):
    await quotefunctx(ctx)

# COMANDO QUOTE SEARCH
@bot.command()
async def qsearch(ctx, texto):
    await qsearchfunctx(ctx, texto)

#########################################################################################
################### LLAMADAS DE COMANDOS SLASH NATIVOS DISCORD (TREE) ###################

# Comandos individuales estan en .src

# COMANDO DOLAR
@bot.tree.command(name="preciodolar", description="Cotizacion del dolar")
async def preciodolar(interaction: Interaction):
    try:
        await interaction.response.send_message(embed= await dolarfun(interaction))
    except:
        print(f"Limite de API calls excedido. Ultimo call hecho por {interaction.user}")
        await interaction.response.send_message("Comando /dolar: Limite de API calls excedido. Sori el CTO no nos dio budget.")

# COMANDO EURO
@bot.tree.command(name="precioeuro", description="Cotizacion del Euro")
async def precioeuro(interaction: Interaction):
    try:
        await interaction.response.send_message(embed= await eurofun(interaction))
    except:
        print(f"Limite de API calls excedido. Ultimo call hecho por {interaction.user}")
        await interaction.response.send_message("Comando /euro: Limite de API calls excedido. Sori el CTO no nos dio budget.")

# COMANDO CLIMA
@bot.tree.command(name="clima", description="Información del clima")
async def Clima(interaction: Interaction, city:str):
    try:
        await interaction.response.send_message(embed=await climafun(interaction, city))  
    except:
        print(f"Limite de API calls excedido. Ultimo call hecho por {interaction.user}")
        await interaction.response.send_message("Comando /clima: Limite de API calls excedido. Sori el CTO no nos dio budget.")

# COMANDO LONDON UNDERGROUND
@bot.tree.command(name="underground", description="Información del London Underground")
async def londonunderground(interaction: Interaction):
    try:
        await interaction.response.send_message(embed=Lines())
    except:
        print(f"Limite de API calls excedido. Ultimo call hecho por {interaction.user}")
        await interaction.response.send_message("Comando /underground: Limite de API calls excedido. Sori el CTO no nos dio budget.")
    
# COMANDO HELP
@bot.tree.command(name="help", description="Como usar el bot")
async def ayudatree(interaction: Interaction):
    try:
        await interaction.response.send_message(embed= await helpfunc(interaction), ephemeral=True)
    except:
        pass

# COMANDO SUBTE
@bot.tree.command(name="subtebsas", description="Información de los Subtes")
async def subtebsas(interaction: Interaction):
    try:
        await interaction.response.send_message(embed=await SubteBA(interaction))
    except:
        print(f"Limite de API calls excedido. Ultimo call hecho por {interaction.user}")
        await interaction.response.send_message("Comando /subte: Limite de API calls excedido. Sori el CTO no nos dio budget.")

# COMANDO FULBO
@bot.tree.command(name="fulbo", description="Ultimos resultados de ligas de futbol")
async def futlbol(interaction: Interaction):
    try:
        await interaction.response.send_message(embed=await futbolimport(interaction))
    except:
        pass

# COMANDO CRIPTO
@bot.tree.command(name="cripto", description="Precio de criptomonedas")
async def preciocripto(interaction: Interaction):
    try:
        await interaction.response.send_message(embed= await criptofun(interaction))
    except:
        print(f"Limite de API calls excedido. Ultimo call hecho por {interaction.user}")
        await interaction.response.send_message("Comando /cripto: Limite de API calls excedido. Sori el CTO no nos dio budget.")

# COMANDO FERIADO ARGENTINA
@bot.tree.command(name="feriadoar", description="Proximos feriados en Argentina")
async def feriadosar(interaction: Interaction):
    try:
        await interaction.response.send_message(embed= await feriadoARfun(interaction))
    except:
        print(f"Limite de API calls excedido. Ultimo call hecho por {interaction.user}")
        await interaction.response.send_message("Comando /feriadoar: Limite de API calls excedido. Sori el CTO no nos dio budget.")

# COMANDO FERIADO URUGUAY
@bot.tree.command(name="feriadouy", description="Proximos feriados en Uruguay")
async def feriadosuy(interaction: Interaction):
    try:
        await interaction.response.send_message(embed= await feriadoUYfun(interaction))
    except:
        print(f"Limite de API calls excedido. Ultimo call hecho por {interaction.user}")
        await interaction.response.send_message("Comando /feriadoar: Limite de API calls excedido. Sori el CTO no nos dio budget.")
    
# COMANDO FERIADO CHILE
@bot.tree.command(name="feriadocl", description="Proximos feriados en Chile")
async def feriadoscl(interaction: Interaction):
    try:
        await interaction.response.send_message(embed= await feriadoCLfun(interaction))
    except:
        print(f"Limite de API calls excedido. Ultimo call hecho por {interaction.user}")
        await interaction.response.send_message("Comando /feriadoar: Limite de API calls excedido. Sori el CTO no nos dio budget.")

# COMANDO FERIADO ESPAÑA
@bot.tree.command(name="feriadoes", description="Proximos feriados en España")
async def feriadoses(interaction: Interaction):
    try:
        await interaction.response.send_message(embed= await feriadoESfun(interaction))
    except:
        print(f"Limite de API calls excedido. Ultimo call hecho por {interaction.user}")
        await interaction.response.send_message("Comando /feriadoar: Limite de API calls excedido. Sori el CTO no nos dio budget.")

# COMANDO FERIADO MEXICO
@bot.tree.command(name="feriadomx", description="Proximos feriados en Mexico")
async def feriadosmx(interaction: Interaction):
    try:
        await interaction.response.send_message(embed= await feriadoMXfun(interaction))
    except:
        print(f"Limite de API calls excedido. Ultimo call hecho por {interaction.user}")
        await interaction.response.send_message("Comando /feriadoar: Limite de API calls excedido. Sori el CTO no nos dio budget.")
    
# COMANDO KARMA RANK
@bot.tree.command(name="karmarank", description="Ranking top 10 usuarios")
async def karmarank(interaction: Interaction):
    await interaction.response.send_message(embed = await karmarankfunc(interaction))

# COMANDO KARMA GIVERS
@bot.tree.command(name="karmagivers", description="Ranking top 5 dadores de karma")
async def karmagivers(interaction: Interaction):
    await interaction.response.send_message(embed= await karmagiversfunc(interaction))

# COMANDO KARMA USER
@bot.tree.command(name="karmauser", description="Ver Karma de un usuario")
async def karmauser(interaction: Interaction, member: discord.Member):
    await interaction.response.send_message(embed= await karmauserfunc(interaction, member))

# COMANDO QUOTE RANDOM
@bot.tree.command(name="quote", description="Devuelve un quote random del hisotrial")
async def quoterandom(interaction: Interaction):
    await interaction.response.send_message(embed= await quotefunc(interaction))

# COMANDO QUOTE SEARCH
@bot.tree.command(name="qsearch", description="Busca un Quote en base a texto")
async def quotesearch(interaction: Interaction, texto:str):
    await interaction.response.send_message(embed= await qsearchfunc(interaction, texto))

if __name__ == '__main__':
    main()

#########################################################################################
##################################### END OF CODE #######################################