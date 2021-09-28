import discord
import nacl
import os
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from discord.ext import commands

voice = None

client = commands.Bot(command_prefix="!")
bot_token = os.environ['TOKEN']

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.command(pass_context=True)
async def play_youtube(ctx, youtube_url):
  print("Play youtube command received")

  YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
  FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

  channel = ctx.message.author.voice.channel
  if(youtube_url.startswith('https://www.youtube.com/watch?v=')):
    global voice
    voice = await channel.connect()
    if not voice.is_playing():
      with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        URL = info['formats'][0]['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
    else:
        await ctx.send("Already playing song")
        return
  else:
    return 'URL_ERROR'

@client.command(pass_context=True)
async def disconnect(ctx):
  if ctx.author.voice is None:
    await ctx.send("Im not in a channel ")
  else:
    await ctx.voice_client.disconnect()

client.run(bot_token)