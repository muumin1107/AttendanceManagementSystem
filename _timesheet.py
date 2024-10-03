import json

from pathlib import Path
from notion_client import Client

class TimeSheet:
    config = json.load(open('config.json', 'r', encoding='utf-8'))
    NOTION_ACCESS_TOKEN = config['NOTION_ACCESS_TOKEN']
    NOTION_MASTER_ID    = config['NOTION_MASTER_ID']