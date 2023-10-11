import pwd
import os
import asyncio

import asyncpg

from msg.security import HashedUsername, HashedPassword


def get_current_username() -> str:
    return pwd.getpwuid(os.getuid()).pw_name


# TODO: add enviorment variables for these
DATABASE_user = get_current_username()
DATABASE_name = "msg"


DBSCHEMA = """
CREATE TABLE IF NOT EXISTS logins (
    user_id BIGINT NOT NULL,
    hashed_username TEXT NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL,
    PRIMARY KEY (user_id)
);
""".strip()


class MsgDBError(Exception): ...
class MissingUsername(MsgDBError): ...
class IncorrectPassword(MsgDBError): ...
class UsernameInUse(MsgDBError): ...


class Database:
    def __init__(self):
        self._connection: asyncpg.Pool | None = None
        self._ensured: bool = False
        self._connection_lock = asyncio.Lock()

    async def _ensure_tables(self, pool: asyncpg.Pool):
        # A lock isnt needed here because .connect is already locked
        if self._ensured:
            return

        self._ensured = True

        async with pool.acquire() as connection:
            await connection.execute(DBSCHEMA)

    async def connect(self) -> asyncpg.Pool:
        async with self._connection_lock:
            if self._connection is not None:
                return self._connection

            self._connection = await asyncpg.create_pool(
                user=DATABASE_user, database=DATABASE_name
            )
            assert self._connection is not None
            await self._ensure_tables(self._connection)
            return self._connection

    async def create_user(self, user_id: int, hashed_username: HashedUsername, hashed_password: HashedPassword):
        pool = await self.connect()

        async with pool.acquire() as connection:
            connection: asyncpg.Connection

            try:
                await connection.execute(
                    "INSERT INTO logins (user_id, hashed_username, hashed_password) VALUES ($1, $2, $3);",
                    user_id,
                    hashed_username.get_hashed(),
                    hashed_password.get_hashed(),
                )
            except asyncpg.UniqueViolationError:
                raise UsernameInUse("Username already in use")

    async def check_login(self, hashed_username: HashedUsername, test_hashed_password: HashedPassword) -> int:
        pool = await self.connect()

        async with pool.acquire() as connection:
            connection: asyncpg.Connection
            row: asyncpg.Record = await connection.fetchrow(
                "SELECT user_id, hashed_password FROM logins WHERE hashed_username = $1;",
                hashed_username.get_hashed(),
            )

            if row is None:
                raise MissingUsername("Username not in database")

            if row["hashed_password"] == test_hashed_password.get_hashed():
                return row["user_id"]

            raise IncorrectPassword("Password hashes did not match")














