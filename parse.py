import sys, getopt
import feedparser
import os
import pytz
from datetime import datetime, timedelta, timezone

tracker_filename = ".ytdl_downloaded"
file_time_format = "%Y-%m-%dT%H:%M:%S%z"

def parse (command, sources, history_path) :
    video_retrieved = 0

    tracker_full_path = os.path.join(history_path, tracker_filename)
    tracker = []
    try:
        with open(tracker_full_path, 'r') as file:
            for line in file:
                tracker.append(strip_newline(line))
            file.close()
    except:
        pass

    out_tracker = []
    file = open(sources, 'r')
    for line in file:
        line = strip_newline(line)
        if line != "" and line[0] != "#" :
            num_downloaded, most_recent = fetch(command, tracker, line)
            out_tracker.append(line)
            out_tracker.append(most_recent.strftime(file_time_format))
            video_retrieved += num_downloaded
    file.close()

    file = open(tracker_full_path, 'w')
    file.writelines("\n".join(out_tracker))
    file.close()
    print("{} videos downloaded".format(video_retrieved))
	
def fetch (command, tracker, url):
    count = 0
    now = datetime.now(timezone.utc)
    last_check_time = now - timedelta(days=3)
    most_recent_time = datetime.min.replace(tzinfo=pytz.utc)

    try:
        i = tracker.index(url)
        last_check_time = datetime.strptime(tracker[i+1], file_time_format)
    except:
        pass

    NewsFeed = feedparser.parse(url)
    for entry in NewsFeed.entries :
        title = entry.title
        link = entry['link']
        updated = datetime.strptime(entry['published'], file_time_format)
        if updated > most_recent_time:
            most_recent_time = updated + timedelta(seconds=1)
        if updated > last_check_time :
            print (title + " " + link)
            cmd = command + " " + link
            os.system(cmd)
            count += 1
            
            
    return count, most_recent_time
		
def strip_newline(str):
    try:
        i = str.index("\n")
        return str[:i]
    except:
        pass
    return str

def main(argv):
    command = ''
    sources = ''
    history = ''
    try:
        opts, args = getopt.getopt(argv,'',['command=','sources=','history='])
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

    parse(command, sources, history)
    return


if __name__ == '__main__':
    main(sys.argv[1:])