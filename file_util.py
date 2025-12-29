import os
import json
from datetime import datetime, timedelta, timezone
import channel_util

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
    # Only keep 30 days of history, to keep the file size and processing under control
    lookback = datetime.now(timezone.utc) - timedelta(days=30)
    for channel in history:
        videos = channel['videos']
        filtered = filter(lambda v: lookback < datetime.strptime(v['updated'], TIME_FORMAT), videos)
        new_vids = list(filtered)
        channel['videos'] = new_vids
    
    history_fullpath = os.path.join(history_path, HISTORY_FILENAME)
    data = { "history": history }
    with open(history_fullpath, 'w') as myFile:
        json.dump(data, myFile)
    return

def add_channel_to_sources(file, channelName):
    """Add a new channel to the sources file by looking up its external id.
    
    Args:
        file: path to the sources JSON file
        channelName: name of the channel to add
    """
    try:
        # Get the channel external id
        channel_id = channel_util.get_channel_external_id(channelName)
        
        if not channel_id:
            # External id not found, leave file unmodified
            return
        
        # Read the sources file
        with open(file, 'r') as f:
            data = json.load(f)
        
        # Create the new channel object
        new_channel = {
            "channel": channelName,
            "url": f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        }
        
        # Check for duplicate URL
        for existing_channel in data['sources']:
            if existing_channel['url'] == new_channel['url']:
                print(f"Channel {channelName} ({channel_id}) already exists in sources.")
                return
        
        # Append to sources array
        data['sources'].append(new_channel)
        
        # Write back to file
        with open(file, 'w') as f:
            json.dump(data, f, indent=4)
        
        print(f"Successfully added channel {channelName} to the sources file.")
        
    except Exception as e:
        print(f"Error adding channel {channelName}: {e}")
        # Application continues
        pass
