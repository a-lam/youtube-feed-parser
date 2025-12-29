import os
import sys, getopt
import subprocess
import file_util
import xml_util
from datetime import datetime, timedelta, timezone

def get_videos(command, channels, histories, days):
    processed = 0
    lookback = datetime.now(timezone.utc) - timedelta(days=days)
    for channel in channels:
        videos = channel['videos']
        prev_videos = get_or_create_channel_history(histories, channel['url'])
        for video in videos:
            updated = datetime.strptime(video['updated'], file_util.TIME_FORMAT)
            if lookback < updated:
                if not video_in_history(prev_videos, video):
                    get_video(command, video)
                    processed += 1

    print ('Processed ' + str(processed) + ' videos')
    return

def get_or_create_channel_history(histories, url):
    for history in histories:
        if history['url'] == url:
            return history['videos']

    new_history = {"url": url, "videos": []}
    histories.append(new_history)
    return new_history['videos']

def video_in_history(prev_videos, new_video):
    for video in prev_videos:
        if video['link'] == new_video['link']:
            return True

    prev_videos.append(new_video)
    return False

def get_video(command, video):
    title = video['title']
    link = video['link']
    print (title + " " + link)
    cmd = f'{command} "{link}"'
    try:
        rc = subprocess.call(cmd, shell=True)
        if rc == 0:
            return True
    except Exception as e:
        print(f"Error executing command: {e}")
    return False


def main(argv):
    command = ''
    sources = ''
    history = ''
    days = 3
    channelName = ''
    try:
        opts, args = getopt.getopt(argv,'',['command=','sources=','history=','days=','add-channel='])
    except getopt.GetoptError:
        print ('parse.py --command <cmd> --sources <sources> --history <folder>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '--command':
            command = arg
        elif opt == '--sources':
            sources = arg
        elif opt == '--history':
            history = arg
        elif opt == '--days':
            days = int(arg)
        elif opt == '--add-channel':
            channelName = arg

    if channelName:
        # Separate execution path: add channel to sources file
        file_util.add_channel_to_sources(sources, channelName)
        return

    # Normal execution path: process videos
    urls = file_util.get_sources(sources)
    feed_videos = xml_util.get_videos(urls)
    processed = file_util.get_history(history)
    get_videos(command, feed_videos, processed, days)
    file_util.set_history(history, processed)
    return


if __name__ == '__main__':
    main(sys.argv[1:])