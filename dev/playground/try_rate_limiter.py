import asyncio
import time

from aiolimiter import AsyncLimiter

limiter = AsyncLimiter(3, 1)

i = 0
ts = time.time()


async def main():
    global i
    async with limiter:
        print(f"{i}! Passed = {time.time() - ts}")
        i += 1
        # await asyncio.sleep(1)


async def runner():
    await asyncio.gather(*(main() for _ in range(100)))


if __name__ == "__main__":
    print("Starting tasks")
    asyncio.run(runner())
    print("Finished all tasks")
