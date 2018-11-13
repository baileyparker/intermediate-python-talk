from argparse import ArgumentParser
from requests import get
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote


WIKIPEDIA_ARTICLE_BASE = 'https://en.wikipedia.org/wiki/'


def is_alive(name):
    url = urljoin(WIKIPEDIA_ARTICLE_BASE, quote(name))
    req = get(url)
    page = BeautifulSoup(req.text, features='html5lib')

    full_name = page.find('h1', {'id': 'firstHeading'})

    for table in page.find_all('table', {'class': 'infobox'}):
        for th in table.find_all('th', {'scope': 'row'}):
            if 'died' in th.text.lower():
                return full_name, False

    return full_name, True


def get_args():
    parser = ArgumentParser(description='determine if someone is still alive')
    parser.add_argument('name', help='The name of the person')

    return parser.parse_args()


def main():
    args = get_args()

    full_name, alive = is_alive(args.name)
    state = 'alive' if alive else 'dead'
    print(f'{args.name} is {state}.')


if __name__ == '__main__':
    main()
