from sqlmodel import SQLModel


class Message(SQLModel, table=True):
    pass


class User(SQLModel, table=True):
    pass




