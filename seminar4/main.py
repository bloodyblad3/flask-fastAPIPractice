import os
import sys
import aiohttp
import asyncio
import aiofiles
import requests
import time
import threading
from multiprocessing import Process, Pool

def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            if not os.path.exists('images'):
                os.makedirs('images')
            image_name = url.split('/')[-1]
            path = 'images/' + image_name
            with open(path, 'wb') as f:
                f.write(response.content)
            print(f"{image_name} downloaded")
        else:
            print(f"download failed {url}")
    except Exception as e:
        print(f"something went wrong while download your image {url}: {e}")

async def download_image_async(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    if not os.path.exists('images'):
                        os.makedirs('images')
                    image_name = url.split('/')[-1]
                    path = 'images/' + image_name
                    async with aiofiles.open(path, 'wb') as f:
                        content = await response.read()
                        await f.write(content)
                    print(f"{image_name} downloaded")
                else:
                    print(f"download failed {url}")
    except Exception as e:
        print(f"something went wrong while download your image {url}: {e}")

def download_images_threaded(urls):
    start_time = time.time()
    threads = []

    for url in urls:
        thread = threading.Thread(target=download_image, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"execution time: {end_time - start_time:.2f}s")

def download_images_multiprocess(urls):
    start_time = time.time()
    processes = []

    for url in urls:
        process = Process(target=download_image, args=(url,))
        processes.append(process)
        process.start()
    
    for process in processes:
        process.join()
    
    end_time = time.time()
    print(f"execution time: {end_time - start_time:.2f}s")

async def download_images_async(urls):
    start_time = time.time()
    tasks = []

    for url in urls:
        task = asyncio.ensure_future(download_image_async(url))
        tasks.append(task)
    await asyncio.gather(*tasks)
    
    end_time = time.time()
    print(f"execution time: {end_time - start_time:.2f}s")

def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: python main.py <method> [<file_with_urls.txt> | <url1> <url2> ...]")
        sys.exit(1)
    
    method = sys.argv[1]

    if sys.argv[2].endswith('.txt'):
        urls = read_urls_from_file(sys.argv[2])
    else:
        urls = sys.argv[2:]

    if method == "threaded":
        print("running script with threaded method")
        download_images_threaded(urls)
    elif method == "multiprocess":
        print("running script with multiprocess method")
        download_images_multiprocess(urls)
    elif method == "async":
        print("running script with async method")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(download_images_async(urls))
    else:
        print("invalid method, try (threaded, multiprocess or async)")