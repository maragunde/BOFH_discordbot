import discord
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# Diccionario para almacenar la ultima fecha de posteo (para verificar dps que el user solo pueda postear una vez x dia)
user_last_post_time = {}

# Clase con las opciones para el formulario que se muestra. Ya tiene maximo de 5 (No se puede mas, Discord te putea)
class JobPostModal(discord.ui.Modal, title="Postear nuevo job"):
    job_title = discord.ui.TextInput(label="Job Title - seniority", placeholder="Ej: Backend Developer - Semi Senior", max_length=120)
    job_link = discord.ui.TextInput(label="Link", placeholder="Pega el link a la posición", style=discord.TextStyle.short)
    salary = discord.ui.TextInput(label="Salario", placeholder="Rango salarial", style=discord.TextStyle.short)
    company = discord.ui.TextInput(label="Empresa / Consultora", placeholder="Empresa / Consultora", style=discord.TextStyle.short)
    description = discord.ui.TextInput(label="Descripción", placeholder="Job description - Por favor se breve", style=discord.TextStyle.long)


    # METODO DE ON SUBMIT PARA CUANDO SE COMPLETA EL POST
    async def on_submit(self, interaction: discord.Interaction):
        FechaActual = datetime.now()

        # Check y manejo de fecha para que solo pueda postear 1 vez por dia
        user_id = interaction.user.id
        if user_id in user_last_post_time:
            last_post_time = user_last_post_time[user_id]

            if FechaActual - last_post_time < timedelta(days=1):
                await interaction.response.send_message("Solo puedes postear una vez por día. Intentalo de nuevo más tarde.", ephemeral=True)
                return

        # Traemos el canal de foro y verificamos que se postee correctamente (los thread channels funcionan distinto)
        JobsChannel = int(os.getenv('JobsChannel'))
        forum_channel = discord.utils.get(interaction.guild.channels, id=JobsChannel)
        if not isinstance(forum_channel, discord.ForumChannel):
            await interaction.response.send_message("El canal no es del tipo foro", ephemeral=True)
            return

        # Formateo del hyperlink para mostrar en el job post
        job_link_markdown = f"{self.job_link.value}"

        # Enviamos un mensaje para que el usuario seleccione los tags con un dropdown (esto se ejecuta al final)
        await interaction.response.send_message(
            f"Por favor, selecciona las etiquetas para la posición: **{self.job_title.value}**",
            view=TagSelectView(forum_channel, self.job_title.value, job_link_markdown, self.salary.value, self.company.value, self.description.value),
            ephemeral=True
        )

        # Updateamos la fecha de posteo del user
        user_last_post_time[user_id] = FechaActual


# CLASE PARA MANEJAR EL DROPDOWN DE SELECCION DE TAGS
class TagSelectView(discord.ui.View):
    def __init__(self, forum_channel, job_title, job_link, salary, company, description):
        super().__init__()
        self.forum_channel = forum_channel
        self.job_title = job_title
        self.job_link = job_link
        self.salary = salary
        self.company = company
        self.description = description

        # Agregamos un dropdown para los tags
        self.add_item(TagSelect(forum_channel))

    # METODO PRINCIPAL PARA CREAR EL THREAD POST EN EL CANAL
    async def complete_post(self, interaction: discord.Interaction, selected_tags):
        JobsChannel = int(os.getenv('JobsChannel'))
        forum_channel = discord.utils.get(interaction.guild.channels, id=JobsChannel)

        # Convertimos los tags seleccionados de string a objeto (no pregunten por que, pero Discord es asi)
        selected_tag_objects = [
            tag for tag in forum_channel.available_tags if tag.name in selected_tags
        ]
      
        # Creamos el contenido del thread post
        thread_content = (
            f"**Link:** {self.job_link}\n"
            f"------\n"
            f"**Salario:** {self.salary}\n"
            f"------\n"
            f"**Recruiter: <@{interaction.user.id}>**\n"
            f"------\n"
            f"**Descripción:** {self.description}"
        )

        # Verificamos la longitud antes de intentar postear el thread
        if len(thread_content) > 2000:
            await interaction.response.send_message(
                f"El contenido total supera el límite de 2000 caracteres (actual: {len(thread_content)}). "
                "Por favor, acorta algunos campos.",
                ephemeral=True
            )
            # Log
            print("Comando /jobpost failed - Supera 2000 caracteres")
            return

        # Si la longitud es válida, creamos el thread
        thread = await forum_channel.create_thread(
            name=f"{self.job_title} - {self.company}",
            content=thread_content,
            applied_tags=selected_tag_objects  # Pasamos los tags
        )

        # Log
        FechaActualLog = datetime.now()
        print(FechaActualLog)
        print(f"Se ha ejecutado el comando /jobpost por {interaction.user}")

        # Confirmación al usuario
        await interaction.response.send_message(f"Posición posteada exitosamente! Revisa el job board", ephemeral=True)


# DEFINICION DEL DROPDOWN PARA SELECCION DE TAGS
class TagSelect(discord.ui.Select):
    def __init__(self, forum_channel):

        # Traemos los tags disponibles para el canal y los convertimos a objetos de SelectOption
        tags = forum_channel.available_tags 
        options = [
            discord.SelectOption(label=tag.name, description=tag.name) for tag in tags
        ]

        super().__init__(
            placeholder="Selecciona los tags (3 max)",
            min_values=1,  # Mínimo de tags
            max_values=3,  # Máximo de tags
            options=options 
        )

    # Funcion de callback para ejecutar el complete post
    async def callback(self, interaction: discord.Interaction):
        if isinstance(self.view, TagSelectView):
            await self.view.complete_post(interaction, self.values)
        else:
            await interaction.response.send_message("Error, algo pinchó. Por favor contactar a admin.", ephemeral=True)