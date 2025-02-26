import argparse
import aiohttp
import asyncio
import time

FILTER_STATUS_CODE = {404}


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


async def fetch(session, guess_url: str) -> None:
    global error
    try:
        async with session.get(guess_url) as response:
            if response.status not in FILTER_STATUS_CODE:
                if response.status == 200:
                    print(
                        f"{bcolors.OKGREEN}{response.status}{bcolors.ENDC} {guess_url} {response.content_length}"
                    )
                elif response.status == 403:
                    print(
                        f"{bcolors.WARNING}{response.status}{bcolors.ENDC} {guess_url} {response.content_length}"
                    )
                else:
                    print(f"{response.status} {guess_url} {response.content_length}")
    except:
        error += 1


async def brute(url: str, wordlist: list, batch_size: int = 100) -> None:
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

    try:
        start_time = time.time()
        asyncio.run(brute(url, read_wordlist(args.wordlist), args.batch_size))
    except KeyboardInterrupt:
        pass
    finally:
        end_time = time.time()
        print(f"Total errors: {error}")
        print(f"Execution time: {end_time - start_time:.2f} seconds")
