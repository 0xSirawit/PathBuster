import argparse
import aiohttp
import asyncio
import time

FILTER_STATUS_CODE = {404}
RESULT = []


async def fetch(session, guess_url):
    global error
    try:
        async with session.get(guess_url) as response:
            if response.status not in FILTER_STATUS_CODE:
                print((guess_url, response.status))
                RESULT.append((guess_url, response.status))
    except:
        error += 1


async def brute(url, wordlist):
    async with aiohttp.ClientSession() as session:
        for word in wordlist:
            guess_url = f"{url}/{word}"
            task = asyncio.create_task(fetch(session, guess_url))
            await task


def read_wordlist(filename):
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
    args = parser.parse_args()
    url = args.url
    error = 0

    start_time = time.time()
    if url.endswith("/"):
        url = url[:-1]
    asyncio.run(brute(url, read_wordlist(args.wordlist)))
    end_time = time.time()

    print(error, "errors")
    print(end_time - start_time)
