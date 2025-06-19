#
#

from MusicIndo.platforms import saavn


async def download(title, video):
    raise ValueError("Failed to download song from youtube")
    video = None
    path, details = await saavn.download(title)
    return path, details, video
