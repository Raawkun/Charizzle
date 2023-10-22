import sqlite3
import disnake
from disnake.ext import commands
import asyncio
import re
import main
import json
from sqlite3 import connect
from main import client
from utility.rarity_db import poke_rarity
from utility.egglist import eggexcl
import datetime

# Zeichen zum Kopieren: [ ] { }

class Listener(commands.Cog):


    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")

    
    #events
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'We have logged in {self.client.user}! ID: {self.client.user.id}')
        print("------")
        print("Time do to ghost stuff!")
        await self.client.change_presence(activity=disnake.Activity(type=disnake.ActivityType.playing, name="with your feelings."))

    @commands.Cog.listener()
    async def on_message(self, message):
        # This function will be called whenever a message is sent in a server where the bot is a member.
        # You can add your custom logic here.
        if message.author == self.client.user:
            return  # Ignore messages sent by the bot itself.
        meow = 664508672713424926     #Meow ID
        celadon = 1080049677518508032
        
        current_time = datetime.datetime.utcnow()
        timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')


        if message.author.bot and message.author.id != meow:
            return
        
        #Open to every Channel!
        if message.content == "^-^":
            await message.channel.send("https://media.tenor.com/LC5ripTgbHkAAAAC/kyogre-kyogresmile.gif")

        if message.content.lower() == "stfu":
            database = self.db.execute(f'SELECT Stfu FROM Admin')
            database=database.fetchall()
            for row in database:
                if row[0] == 1:
                    await message.channel.send("No u.")


        if message.content.lower() == "lol":
            database = self.db.execute(f'SELECT Lol FROM Admin')
            database=database.fetchall()
            if database:
                if database[0][0] == 1:
                    await message.channel.send("Rofl.")
                else: return

        database = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {message.author.id}')
        database = database.fetchall()
        if database:
            if database[0][4] == 1:
                emoji = False
                emoji2 = False
                # print("Starter is toggled on")
                if re.search(r'\bsquirtle\b', message.content, re.IGNORECASE):
                    emoji = '👎'
                    emoji2 = self.client.get_emoji(1083883409404854322)
                if re.search(r'\bcharmander\b', message.content, re.IGNORECASE):
                    emoji = '👍'
                    emoji2 = self.client.get_emoji(1083883459883315200)
                if emoji and emoji2:
                    await message.add_reaction(emoji)
                    await message.add_reaction(emoji2)

        if message.author.id == meow:
            
        
            if "found a wild" in message.content:
                try:
                    referenced_message = await message.channel.fetch_message(message.reference.message_id)
                except:
                    return
                else: 
                    referenced_message = await message.channel.fetch_message(message.reference.message_id)
                #print(referenced_message)
                if referenced_message:
                    sender = referenced_message.author.id
                    # print(sender)
                    database = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {sender}')
                    database = database.fetchall()
                    #print(database)
                    if database:
                        if database[0][3] == 1:
                            #print("repel activated"+str(database[0][3]))
                            if "super_repel" in message.content and "boost" in message.content:
                                await message.channel.send("<@"+str(sender)+"> Hey, your <:superrepel:1165230878474113025> boost expired!")
                            if "max_repel" in message.content and "boost" in message.content:
                                await message.channel.send("<@"+str(sender)+"> Hey, your <:maxrepel:1165230966164434974> boost expired!")
                            if ":repel" in message.content and "boost" in message.content:
                                await message.channel.send("<@"+str(sender)+"> Hey, your <:repel:1164286208822738967> boost expired!")
                        else: return
                        if database[0][2] == 1:
                            #print("grazz activated"+str(database[0][2]))
                            if "goldenrazz" in message.content and "boost" in message.content:
                                await message.channel.send("<@"+str(sender)+"> Hey, your <:grazz:1164341690442727464> boost expired!")
                            if "honey" in message.content and "boost" in message.content:
                                await message.channel.send("<@"+str(sender)+"> Hey, your <:honey:1165231049287155793> boost expired!")
                        else: return
                

            #Rare Spawn Listener
        receiver_channel = 825958388349272106 #bot-testing channel
        log_channel = 1164544776985653319
        if message.author.id == meow:
            if (len(message.embeds) > 0):
                _embed = message.embeds[0]
                color = _embed.color
                print(_embed.author.name)
                announce_channel = self.client.get_channel(receiver_channel)
                
                Rare_Spawned = ["Event", "Legendary", "Shiny"]
                if message.reference:
                    ref_msg = await message.channel.fetch_message(message.reference.message_id)
                
                if "found a wild" in message.content:
                    log_channel = self.client.get_channel(log_channel)
                    if (len(message.embeds) > 0):
                        #Check if reaction or interaction
                        try:
                            interaction_message = await message.channel.fetch_message(message.interaction.message_id)
                            # print(interaction_message)
                        except:
                            referenced_message = await message.channel.fetch_message(message.reference.message_id)
                        else: interaction_message = await message.channel.fetch_message(message.interaction.message_id)
                            #print(referenced_message)
                        if referenced_message:
                            sender = referenced_message.author
                            #print(sender)
                        elif interaction_message:
                            sender = interaction_message.author
                            #print(sender)
                        ## Checking for a User in Database, if not, initializing
                        database = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID={sender.id}')
                        database = database.fetchall()
                        if not database:
                            self.db.execute(f'INSERT INTO Toggle (USER_ID) VALUES ({sender.id})')
                            self.db.commit()
                            await log_channel.send(str(sender)+" is now in the database. "+str(sender.id))
                            await message.channel.send(f"Is this your first visit here? Welcome! I've added you to my database. Check ```<toggle``` for more info.")

                ######## Repel/Grazz notifier 
                        databaserep = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {sender.id}')
                        databaserep = databaserep.fetchall()
                        #print(database)
                        if databaserep:
                            if databaserep[0][3] == 1:
                                #print("repel activated"+str(database[0][3]))
                                if "super_repel" in message.content and "boost" in message.content:
                                    await message.channel.send("<@"+str(sender)+"> Hey, your <:superrepel:1165230878474113025> boost expired!")
                                if "max_repel" in message.content and "boost" in message.content:
                                    await message.channel.send("<@"+str(sender)+"> Hey, your <:maxrepel:1165230966164434974> boost expired!")
                                if ":repel" in message.content and "boost" in message.content:
                                    await message.channel.send("<@"+str(sender)+"> Hey, your <:repel:1164286208822738967> boost expired!")
                            else: return
                            if databaserep[0][2] == 1:
                                #print("grazz activated"+str(database[0][2]))
                                if "goldenrazz" in message.content and "boost" in message.content:
                                    await message.channel.send("<@"+str(sender)+"> Hey, your <:grazz:1164341690442727464> boost expired!")
                                if "honey" in message.content and "boost" in message.content:
                                    await message.channel.send("<@"+str(sender)+"> Hey, your <:honey:1165231049287155793> boost expired!")
                            else: return

                ######## Start here for Spawn Listener
                        databasesp = self.db.execute(f'SELECT * FROM Dex WHERE Img_url = "{_embed.image.url}"')
                        databasesp = databasesp.fetchall()
                    
                        sender = ref_msg.author.display_name
                        author_icurl = _embed.author.icon_url
                        raremon = poke_rarity[(databasesp[0][14])]
                        description_text = f"Original message: [Click here]({ref_msg.jump_url})\n"
                        if databasesp[0][14] in Rare_Spawned or _embed.color == 0xe9270b:
                            embed = disnake.Embed(title=raremon+" **"+databasesp[0][1]+"** \nDex: #"+str(databasesp[0][0]), color=color,description=description_text)
                            embed.set_author(name=(sender+" just spawned a:"), icon_url=author_icurl)
                            embed.set_image(_embed.image.url)
                            embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                            await announce_channel.send(embed=embed)
                if _embed.author.name:
                    if "hatched" in _embed.author.name:
                        data_egg = self.db.execute(f'SELECT * FROM Dex WHERE Img_url = "{_embed.image.url}"')
                        data_egg = data_egg.fetchall()
                        sender = ref_msg.author.display_name
                        author_icurl = _embed.author.icon_url
                        raremon = poke_rarity[(data_egg[0][14])]
                        description_text = f"Original message: [Click here]({ref_msg.jump_url})\n"
                        #Rare_Spawned = ["Event", "Legendary", "Shiny", "Rare", "SuperRare"]

                        if data_egg[0][14] in Rare_Spawned or str(data_egg[0][0]) in eggexcl:
                            print("Its in the one list!")
                            print(str(data_egg[0][0]))
                            embed = disnake.Embed(title=raremon+" **"+data_egg[0][1]+"** \nDex: #"+str(data_egg[0][0]), color=color,description=description_text)
                            embed.set_author(name=(sender+" just hatched an exclusive:"),icon_url="https://cdn.discordapp.com/emojis/689325070015135745.gif?size=96&quality=lossless")
                            embed.set_image(_embed.image.url)
                            embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                            await announce_channel.send(embed=embed)
                    if "opened a " in _embed.author.name:
                        if _embed.image:
                            data_box = self.db.execute(f'SELECT * FROM Dex WHERE Img_url = "{_embed.image.url}"')
                            data_box = data_box.fetchall()
                            sender = ref_msg.author.display_name
                            author_icurl = _embed.author.icon_url
                            raremon = poke_rarity[(data_box[0][14])]
                            description_text = f"Original message: [Click here]({ref_msg.jump_url})\n"
                            if data_box[0][14] in Rare_Spawned:
                                embed = disnake.Embed(title=raremon+" **"+data_box[0][1]+"** \nDex: #"+str(data_box[0][0]), color=color,description=description_text)
                                embed.set_author(name=(sender+" just unboxed an exclusive:"),icon_url="https://cdn.discordapp.com/emojis/784865588207157259.gif?size=96&quality=lossless")
                                embed.set_image(_embed.image.url)
                                embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                                await announce_channel.send(embed=embed)
                    if "PokeMeow Swaps" in _embed.author.name:
                        data_sw = self.db.execute(f'SELECT * FROM Dex WHERE Img_url = "{_embed.image.url}"')
                        data_sw = data_sw.fetchall()
                        sender = ref_msg.author.display_name
                        author_icurl = _embed.author.icon_url
                        raremon = poke_rarity[(data_sw[0][14])]
                        #Rare_Spawned = ["Event", "Shiny", "Legendary", "SuperRare", "Rare", "Uncommon", "Common"]
                        description_text = f"Original message: [Click here]({ref_msg.jump_url})\n"
                        if data_sw[0][14] in Rare_Spawned:
                            embed = disnake.Embed(title=raremon+" **"+data_sw[0][1]+"** \nDex: #"+str(data_sw[0][0]), color=color,description=description_text)
                            embed.set_author(name=(sender+" just swapped for a:"),icon_url="https://cdn.discordapp.com/emojis/869901886080315392.webp?size=96&quality=lossless")
                            embed.set_image(_embed.image.url)
                            embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                            await announce_channel.send(embed=embed)
                if _embed.description:
                    if "returned with" in _embed.description:
                        # await message.channel.send(_embed.description)
                        description_text = f"Original message: [Click here]({ref_msg.jump_url})\n"
                        sender = ref_msg.author.display_name
                        author_icurl = _embed.author.icon_url
                        # if "SuperRare" in _embed.description:
                        #     legy_mon = _embed.description.split(":SuperRare:")[1]
                        #     legy_numb = legy_mon.split(":")[1]
                        #     data_cb = self.db.execute(f'SELECT * FROM Dex WHERE DexID = "{legy_numb}"')
                        #     data_cb = data_cb.fetchall()
                        #     raremon = poke_rarity[(data_cb[0][14])]
                        #     embed = disnake.Embed(title=raremon+" **"+data_cb[0][1]+"** \nDex: #"+str(data_cb[0][0]), color=color,description=description_text)
                        #     embed.set_author(name=(sender+"'s catchbot brought a:"),icon_url="https://cdn.discordapp.com/emojis/869901886080315392.webp?size=96&quality=lossless")
                        #     embed.set_image(data_cb[0][15])
                        #     embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                        #     await announce_channel.send(embed=embed)
                        if "Legendary" in _embed.description:
                            sender = ref_msg.author.display_name
                            author_icurl = _embed.author.icon_url
                            legy_mon = _embed.description.split(":Legendary:")[1]
                            legy_numb = legy_mon.split(":")[1]
                            data_cb = self.db.execute(f'SELECT * FROM Dex WHERE DexID = "{legy_numb}"')
                            data_cb = data_cb.fetchall()
                            raremon = poke_rarity[(data_cb[0][14])]
                            embed = disnake.Embed(title=raremon+" **"+data_cb[0][1]+"** \nDex: #"+str(data_cb[0][0]), color=color,description=description_text)
                            embed.set_author(name=(sender+"'s catchbot brought a:"),icon_url="https://cdn.discordapp.com/emojis/717198164280606802.gif?size=96&quality=lossless")
                            embed.set_image(data_cb[0][15])
                            embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                            await announce_channel.send(embed=embed)
                        if "Shiny" in _embed.description:
                            sender = ref_msg.author.display_name
                            author_icurl = _embed.author.icon_url
                            shiny_mon = _embed.description.split(":Shiny:")[1]
                            shiny_numb = shiny_mon.split(":")[1]
                            data_cb = self.db.execute(f'SELECT * FROM Dex WHERE DexID = "{shiny_numb}"')
                            data_cb = data_cb.fetchall()
                            real_mon = "Shiny "+data_cb[0][1]
                            data_cb = self.db.execute(f'SELECT * FROM Dex WHERE Name = "{real_mon}"')
                            data_cb = data_cb.fetchall()
                            raremon = poke_rarity[(data_cb[0][14])]
                            embed = disnake.Embed(title=raremon+" **"+data_cb[0][1]+"** \nDex: #"+str(data_cb[0][0]), color=color,description=description_text)
                            embed.set_author(name=(sender+"'s catchbot brought a:"),icon_url="https://cdn.discordapp.com/emojis/717198164280606802.gif?size=96&quality=lossless")
                            embed.set_image(data_cb[0][15])
                            embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                            await announce_channel.send(embed=embed)
                        if "Golden" in _embed.description:
                            sender = ref_msg.author.display_name
                            author_icurl = _embed.author.icon_url
                            gold_mon = _embed.description.split(":Golden:")[1]
                            gold_numb = gold_mon.split(":")[1]
                            data_cb = self.db.execute(f'SELECT * FROM Dex WHERE DexID = "{gold_numb}"')
                            data_cb = data_cb.fetchall()
                            real_mon = "Golden "+data_cb[0][1]
                            data_cb = self.db.execute(f'SELECT * FROM Dex WHERE Name = "{real_mon}"')
                            data_cb = data_cb.fetchall()
                            raremon = poke_rarity[(data_cb[0][14])]
                            embed = disnake.Embed(title=raremon+" **"+data_cb[0][1]+"** \nDex: #"+str(data_cb[0][0]), color=color,description=description_text)
                            embed.set_author(name=(sender+"'s catchbot brought a:"),icon_url="https://cdn.discordapp.com/emojis/717198164280606802.gif?size=96&quality=lossless")
                            embed.set_image(data_cb[0][15])
                            embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                            await announce_channel.send(embed=embed)















        log_channel = 1164544776985653319
        if message.author.id == meow:
            if (len(message.embeds) > 0):
                _embed=message.embeds[0]
                try:
                    if "version" in _embed.description:
                        dex=_embed.author.name.split("#")[1]
                        #print(dex)
                        name=_embed.author.name.split("#")[0]
                        #print(name)
                        for field in _embed.fields:
                            if field.name == "Type":
                                type1= field.value.split()[0]
                                #print(type1)
                                type1_semi = type1.split(":")[1]
                                #print(type1_semi)
                                try:
                                    type2 = field.value.split()[1]
                                    #print(type2)
                                    type2_semi = type2.split(":")[1]
                                    #print(type2_semi)
                                except: type2_semi = None
                            if field.name == "Base Attack":
                                b_atk = field.value.split()[1]
                                #print(b_atk)
                            if field.name == "Base Defense":
                                b_def = field.value.split()[1]
                                #print(b_def)
                            if field.name == "Base HP":
                                b_hp = field.value.split()[1]
                                #print(b_hp)
                            if field.name == "Base Sp. Atk":
                                b_spatk = field.value.split()[1]
                                #print(b_spatk)
                            if field.name == "Base Sp. Def":
                                b_spdef = field.value.split()[1]
                                #print(b_spdef)
                            if field.name == "Base Speed":
                                b_spd = field.value.split()[1]
                                #print(b_spd)
                            if field.name == "Rarity":
                                rarity = field.value.split(":")[1]
                                #print(rarity)
                                if rarity.lower() == "legendary":
                                    legendary = True
                                else: legendary = False
                                if rarity.lower() == "shiny":
                                    shiny = True
                                else: shiny = False
                                if rarity.lower() == "golden":
                                    golden = True
                                else: golden = False
                                if rarity.lower() == "mega":
                                    mega = True
                                else: mega = False
                                if rarity.lower() == "shinymega":
                                    shiny = True
                                    mega = True
                            imageurl = _embed.image.url
                                #print(imageurl)
                        self.db.execute(f'INSERT or REPLACE INTO Dex VALUES ({dex},"{name}","{type1_semi}","{type2_semi}",{b_hp},{b_atk},{b_def},{b_spatk},{b_spdef},{b_spd},{legendary},{shiny},{golden},{mega},"{rarity}","{imageurl}")')
                        self.db.commit()
                except: return
        # Only wotks in specific channels!
        # channel_ids = [825817765432131615, 825813023716540429, 890255606219431946, 1161018942555422792, 827510854467584002]
        # if message.channel.id in channel_ids:
        
                

                    
                    

#------------------------------------- Testing area---------------------------------------------------------------------------------------------#


#1037323228961579049
        channel_ids = [1083131761451606096, 827510854467584002] #test-spawns
        receiver_channel = 825958388349272106 #bot-testing channel
        if message.channel.id in channel_ids:
            await message.channel.send("Message received: "+message.author.display_name)
            await message.channel.send(message.content)
            if message.author.id == meow:
                announce_channel = self.client.get_channel(receiver_channel)
                if (len(message.embeds) > 0):
                    _embed = message.embeds[0]
                    if message.content != None:
                        await message.channel.send("Text: "+message.content)
                    if _embed.author != None:
                        await message.channel.send("Author:")
                        await message.channel.send(f"```{_embed.author}```")
                    if _embed.title != None:
                        await message.channel.send("Title:")
                        await message.channel.send(f"```{_embed.title}```")
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