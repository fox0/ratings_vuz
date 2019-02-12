import re

import requests
from bs4 import BeautifulSoup

from settings import RATINGS


def parse1(soup: BeautifulSoup):
    # https://www.topuniversities.com/universities/0000
    return soup.find('div', {'class': 'rank-r'}).text


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
    parsers = {
        1: parse1,
        9: parse9,
    }
    for i, url in RATINGS.items():
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        text = parsers[i](soup)
        print('{}. {}'.format(i, text))


if __name__ == '__main__':
    main()
