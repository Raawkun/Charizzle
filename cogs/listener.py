import disnake
from disnake.ext import commands
import asyncio
import re
import main
import json

# Zeichen zum Kopieren: [ ] { }

class Listener(commands.Cog):

    with open("config.json", "r") as config_file:
        config = json.load(config_file)


    def __init__(self, client):
        self.client = client

    #events
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'We have logged in {self.client.user}! ID: {self.client.user.id}')
        print("------")
        print("Checking for config.json")
        if __file__.startswith("config") == False:
            config_info = { 
                "squirtle" : 1,
                "charmander" : 1,
                "lol" : 1,
                "annoy" : 0,
                "client_id" : 0,
                "attempts" : 0
            }
            myJSON = json.dumps(config_info)
            with open("config.json", "w") as jsonfile:
                jsonfile.write(myJSON)
                print("Config written successful")
        else: print("Config already there")
        
        await self.client.change_presence(activity=disnake.Activity(type=disnake.ActivityType.playing, name="with your feelings."))

    @commands.Cog.listener()
    async def on_message(self, message):
        # This function will be called whenever a message is sent in a server where the bot is a member.
        # You can add your custom logic here.
        if message.author == self.client.user:
            return  # Ignore messages sent by the bot itself.
        bot_wl = 664508672713424926
        #Meow ID
        if message.author.bot and message.author.id != bot_wl:
            return
        
        with open("config.json", "r") as config_file:
            parser = json.load(config_file)
            
        # Example: Respond to a specific message content
        channel_ids = [825817765432131615, 825813023716540429, 890255606219431946, 1161018942555422792, 827510854467584002]
        if message.channel.id in channel_ids:
            
            #if message.content.lower() == "no":
                #await message.channel.send("Yes.")
            #elif message.content.lower() == "yes":
                #await message.channel.send("No.")

            if message.author.id == parser.get('client_id'):
                if int(parser.get('attempts')) >= 1:
                    parser['attempts'] -= 1
                    clowning = message.content
                    await message.send(clowning)
                

            if message.content.lower() == "stfu":
                await message.channel.send("No u.")

            elif message.content.lower() == "lol":
                if parser['lol'] == 1:
                    await message.channel.send("Rofl.")
        
            elif re.search(r'\bsquirtle\b', message.content, re.IGNORECASE):

                if parser['squirtle'] == 1:
                    emoji = '👎'
                    emoji2 = self.client.get_emoji(1083883409404854322)
                    await message.add_reaction(emoji)
                    await message.add_reaction(emoji2)
                    await message.channel.send("Worst starter fr.")

            elif re.search(r'\bcharmander\b', message.content, re.IGNORECASE):
                if parser['charmander'] == 1:
                    emoji = '👍'
                    emoji2 = self.client.get_emoji(1083883459883315200)
                    await message.add_reaction(emoji)
                    await message.add_reaction(emoji2)
                    await message.channel.send("Wow! What a great Pokémon starter!")

            elif parser['annoy'] == 1:
                if message.author.id == parser.get('client_id'):
                    copymessage = message.content
                    await message.send(copymessage)


        channel_ids = [1079815106277425243]
        if message.channel.id in channel_ids:
                message_id = message.message_id
                channel_id = message.channel_id

                if message.emoji.name == "🎨":
                    channel = await main.client.fetch_channel(channel_id)
                    message = await channel.fetch_message(message_id)

                    if message.embeds:
                        for embed in message.embeds:
                            color_hex = embed.color
                            await message.channel.send(f"The color is {color_hex}")
        
        channel_ids = [827510854467584002] #My personal channel
        receiver_channel = 825958388349272106 #bot-testing channel
        meowbot = 664508672713424926 #id from PokeMeow
        if message.channel.id in channel_ids:
            print("Message received")
            if message.author.id == meowbot:
                announce_channel = self.client.get_channel(receiver_channel)
                #Legendary Embed HEX #a007f8 160, 7, 248
                #Shiny Embed HEX #fe98cb 254, 152, 203
                #Event Excl HEX #e9270b 233, 39, 11
                embedc = ["a007f8", "fe98cb" , "e9270b"]

                if re.search(r'\bfound a wild\b', message.content, re.IGNORECASE):
                    await message.channel.send("Thats a spawn")
                    for embed in message.embeds:
                        print(embed.color.value)
                        print(embed.color.to_rgb)
                        _embed = message.embeds[0]
                        _color = _embed.color
                        print(str(_color))
                        if embed.color.value == embedc:
                            await message.channel.send("purple")
                        await announce_channel.send("We tried to grab the color")
                    else: await message.channel.send("Wrong color")
                        
                if re.search(r'\bhatched a\b', message.content, re.IGNORECASE):



        
# Zeichen zum Kopieren: [ ] { }

def setup(client):
    client.add_cog(Listener(client))