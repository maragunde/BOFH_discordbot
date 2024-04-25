import discord
from discord.ui import Select, View
from datetime import datetime


# El mensaje detallado de help y de funcionamiento de comandos es demasiado largo y excede los caracteres del response de Discord (2000).
# Por ahora lo solucionamos mandano a la gente a un canal de help y chau. La idea para el futuro es tener helps especificos para cada comando

async def helpfunc(interaction):
  FechaActual = datetime.now()
  await interaction.response.send_message("Si necesitas ayuda, todos los detalles de como usar el bot estan en el canal #help-bot-commands", ephemeral=True)
