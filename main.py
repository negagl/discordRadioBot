from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
RADIO_TIEMPO = os.getenv("RADIO_TIEMPO")

print(f"Token: {TOKEN}")
print(f"Radio Tiempo: {RADIO_TIEMPO}")

bot = commands.Bot(command_prefix='*', intents=discord.Intents.all())

@bot.event
async def on_ready():
  print(f'Bot conectado como {bot.user}!')
  
@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        vc = await channel.connect()
        await ctx.send(f"Conectado al canal: {channel.name}")

        # Iniciar reproducción de la emisora
        vc.play(discord.FFmpegPCMAudio(RADIO_TIEMPO), after=lambda e: print(f"Error: {e}") if e else None)
        await ctx.send("Reproduciendo la emisora...")
    else:
        await ctx.send("Debes estar en un canal de voz para usar este comando.")

# Comando para salir del canal de voz
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Desconectado del canal de voz.")
    else:
        await ctx.send("No estoy en un canal de voz.")
        
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_http_server():
    server = HTTPServer(("0.0.0.0", 8080), HealthCheckHandler)
    server.serve_forever()

# Ejecutar el servidor HTTP en un hilo separado
threading.Thread(target=run_http_server, daemon=True).start()

# Ejecutar el bot
bot.run(TOKEN)