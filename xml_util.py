import feedparser

def get_videos_from_feed(url):
    NewsFeed = feedparser.parse(url)
    videos = []
    for entry in NewsFeed.entries :
        video = { "title": entry.title, "link": entry['link'], "updated": entry['published'] }
        videos.append(video)
    channel = {"url": url, "videos": videos}
    return channel

def get_videos(list_of_channels):
    channels = []
    for channel in list_of_channels:
        channels.append(get_videos_from_feed(channel['url']))
    return channels