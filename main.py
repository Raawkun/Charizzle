import asyncio
import os
import disnake
from disnake.ext import commands
from disnake.ext.commands import CommandNotFound


f = open("key.txt", "r")
token = f.read()

intents = disnake.Intents.all()

def __init__(self, client):
    self.client = client

client = commands.AutoShardedBot(intents = intents, command_prefix =commands.when_mentioned_or("m", "M"), reload = True, sync_commands_debug=True)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


client.loop.run_until_complete(client.start(token))