'''Script to download images from the Internet in async mode '''
import asyncio
import time
import os
import aiohttp
import requests


BASE_URL = 'https://aws.random.cat/meow'
DEST_DIR = 'downloads/'
COUNT = 10


def get_list(url: str, count: int):
    '''Get list with URL of images'''
    return [requests.get(url).json()['file'] for _ in range(count)]


def get_filename(url: str):
    '''Get filename from URL'''
    return os.path.basename(url)


async def get_cat(url: str):
    '''Get data of image from URL in async mode'''
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            image = await response.read()
    return image


def save_cat(image: bytes, filename: str):
    '''Save image in a local filesystem. If a folder does not exist - create it'''
    path = os.path.join(DEST_DIR, filename)
    if not os.path.exists(DEST_DIR):
        os.mkdir(DEST_DIR)
    with open(path, 'wb') as file:
        file.write(image)


async def download_one(url: str, filename: str):
    '''Download and save one image'''
    image = await get_cat(url)
    save_cat(image, filename)


def download(count: int):
    '''Create and run tasks to download images in async mode'''
    start_time = time.time()
    to_do = [download_one(url, get_filename(url)) for url in get_list(BASE_URL, count)]
    wait_coro = asyncio.wait(to_do)
    asyncio.run(wait_coro)
    print(f'{count} images were downloaded in {time.localtime(time.time() - start_time).tm_sec} seconds')


if __name__ == '__main__':
    download(COUNT)