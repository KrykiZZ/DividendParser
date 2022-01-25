import aiohttp
from bs4 import BeautifulSoup
import asyncio
import config
import xlsxwriter

async def main():
    async with aiohttp.ClientSession() as session:
            async with session.get("https://ru.investing.com/equities/united-states", headers={"user-agent": config.user_agent}) as response:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                print(soup.title.string)
                await search(session, soup)

async  def search(session, soup):
    index = 0
    for company in soup.select("div#marketInnerContent tbody tr"):
        print(company.a.get("title"))
        amount = await get_dividend(session, company.a.get("href"))
        if amount is not None:
            worksheet.write(index, 0, company.a.get("title"))
            worksheet.write(index, 1, amount)
            index += 1
        if index == 5:
            break
    workbook.close()

async  def get_dividend(session, url):
    async with session.get(f"https://ru.investing.com{url}", headers={"user-agent": config.user_agent}) as response:
        soup = BeautifulSoup(await response.text(), "html.parser")
        element = soup.select("div.flex:nth-child(9) > dd:nth-child(2) > div:nth-child(1) > span:nth-child(1) > span:nth-child(1)")
        if len(element) != 0:
            return element[0].text


workbook = xlsxwriter.Workbook('Dividend.xlsx')
worksheet = workbook.add_worksheet()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())