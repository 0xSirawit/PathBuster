import argparse
import requests
import asyncio
import time

WORDLIST = ['alumni','api','test','hello','book','info', 'login', 'panel', 'dashboard', 'monitor']
FILTER_STATUS_CODE =[404]

def brute(url):
    for word in WORDLIST:
        guess_url = f"{url}/{word}"
        response = requests.get(guess_url)
        if response.status_code not in FILTER_STATUS_CODE:
            print(response.status_code, guess_url)

if __name__ == '__main__':
    start_time = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help='Target URL for brute-force path discovery')
    args = parser.parse_args()
    url = args.url
    brute(url)

    end_time = time.time()
    print(start_time - end_time)
    