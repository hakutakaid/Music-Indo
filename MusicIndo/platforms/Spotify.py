import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython.__future__ import VideosSearch
import config
from MusicIndo.utils.decorators import asyncify

class SpotifyAPI:
    def __init__(self):
        self.regex = r"^(https:\/\/open.spotify.com\/)(.*)$"
        self.client_id: str = config.SPOTIFY_CLIENT_ID
        self.client_secret: str = config.SPOTIFY_CLIENT_SECRET

        if self.client_id and self.client_secret:
            self.client_credentials_manager = SpotifyClientCredentials(
                self.client_id, self.client_secret
            )
            self.spotify = spotipy.Spotify(
                client_credentials_manager=self.client_credentials_manager
            )
        else:
            self.spotify = None

    async def valid(self, link: str) -> bool:
        return bool(re.search(self.regex, link))

    async def track(self, link: str) -> tuple:
        try:
            track = self.spotify.track(link)
            info = track["name"]
            for artist in track["artists"]:
                fetched = f" {artist['name']}"
                if "Various Artists" not in fetched:
                    info += fetched
            results = VideosSearch(info, limit=1)
            for result in (await results.next())["result"]:
                ytlink = result["link"]
                title = result["title"]
                vidid = result["id"]
                duration_min = result["duration"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                track_details = {
                    "title": title,
                    "link": ytlink,
                    "vidid": vidid,
                    "duration_min": duration_min,
                    "thumb": thumbnail,
                }
                return track_details, vidid
        except Exception as e:
            print(f"Error: {e}")
            return None

    async def playlist(self, url: str) -> tuple:
        try:
            playlist = self.spotify.playlist(url)
            playlist_id = playlist["id"]
            results = []
            for item in playlist["tracks"]["items"]:
                music_track = item["track"]
                info = music_track["name"]
                for artist in music_track["artists"]:
                    fetched = f" {artist['name']}"
                    if "Various Artists" not in fetched:
                        info += fetched
                results.append(info)
            return results, playlist_id
        except Exception as e:
            print(f"Error: {e}")
            return None

    async def album(self, url: str) -> tuple:
        try:
            album = self.spotify.album(url)
            album_id = album["id"]
            results = []
            for item in album["tracks"]["items"]:
                info = item["name"]
                for artist in item["artists"]:
                    fetched = f" {artist['name']}"
                    if "Various Artists" not in fetched:
                        info += fetched
                results.append(info)
            return results, album_id
        except Exception as e:
            print(f"Error: {e}")
            return None

    async def artist(self, url: str) -> tuple:
        try:
            artist_info = self.spotify.artist(url)
            artist_id = artist_info["id"]
            results = []
            artist_top_tracks = self.spotify.artist_top_tracks(url)
            for item in artist_top_tracks["tracks"]:
                info = item["name"]
                for artist in item["artists"]:
                    fetched = f" {artist['name']}"
                    if "Various Artists" not in fetched:
                        info += fetched
                results.append(info)
            return results, artist_id
        except Exception as e:
            print(f"Error: {e}")
            return None