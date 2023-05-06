import pytest
import pendulum

from msg import SnowFlakeGenerator


def default_generator() -> SnowFlakeGenerator:
    return SnowFlakeGenerator(machine_id=1)


@pytest.mark.asyncio
async def test_basic():
    gen = default_generator()

    now = int(pendulum.now("UTC").timestamp() * 1000)

    flake = await gen.next()

    assert(flake.counter == 0)
    assert(flake.machine_id == 1)
    assert((flake.timestamp - now) < 100)


@pytest.mark.asyncio
async def test_counter_roll_over():
    gen = default_generator()

    for _ in range(0b111111111111):
        await gen.next()

    assert(gen.counter == 0)

    for _ in range(0b111111111111):
        last = await gen.next()

    rollover = await gen.next()

    assert(last.timestamp != rollover.timestamp)
