import json
import logging
from fake_useragent import UserAgent
from datas import headers
from datetime import datetime
import asyncio
import aiohttp

remaining_count = 0
all_data = []


async def collect_data(number):
    global remaining_count, all_data
    url = f"https://www.udemy.com/api-2.0/discovery-units/all_courses/?p={number}&page_size=60&subcategory=&instructional_level=&lang=&price=&duration=&closed_captions=&subs_filter_type=&subcategory_id=12&source_page=subcategory_page&locale=en_US&currency=usd&navigation_locale=en_US&skip_price=true&sos=ps&fl=scat"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            items = data["unit"]["items"]
            remaining_count = data["unit"]["remaining_item_count"]
            for item in items:
                data_json = {}
                title = item["title"]
                url = "https://www.udemy.com" + item["url"]
                headline = item["headline"]
                data_json["title"] = title
                data_json["url"] = url
                data_json["headline"] = headline
                all_data.append(data_json)
            logging.log(msg=f"Page-{number} is completed")


async def main():
    before = datetime.now()
    tasks = []
    for i in range(1, 101):
        task = collect_data(number=i)
        tasks.append(task)

        i = i + 1
    L = await asyncio.gather(*tasks)

    after = datetime.now()
    print(after - before)


if __name__ == '__main__':
    asyncio.run(main())
    with open("data/data.json","w",encoding="utf-8") as file:
        json.dump(all_data,file,ensure_ascii=False,indent=4)