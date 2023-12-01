import asyncio
import os
import disnake
from disnake.ext import commands


f = open("key.txt", "r")
token = f.read()

intents = disnake.Intents.all()

def __init__(self, client):
    self.client = client
    
command_sync_flags = commands.CommandSyncFlags.from_string('all')
client = commands.AutoShardedBot(intents = intents, command_prefix =commands.when_mentioned_or("m","M"), reload = True, command_sync_flags=command_sync_flags)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


client.loop.run_until_complete(client.start(token))