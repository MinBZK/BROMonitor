from typing import Dict
from bs4 import BeautifulSoup


def get_total_registered_objects(input: str) -> int:
    soup = BeautifulSoup(input, "lxml")
    rows = soup.find("table", border=1).find("tbody").find_all("tr")
    sum_ = 0
    for row in rows:
        cells = row.find_all("td")
        sum_ += int(cells[-1].getText().replace(".", ""))
    return '{:,}'.format(sum_).replace(',','.')

def parse_weekly_top20(input: str) -> Dict:
    numbers = {
        "bronhouders": 0,
        "registraties": 0,
        "glds": 0
    }
    soup = BeautifulSoup(input, "lxml")
    rows = soup.find("table", border=1).find("tbody").find_all("tr")
    bronhouders = []
    for row in rows:
        cells = row.find_all("td")
        bronhouders.append(cells[0].getText())
        numbers["registraties"] += int(cells[2].getText().replace(".", ""))
        numbers["registraties"] += int(cells[3].getText().replace(".", ""))
        if cells[1].getText() == "GLD":
            numbers["glds"] += int(cells[2].getText().replace(".", ""))
    numbers["bronhouders"] = len(set(bronhouders))
    for key in numbers:
        numbers[key] = '{:,}'.format(numbers[key]).replace(',','.')
    return numbers