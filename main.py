import asyncio
import os

import disnake
from disnake.ext import commands
from dotenv import dotenv_values

config = dotenv_values(".env")
token = config["YOUR_BOT_TOKEN"]

intents = disnake.Intents.all()

def __init__(self, client):
    self.client = client

client = commands.AutoShardedBot(intents = intents, command_prefix = ["<"], reload = True, sync_commands_debug=True)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.loop.run_until_complete(client.start(token))