import requests
import logging
from lxml import etree
from dateutil.parser import *

from etl.extract.feed import Feed

log = logging.getLogger(__name__)
feed_ns = {'a': 'http://www.w3.org/2005/Atom',
           'b': 'http://www.georss.org/georss'}


def fetch_geopackage_feed(url):
    response = requests.get(url)
    if response.status_code == 200:
        root = etree.fromstring(response.content)

        # Grab the last part of the URL,
        # since a filename is not given in the ID field but a full URL
        filename = root.xpath('/a:feed/a:entry/a:link/@href',
                              namespaces=feed_ns)[0].rsplit('/', 1)[1]
        zip_url = root.xpath(
            '/a:feed/a:entry/a:link/@href', namespaces=feed_ns)[0]
        zip_size = root.xpath(
            '/a:feed/a:entry/a:link/@length', namespaces=feed_ns)[0]
        updated = root.xpath(
            '/a:feed/a:entry/a:updated/text()', namespaces=feed_ns)[0]

        return Feed(filename, zip_url, zip_size, parse(updated))


def download_zip(url, tmp_file):
    with requests.get(url, stream=True, timeout=10) as request:
        request.raise_for_status()
        written_bytes = 0
        with open(tmp_file, 'wb') as f:
            for chunk in request.iter_content(chunk_size=10000):
                if written_bytes % 100000000 == 0:
                    log.info("%s mb downloaded" % str(written_bytes / 1000000))
                if chunk:
                    f.write(chunk)
                written_bytes += 10000
            return True
