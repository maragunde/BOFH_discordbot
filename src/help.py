import discord
from discord.ui import Select, View
from datetime import datetime

async def helpfunc(interaction):
  FechaActual = datetime.now()
  await interaction.response.send_message("Si necesitas ayuda, todos los detalles de como usar el bot estan en el canal #help-bot-commands", ephemeral=True)


'''

OLD VERSION 

async def helpfunc(message):
  FechaActual = datetime.now()

# MENSAJES DE RESPUESTA DE HELP - Guarda: hay un limite de caracteres de 2000. Si se tienen que agregar cosas en el futuro, es posible que haya que partirlo en mas mensajes
  mensajecomandos = ("""       
                    ### COMANDOS     
                    !dolar
                    Este comando devuelve el precio del dolar al dia de la fecha. Usamos la api de dolarapi.com
                    !cripto
                    Este comando devuelve el precio de monedas cripto al dia de la fecha. Usamos la api de coinranking.com. Para sugerencias de monedas, decile a algun root de sysarmy
                    !euro
                    Este comando devuelve el precio del euro al dia de la fecha. Usamos la api de theforexapi.com                   
                    !fulbo
                    Este comando devuelve los resultados de la ultima fecha de la liga seleccionada (premier, bundes, seriea, laliga, league1. Ej: "!fulbo laliga)
                    !clima
                    Este comando devuelve el estado del clima para una ciudad seleccionada. Asegurate de poner el nombre de la ciudad correctamente. Usamos la api de weatherapi.com.                    
                    !subte
                    Este comando devuelve el estado del subte de Buenos Aires. Usamos la api de apitransporte.buenosaires.gob.ar
                    !tube
                    Este comando devuelve el estado del subte de Londres. Usamos la api de tfl.gov.uk
                    !feriadoAR - !feriadoCL - !feriadoES - !feriadoMX - !feriadoUY
                    Este comando devuelve los proximos feriados para cada pais. Usamos la api de date.nager.at. Para sugerencias de nuevos paises, decile a algun root de sysarmy
        """)
  mensajekarma = ("""       
                    ### COMANDOS    
                    !rank
                    Este comando devuelve el ranking del top 10 de usuarios con mas Karma
                    !karmagivers
                    Este comando devuelve el ranking del top 10 de usuarios que mas dan Karma
                    !karmauser
                    Este comando devuelve el karma para un usuario especifico. Asegurate de poner bien el formato del usuario de Discord sin el "@". Ej: "!karmauser aragunde"
                  
                    ### KARMA
                    reaccion kup ==> Da +1 de Karma al autor del mensaje al que se reacciona. Si la reaccion se quita, el punto de Karma tambien es quitado.
                    reaccion kup ==> Da -1 de Karma al autor del mensaje al que se reacciona. Si la reaccion se quita, el punto de Karma tambien es devuelto.
                    Cada usuario tiene un maximo de 10 puntos de Karma para entregar por dia. El budget de Karma se resetea diariamente a las 00hs, hora de Argentina.
                    
        """)
  mensajequotes = ("""       
                    
                    ### COMANDOS
                    !q
                    Este comando devuelve un quote random del archivo historico de sysarmy
                    !qsearch
                    Este comando devuelve 3 quotes random en base al texto que el ususario da de input. El texto puede incluir nombre de usuario. Ej: "!qsearch ubuntu"

                    ### QUOTING
                    reaccion qadd ==> Se agrega el mensaje reaccionado al archivo historico de quotes de sysarmy. Si la reaccion se quita, el quote se remueve
                    Cada usuario tiene un maximo de 1 quote para hacer por dia. El budget de quote se resetea diariamente a las 00hs, hora de Argentina.
    
        """)

#Se crea el select donde el usuario elige sobre que necesita ayuda
  select = Select(options =[
      discord.SelectOption(label="Ayuda sobre Karma", value="karma"),
      discord.SelectOption(label="Ayuda sobre quotes", value="quotes"),
      discord.SelectOption(label="Ayuda sobre comandos generales", value="comandos")
      ])
  
#Devuelve el mensaje de ayuda en base a la seleccion
  async def respuesta(interaction):
      selected_value= interaction.data["values"][0]
      if selected_value== "karma":
          await interaction.response.send_message(mensajekarma, ephemeral=True)
      elif selected_value == "comandos":
          await interaction.response.send_message(mensajecomandos, ephemeral=True)
      elif selected_value == "quotes":
          await interaction.response.send_message(mensajequotes, ephemeral=True)

  select.callback = respuesta
  view = View()
  view.add_item(select)

#Log
  print(FechaActual)
  print(f"Se ha ejecutado el comando Help")


#Pregunta que liga al usuario
  await message.channel.send("Sobre que necesitas ayuda? Recorda que", view=view)
'''  
  
  