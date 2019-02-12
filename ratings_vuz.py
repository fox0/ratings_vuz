import hashlib
from lxml import etree as ET
from lxml.builder import E

import requests
from bs4 import BeautifulSoup

from settings import RATINGS


def parse1(soup: BeautifulSoup):
    # https://www.topuniversities.com/universities/0000
    return soup.find('div', {'class': 'rank-r'}).text


def parse2(soup: BeautifulSoup):
    # http://www.webometrics.info/en/detalles/000
    cols = soup.find('table', {'id': 'mytable'}).find_all('tr')[1].find_all('td')
    return 'Country Rank %s. World Ranking %s' % (cols[2].text, cols[0].text)


def parse9(soup: BeautifulSoup):
    # https://www.4icu.org/reviews/rankings/university-ranking-0000.htm
    # todo rewrite
    result = []
    for i in soup.find_all('tr'):
        r = i.text.strip().replace('\n', ' ')
        if r:
            result.append(r)
    return '. '.join(result)


def to_rss(result):
    # когда в руках молоток, всё кажется гвоздями…
    ls = []
    for i, text in result.items():
        h = hashlib.new('ripemd160')
        h.update(text.encode())
        hash = h.hexdigest()
        ls.append(E.item(
            E.link('%s#%s' % (RATINGS[i], hash)),
            E.guid('rating_%s' % hash),
            E.title('%d. %s' % (i, text)),
        ))
    rss = E.rss(E.channel(*ls), version='2.0')
    print(ET.tostring(rss, xml_declaration=True, encoding='utf-8').decode('utf-8'))


def main():
    result = {}
    for i, url in RATINGS.items():
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        result[i] = globals()['parse%d' % i](soup)
    to_rss(result)


if __name__ == '__main__':
    main()
