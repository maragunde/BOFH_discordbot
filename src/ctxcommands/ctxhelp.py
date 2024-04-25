import discord
from datetime import datetime

async def helpfunctx(ctx):
  FechaActual = datetime.now()

# MENSAJES DE RESPUESTA DE HELP - Guarda: hay un limite de caracteres de 2000. Si se tienen que agregar cosas en el futuro, es posible que haya que partirlo en mas mensajes
  mensajeayuda = ("""Informacion general sobre los comandos del bot de Sysarmy       
                    !dolar !cripto !euro !fulbo !clima !subte !underground !feriadoAR !feriadoCL !feriadoES !feriadoMX !feriadoUY !q !qsearch !qadd !rank !kgivers !kgiven !karma
                     Mas detalles en el canal #help-bot-commands de Discord, dentro de la seccion de Welcome! - o ejecutando /help desde Discord
                  """)
  
  # Se manda el mensaje
  user = ctx.author
  await ctx.send(mensajeayuda)
  
#Log
  print(FechaActual)
  print(f"Se ha ejecutado el comando Help")
