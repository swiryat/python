import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs
import pandas as pd
import os

URL_TEMPLATE = "https://hh.ru/search/vacancy?area=1&page={}"
FILE_NAME = "C:/Users/swer/Documents/hh_vacancies.csv"

async def fetch(url, session):
    async with session.get(url) as response:
        return await response.text()

async def parse(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch(url, session)
        soup = bs(html, "html.parser")
        vacancies_names = soup.find_all('div', class_='vacancy-serp-item__info')
        vacancies_info = soup.find_all('div', class_='vacancy-serp-item__meta-info')
        result_list = {'title': [], 'about': []}
        for name in vacancies_names:
            result_list['title'].append(name.a.text)
        for info in vacancies_info:
            result_list['about'].append(info.text)
        return result_list

async def main():
    tasks = []
    for page in range(1, 11):
        url = URL_TEMPLATE.format(page)
        tasks.append(parse(url))

    results = await asyncio.gather(*tasks)

    valid_results = [result for result in results if len(result['title']) == len(result['about'])]
    dfs = [pd.DataFrame(result) for result in valid_results]
    
    df = pd.concat(dfs, ignore_index=True)
    
    directory = os.path.dirname(FILE_NAME)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(FILE_NAME, 'w') as f:
        df.to_csv(f, index=False)

if __name__ == "__main__":
    asyncio.run(main())
