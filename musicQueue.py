class musicQueue:
  urls = []

  @classmethod
  def getNextSong():
    if(len(musicQueue.urls) != 0):
      return musicQueue.urls[0]
    return ""

  @classmethod
  def clearQueue():
    musicQueue.urls = []

  @classmethod
  def addSong(url):
    musicQueue.urls.add(url);