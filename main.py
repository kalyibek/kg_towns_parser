import requests
import csv
from bs4 import BeautifulSoup

URL = 'https://ru.wikipedia.org/wiki/%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D0%B0_%D0%9A%D0%B8%D1%80%D0%B3%D0%B8%D0%B7%D0%B8' \
      '%D0%B8 '

response = requests.get(URL)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table', class_='wikitable sortable')
content = table.find('tbody')


with open('kg_towns.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    header_list = ['link']
    tr_tags = content.findChildren('tr')

    for tr in tr_tags:
        for th in tr.findChildren('th'):
            header_list.append(th.text)

    writer.writerow(header_list)

    for tr in tr_tags:
        towns_list = []
        for td in tr.findChildren('td'):
            if tr.findChildren('td').index(td) == 0:
                towns_list.append('https://ru.wikipedia.org' + td.a['href'])
            elif tr.findChildren('td').index(td) == 2:
                images = td.findChildren('a')
                if len(images) != 0:
                    towns_list.append(
                        f"https://ru.wikipedia.org{images[0]['href']}"
                    )
            towns_list.append(td.text)

        writer.writerow(towns_list)
