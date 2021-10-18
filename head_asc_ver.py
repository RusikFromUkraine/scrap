from bs4 import BeautifulSoup
from datetime import datetime
from fake_useragent import UserAgent
import requests
import json
import os
import time
import asyncio
import aiohttp


ua = UserAgent()

if not os.path.exists("blank"):
    os.mkdir("blank")

headers = {
    'Accept': 'text/html, */*; q=0.01',
    'User-Agent': ua.firefox
}

main_url = r'https://www.work.ua/jobs-it-python/'


async def get_job_url():
    pass


async def search_job():
    pass


async def get_information():
    pass


def main():
    pass


if __name__ == '__main__':
    main()
