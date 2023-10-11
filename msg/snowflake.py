import asyncio

import pendulum
from dataclasses import dataclass


# this is the first second of 2023
MSG_EPOCH: int = 1672531200 * 1000


@dataclass
class SnowFlake:
    value: int

    @property
    def timestamp(self) -> int:
        return (self.value >> 22) + MSG_EPOCH

    @property
    def machine_id(self) -> int:
        return (self.value >> 12) & 0b1111111111
    
    @property
    def counter(self) -> int:
        return self.value & 0b111111111111

    @property
    def when(self) -> pendulum.DateTime: # type: ignore
        # note: this does utc by default
        return pendulum.from_timestamp(self.timestamp)


class SnowFlakeGenerator:
    def __init__(self, *, machine_id: int):
        """Snowflake generator

        Args:
            machine_id (int): Id of the machine generator is running on
        """
        if machine_id > 0b1111111111:
            raise ValueError(f"{machine_id} is over max machine id of {0b1111111111}")

        self.counter: int = 0
        self.machine_id: int = machine_id

        self._rollover_timestamp: int = 0

        self.lock = asyncio.Lock()

    async def next(self) -> SnowFlake:
        """Get the next snowflake
        
        Returns:
            SnowFlake: The next snowflake
        """
        async with self.lock:
            # note: do not replace this with datetime.utcnow(), it's garbage
            #  // for some reason it uses local time???
            timestamp = int(pendulum.now("UTC").timestamp() * 1000) - MSG_EPOCH

            if self.counter == 0:
                while timestamp == self._rollover_timestamp:
                    timestamp = int(pendulum.now("UTC").timestamp() * 1000) - MSG_EPOCH

            snowflake_value = timestamp << 22

            snowflake_value |= self.machine_id << 12
            snowflake_value |= self.counter & 0b111111111111

            # python ints are unsized, this makes it be u64 sized
            snowflake_value &= 0xFFFF_FFFF_FFFF_FFFF

            self.counter += 1

            # TODO: make sure the last timestamp and the next don't collide
            if self.counter >= 0b111111111111:
                self._rollover_timestamp = timestamp
                self.counter = 0

            return SnowFlake(snowflake_value)
