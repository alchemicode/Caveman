#!/usr/bin/env python3

import yaml

from log import log

import disnake
from disnake.ext import commands

with open("conf.yml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as err:
        print(err)

description = """Caveman go brrrr"""
token = config['token']

intents = disnake.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(
    description=description, intents=intents
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}, ID: {bot.user.id}")


class Confirm(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @disnake.ui.button(label="Press me!", style=disnake.ButtonStyle.green)
    async def confirm(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        embed = disnake.Embed(description="Confirmed!")
        embed.set_footer(text="Bought to you with hopes and dreams")

        await interaction.response.send_message(embed=embed, ephemeral=True)
        self.value = True
        self.stop()


@bot.slash_command(
    name="ping",
    description="A simple Ping command",
)
async def ping(ctx):
    embed = disnake.Embed(description="Pong!")
    embed.set_footer(text="Bought to you with hopes and dreams")

    view = Confirm()

    await ctx.response.send_message(
        embed=embed,
        view=view,
        ephemeral=True,
    )

    await view.wait()
    if view.value is None:
        print("Timed out")
    elif view.value:
        print("Confirmed")
    else:
        print("Cancelled")


if __name__ == '__main__':
    log()
    bot.run(token)
