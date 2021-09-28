
import os
from discord.ext import commands
from MusicCog import MusicCog

client = commands.Bot(command_prefix=".")
bot_token = os.environ['TOKEN']

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

cogs = [MusicCog]

for i in range(len(cogs)):
  cogs[i].setup(client)

client.run(bot_token)
