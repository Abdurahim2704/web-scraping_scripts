from bs4 import BeautifulSoup
import lxml
from aiohttp import ClientSession
import json
from requests import get
import asyncio
from datetime import datetime

pages = 0
all_data=[]

def pagination():
    global pages
    url = "http://uzmovi.com/tarjima-kino/page/1"
    response = get(url)
    soup_1 = BeautifulSoup(response.content, "lxml")
    pages = int(soup_1.find("div", class_="pages-numbers").find_all("a")[-1].text)


async def collect_data(url,number):
    global all_data
    data = []
    async with ClientSession() as session:
        async with session.get(url) as response:
            soup = BeautifulSoup(await response.text(), "lxml")
            items = soup.find("div", class_="row").find_all("h4")
            for item in items:
                item = item.find("a")
                link = item.get("href")
                title = item.get("title")
                data.append({"title": title, "link": link})
            all_data += data
            print(f"page-{number} completed")
            if number % 5 == 0:
                with open(f"data-{number/5}.json", "w", encoding="utf-8") as file:
                    json.dump(all_data, file, indent=4, ensure_ascii=False)
                all_data = []


async def main():
    tasks = []
    pagination()
    for i in range(1, pages + 2):
        url = f"http://uzmovi.com/tarjima-kino/page/{i}"
        task=asyncio.create_task(collect_data(url=url,number=i))
        tasks.append(task)
    await asyncio.gather(*tasks,return_exceptions=False)


if __name__ == '__main__':
    before = datetime.now()
    asyncio.run(main())
    after = datetime.now()
    print(after - before)
