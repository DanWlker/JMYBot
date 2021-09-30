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

  def appendSong(self, url):
      self.urls[self.getSongTitle(url)] = url
  
  def insertToPos(self, url, pos):
    new_entry = {self.getSongTitle(url): url}
    new_list = list(self.urls.items())[:pos] + list(new_entry.items()) + list(self.urls.items())[pos:]
    new_dict = {}

    for entry in new_list:
        new_dict[entry[0]] = entry[1]
    
    self.urls = new_dict
  
  def remove(self, index):
    del self.urls[next(islice(self.urls, index, None))]
    print(self.urls)

  def getSongTitle(self, url):
    with YoutubeDL({}) as ydl:
      info = ydl.extract_info(url, download=False)
      return info['title']
