from os import path
from yt_dlp import YoutubeDL
from MusicIndo.utils import formatters, decorators
import asyncio

class SoundCloud:
    def __init__(self):
        self.opts: dict = {
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "format": "best",
            "retries": 3,
            "nooverwrites": False,
            "continuedl": True,
        }

    async def valid(self, link: str) -> bool:
        return "soundcloud" in link

    async def download(self, url: str) -> dict | bool:
        if not await self.valid(url):
            return False

        d = YoutubeDL(self.opts)
        try:
            info = await d.extract_info(url)
        except yt_dlp.utils.DownloadError as e:
            print(f"Error download: {e}")
            return False

        xyz = path.join("downloads", f"{info['id']}.{info['ext']}")
        duration_min = formatters.seconds_to_min(info["duration"])
        track_details = {
            "title": info["title"],
            "duration_sec": info["duration"],
            "duration_min": duration_min,
            "uploader": info["uploader"],
            "filepath": xyz,
        }
        return track_details, xyz