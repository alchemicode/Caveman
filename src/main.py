import disnake
from disnake.ext import commands

description = """Caveman go brrrr"""

intents = disnake.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(
    description=description, intents=intents
)

bot.load_extension('src.exts.moderation')

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}, ID: {bot.user.id}")

