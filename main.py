import requests
from bs4 import BeautifulSoup
from sqlighter import SQLighter
url_links = 'https://wiki.warthunder.ru/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9D%D0%B0%D0%B7%D0%B5%D0%BC%D0%BD%D0%B0%D1%8F_%D1%82%D0%B5%D1%85%D0%BD%D0%B8%D0%BA%D0%B0_%D0%A4%D1%80%D0%B0%D0%BD%D1%86%D0%B8%D0%B8'
# URL = 'https://wiki.warthunder.ru/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9D%D0%B0%D0%B7%D0%B5%D0%BC%D0%BD%D0%B0%D1%8F_%D1%82%D0%B5%D1%85%D0%BD%D0%B8%D0%BA%D0%B0_%D0%93%D0%B5%D1%80%D0%BC%D0%B0%D0%BD%D0%B8%D0%B8'

url = f'https://wiki.warthunder.ru'

db = SQLighter('db.db')

HEADERS = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0",
     }

def get_links(url_for_links):
    src = get_html(url_for_links)

    soup = BeautifulSoup(src.text, "html.parser")

    all_links = soup.find_all("div", class_='tree-item')

    links = []
    for link in all_links:
        link = link.find("a").get("href")
        links.append(link)
    return links

def get_html(url, params=None):
    req = requests.get(url, headers=HEADERS, params=params)
    return req

def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    tanks = []

    all_categories = soup.find_all("div", class_='general_info_br')
    i = []
    for modes in all_categories:
        modes = modes.find_all("td")
        for mode in modes:
            mode = mode.text
            i.append(mode)
        tanks.append([soup.find("div", class_='general_info_name').text, i[3], i[4], i[5]])

    db.add_tank(tanks[0][0], tanks[0][1], tanks[0][2], tanks[0][3])



def parse(links):

    for link in links:
        html = get_html(f'{url}{link}')
        if html.status_code == 200:
            get_content(html.text)
        else:
            print('Error')



parse(get_links(url_links))
