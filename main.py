
import os
from discord.ext import commands
from MusicCog import MusicCog
from keep_alive import keep_alive

client = commands.Bot(command_prefix=".")


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

cogs = [MusicCog]

for i in range(len(cogs)):
  cogs[i].setup(client)

keep_alive()
bot_token = os.environ['TOKEN']
client.run(bot_token)
