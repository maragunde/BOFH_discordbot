import feedparser
import time
import threading
import asyncio
from datetime import datetime
import html
import re


##################################################################################################################
##############################################  SHITHAPPENS ######################################################
# Esta funcion envia updates tecnicos de plataformas, proveedores cloud, etc. a un canal de Discord
# Usamos los RSS feeds oficiales de cada proveedor, los feedeamos, parseamos, y enviamos al canal cuando hay
# alguna novedad que los usuarios necesiten saber: servicios caidos, problemas, y otros updates.
##################################################################################################################

# Listado de Feeds RSS. Nuevos se ponene aca directamente
RSS_FEEDS = {
    "https://discordstatus.com/history.rss": "Discord Status",
    "https://status.python.org/history.rss": "Python.org Update",
    "https://status.zoom.us/history.rss": "Zoom Status",
    "https://status.teamviewer.com/history.rss": "TeamViewer Status",
    "https://status.starter.openshift.com/history.atom": "OpenShift Status",
    "https://cloud.ibm.com/status/api/notifications/feed.rss": "IBM Cloud Status",
    "http://feeds.feedburner.com/OktaTrustRSS": "Okta Status",
    "https://status.slack.com/feed/rss": "Slack Status",
    "https://status.gandi.net/history.rss": "Gandi Status",
    "https://status.datadoghq.com/history.atom": "DataDog Status",
    "https://www.cloudflarestatus.com/history.atom": "Cloudflare Status",
    "https://azurestatuscdn.azureedge.net/es-mx/status/feed/": "Azure Status",
    "https://www.githubstatus.com/history.rss": "Github Status",
    "https://status.aws.amazon.com/rss/all.rss": "AWS Status",
    "https://status.linode.com/history.atom": "Linode Status",
    "https://status.digitalocean.com/history.atom": "Digital Ocean Status",
    "https://www.google.com/appsstatus/rss/es": "Google Status",
}

class RSSFeed:
    def __init__(self, channel, bot):
        self.channel = channel
        self.bot = bot
        self.last_posts = {url: None for url in RSS_FEEDS.keys()}  # Trackea el ultimo post para cada feed
        self.last_post_time = 0

    # Formateo del HTML
    def format_summary(self, html_content):
        text = html.unescape(html_content)
        clean_text = re.sub(r'<.*?>', '', text)
        return clean_text

    # FUNCION PRINCIPAL
    def fetch_and_send(self):
        while True:

            # Traemos los posts del listado de RSS
            for rss_url, source_title in RSS_FEEDS.items():
                feed = feedparser.parse(rss_url)
                if feed.entries:
                    latest_entry = feed.entries[0]

                    # Chequea si el ultimo post es nuevo
                    if self.last_posts[rss_url] is None or latest_entry.link != self.last_posts[rss_url]:
                        current_time = time.time()

                        # Chequeamos que pasen 10 segundos entre los posts, para evitar quilombos / flood
                        if current_time - self.last_post_time >= 10:
                            self.last_posts[rss_url] = latest_entry.link
                            title = latest_entry.title
                            published = getattr(latest_entry, 'published', 'No published date available')
                            summary = getattr(latest_entry, 'summary', None)

                            # Formatea el summary y le sacamos el HTML
                            if summary:
                                summary = self.format_summary(summary)

                            # Creamos el post
                            main_title = f"**{source_title} Update**"
                            message = f"**{main_title}**\n - {title}\nFecha: {published}\n"
                            if summary:
                                message += f"{summary}\n"
                            message += f"[Leer más]({latest_entry.link})"

                            # Manda la funcion de send al loop de eventos del bot
                            asyncio.run_coroutine_threadsafe(self.channel.send(message), self.bot.loop)

                            # Log
                            FechaActual = datetime.now()
                            print(FechaActual)
                            print(f"New RSS post sent to #shithappens from {rss_url}")

                            # Actualizamos la ultima fecha de posteo
                            self.last_post_time = current_time

            time.sleep(30)  # Chequea todo el feed cada 30 segundos

# Funcion principal para arrancar el RSS feed en un thread separado
def ShitHappens(channel, bot):
    rss_feed = RSSFeed(channel, bot)
    thread = threading.Thread(target=rss_feed.fetch_and_send, daemon=True)
    thread.start()