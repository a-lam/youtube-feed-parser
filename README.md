# Youtube-Feed-Parser
This tool takes in a list of Youtube channels or playlists and executes a command against the videos found. This tool can be used in conjunction with downloaders such as [yt-dlp](https://github.com/yt-dlp/yt-dlp) or other forks of the project.

## Requirements
- [Python](https://www.python.org/downloads/) 3.0+

## Usage
1. Download the application.
    ```
    curl -L https://github.com/a-lam/youtube-feed-parser/archive/refs/heads/main.zip --output main.zip
    unzip main.zip
    ```
1. Prepare the sources file.
1. Execute the tool.
    ```
    python parse.py --command CMD --sources SOURCE_FILE --history HISTORY_FOLDER
    ```

### Arguments
    --command COMMAND           Command to execute against each file. (Required)
    --sources FILE              File that contains the URLs of channels/playlists. (Required)
    --history FOLDER            Folder to store the history of processed videos. (Required)
    --days NUMBER               How old a video's published date can be to be processed. (Default=3)

## Preparing Sources
The sources file is a list of URLs for the tool to fetch videos from. The sample-sources.json file contains an example of what this file may look like. It contains a json object with a single key/value pair of "sources" which is a list. Each item in the list is another json object with two keys "channel" and "url". "channel" is only used for readability, the tool does not use this value. "url" is a direct link to the channel or playlist's XML feed.

The sample-sources.json file has an example of both a channel feed and a playlist feed, denoted by the "channel_id" and "playlist_id" parameters of the URL, respectively. A channel or playlist's id may be obtained by navigating directly to the channel or playlist through a browser. For channels, if found via search might lead to a URL with the channel's friendly name, such as "https://www.youtube.com/c/mkbhd". In this case, you will need to parse through the source of the page to grab its' external ID via [this method](https://stackoverflow.com/a/16326307).
