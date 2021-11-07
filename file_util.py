import os
import json

HISTORY_FILENAME = 'youtube-feed-parser.history.json'
TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"

def get_sources(file):
    with open(file, 'r') as myfile:
        data = myfile.read()
    obj = json.loads(data)
    return obj['sources']

def get_history(history_path):
    history_fullpath = os.path.join(history_path, HISTORY_FILENAME)
    if not os.path.exists(history_fullpath):
        return []
    with open(history_fullpath, 'r') as myFile:
        data = myFile.read()
    try:
        obj = json.loads(data)
        return obj['history']
    except:
        pass
    return []

def set_history(history_path, history):
    history_fullpath = os.path.join(history_path, HISTORY_FILENAME)
    data = { "history": history }
    with open(history_fullpath, 'w') as myFile:
        json.dump(data, myFile)
    return