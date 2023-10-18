import sqlite3
import disnake
from disnake.ext import commands
import asyncio
import re
import main
import json
from sqlite3 import connect

# Zeichen zum Kopieren: [ ] { }

class Listener(commands.Cog):

    with open("config.json", "r") as config_file:
        config = json.load(config_file)


    def __init__(self, client):
        self.client = client
        self.db = connect("pokemon.db")
        self.db_lot = connect("event.db")

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
        
        channel_ids = [1163743648744226886, 827510854467584002] #test-spawns
        receiver_channel = 825958388349272106 #bot-testing channel
        meowbot = 664508672713424926 #id from PokeMeow
        if message.channel.id in channel_ids:
            print("Message received")
            if message.author.id == meowbot:
                announce_channel = self.client.get_channel(receiver_channel)
                #Legendary Embed HEX #a007f8 160, 7, 248
                #Shiny Embed HEX #fe98cb 254, 152, 203
                #Event Excl HEX #e9270b 233, 39, 11
                #SR HEX #f8f407
                #R HEX  #fb8908
                #UC HEX #13b4e7
                #C HEX  #0855fb
                embedc = ["#0855fb","13b4e7","fb8908","f8f407","#a007f8", "#fe98cb" , "#e9270b"]

                if "found a wild" in message.content:
                    await message.channel.send("Thats a spawn")
                    if (len(message.embeds) > 0):
                        _embed = message.embeds[0]
                        color = _embed.color
                        value = color.value
                        rgb = color.to_rgb
                        await message.channel.send(value)
                        #await message.channel.send(rgb)
                        await message.channel.send(str(color))
                        if str(color) in embedc:
                            author_name = _embed.author.name
                            author_icurl = _embed.author.icon_url
                            thumb = _embed.image.url
                            desc = _embed.description
                            await message.channel.send("I see you...")
                            embedded=disnake.Embed(
                                title="Much wow", color=color,description=desc,
                            )
                            embedded.set_author(
                                name=author_name, icon_url=author_icurl
                            )
                            embedded.set_image(url=thumb)
                            await announce_channel.send(embed=embedded)
                            await announce_channel.send("This will be an embed in the future")
                        
                    else: await message.channel.send("Wrong color")
                        
                if (len(message.embeds) > 0):
                    _embed = message.embeds[0]
                    if _embed.author != None:
                        await message.channel.send("Author:")
                        await message.channel.send(f"```{_embed.author}```")
                    if _embed.description != None:
                        await message.channel.send("Description:")
                        await message.channel.send(f"```{_embed.description}```")
                    if _embed.fields != None:
                        await message.channel.send("Fields:")
                        await message.channel.send(f"```{_embed.fields}```")
                    if _embed.footer != None:
                        await message.channel.send("Footer:")
                        await message.channel.send(f"```{_embed.footer}```")
                    if _embed.image != None:
                        await message.channel.send("Image:")
                        await message.channel.send(f"```{_embed.image.url}```")
                        await message.channel.send(f"```{_embed.image.proxy_url}```")
                    if _embed.thumbnail != None:
                        await message.channel.send("Thumnbail:")
                        await message.channel.send(f"```{_embed.thumbnail}```")
                    for field in _embed.fields:
                        if field.name == "Base Attack":
                            b_atk = field.value.split()[1]
                            await message.channel.send(b_atk)
                        if field.name == "Base Defense":
                            b_def = field.value.split()[1]
                            await message.channel.send(b_def)
                        if field.name == "Base HP":
                            b_hp = field.value.split()[1]
                            await message.channel.send(b_hp)
                        if field.name == "Base Sp. Atk":
                            b_spatk = field.value.split()[1]
                            await message.channel.send(b_spatk)
                        if field.name == "Base Sp. Def":
                            b_spdef = field.value.split()[1]
                            await message.channel.send(b_spdef)
                        if field.name == "Base Speed":
                            b_spd = field.value.split()[1]
                            await message.channel.send(b_spd)
                    

                if (len(message.embeds) > 0):
                    _embed = message.embeds[0]
                    if _embed.fields != None:
                        for field in _embed.fields:
                            field_name = field.name
                            field_value = field.value
                            insert_data(field_name, field_value)
                            
                if channel.id == 825822261625880576:
                    if (len(message.embeds) > 0:
                        _embed = message.embeds[0]
                        if "PokeLottery" in _embed.author:
                            author = _embed.author
                            title = _embed.title
                            desc = _embed.description
                            file = _embed.files
                            footer = _embed.footer
                            color = _embed.color
                            self.db_lot.execute(f```
                            INSERT INTO Events(
                            author_lot, title_lot, desc_lot, footer_lot, color_lot
                            ) VALUES (
                            author, title, desc, file, footer, color
                            )
                            self.db_lot.commit
                        if "Tower Result" in _embed.author:
                            author = _embed.author
                            title = _embed.title
                            desc = _embed.description
                            file = _embed.files
                            footer = _embed.footer
                            color = _embed.color
                            self.db_lot.execute(f```
                            INSERT INTO Events(
                            author_BT, title_BT, desc_BT, footer_BT, color_BT
                            ) VALUES (
                            author, title, desc, file, footer, color
                            )
                            self.db_lot.commit
                            



        def insert_data(field_name, field_value):
            conn = sqlite3.connect('pokemon.db')
            cursor = conn.cursor()

            cursor.execute('INSERT INTO embed_data (FieldName, FieldValue) VALUES (?, ?)', (field_name, field_value))
            conn.commit()
            conn.close()




        
# Zeichen zum Kopieren: [ ] { }

def setup(client):
    client.add_cog(Listener(client))