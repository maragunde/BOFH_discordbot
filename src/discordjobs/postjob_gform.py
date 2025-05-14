import discord
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from .shortlink import create_shortlink

load_dotenv()
FechaActual = datetime.now()

# Traemos el JSON
async def fetch_json():
    file_path = "src/discordjobs/gform_job.json"
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            job_data = json.load(file)
            return job_data
    except FileNotFoundError:
        print(f"Discord Jobs (Gform) - ❌ Error: gforms_jobbs.json no encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"Discord Jobs (Gform) - ❌ Error: JSON invalido.")
        return None

async def gformjobpost(bot, job_data):

    # Traemos los canales
    JobsChannel = int(os.getenv('JobsChannel'))
    SysarmyChannel = int(os.getenv('SysarmyChannel'))
    forum_channel = bot.get_channel(JobsChannel)
    sysarmy_channel = bot.get_channel(SysarmyChannel)


    # Parseamos los datos del JSON
    job_title = job_data['job_title']
    job_link = create_shortlink(job_data['job_link'])
    salary_range = job_data['salary_range']
    company = job_data['company']
    job_description = job_data['job_description']
    discord_id = job_data['discord_id']
    tags = [tag.strip() for tag in job_data['tags'].split(",")]
    job_scheme = job_data['job_scheme']
    location = job_data['location']
    experiencia = job_data['experiencia']
    ingles = job_data['ingles']

    # Ponemos el job link en markdown para que no rompa
    job_link_markdown = f"{job_link}"

    # Convertimos los tags a los tags objects diponibles en el canal de foro
    selected_tag_objects = [
        tag for tag in forum_channel.available_tags if tag.name.lower() in [t.lower() for t in tags]
    ]

    # Convertimos el ID a mention de discord. Si no hay ID de Discord, mandamos el del bot
    discord_mention = f"<@{discord_id}>" if discord_id else "<@710993904886874153>"


    # Body de contenido del post
    thread_content = (
        f"**Link:** {job_link_markdown}\n"
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

    # Se manda el thread
    thread = await forum_channel.create_thread(
        name=f"{job_title} - {company}",
        content=thread_content,
        applied_tags=selected_tag_objects
    )

    # Mensaje de confirmacion
    ConfirmationChannel = int(os.getenv('JobsAdminChannel'))
    confirm_channel = bot.get_channel(ConfirmationChannel)

    if confirm_channel:
        await confirm_channel.send(f"Discord Jobs - 📢 Nuevo job posteado via Google Forms: {job_title} - {company}\n🔗 {job_link}")

    if sysarmy_channel:
        await sysarmy_channel.send(f"Pala Alert  ⛏️  {job_title} - {company}\n🔗 {job_link}")

    print(f"Discord Jobs - 📢 Nuevo job posteado via Google Forms: {job_title} - {company}")
