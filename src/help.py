import discord
from discord.ui import Select, View
from datetime import datetime
import logging

# El mensaje detallado de help y de funcionamiento de comandos es demasiado largo y excede los caracteres del response de Discord (2000).
# Por ahora lo solucionamos enviando a los usuarios a un canal de ayuda. En el futuro, implementaremos ayuda específica para cada comando.

async def helpfunc(interaction: discord.Interaction):
    # Configurar logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    # Log de la ejecución del comando
    logger.info(f"Se ha ejecutado el comando /help por el usuario {interaction.user}")

    # Crear un embed para una respuesta más atractiva
    embed = discord.Embed(
        title="Ayuda del Bot",
        description="Todos los detalles sobre cómo usar el bot están disponibles en un canal dedicado.",
        color=discord.Color.blue()
    )
    embed.add_field(name="Canal de Ayuda", value="#help-bot-commands", inline=False)
    embed.set_footer(text="Para obtener ayuda específica, visita el canal mencionado.")

    # Enviar el mensaje de ayuda como un embed efímero
    await interaction.response.send_message(embed=embed, ephemeral=True)
