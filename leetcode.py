import json

from bs4 import BeautifulSoup
from aiohttp import ClientSession
import lxml
import asyncio
from requests import get

pages = 12
difficulties = ["EASY", "MEDIUM", "HARD"]
domain = "https://leetcode.com"


# def pagination():
#     global pages, difficulties
#     response = get(url=f"https://leetcode.com/problemset/all/?difficulty={difficulties[0]}&page=1").content
#     soup = BeautifulSoup(response, "lxml")
#     pages = soup.find("nav", role="navigation").find_all("button")
#
#     for i in pages:
#         print(i.text)


async def collect_data(url, number):
    data = []
    async with ClientSession() as session:
        async with session.get(url) as request:
            soup = BeautifulSoup(await request.text(), "lxml")
            problems = soup.find("div", role="rowgroup").find_all("div", role="row")
            for problem in problems:
                link = domain + problem.find("a").get("href")
                title = problem.find("a").text
                data.append({"title": title, "link": link})
            with open(f"data/data-{number}.json", "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            print(f"Page-{number} completed")

async def main():
    tasks=[]
    for i in range(1,pages+1):
        url = f"https://leetcode.com/problemset/all/?difficulty={difficulties[0]}&page={i}"
        task=asyncio.create_task(collect_data(url, i))
        tasks.append(task)
    await asyncio.gather(*tasks,return_exceptions=False)

if __name__ == '__main__':
    asyncio.run(main())
