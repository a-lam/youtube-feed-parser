import urllib.request
import xml.etree.ElementTree as ET

def get_videos_from_feed(url):
    try:
        with urllib.request.urlopen(url) as response:
            xml_data = response.read()
    except Exception as e:
        print(f"Could not retrieve data from {url}: {e}")
        return {"url": url, "videos": []}

    try:
        root = ET.fromstring(xml_data)
    except Exception as e:
        print(f"Could not parse XML from {url}: {e}")
        return {"url": url, "videos": []}
    
    # Define namespaces for Atom/RSS feeds
    namespaces = {
        'atom': 'http://www.w3.org/2005/Atom',
        'media': 'http://search.yahoo.com/mrss/',
        'yt': 'http://www.youtube.com/xml/schemas/2015'
    }
    
    videos = []
    
    # Parse Atom feed (YouTube uses Atom)
    for entry in root.findall('atom:entry', namespaces):
        title_elem = entry.find('atom:title', namespaces)
        link_elem = entry.find('atom:link', namespaces)
        published_elem = entry.find('atom:published', namespaces)
        
        if title_elem is not None and link_elem is not None and published_elem is not None:
            video = {
                "title": title_elem.text,
                "link": link_elem.get('href'),
                "updated": published_elem.text
            }
            videos.append(video)
    
    channel = {"url": url, "videos": videos}
    return channel

def get_videos(list_of_channels):
    channels = []
    for channel in list_of_channels:
        channels.append(get_videos_from_feed(channel['url']))
    return channels