import os

MAX_CONNECTIONS_COUNT = int(os.environ.get("maxConnectionsCount", 10))
MIN_CONNECTIONS_COUNT = int(os.environ.get("minConnectionsCount", 10))
logging_format = '''{"@timestamp": "%(asctime)s", "level": "%(levelname)s",
 "logger": "%(name)s", "message": "%(message)s"}'''
date_format = '%Y-%m-%d %H:%M:%S'

MONGODB_URL = os.environ.get('mongodbUrl', 'mongodb://localhost:27017')
