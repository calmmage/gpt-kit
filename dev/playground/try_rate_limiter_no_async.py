import time

from aiolimiter import AsyncLimiter

limiter = AsyncLimiter(3, 1)

i = 0
ts = time.time()


def main():
    global i
    async with limiter:
        print(f"{i}! Passed = {time.time() - ts}")
        i += 1
        # await asyncio.sleep(1)


if __name__ == "__main__":
    print("Starting tasks")
    for _ in range(100):
        main()
    print("Finished all tasks")
