### STOAT
from __future__ import annotations

import stoat

### .env file load
import os
from dotenv import load_dotenv

### YouTube/Twitch Feed Parser
import feedparser


load_dotenv()
STOAT_BOT_TOKEN = os.getenv('STOAT_BOT_TOKEN')
TWITCH_CHANNEL_NAME = os.getenv('TWITCH_CHANNEL_NAME')
YOUTUBE_CHANNEL_ID = os.getenv('YOUTUBE_CHANNEL_ID')

YOUTUBE_RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={YOUTUBE_CHANNEL_ID}"


### TODO: Add retry logic, due to "bozo_exception"
# {'bozo': 1, 'entries': [], 'feed': {'html': {'lang': 'en'}, 'meta': {'name': 'viewport', 'content': 'initial-scale=1, minimum-scale=1, width=device-width'}, 'a': {'href': '//www.google.com/'}, 'span': {'id': 'logo', 'aria-label': 'Google'}}, 'headers': {'date': 'Mon, 16 Feb 2026 05:32:44 GMT', 'content-type': 'text/html; charset=UTF-8', 'server': 'YouTube RSS Feeds server', 'content-length': '1613', 'x-xss-protection': '0', 'x-frame-options': 'SAMEORIGIN', 'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000', 'connection': 'close'}, 'href': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCxksf38e-ArIHqtfYwoxNsw', 'status': 404, 'encoding': 'UTF-8', 'bozo_exception': SAXParseException('not well-formed (invalid token)'), 'version': '', 'namespaces': {}}
feed = feedparser.parse(YOUTUBE_RSS_URL)
latest_entry = feed.entries[0]

if "media_liveBroadcastStatus" in latest_entry and latest_entry.media_liveBroadcastStatus == "active":
    print("YouTube Channel is LIVE!")
else:
    print("YouTube Not live.")

TWITCH_RSS_URL = f"https://twitchrss.com/feeds/?username={TWITCH_CHANNEL_NAME}&feed=streams"

feed = feedparser.parse(TWITCH_RSS_URL)
latest_entry = feed.entries[0]

if "summary" in latest_entry and "stream is live" in latest_entry.summary:
    print("Twitch Channel is LIVE!")
else:  
    print("Twitch Not live.")


# Whether the example should be ran as a user account or not
self_bot = False

client = stoat.Client(token=STOAT_BOT_TOKEN, bot=not self_bot)


@client.on(stoat.ReadyEvent)
async def on_ready(_, /) -> None:
    print('Logged on as', client.me)


@client.on(stoat.MessageCreateEvent)
async def on_message(event: stoat.MessageCreateEvent) -> None:
    message = event.message

    # Don't respond to ourselves/others
    if (message.author.relationship is stoat.RelationshipStatus.user) ^ self_bot:
        return

    if message.content == '!ping':
        print(f'Message: {message}')
        await message.channel.send('pong')

client.run()