from youtube_dl import YoutubeDL
from itertools import islice

class MusicQueue:

  def __init__(self):
    self.urls = {}

  def getNextSong(self):
    if(len(self.urls) != 0):
      return list(self.urls.values())[0]
    return ""

  def removeNextSong(self):
    del self.urls[next(islice(self.urls, 0, None))]

  async def clearQueue(self):
    self.urls = {}

  async def addSong(self, url):
      self.urls[await self.getSongTitle(url)] = url

  async def remove(self, index):
    del self.urls[next(islice(self.urls, index, None))]
    print(self.urls)

  async def addToStart(self, url):
    new_dictionary = {await self.getSongTitle(url): url}
    new_dictionary.update(self.urls)
    self.urls = new_dictionary

  async def getSongTitle(self, url):
    with YoutubeDL({}) as ydl:
      info = ydl.extract_info(url, download=False)
      return info['title']