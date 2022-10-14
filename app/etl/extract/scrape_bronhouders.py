from bs4 import BeautifulSoup
import logging
import os
import pickle
import requests
from common.config import date_format, logging_format


class BronhouderScraper:
    def __init__(self):
        location = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__))
        )
        file_name = "bronhouders.pickle"
        logging.basicConfig(
            level=os.environ.get("LOGLEVEL", "INFO"),
            format=logging_format,
            datefmt=date_format,
        )

        self.logger = logging.getLogger(__name__)
        self.path = os.path.join(location, file_name)
        self.URL = "https://basisregistratieondergrond.nl/service-contact/formulieren/aangemeld-bro/"

    def scrape(self):
        page = self.__get_page()
        if not page:
            return
        soup = BeautifulSoup(page.content, "html.parser")
        kvk_list = soup.find(id="block-tno-content_1").prettify().split("<br/>")
        bronhouders = set()
        for kvk in kvk_list:
            bronhouder = self.__process_kvk(kvk)
            if bronhouder:
                bronhouders.add(bronhouder)
        self.logger.info(
            f"Total scraped bronhouders: {len(bronhouders)} out of {len(kvk_list)} kvks listed."
        )
        self.__write_to_pickle(bronhouders)

    def read_pickle(self):
        try:
            bronhouders = pickle.load(open(self.path, "rb"))
            return bronhouders
        except Exception:
            return None

    def __get_page(self):
        try:

            headers = {
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9,nl;q=0.8",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Cache-Control": "no-cache",
                "pragma": "no-cache",
                "update-insecure-requests": "1",
            }
            r = requests.get(self.URL, headers=headers)
            return r
        except requests.exceptions.RequestException as e:
            self.logger.warning(f"Request exception: {e}")
            return None
        except Exception as e:
            self.logger.warning(f"{e}")
            return None

    def __process_kvk(self, kvk_element):
        name = kvk_element.split("|")[0].strip()
        kvk = kvk_element.split("|")[-1].strip().split("\n")[0]
        if len(kvk) != 8:
            self.logger.warning(f"Scraped invalid KVK: {kvk}")
        is_bronhouder = kvk_element.find("strong")
        if is_bronhouder != -1:
            return kvk
        else:
            return None

    def __write_to_pickle(self, bronhouders: set):
        if len(bronhouders) <= 300:
            self.logger.warning(
                f"Found an abnormally small number of bronhouders ({len(bronhouders)}). Not writing new results to the pickle."
            )
            return
        try:
            os.remove(self.path)
        except OSError:
            self.logger.info(
                f"Exception during deletion of old pickle. Possibly no old pickle was present."
            )
            pass
        finally:
            pickle.dump(bronhouders, open(self.path, "wb"))
            self.logger.info(f"Written bronhouder data to new pickle.")
