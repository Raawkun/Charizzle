import sqlite3
import disnake
from disnake.ext import commands
import asyncio
import re
import main
import json
from sqlite3 import connect
from main import client

# Zeichen zum Kopieren: [ ] { }

class Listener(commands.Cog):

    with open("config.json", "r") as config_file:
        config = json.load(config_file)


    def __init__(self, client):
        self.client = client
        self.db = connect("pokemon.db")

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
        
            
        #Open to every Channel!

        if message.content == "^-^":
            await message.channel.send("https://media.tenor.com/LC5ripTgbHkAAAAC/kyogre-kyogresmile.gif")

        if message.content.lower() == "stfu":
            database = self.db.execute(f'SELECT Stfu FROM Admin')
            database.fetchall()
            for row in database:
                if row[0] == 1:
                    await message.channel.send("No u.")

        elif message.content.lower() == "lol":
            database = self.db.execute(f'SELECT Lol FROM Admin')
            database.fetchall()
            for row in database:
                if row[0] == 1:
                    await message.channel.send("Rofl.")

        elif re.search(r'\bsquirtle\b', message.content, re.IGNORECASE):
            database = self.db.execute(f'SELECT Starter FROM Toggle WHERE User_ID = {message.author.id}')
            database.fetchall()
            for row in database:
                if row[0] == 1:
                    emoji = '👎'
                    emoji2 = self.client.get_emoji(1083883409404854322)
                    await message.add_reaction(emoji)
                    await message.add_reaction(emoji2)
            #        await message.channel.send("Worst starter fr.")

        elif re.search(r'\bcharmander\b', message.content, re.IGNORECASE):
            database = self.db.execute(f'SELECT Repel FROM Toggle WHERE User_ID = {sender.author.id}')
            database.fetchall()
            for row in database:
                if row[0] == 1:
                    emoji = '👍'
                    emoji2 = self.client.get_emoji(1083883459883315200)
                    await message.add_reaction(emoji)
                    await message.add_reaction(emoji2)
            #        await message.channel.send("Wow! What a great Pokémon starter!")

        if "boost has expired" in message.content:
            referenced_message = await message.channel.fetch_message(message.reference.message_id)
            interaction_message = await message.channel.fetch_message(message.interaction.message_id)
            if referenced_message:
                                # Print the user ID of the message that received the response
                sender = referenced_message.author.id
                if "repel" in message.content:
                    database = self.db.execute(f'SELECT Repel FROM Toggle WHERE User_ID = {sender.author.id}')
                    database.fetchall()
                    for row in database:
                        if row[0] == 1:
                            await message.channel.send("<@"+str(sender)+"> Hey, your <:repel:1164286208822738967> boost expired!")
                if "goldenrazz" in message.content:
                    database = self.db.execute(f'SELECT Grazz FROM Toggle WHERE User_ID = {sender.author.id}')
                    database.fetchall()
                    for row in database:
                        if row[0] == 1:
                            await message.channel.send("<@"+str(sender)+"> Hey, your <:grazz:1164341690442727464> boost expired!")
            elif interaction_message:
                sender = interaction_message.author.id
                if "repel" in message.content:
                    database = self.db.execute(f'SELECT Repel FROM Toggle WHERE User_ID = {sender.author.id}')
                    database.fetchall()
                    for row in database:
                        if row[0] == 1:
                            await message.channel.send("<@"+str(sender)+"> Hey, your <:repel:1164286208822738967> boost expired!")
                if "goldenrazz" in message.content:
                    database = self.db.execute(f'SELECT Grazz FROM Toggle WHERE User_ID = {sender.author.id}')
                    database.fetchall()
                    for row in database:
                        if row[0] == 1:
                            await message.channel.send("<@"+str(sender)+"> Hey, your <:grazz:1164341690442727464> boost expired!")

            #Rare Spawn Listener
            receiver_channel = 825958388349272106 #bot-testing channel
            if "found a wild" in message.content:
                announce_channel = self.client.get_channel(receiver_channel)
                if (len(message.embeds) > 0):
                    _embed = message.embed[0]
                    #Check if reaction or interaction
                    referenced_message = await message.channel.fetch_message(message.reference.message_id)
                    interaction_message = await message.channel.fetch_message(message.interaction.message_id)
                    if referenced_message:
                        sender = referenced_message.author.id
                        database = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID={sender.author.id}')
                        database.fetchall()
                        if not database:
                            self.db.execute(f'INSERT INTO Toggle (USER_ID, Username) VALUES ({sender.author.id}, "{sender.author.name}")')
                            self.db.commit()
                            await message.channel.send(f"Is this your first visit here? Welcome! I've added you to my database. Check '''<toggle''' for more info.")
                    if interaction_message:
                        sender = interaction_message.author.id
                        database = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID={sender.author.id}')
                        database.fetchall()
                        if not database:
                            self.db.execute(f'INSERT INTO Toggle (USER_ID, Username) VALUES ({sender.author.id}, "{sender.author.name}")')
                            self.db.commit()
                            await message.channel.send(f"Is this your first visit here? Welcome! I've added you to my database. Check '''<toggle''' for more info.")





        # Only wotks in specific channels!
        # channel_ids = [825817765432131615, 825813023716540429, 890255606219431946, 1161018942555422792, 827510854467584002]
        # if message.channel.id in channel_ids:
            
            #if message.content.lower() == "no":
                #await message.channel.send("Yes.")
            #elif message.content.lower() == "yes":
                #await message.channel.send("No.")

            # if message.author.id == parser.get('client_id'):
            #     if int(parser.get('attempts')) >= 1:
            #         parser['attempts'] -= 1
            #         clowning = message.content
            #         await message.send(clowning)
                
            
            # elif parser['annoy'] == 1:
            #     if message.author.id == parser.get('client_id'):
            #         copymessage = message.content
            #         await message.send(copymessage)


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
                    if message.content != None:
                        await message.channel.send("Test: "+message.content)
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
                    

                    if _embed.image.url:
                        if "xyani" in _embed.image.url:
                            await message.channel.send("Regular")
                        elif "shiny" in _embed.image.url:
                            await message.channel.send("Shiny")
                        elif "golden" in _embed.image.url:
                            await message.channel.send("Golden")
                        else: return
                        name = _embed.image.url.split("/")[5]
                        real_name = name.split(".")[0]
                        await message.channel.send(real_name)
                    else: return

                if "personal contributions" in _embed.description:
                    if message.channel.id in bot_wl:
                        ann_msg = _embed.description.split("`")[3]
                        print(ann_msg)
                    else: return
                else: return

                if re.search(r'\bpersonal contribution\b', _embed.description, re.IGNORECASE):
                    if message.channel.id in bot_wl:
                        ann_msg = _embed.description.split("`")[3]
                        print(ann_msg)
                    
                for embed in message.embeds:
                    if 'personal contribution' in embed.description.lower():
                        await message.channel.send('Found "personal contribution" in an embed description.')


        if message.channel.id == 825822261625880576:
            if (len(message.embeds)) > 0:
                _embed = message.embeds[0]
                if "Lottery" in _embed.author:
                    lot_dict = _embed.to_dict()
                    print(lot_dict)
                    announce_channel.id = 1163534668281421915
                    lot_embed = disnake.Embed.from_dict(lot_dict)
                    await announce_channel.send(embed=lot_dict)
                if "Tower" in _embed.author:
                    tower_dict = _embed.to_dict()
                    print(tower_dict)
                    announce_channel.id = 1163534668281421915
                    lot_embed = disnake.Embed.from_dict(lot_dict)
                    await announce_channel.send(embed=lot_dict)
        elif "<lot" in message.content:
            if lot_dict:
                lot_embed = disnake.Embed.from_dict(lot_dict)
                await message.channel.send(embed=lot_embed)
            else: return
        elif "<tower" in message.content:
            if tower_dict:
                tower_embed = disnake.Embed.from_dict(tower_dict)
                await message.channels.end(embed=tower_embed)
            else: return
                        

        def insert_data(field_name, field_value):
            conn = sqlite3.connect('pokemon.db')
            cursor = conn.cursor()

            cursor.execute('INSERT INTO embed_data (FieldName, FieldValue) VALUES (?, ?)', (field_name, field_value))
            conn.commit()
            conn.close()


            if (len(message.embeds) > 0):
                _embed = message.embeds[0]
                if _embed.fields != None:
                    for field in _embed.fields:
                        field_name = field.name
                        field_value = field.value
                        insert_data(field_name, field_value)
                            
            

        
# Zeichen zum Kopieren: [ ] { }

    # @commands.Cog.listener()
    # async def on_message_edit(before, after, lol):
    #     if before.author == client.user:
    #         return
    #     if before.author.id == 664508672713424926:
    #         if "score of" in after.content:
    #     # Send a message if the edited content contains the word "lantern"
    #             await after.channel.send(f"Message edited by {before.author.name} contains 'lantern': {after.content}")


def setup(client):
    client.add_cog(Listener(client))