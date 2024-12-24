from config import YOUTUBE_IMG_URL
from youtubesearchpython.__future__ import VideosSearch


async def gen_thumb(videoid):
    try:
        results = VideosSearch(videoid, limit=1)
        search_results = await results.next()
        if "result" in search_results and search_results["result"]:
            thumbnail = search_results["result"][0]["thumbnails"][0]["url"].split("?")[
                0
            ]
            return thumbnail
        else:
            return YOUTUBE_IMG_URL
    except Exception as e:
        return YOUTUBE_IMG_URL


async def gen_qthumb(videoid):
    try:
        results = VideosSearch(videoid, limit=1)
        search_results = await results.next()
        if "result" in search_results and search_results["result"]:
            thumbnail = search_results["result"][0]["thumbnails"][0]["url"].split("?")[
                0
            ]
            return thumbnail
        else:
            return YOUTUBE_IMG_URL
    except Exception as e:
        return YOUTUBE_IMG_URL
