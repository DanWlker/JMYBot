import nacl
import youtube_dl
from discord.ext import commands
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from MusicQueue import MusicQueue

class MusicCog(commands.Cog):

  def __init__(self, client):
    self.client = client
    self.songList = MusicQueue()
    self.currentBotVoice = None
    self.repeatMode = 0

  def setup(client): 
    client.add_cog(MusicCog(client))

  #helps the bot to determine if it needs to join a new room, switch to a new room, or remain in current room
  #returns false if not in a channel
  #TODO: May need to refactor this into two separate classes, one for chiecking one for actual join room
  async def join(self, ctx):
    if(ctx.author.voice is None): #if author is not in channel
      await ctx.send("Please enter a voice channel before using bot")
      return False

    if(ctx.voice_client is None):
      await ctx.author.voice.channel.connect()
      return True

    if(ctx.voice_client.channel != ctx.author.voice.channel): #move if not in same voice channel
      print("Not in same channel, switching")
      await self.disconnect(ctx)
      await self.join(ctx)
      return True

    print("Same channel")
    return True

  @commands.command(pass_context=True)
  async def disconnect(self, ctx):
    await ctx.voice_client.disconnect()
    self.currentBotVoice = None #Garbage cleanup, not sure if will have bug or not

  @commands.command(pass_context=True)
  async def play(self, ctx, youtube_url=""):

    if (not await self.join(ctx)):#if the bot cannot join or is not in a channel
      return

    ctx.voice_client.stop() #stop the current playing song

    #There are 3 possible inputs: "", youtube url, jargon
    #if "" check if there is queued songs, if yes then play it
    #if youtube_url add to queue and play it
    #if jargon return

    if(youtube_url == ""): #if the url is blank
      if(self.songList.getNextSong() == ""): #check for the next song
        return #end if there are no queued songs
    else:
      if(self.is_supported(youtube_url)): #if it is not blank, check if it is jargon
        self.songList.addToStart(youtube_url) #add to the first in the queue if it is a valid url
      else:
        return #return if jargon

    self.currentBotVoice = ctx.voice_client #save the current context to be used when replaying
    self.startSong() #start the actual song playback

  def playNextSong(self): 
    thisSong = self.songList.getNextSong()
    self.songList.removeNextSong();

    if(self.repeatMode == 1):
      self.songList.addSong(thisSong)

    if(self.repeatMode == 2):
      self.songList.addToStart(thisSong)

    if(self.songList.getNextSong() != ""): #check if next song is available
      self.startSong();

  def startSong(self):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': True,}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    youtube_url = self.songList.getNextSong()
    
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        URL = info['formats'][0]['url']
        self.currentBotVoice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after= lambda e: self.playNextSong())
  
  #check if youtube_dl can open the song
  def is_supported(self, url): 
    extractors = youtube_dl.extractor.gen_extractors()
    for e in extractors:
      if e.suitable(url) and e.IE_NAME != 'generic':
        return True
    return False
    
  @commands.command(pass_context=True)
  async def pause(self, ctx):
    self.currentBotVoice = ctx.voice_client
    await ctx.send("Music has been paused")
    await ctx.voice_client.pause()
    
  @commands.command(pass_context=True)
  async def resume(self, ctx):
    self.currentBotVoice = ctx.voice_client
    await ctx.send("Music has been resumed")
    await ctx.voice_client.resume()

  #difference between this and join is that this does not interrupt the song play
  @commands.command(pass_context=True)
  async def move(self, ctx):
    if(ctx.author.voice is None): #if author is not in channel
      await ctx.send("Please enter a voice channel before using bot")
      return
    await ctx.voice_client.move_to(ctx.author.voice.channel)
    self.currentBotVoice = ctx.author.voice.channel
    
  @commands.command(pass_context=True)
  async def queue(self, ctx, youtube_url):
    if(not self.is_supported(youtube_url)):
      await ctx.send("Link not supported, please use a youtube link")
    
    self.songList.addSong(youtube_url)
    await ctx.send("Song queued")

  @commands.command(pass_context=True)
  async def showQueue(self, ctx):
    if(len(self.songList.urls) == 0):
      await ctx.send("No music is queued")
      return
    str = ""
    strExtra = "**(Now playing)**"
    queueNames = list(self.songList.urls.keys())
    for i in range(len(queueNames)):
      str += f"{i+1}. {queueNames[i]} {strExtra}\n"
      strExtra = ""

    await ctx.send(str)

  @commands.command(pass_context=True)
  async def remove(self, ctx, number):
    if(not number.isdigit()):
      await ctx.send("Please enter the index of the song you want to remove")
      return

    actualIndex = int(number)-1

    if(actualIndex == 0):
      await ctx.send("Cannot remove currently playing song")
      return

    if(actualIndex >= len(self.songList.urls) or actualIndex < 0):
      await ctx.send("Please enter a valid number")
      return

    self.songList.remove(actualIndex)
    await ctx.send(f"Song in position {number} is removed")

  @commands.command(pass_context=True)
  async def clearQueue(self, ctx):
    self.songList.clearQueue()

  @commands.command(pass_context=True)
  async def skip(self, ctx): 
    await self.play(ctx)

  @commands.command(pass_context=True)
  async def repeatQueue(self, ctx):
    if(self.repeatMode == 1):
      self.repeatMode = 0 #reset to no repeat
      await ctx.send("Repeat function is off")
    else:
      self.repeatMode = 1
      await ctx.send("Repeat song queue is on")

  @commands.command(pass_context=True)
  async def repeatSong(self, ctx):
    if(self.repeatMode == 2):
      self.repeatMode = 0 #reset to no repeat
      await ctx.send("Repeat function is off")
    else:
      self.repeatMode = 2
      await ctx.send("Repeat current song is on")
  
  @commands.command(pass_context=True)
  async def repeatOff(self, ctx):
    self.repeatMode = 0
    await ctx.send("Repeat function is off")

  @commands.command(pass_context=True)
  async def musichelp(self, ctx):
    str = \
    """
**.play <youtube link>**
> Play song from youtube link
**.pause**
> Pause playback of current song
**.resume**
> Resume playback of current song
**.move**
> To move the bot to another channel without changing song
**.disconnect**
> Disconnect bot from channel
**.skip**
> Skip the current track
**.clearQueue**
> clear the current queue
**.remove <queue number>**
> remove the songs based on queue number. Note: do not remove the first one, it is the one that is currently playing
**.showQueue**
> Show all songs being queued to play
**.queue <youtube link>**
> Queue this song to be played next
**.repeatQueue**
> Repeat the current song queue
**.repeatSong**
> Repeat the current song that is being played
**.repeatOff**
> Turn off the repeat function
    """
    await ctx.send(str)