# PathBuster: Asyncio-based Brute-force Path Discovery
<small>240-123 Module Data Structure, Algorithms and Programming</small>

## Overview
This script performs brute-force path discovery on a target URL using `asyncio` and `aiohttp` for concurrent HTTP requests and it uses a separate monitoring thread to display request rates in real time.

## Features
- Using `asyncio` and `aiohttp` for asynchronous HTTP requests
- Using threading for request rate monitoring 
- Supports custom wordlists
- Batch sizes

## Requirements
dependencies:

```bash
pip install aiohttp
```

## Usage
Run the script with the following arguments:

```bash
python pathbuster.py --url <TARGET_URL> --wordlist <WORDLIST_FILE> --batch-size <BATCH_SIZE>
```

- `--url`: The target URL for brute-force path discovery
- `--wordlist`: Path to the wordlist file
- `--batch-size`:  Number of concurrent requests to send per batch (default: 100)

### Example Usage
```bash
python pathbuster.py --url https://example.com --wordlist common.txt --batch-size 50
```

## How It Works
1. Reads the wordlist and creates potential paths.
2. Uses `asyncio` and `aiohttp` to send HTTP requests.
3. Filters out responses with status code `404`.
4. A separate thread monitors and displays request rates.
5. Handles errors gracefully and reports execution time at the end.

## Output Example
```
200 https://example.com/admin 3456
301 https://example.com/login 1234
...
Total errors: 2
Execution time: 5.23 seconds
