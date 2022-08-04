import disnake
from disnake.ext import commands


class Actions(disnake.ui.View):
    def __init__(self, user: disnake.User):
        super().__init__(timeout=None)
        self.user = user

    @disnake.ui.button(label="🗒️ Note", style=disnake.ButtonStyle.primary)
    async def note(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        user = self.user
        embed = disnake.Embed(
            title="Note Added",
            description=f"Note added for user {user.name}#{user.discriminator}!",
            colour=disnake.Colour.teal(),
        )
        embed.set_thumbnail(url=user.display_avatar.url)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @disnake.ui.button(label="⚠️ Warn", style=disnake.ButtonStyle.primary)
    async def warn(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        user = self.user
        embed = disnake.Embed(
            title="User Warned",
            description=f"User {user.name}#{user.discriminator} has been warned!",
            colour=disnake.Colour.gold(),
        )
        embed.set_thumbnail(url=user.display_avatar.url)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @disnake.ui.button(label="👞 Kick", style=disnake.ButtonStyle.primary)
    async def kick(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        user = self.user
        embed = disnake.Embed(
            title="User Kicked",
            description=f"User {user.name}#{user.discriminator} has been kicked!",
            colour=disnake.Colour.red(),
        )
        embed.set_thumbnail(url=user.display_avatar.url)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @disnake.ui.button(label="🔨 Ban", style=disnake.ButtonStyle.primary)
    async def ban(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        user = self.user
        embed = disnake.Embed(
            title="User Banned",
            description=f"User {user.name}#{user.discriminator} has been banned!",
            colour=disnake.Colour.dark_red(),
        )
        embed.set_thumbnail(url=user.display_avatar.url)

        await interaction.response.send_message(embed=embed, ephemeral=True)


@commands.user_command(name="Info")
async def info_context(
        ctx,
        user: disnake.User
):
    await info(ctx, user)


@commands.slash_command(
    name="info",
    description="Get simple user info",
)
async def info(
    ctx,
    user: disnake.User
):
    embed = disnake.Embed(
        title=f"**{user.name}#{user.discriminator}**",
        description=f"""
                    **User ID:**
                    {user.id}
                    
                    **Created at:**
                    {user.created_at}
                    
                    **Public Flags:**
                    {user.public_flags.all()}
                    """,
        colour=user.accent_colour
    )
    embed.set_footer(text="Bought to you with hopes and dreams")
    embed.set_thumbnail(url=user.display_avatar.url)

    view = Actions(user)

    await ctx.response.send_message(
        embed=embed,
        view=view,
        ephemeral=True,
    )

    await view.wait()


def setup(bot):
    print('Loading Moderation Ext.')
    bot.add_user_command(info_context)
    bot.add_slash_command(info)
    print('Moderation Ext. Loaded')
