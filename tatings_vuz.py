from pprint import pprint
from json import JSONEncoder, JSONDecoder

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


def main():
    result = {}
    for i, url in RATINGS.items():
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        result[i] = globals()['parse%d' % i](soup)

    with open('db.json') as f:
        old_result = {}
        for k, v in JSONDecoder().decode(f.read()).items():
            old_result[int(k)] = v

    diff = []
    for i in result.keys():
        if result[i] != old_result[i]:
            diff.append('%s' % RATINGS[i])
            diff.append('old: %s' % old_result[i])
            diff.append('new: %s' % result[i])
            diff.append('')
    print('\n'.join(diff))
    # todo save


if __name__ == '__main__':
    main()
