import nacl
from discord.ext import commands
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from MusicQueue import MusicQueue

class MusicCog(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.queue = MusicQueue()

  def setup(client): 
    client.add_cog(MusicCog(client))

  async def join(self, ctx):
    if(ctx.author.voice is None): #if author is not in channel
      await ctx.send("Please enter a voice channel before using bot")
      return

    voiceChannel = ctx.author.voice.channel

    if(ctx.voice_client is None):
      await voiceChannel.connect()
      return

    if(ctx.voice_client != voiceChannel): #no need to move if in same voice channel
      await self.disconnect(ctx)
      await self.join(ctx)
      return

    print("same channel")

  @commands.command(pass_context=True)
  async def disconnect(self, ctx):
    await ctx.voice_client.disconnect()

  @commands.command(pass_context=True)
  async def play(self, ctx, youtube_url):
    await self.join(ctx)
    ctx.voice_client.stop()

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': True,}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = ctx.voice_client

    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        URL = info['formats'][0]['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))

  @commands.command(pass_context=True)
  async def pause(self, ctx):
    await ctx.send("Music has been paused")
    await ctx.voice_client.pause()
  
  @commands.command(pass_context=True)
  async def resume(self, ctx):
    await ctx.send("Music has been resumed")
    await ctx.voice_client.resume()

  @commands.command(pass_context=True)
  async def move(self, ctx):
    if(ctx.author.voice is None): #if author is not in channel
      await ctx.send("Please enter a voice channel before using bot")
      return
    await ctx.voice_client.move_to(ctx.author.voice.channel)

  @commands.command(pass_context=True)
  async def queue(self, ctx, youtube_url):
    if(not youtube_url.startswith('https://www.youtube.com/watch?v=')):
      await ctx.send("Link not supported, please use a youtube link")
    
    await self.queue.addSong(youtube_url)

  @commands.command(pass_context=True)
  async def showQueue(self, ctx):
    if(len(self.queue.urls) == 0):
      await ctx.send("No music is queued")
      return
    str = ""
    queueNames = list(self.queue.urls.keys())
    for i in range(len(queueNames)):
      str += f"{i+1}. {queueNames[i]}\n"

    await ctx.send(str)

  @commands.command(pass_context=True)
  async def remove(self, ctx, number):
    if(not number.isdigit()):
      await ctx.send("Please enter the index of the song you want to remove")

    actualIndex = int(number)-1

    if(actualIndex >= len(self.queue.urls) or actualIndex < 0):
      await ctx.send("There is not that much songs queued")

    await self.queue.remove(actualIndex)

  @commands.command(pass_context=True)
  async def clearQueue(self, ctx):
    await self.queue.clearQueue

  @commands.command(pass_context=True)
  async def musichelp(self, ctx):
    str = \
    """
**!play <youtube link>**
> Play song from youtube link
**!pause**
> Pause playback of current song
**!resume**
> Resume playback of current song
**!move**
> To move the bot to another channel without changing song
**!disconnect**
> Disconnect bot from channel
    """
    await ctx.send(str)