import disnake
from disnake.ext import commands
import asyncio
import re
import main
from configparser import SafeConfigParser

# Zeichen zum Kopieren: [ ] { }

class Listener(commands.Cog):

    parser = SafeConfigParser()
    parser.read('settings.ini')

    def __init__(self, client):
        self.client = client

    #events
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'We have logged in {self.client.user}! ID: {self.client.user.id}')
        print("------")
        await self.client.change_presence(activity=disnake.Activity(type=disnake.ActivityType.playing, name="with your feelings."))
        
    @commands.Cog.listener()
    async def on_message(self, message):
        # This function will be called whenever a message is sent in a server where the bot is a member.
        # You can add your custom logic here.
        if message.author == self.client.user:
            return  # Ignore messages sent by the bot itself.
        if message.author.bot:
            return
            
        # Example: Respond to a specific message content
        channel_ids = [825817765432131615, 825813023716540429, 890255606219431946, 1161018942555422792, 827510854467584002]
        if message.channel.id in channel_ids:
            parser = SafeConfigParser()
            parser.read('settings.ini')
            #if message.content.lower() == "no":
                #await message.channel.send("Yes.")
            #elif message.content.lower() == "yes":
                #await message.channel.send("No.")

            if message.content.lower() == "stfu":
                await message.channel.send("No u.")

            elif message.content.lower() == "lol":
                if parser.get('lol') == 1:
                    await message.channel.send("Rofl.")
        
            elif re.search(r'\bsquirtle\b', message.content, re.IGNORECASE):

                if parser.get('squirtle') == 1:
                    emoji = '👎'
                    emoji2 = self.client.get_emoji(1083883409404854322)
                    await message.add_reaction(emoji)
                    await message.add_reaction(emoji2)
                    await message.channel.send("Worst starter fr.")

            elif re.search(r'\bcharmander\b', message.content, re.IGNORECASE):
                if parser.get('charmander') == 1:
                    emoji = '👍'
                    emoji2 = self.client.get_emoji(1083883459883315200)
                    await message.add_reaction(emoji)
                    await message.add_reaction(emoji2)
                    await message.channel.send("Wow! What a great Pokémon starter!")

            elif parser.get('annoy') == 1:
                if message.author.id == parser.get('client_id'):
                    copymessage = message.content
                    await message.send(copymessage)


        channel_ids = [1079815106277425243]
        if message.channel.id in channel_ids:
            async def on_raw_reaction_add(payload):
                message_id = payload.message_id
                channel_id = payload.channel_id
                user_id = payload.user_id

                if payload.emoji.name == "🎨":
                    channel = await main.client.fetch_channel(channel_id)
                    message = await channel.fetch_message(message_id)

                    if message.embeds:
                        for embed in message.embeds:
                            color_hex = embed.color
                            await message.channel.send(f"The color is {color_hex}")

        

def setup(client):
    client.add_cog(Listener(client))