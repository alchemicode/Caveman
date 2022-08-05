from peewee import *

db = SqliteDatabase('caveman.db')

class Server(Model):
    id = IntegerField()
    users = List[User]

class User(Model):
    id = IntegerField()
    warns = List[Warn]
    notes = List[Note]

class Warn(Model):
    reason = TextField()
    author = IntegerField()

class Note(Model):
    note = TextField()
    date = DateField()
    author = IntegerField()

    class Meta:
        database = db

db.connect()

