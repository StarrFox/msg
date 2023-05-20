from pydantic import BaseModel

from msg import SnowFlake


class SnowFlakeCarrier(BaseModel):
    id: int

    @property
    def snowflake(self):
        return SnowFlake(self.id)


class Channel(SnowFlakeCarrier):
    name: str


class User(SnowFlakeCarrier):
    username: str


class Message(SnowFlakeCarrier):
    content: str
    channel: Channel

