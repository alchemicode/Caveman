import os
import pickle
import random
from datetime import datetime
from typing import List

import disnake

from src.main import bot


class Warn:
    id = int
    reason = str
    author = int
    user = int
    date = datetime

    def __init__(self, reason, author, user, date=datetime.now(), id=random.getrandbits(63)):
        self.id = id
        self.reason = reason
        self.author = author
        self.user = user
        self.date = date


class Note:
    id = int
    content = str
    author = int
    user = int
    date = datetime

    def __init__(self, content, author, user, date=datetime.now(), id=random.getrandbits(63)):
        self.id = id
        self.content = content
        self.author = author
        self.user = user
        self.date = date

    def parse(self):
        embed = disnake.Embed(
            title="Note",
            colour=disnake.Colour.blurple(),
        )
        embed.add_field(
            name="Content",
            value=self.content,
            inline=True,
        )
        embed.add_field(
            name="Author",
            value=(bot.get_user(self.author).mention if bot.get_user(self.author) else "Unknown"),
            inline=True,
        )
        embed.add_field(
            name="Date",
            value=self.date.strftime("%d %b %Y %H:%M:%S"),
            inline=False,
        )
        embed.add_field(
            name="ID",
            value=str(self.id),
            inline=True,
        )
        embed.set_thumbnail((bot.get_user(self.user).display_avatar.url if bot.get_user(
            self.user) else "https://cdn.discordapp.com/embed/avatars/0.png"))
        return embed


class User:
    id = int
    warns = List[Warn]
    notes = List[Note]

    def __init__(self, id, warns=None, notes=None):
        if notes is None:
            notes = []
        if warns is None:
            warns = []
        self.id = id
        self.warns = warns
        self.notes = notes

    def add_warn(self, warn):
        self.warns.append(warn)

    def add_note(self, note):
        self.notes.append(note)


class ServerOptions:
    mod_role = int

    def __init__(self, mod_role=None):
        self.mod_role = mod_role


class Server:
    id = int
    options = ServerOptions
    users = List[User]

    def __init__(self, id, options=ServerOptions(), users=None):
        if users is None:
            users = []
        self.id = id
        self.options = options
        self.users = users

    def get_user(self, user_id: int) -> User | None:
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    def add_user(self, user: User):
        self.users.append(user)

    def initialise(self):
        if not os.path.exists(f'data/{self.id}.pickle'):
            with open(f'data/{self.id}.pickle', 'wb') as f:
                pickle.dump(self, f)

    def save(self):
        with open(f'data/{self.id}.pickle', 'wb') as f:
            pickle.dump(self, f)


def server(id: int):
    if not os.path.exists(f'data/{id}.pickle'):
        server_ = Server(id)
        server_.initialise()

    with open(f'data/{id}.pickle', 'rb') as f:
        return pickle.load(f)
