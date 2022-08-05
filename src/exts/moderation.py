import asyncio
from datetime import datetime
from typing import List

import disnake
from disnake.ext import commands

from ..db import Note
from ..main import bot


def parse_notes(notes: List[Note]) -> List[disnake.Embed]:
    embeds = []
    for i, note in enumerate(notes):
        embed = disnake.Embed(
            title=f"Note {i + 1}",
            colour=disnake.Colour.random(),
        )
        embed.add_field(
            name="Details",
            value=note.note,
            inline=True
        )
        embed.add_field(
            name="Added by",
            value=bot.get_user(note.author).mention,
            inline=True
        )
        embed.add_field(
            name="Time Added",
            value=datetime.now(),
            inline=False
        )
        embed.set_thumbnail(url=bot.get_user(note.user).display_avatar.url)
        embeds.append(embed)

    return embeds


class Notes(disnake.ui.View):
    def __init__(self, notes: List[disnake.Embed]):
        super().__init__(timeout=None)
        self.notes = notes
        self.notes_count = 0

        self.first_page.disabled = True
        self.prev_page.disabled = True

        for i, note in enumerate(self.notes):
            note.set_footer(text=f"Note {i + 1} of {len(self.notes)}")

    @disnake.ui.button(emoji="⏮️", style=disnake.ButtonStyle.blurple)
    async def first_page(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.notes_count = 0
        embed = self.notes[self.notes_count]
        embed.set_footer(text=f"Note 1 of {len(self.notes)}")

        self.first_page.disabled = True
        self.prev_page.disabled = True
        self.next_page.disabled = False
        self.last_page.disabled = False
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(emoji="◀", style=disnake.ButtonStyle.primary)
    async def prev_page(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.notes_count -= 1
        embed = self.notes[self.notes_count]

        self.next_page.disabled = False
        self.last_page.disabled = False
        if self.notes.count == 0:
            self.first_page.disabled = True
            self.prev_page.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(emoji="▶", style=disnake.ButtonStyle.primary)
    async def next_page(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.notes_count += 1
        embed = self.notes[self.notes_count]

        self.first_page.disabled = False
        self.prev_page.disabled = False
        if self.notes_count == len(self.notes) - 1:
            self.next_page.disabled = True
            self.last_page.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(emoji="⏭️", style=disnake.ButtonStyle.primary)
    async def last_page(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.notes_count = len(self.notes) - 1
        embed = self.notes[self.notes_count]

        self.first_page.disabled = False
        self.prev_page.disabled = False
        self.next_page.disabled = True
        self.last_page.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)


class Reason(disnake.ui.Modal):
    def __init__(self, type_) -> None:
        components = [
            disnake.ui.TextInput(
                label=f"Reason for the {type_}:",
                placeholder="Poured milk before cereal",
                custom_id="reason",
                style=disnake.TextInputStyle.long,
                max_length=512,
                required=False,
            ),
        ]
        super().__init__(title="Provide a Reason", custom_id="reason_modal", components=components)

    async def on_error(self, error: Exception, inter: disnake.ModalInteraction) -> None:
        await inter.response.send_message(f"Something went wrong: {error}", ephemeral=True)


class Actions(disnake.ui.View):
    def __init__(self, ctx, user):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.user = user

    @disnake.ui.button(label="🗒️ Notes", style=disnake.ButtonStyle.primary)
    async def note(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        notes = [
            Note(note="Killed my dog", date=datetime.now(), author=self.ctx.author.id, user=self.user.id),
            Note(note="Killed my cat", date=datetime.now(), author=self.ctx.author.id, user=self.user.id),
            Note(note="Killed my mom", date=datetime.now(), author=self.ctx.author.id, user=self.user.id),
            Note(note="Killed my dad", date=datetime.now(), author=self.ctx.author.id, user=self.user.id),
        ]

        embeds = parse_notes(notes)

        await interaction.response.send_message(embed=embeds[0], view=Notes(embeds), ephemeral=True)

    @disnake.ui.button(label="⚠️ Warn", style=disnake.ButtonStyle.primary)
    async def warn(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        ctx = self.ctx
        user = self.user

        await interaction.response.send_modal(modal=Reason("warn"))

        try:
            modal_inter: disnake.ModalInteraction = await bot.wait_for(
                "modal_submit",
                check=lambda i: i.custom_id == "reason_modal" and i.author.id == ctx.author.id,
                timeout=300,
            )
        except asyncio.TimeoutError:
            return

        embed = disnake.Embed(
            title="User Warned",
            description=f"User {user.name}#{user.discriminator} has been warned!\n\n",
            colour=disnake.Colour.gold(),
        )
        embed.set_thumbnail(url=user.display_avatar.url)

        for custom_id, value in modal_inter.text_values.items():
            embed.add_field(name=custom_id.capitalize(), value=(value or "No reason provided"), inline=False)

        await modal_inter.response.send_message(embed=embed)

    @disnake.ui.button(label="👞 Kick", style=disnake.ButtonStyle.primary)
    async def kick(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        ctx = self.ctx
        user = self.user

        await interaction.response.send_modal(modal=Reason("kick"))

        try:
            modal_inter: disnake.ModalInteraction = await bot.wait_for(
                "modal_submit",
                check=lambda i: i.custom_id == "reason_modal" and i.author.id == ctx.author.id,
                timeout=300,
            )
        except asyncio.TimeoutError:
            return

        embed = disnake.Embed(
            title="User Kicked",
            description=f"User {user.name}#{user.discriminator} has been kicked!\n\n",
            colour=disnake.Colour.red(),
        )
        embed.set_thumbnail(url=user.display_avatar.url)

        for custom_id, value in modal_inter.text_values.items():
            embed.add_field(name=custom_id.capitalize(), value=(value or "No reason provided"), inline=False)

        await modal_inter.response.send_message(embed=embed)

    @disnake.ui.button(label="🔨 Ban", style=disnake.ButtonStyle.primary)
    async def ban(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        ctx = self.ctx
        user = self.user

        await interaction.response.send_modal(modal=Reason("ban"))

        try:
            modal_inter: disnake.ModalInteraction = await bot.wait_for(
                "modal_submit",
                check=lambda i: i.custom_id == "reason_modal" and i.author.id == ctx.author.id,
                timeout=300,
            )
        except asyncio.TimeoutError:
            return

        embed = disnake.Embed(
            title="User Banned",
            description=f"User {user.name}#{user.discriminator} has been banned!\n\n",
            colour=disnake.Colour.dark_red(),
        )
        embed.set_thumbnail(url=user.display_avatar.url)

        for custom_id, value in modal_inter.text_values.items():
            embed.add_field(name=custom_id.capitalize(), value=(value or "No reason provided"), inline=False)

        await modal_inter.response.send_message(embed=embed)


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
        colour=user.accent_colour
    )
    embed.set_footer(text="Bought to you with hopes and dreams")
    embed.set_thumbnail(url=user.display_avatar.url)

    roles = []
    for role in user.roles:
        if role.name != "@everyone":
            roles.append(role.mention)

    roles.reverse()

    embed.add_field(name="User ID", value=user.id, inline=False)
    embed.add_field(name="Created At", value=user.created_at, inline=False)
    embed.add_field(name="Roles", value=' '.join(roles), inline=False)

    if ctx.author.guild_permissions.kick_members and ctx.author.guild_permissions.ban_members:
        view = Actions(ctx, user)
    else:
        view = disnake.ui.View()

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
