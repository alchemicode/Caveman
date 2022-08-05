from typing import List

from peewee import *


class Note(Model):
    note = TextField()
    date = DateField()
    author = IntegerField()
    user = IntegerField()


class Warn(Model):
    reason = TextField()
    author = IntegerField()
    user = IntegerField()


class User(Model):
    id = IntegerField()
    warns = List[Warn]
    notes = List[Note]


class Server(Model):
    id = IntegerField()
    mod_role = IntegerField()
    users = List[User]

    class Meta:
        database = SqliteDatabase('caveman.db')
