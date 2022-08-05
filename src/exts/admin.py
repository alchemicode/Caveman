import disnake.ext.commands
from disnake.ext import commands


@disnake.ext.commands.is_owner()
@commands.slash_command(
    name="botinfo",
    description="Get info about the bot",
)
async def bot_info(ctx):
    embed = disnake.Embed(
        title="Bot Info",
        colour=disnake.Colour.blurple(),
    )

    embed.add_field(name="Name", value=ctx.bot.user, inline=True)
    embed.add_field(name="ID", value=ctx.bot.user.id, inline=True)
    embed.add_field(name="Created At", value=ctx.bot.user.created_at, inline=False)
    embed.add_field(name="Guilds", value=len(ctx.bot.guilds), inline=True)
    embed.add_field(name="Users", value=len(ctx.bot.users), inline=True)

    embed.set_thumbnail(url=ctx.bot.user.display_avatar.url)

    await ctx.response.send_message(embed=embed, ephemeral=True)


def setup(bot):
    print('Loading Admin Ext.')
    bot.add_slash_command(bot_info)
    print('Admin Ext. Loaded')
