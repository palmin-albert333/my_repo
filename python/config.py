from os import path, getenv
import json


APP_DIR = path.dirname(path.abspath(__file__))

with open(path.join(APP_DIR, 'config.json'), 'r') as fp:
    config = json.load(fp)

