import discord
from datetime import datetime
from discord.ext import commands



async def helpfunctx(ctx, texto):
    FechaActual = datetime.now()
    
    if texto is None:
        
        mensajeayuda_general = """Informacion general sobre los comandos del bot de Sysarmy       
                          !dolar !cripto !euro !fulbo !clima !subte !underground !feriadoAR !feriadoCL !feriadoES !feriadoMX !feriadoUY !q !qsearch !qadd !rank !kgivers !kgiven !karma
                          Mas detalles en el canal #help-bot-commands de Discord, dentro de la seccion de Welcome! - o ejecutando /help desde Discord"""
        await ctx.send(mensajeayuda_general)
   
    elif texto == "clima":
        mensajeayuda_clima = """clima en Discord o !clima para usuarios externos. Devuelve el clima en base a la ciudad de input. Ej: '!clima London'. 
                                Recordar poner bien el input de la ciudad. Tener en cuenta que algunas ciudades pueden llevar el nombre en ingles (por ejemplo, London)
                            """
        await ctx.send(mensajeayuda_clima)
    elif texto == "karma":
        mensajeayuda_karma = """/karma en Discord o !karma para usuarios externos. Devuelve el karma de la palabra o usuario que se inserte. Ej: '!karma ubuntu'. Para dar karma
                                usar ++ o -- en cada palabra o usuario. Ej: 'ubuntu--' o jedux++'
                            """
        await ctx.send(mensajeayuda_karma)
    elif texto == "fulbo":
        mensajeayuda_fulbo = """fulbo en Discord o !fulbo para usuarios externos. Devuelve los resultados de la ultima fecha de la liga seleccionada ('!fulbo BL1'). 
                                Ligas disponibles ==> PL = Premiere League, BL1 = Bundesliga, PD = La Liga España, FL1 = Liga Francia, SA = Serie A Italia
                            """
        await ctx.send(mensajeayuda_fulbo)
    elif texto == "qadd":
        mensajeayuda_qadd = """Agrega todo el texto insertado despues del comando. EL_FORMATO IS DEFINED AS: <@supreme_leader> because I say so. | <peasant1> yes m'Lord. 
                                | <peasant2> it wont happen again, Sire. | <peasant-n> please forgive us.
                            """
        await ctx.send(mensajeayuda_qadd)

    elif texto == "cripto":
        await ctx.send("Pone !cripto y te da los precios de la timba. No requiere argumentos")

    elif texto == "dolar":
        await ctx.send("Pone !dolar y te da los precios de la timba. No requiere argumentos")

    elif texto == "feriado" or "feriadoar" or "feriadomx" or "feriadoes" or "feriadocl" or "feriadouy":
      await ctx.send("Pone !feriadouy !feriadoar !feriadocl !feriadoes !feriadomx y te da los proximos feriados. No requiere argumentos")   

    elif texto == "euro":
      await ctx.send("Pone !euro y te da los precios de la timba. No requiere argumentos")
    
    elif texto == "subte":
      await ctx.send("Pone !subte y te da el estado del subte en Buenos Aires. No requiere argumentos")

    elif texto == "underground":
      await ctx.send("Pone !underground y te da el estado del subte en Londres. No requiere argumentos")

    elif texto == "underground":
      await ctx.send("Pone !underground y te da el estado del subte en Londres. No requiere argumentos")

    # Log
    print(FechaActual)
    print ("Se ha ejecutado el comando !help")