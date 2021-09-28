from youtube_dl import YoutubeDL
from itertools import islice

class MusicQueue:

  def __init__(self):
    self.urls = {}

  async def getNextSong(self):
    if(len(self.urls) != 0):
      
      return list(self.urls)[0]
    return ""

  async def clearQueue(self):
    self.urls = {}

  async def addSong(self, url):
    with YoutubeDL({}) as ydl:
      info = ydl.extract_info(url, download=False)
      print(info['title'])
      self.urls[info['title']] = url

  async def remove(self, index):
    del self.urls[next(islice(self.urls, index, None))]
    print(self.urls)