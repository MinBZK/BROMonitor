import os
import logging
import shutil


def clean_folder(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))


log = logging.getLogger(__name__)
download_location = os.getenv('downloadLocation', '/mnt/brodata/')
unzip_location = os.getenv('unzipLocation', '/mnt/brodata/')

log.info("Cleaning download location at: " + download_location)
clean_folder(download_location)
log.info("Cleaning unzip location at: " + unzip_location)
clean_folder(unzip_location)
