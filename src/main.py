import disnake
import yaml
from disnake.ext import commands

from .activity import activity

with open("conf.yml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as err:
        print(err)

intents = disnake.Intents.default()
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

    # Not sure why this isn't currently working
    print(f"Activity: {activity.emoji} {activity.name}")
    await bot.change_presence(activity=activity)
