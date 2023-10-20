import asyncio
import os
import disnake
from disnake.ext import commands

# Zeichen zum Kopieren: [ ] { }


f = open("key.txt", "r")
token = f.read()

intents = disnake.Intents.all()

def __init__(self, client):
    self.client = client

prefixes = ["m", "<@1161011648585285652>"]
client = commands.AutoShardedBot(intents = intents, command_prefix = prefixes, reload = True, sync_commands_debug=True)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


client.loop.run_until_complete(client.start(token))