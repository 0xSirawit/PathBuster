import argparse
import aiohttp
import asyncio
import time
import sys
from threading import Thread

FILTER_STATUS_CODE = {404}


class bcolors:
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    ENDC = "\033[0m"


async def fetch(session, guess_url: str) -> None:
    global error, req
    try:
        async with session.get(guess_url) as response:
            if response.status not in FILTER_STATUS_CODE:
                status_color = (
                    bcolors.OKGREEN if response.status == 200 else bcolors.WARNING
                )
                print(
                    f"{status_color}{response.status}{bcolors.ENDC} {guess_url} {response.content_length}"
                )
    except:
        error += 1
    finally:
        req += 1


async def brute(url: str, wordlist: list, batch_size: int) -> None:
    if not batch_size:
        batch_size = 100
    async with aiohttp.ClientSession() as session:
        for i in range(0, len(wordlist), batch_size):
            batch = wordlist[i : i + batch_size]
            tasks = [fetch(session, f"{url}/{word}") for word in batch if word]
            await asyncio.gather(*tasks)


def read_wordlist(filename: str) -> list:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            wordlist = f.read().splitlines()
    except FileNotFoundError:
        print("Error: Wordlist file not found!")
        exit(1)
    return wordlist


def monitor():
    global req, running
    while running:
        time.sleep(1)
        sys.stdout.write(f"{req} reqs/sec\r")
        sys.stdout.flush()
        req = 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="Target URL for brute-force path discovery")
    parser.add_argument("--wordlist", help="wordlist")
    parser.add_argument(
        "--batch-size", help="Batch size for concurrent requests", type=int
    )
    args = parser.parse_args()
    url = args.url.rstrip("/")
    error = 0
    req = 0
    running = True

    try:
        start_time = time.time()
        monitor_thread = Thread(target=monitor, daemon=True)
        monitor_thread.start()
        asyncio.run(brute(url, read_wordlist(args.wordlist), args.batch_size))
    except KeyboardInterrupt:
        running = False
    finally:
        end_time = time.time()
        monitor_thread.join()
        print(f"Total errors: {error}")
        print(f"Execution time: {end_time - start_time:.2f} seconds")
