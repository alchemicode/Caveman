#!/usr/bin/env python3

import os

from log import log

import disnake
from disnake.ext import commands

description = """Caveman go brrrr"""
token = os.getenv('CAVEMAN_TOKEN')

intents = disnake.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("_"), description=description, intents=intents
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}, ID: {bot.user.id}")


@bot.slash_command(
    name="ping",
    description="A simple Ping command",
)
async def ping(ctx):
    await ctx.response.send_message(
        "Pong!", ephemeral=True
    )

if __name__ == '__main__':
    log()
    bot.run(token)
