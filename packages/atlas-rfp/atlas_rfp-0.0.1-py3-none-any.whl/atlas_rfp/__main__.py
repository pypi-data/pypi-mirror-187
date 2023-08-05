import json
from touchstone_auth import TouchstoneSession
from .atlas_parsing import parse_search, parse_rfp_details
from . import search
with open('credentials.json', encoding='utf-8') as configfile:
    config = json.load(configfile)

with TouchstoneSession('https://adminappsts.mit.edu/rfp/SearchEntry.action?sapSystemId=PS1',
        config['certfile'], config['password'], 'cookiejar.pickle',
        verbose=True) as s:
	pass