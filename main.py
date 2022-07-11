import datetime
from datetime import timedelta, date
import requests as req
from time import sleep
from bs4 import BeautifulSoup
import re


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


start_date = date(2000, 1, 1)
end_date = datetime.date.today()
list_of_prices = list()

for single_date in daterange(start_date, end_date):
    URL = f'https://www.xe.com/currencytables/?from=USD&date={single_date.strftime("%Y-%m-%d")}'
    page = req.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="table-section")
    currencies_table = results.find_all("table", class_="currencytables__Table-xlq26m-3 jaGdii")[-1].extract()
    currencies_list = currencies_table.find_all("td")

    for item in currencies_list:
        if re.match("^(.*?([Gg]old))", str(item)):
            list_of_prices.append(currencies_list[currencies_list.index(item)+2])
            print(single_date, currencies_list[currencies_list.index(item)+2], end="\n")
            sleep(1)