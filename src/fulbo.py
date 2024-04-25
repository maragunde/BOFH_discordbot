import discord
from discord import Interaction
from discord.ui import Select, View
from src.fulboapi import fulboapicall

# Esta sub-funcion funciona en conjunto con fulboapi.py. Lo separamos por una cuestion higienica, en caso de que en el futuro se quiten o agreguen ligas

# Se crea el select donde el usuario elige la liga
async def futbolimport(message):
        select = Select(options =[
            discord.SelectOption(label="Premier League", value="PL", emoji="🏴󠁧󠁢󠁥󠁮󠁧󠁿"),
            discord.SelectOption(label="Bundesliga", value="BL1", emoji="🇩🇪"),
            discord.SelectOption(label="La liga", value="PD", emoji="🇪🇸"),
            discord.SelectOption(label="League 1", value="FL1", emoji="🇫🇷"),
            discord.SelectOption(label="Serie A", value="SA", emoji="🇮🇹")
        ])

       # Devuelve el resultado de la liga en base a lo que selecciono (trae cada resultado de fulboapy.py)
        async def respuesta(interaction):
             try:
              selected_value= interaction.data["values"][0]
              if selected_value== "PL":
                    await interaction.response.send_message(embed = await fulboapicall("PL", interaction, "🏴󠁧󠁢󠁥󠁮󠁧󠁿" ))
              elif selected_value == "BL1":
                     await interaction.response.send_message(embed = await fulboapicall("BL1", interaction, "🇩🇪" ))
              elif selected_value == "PD":
                     await interaction.response.send_message(embed = await fulboapicall("PD", interaction,"🇪🇸" ))
              elif selected_value == "FL1":
                     await interaction.response.send_message(embed = await fulboapicall("FL1", interaction, "🇫🇷" ))
              elif selected_value == "SA":
                     await interaction.response.send_message(embed = await fulboapicall("SA", interaction, "🇮🇹" ))
             except:
                  await interaction.response.send_message("Comando /fulbo: Limite de API calls excedido. Sori el CTO no nos dio budget.")

        select.callback = respuesta
        view = View()
        view.add_item(select)

       # Pregunta que liga al usuario
        await  message.channel.send("Que liga?", view=view)