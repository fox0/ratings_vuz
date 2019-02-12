import re

import requests
from bs4 import BeautifulSoup

from settings import RATINGS


def parse9(url):
    # https://www.4icu.org/reviews/rankings/university-ranking-0000.htm
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    result = []
    for i in soup.find_all('tr'):
        r = i.text.strip().replace('\n', ' ')
        if r:
            result.append(r)
    return '. '.join(result)


def main():
    parsers = {
        9: parse9,
    }
    for i, url in RATINGS.items():
        text = parsers[i](url)
        print(text)


if __name__ == '__main__':
    main()
