import discord
import json
import os
from dotenv import load_dotenv
from src.discordjobs.postjob_bulk_convert import process_all_new_excels
from .shortlink import create_shortlink

load_dotenv()

# Funcion principal de job post
async def bulkjobpost(interaction: discord.Interaction):
    
    await interaction.response.defer()  # Esto es para que no pinche con timeout
    
    # Procesamos los archivos de Excel antes de continuar
    print("Discord Jobs - ✅ Procesando archivos nuevos...")
    if not process_all_new_excels():
        await interaction.followup.send("Discord Jobs - ⚠️ Advertencia. No hay archivos nuevos que procesar")
        return

    # Cargamos la data del JSON (ahora ya debería estar actualizado)
    job_file = "src/discordjobs/bulk/job.json"
    if not os.path.exists(job_file):
        await interaction.followup.send("Discord Jobs - ❌ No encontre archivo JSON. Revisa que onda")
        return
    
    with open(job_file, "r", encoding="utf-8") as file:
        job_list = json.load(file)
    
    if not job_list:
        await interaction.followup.send("Discord Jobs - ⚠️ No hay nuevos jobs para postear")
        return
    
    # Traemos el canal
    JobsChannel = int(os.getenv('JobsChannel'))
    forum_channel = discord.utils.get(interaction.guild.channels, id=JobsChannel)
    
    # Posteo de jobs
    posted_count = 0
    for job_data in job_list:
        
        if not job_data.get('job_title') or not job_data.get('company'): # Skipeamos jobs que no tengan por lo menos un job title y la empresa
            continue
            
        job_title = job_data.get('job_title', 'Sin título')
        job_link = create_shortlink(job_data.get('job_link')) if job_data.get('job_link') else ''
        salary_range = job_data.get('salary_range', 'No especificado')
        company = job_data.get('company', 'No especificado')
        job_description = job_data.get('job_description', 'Sin descripción')
        discord_id = job_data.get('discord_id', '1235914603435790377')
        tags = [tag.strip() for tag in job_data.get('tags', '').split(",") if tag.strip()]
        job_scheme = job_data.get('job_scheme', 'No especificado')
        location = job_data.get('location', 'No especificada')
        experiencia = job_data.get('experiencia', 'No especificada')
        ingles = job_data.get('ingles')
        print(job_link)

        # Convertimos las tags a objetos para poder appendearlos al post
        selected_tag_objects = [
            tag for tag in forum_channel.available_tags if tag.name.lower() in [t.lower() for t in tags]
        ]

        # Convertimos el ID a mention de discord. Si no hay ID de Discord, mandamos el del bot
        try:
            discord_id = discord_id.strip()
            discord_mention = f"<@{discord_id}>" if discord_id.isdigit() else "1235914603435790377"
        except:
            discord_mention = "No especificado"

        # Body de contenido del post
        thread_content = (
            f"**Link:** {job_link}\n"
            f"------\n"
            f"**Salario:** {salary_range}\n"
            f"------\n"
            f"**Descripción:** {job_description}\n"
            f"------\n"
            f"**Location:** {location}\n"
            f"------\n"
            f"**Esquema:** {job_scheme}\n"
            f"------\n"
            f"**Experiencia:** {experiencia}\n"
            f"------\n"
            f"**Ingles:** {ingles}\n"
            f"------\n"
            f"**Publicado por:** {discord_mention}"
        )

        # Posteamos el job en el foro
        try:
            thread = await forum_channel.create_thread(
                name=f"{job_title} - {company}",
                content=thread_content,
                applied_tags=selected_tag_objects
            )
            posted_count += 1
            print(f"Discord Jobs - 📢 Nuevo job posteado: {job_title} - {company}")
        except Exception as e:
            print(f"Discord Jobs - ⚠️ Error posteando job {job_title}: {e}")

    # Mensaje de confirmacion
    await interaction.followup.send(f"Discord Jobs - ✅ Se han posteado {posted_count} jobs.")
    
    # Limpiamos el JSON para poder procesar un nuevo batch
    with open(job_file, "w", encoding="utf-8") as file:
        json.dump([], file)