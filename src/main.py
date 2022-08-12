import disnake
import yaml
from disnake.ext import commands

with open("conf.yml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as err:
        print(err)

intents = disnake.Intents().default()
# noinspection PyDunderSlots,PyUnresolvedReferences
intents.members = True

bot = commands.InteractionBot(
    status=disnake.Status.online,
    intents=intents,
)

bot.load_extension('src.exts.moderation')
bot.load_extension('src.exts.admin')


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}, ID: {bot.user.id}")
    print(f"Connected to {len(bot.guilds)} guilds, serving {len(bot.users)} users")
