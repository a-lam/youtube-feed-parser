"""Utilities to resolve a YouTube channel's external id (the "UC..." id).

This is a best-effort implementation that fetches a YouTube channel page
and extracts the channel id from the HTML. It does not use the
official YouTube Data API and therefore may be brittle.
"""
import re
import urllib.request
import urllib.parse

__all__ = ["get_channel_external_id"]


def get_channel_external_id(channel_name: str, timeout: int = 10) -> str | None:
    """Return the external channel id (starting with 'UC') for `channel_name`.

    Args:
        channel_name: YouTube channel handle (without @ prefix) or username.
        timeout: request timeout in seconds.

    Returns:
        The channel id string (e.g. 'UCxxxxxxxx...') or None if not found.
    """
    if not channel_name:
        return None

    # Remove @ prefix if present
    if channel_name.startswith('@'):
        channel_name = channel_name[1:]

    # Construct direct channel URL
    channel_url = f"https://www.youtube.com/@{channel_name}"
    req = urllib.request.Request(channel_url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    })

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"Could not retrieve data from {channel_url}: {e}")
        return None

    # Look for explicit /channel/ links in the HTML
    m = re.search(r"/channel/(UC[0-9A-Za-z_-]{20,})", html)
    if m:
        return m.group(1)

    # Fall back to JSON-like properties present in the page
    m = re.search(r'"externalId":"(UC[0-9A-Za-z_-]{20,})"', html)
    if m:
        return m.group(1)

    m = re.search(r'"channelId":"(UC[0-9A-Za-z_-]{20,})"', html)
    if m:
        return m.group(1)

    print(f"Could not find channel external id for '{channel_name}' on channel page.")
    return None
