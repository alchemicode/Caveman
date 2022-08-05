import disnake
import yaml
from disnake.ext import commands

with open("conf.yml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as err:
        print(err)

description = """Caveman go brrrr"""
intents = disnake.Intents.default()

bot = commands.Bot(
    description=description, intents=intents
)

bot.load_extension('src.exts.moderation')


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}, ID: {bot.user.id}")
