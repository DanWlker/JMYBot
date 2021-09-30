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

  def clearQueue(self):
    self.urls = {}

  def addSong(self, url):
      self.urls[self.getSongTitle(url)] = url
  
  def remove(self, index):
    del self.urls[next(islice(self.urls, index, None))]
    print(self.urls)

  def addToStart(self, url):
    new_dictionary = {self.getSongTitle(url): url}
    new_dictionary.update(self.urls)
    self.urls = new_dictionary

  def getSongTitle(self, url):
    with YoutubeDL({}) as ydl:
      info = ydl.extract_info(url, download=False)
      return info['title']
