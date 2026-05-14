#!/usr/bin/env python3
"""
Fetch Nagpur news from Google News RSS and output a digest.
"""
import os
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
import re

def load_env():
    env_path = os.path.expanduser('~/.hermes/.env')
    env = {}
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    k, v = line.split('=', 1)
                    env[k] = v.strip('"\'')
    return env

def fetch_nagpur_news():
    url = "https://news.google.com/rss/search?q=Nagpur&hl=en-IN&gl=IN&ceid=IN:en"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            return data
    except Exception as e:
        print(f"ERROR fetching RSS: {e}")
        return None

def parse_rss(xml_data):
    if xml_data is None:
        return []
    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        print(f"XML parse error: {e}")
        return []
    # Find channel
    channel = root.find('channel')
    if channel is None:
        return []
    items = []
    for item in channel.findall('item'):
        title_elem = item.find('title')
        title = title_elem.text if title_elem is not None else ''
        link_elem = item.find('link')
        link = link_elem.text if link_elem is not None else ''
        pubdate_elem = item.find('pubDate')
        pubdate = pubdate_elem.text if pubdate_elem is not None else ''
        source_elem = item.find('source')
        source_name = source_elem.text if source_elem is not None else ''
        description_elem = item.find('description')
        description = description_elem.text if description_elem is not None else ''
        # strip HTML tags
        if description:
            description = re.sub('<[^<]+?>', '', description)
        else:
            description = ''
        items.append({
            'title': title.strip(),
            'link': link.strip(),
            'pubdate': pubdate.strip(),
            'source': source_name.strip(),
            'description': description.strip()[:200]
        })
    return items

def format_digest(items):
    if not items:
        return "No news found."
    lines = []
    lines.append(f"📰 Nagpur News Digest — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"Total articles: {len(items)}")
    lines.append("\n**Top stories:**")
    for i, it in enumerate(items[:5], 1):
        lines.append(f"{i}. {it['title']}")
        lines.append(f"   Source: {it['source']} | {it['pubdate']}")
        if it['description']:
            lines.append(f"   {it['description']}")
        lines.append("")
    return "\n".join(lines)

def main():
    env = load_env()
    xml_data = fetch_nagpur_news()
    if xml_data is None:
        print("Failed to fetch news")
        return
    items = parse_rss(xml_data)
    digest = format_digest(items)
    print(digest)

if __name__ == "__main__":
    main()