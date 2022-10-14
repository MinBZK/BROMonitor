from jinja2 import FileSystemLoader, Environment
import logging
import os
from pymongo import MongoClient
from bs4 import BeautifulSoup

from bromonitorgenerator.templates.figure_mapping import figure_mapping, data
from bromonitorgenerator.utils.start_date import set_start_date
from bromonitorgenerator.utils.utils import today
from common.config import MONGODB_URL

# Load the bromonitor_template html from filesystem
file_loader = FileSystemLoader("templates")
env = Environment(loader=file_loader)
template = env.get_template("bromonitor_template.html")

# Render the template with figures and links inserted at the mapped keys
html = template.render(figure_mapping)
output_recent = {"date": today(), "html": html, "static_data": data, "most_recent": True}

# Remove hrefs for the archived version
soup = BeautifulSoup(html, "lxml")
for a in soup.findAll("a"):
    del a["href"]

# Remove divs containing explanation on how the links work for archived version
for div in soup.find_all("div", {"class": "bromonitor-link-toelichting"}):
    div.decompose()

output_archive = {"date": today(), "html": str(soup), "most_recent": False}

# Mongodb connection
client = MongoClient(MONGODB_URL)
db = client.bro

# Insert fully generated archive html into mongo
# keeping one archive for each date
db.bromonitor.replace_one(
    filter={"date": output_archive["date"], "most_recent": False},
    replacement=output_archive,
    upsert=True,
)

# Insert fully generated most recent html into mongo
# Keep only exact 1 most_recent bromonitor
db.bromonitor.replace_one(
    filter={"most_recent": True}, replacement=output_recent, upsert=True
)

# Set the startdate value in the mongodb to the final registrationobject in the database currently
set_start_date()
