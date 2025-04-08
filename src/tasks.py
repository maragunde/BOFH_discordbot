import discord
import json
import os

from datetime import datetime
from discord.ext import tasks
from src.discordjobs.postjob_bulk_convert import process_all_new_excels
from src.discordjobs.postjob_gform_convert import checkforjobs
from src.discordjobs.postjob_gform import gformjobpost
from src.discordjobs.shortlink import create_shortlink


# Este archivo contiene las tareas programadas para el bot de Discord.
# discord.ext.tasks es una extensión de discord.py que permite crear tareas programadas.
# Se utiliza para ejecutar funciones de forma periódica, como la publicación de trabajos.


@tasks.loop(minutes=10)
async def scheduled_job_posting(bot):
    """
    Esta función se encarga de ejecutar la tarea programada de publicación de trabajos.
    Se ejecuta cada 30 minutos y verifica si hay nuevos trabajos para publicar.
    Si hay nuevos trabajos, los publica en el canal correspondiente.

    Args:
        bot (commands.Bot): La instancia del bot de Discord.
    """
    try:
        new_jobs = await checkforjobs(verbose=False)
        if new_jobs:
            print(f"[Scheduled] {datetime.now()} - Nuevos trabajos encontrados en el Google Form")
            jobs_posted = 0
            for job_data in new_jobs:
                try:
                    await gformjobpost(bot, job_data)
                    jobs_posted += 1
                except Exception as e:
                    print(f"Discord Jobs (Gform) - ❌ Error posteando job: {e}")
            print(f"Discord Jobs (Gform) - ✅ Publique {jobs_posted} jobs automaticamente!")
    except Exception as e:
        print(f"Error ejecutando publicación de trabajos: {e}")


@tasks.loop(minutes=10)
async def scheduled_bulk_job_posting(bot):
    """
    Esta función se encarga de ejecutar la tarea programada de publicación de trabajos en bulk.
    Se ejecuta cada 30 minutos, procesa archivos Excel nuevos y publica los trabajos encontrados.

    Args:
        bot (commands.Bot): La instancia del bot de Discord.
    """

    if not process_all_new_excels(verbose=False):
        return

    job_file = "src/discordjobs/bulk/job.json"
    if not os.path.exists(job_file):
        print("Discord Jobs (Bulk Auto) - ❌ No encontré archivo JSON. Revisa que onda")
        return

    try:
        with open(job_file, "r", encoding="utf-8") as file:
            job_list = json.load(file)

        if not job_list:
            return

        print(f"[Scheduled] {datetime.now()} - Nuevos trabajos encontrados en formato Excel")

        JobsChannel = int(os.getenv("JobsChannel"))
        guild_id = int(os.getenv("guild_id"))
        guild = bot.get_guild(guild_id)

        if not guild:
            print(f"Discord Jobs (Bulk Auto) - ❌ No pude encontrar el servidor con ID {guild_id}")
            return

        forum_channel = discord.utils.get(guild.channels, id=JobsChannel)

        if not forum_channel:
            print(f"Discord Jobs (Bulk Auto) - ❌ No pude encontrar el canal de jobs con ID {JobsChannel}")
            return

        posted_count = 0
        for job_data in job_list:

            if not job_data.get("job_title") or not job_data.get("company"):  # Skipeamos jobs que no tengan por lo menos un job title y la empresa
                continue

            job_title = job_data.get("job_title", "Sin título")
            job_link = create_shortlink(job_data.get("job_link")) if job_data.get("job_link") else ""
            salary_range = job_data.get("salary_range", "No especificado")
            company = job_data.get("company", "No especificado")
            job_description = job_data.get("job_description", "Sin descripción")
            discord_id = job_data.get("discord_id", "1235914603435790377")
            tags = [tag.strip() for tag in job_data.get("tags", "").split(",") if tag.strip()]
            job_scheme = job_data.get("job_scheme", "No especificado")
            location = job_data.get("location", "No especificada")
            experiencia = job_data.get("experiencia", "No especificada")
            ingles = job_data.get('ingles')
            print(f"Discord Jobs (Bulk Auto) - Procesando job: {job_title} - {company}")

            selected_tag_objects = [tag for tag in forum_channel.available_tags if tag.name.lower() in [t.lower() for t in tags]]

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
                thread = await forum_channel.create_thread(name=f"{job_title} - {company}", content=thread_content, applied_tags=selected_tag_objects)
                posted_count += 1
                print(f"Discord Jobs (Bulk Auto) - 📢 Nuevo job posteado: {job_title} - {company}")
            except Exception as e:
                print(f"Discord Jobs (Bulk Auto) - ⚠️ Error posteando job {job_title}: {e}")

        print(f"Discord Jobs (Bulk Auto) - ✅ Se han posteado {posted_count} jobs automáticamente.")

        # Limpiamos el JSON para poder procesar un nuevo batch
        with open(job_file, "w", encoding="utf-8") as file:
            json.dump([], file)

    except Exception as e:
        print(f"Discord Jobs (Bulk Auto) - ❌ Error general en bulk job posting: {e}")
