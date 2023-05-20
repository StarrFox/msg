import tempfile
from pathlib import Path

import pypika

from views import Channel, User, Message

# for testing
tmpdir = Path(tempfile.gettempdir())


channels = pypika.Table("channels")
users = pypika.Table("users")
messages = pypika.Table("messages")


class ParamGen:
    def __init__(self, *, debug: bool = False):
        self.debug = debug

        self.counter = 0

    def next(self):
        # this makes it start at 1
        self.counter += 1
        return self.counter

    def __enter__(self):
        self.counter = 0

    def __exit__(self, *args):
        pass


class DbDriver:
    def __init__(self, *, debug: bool = False):
        self.debug = debug

    async def execute(self, sql: str, *params: list):
        print(f"execute: {sql}")

    async def create_channel(self, channel: Channel):
        sql = channels.insert(channel.id, channel.name)

        return await self.execute(sql)

    async def create_user(self, user: User):
        pass

    async def create_message(self, message: Message):
        pass


if __name__ == "__main__":
    # import asyncio

    # async def _main():
    #     driver = DbDriver(debug=True)

    #     await driver.create_channel(
    #         Channel(id=123, name="test_channel")
    #     )

    # asyncio.run(_main())

    par = ParamGen()

    with par:
        print(par.next())
        print(par.next())
        print(par.next())
        print(par.next())

