import re
from typing import Dict
from bs4 import BeautifulSoup


def get_static_html(input: str) -> Dict:
    static_content = {}
    soup = BeautifulSoup(input, "lxml")
    for div in soup.findAll("div", attrs={'class': re.compile('scrape-element')}):
        static_content[div.get('id')] = str(div)
    for div in soup.findAll("div", attrs={'id': re.compile('^table-types-*')}):
        static_content[div.get('id')] = str(div)
    for div in soup.findAll("div", attrs={'id': re.compile('^table-kwaliteitsregimes-*')}):
        static_content[div.get('id')] = str(div)
    return static_content
