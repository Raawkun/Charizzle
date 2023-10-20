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
        bot_wl = 664508672713424926     #Meow ID
        celadon = 1080049677518508032


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
        
        #if message.content.lower() == "<toggle":
            #user_id = message.author.id
            #database = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {user_id}')
            #database = database.fetchall()
            #author_url = "https://cdn.discordapp.com/emojis/1153729922620215349.webp?size=96&quality=lossless"
            #author_name = "Mega-Gengar Service Alpha"
            #gengar_bot = self.client.get_user(1161011648585285652)
            #footer_icon = gengar_bot.display_avatar.url
            #footer_name = "Mega Gengar"
            #emo_yes = ":white_check_mark:"
            #emo_no = ":x:"
            #color = 0x807ba6
            #if database:
                #if database[0][2] == 1:
                    #value_grazz = emo_yes
                #else: 
                    #value_grazz = emo_no
                #if database[0][3] == 1:
                    #value_repel = emo_yes
                #else:
                    #value_repel = emo_no
                #if database[0][4] == 1:
                    #value_start = emo_yes
                #else: 
                    #value_start = emo_no
                #if database[0][5] == 1:
                    #value_priv = emo_yes
                #else:
                    #value_priv = emo_no
                #embed = disnake.Embed(
                    #title="**Settings**", color=color, description="Here you can see your current toggle settings. \nChangeable via ``/toggle`` \n\nThe current settings are:"
                #)
                #embed.set_author(icon_url=author_url,name=author_name)
                #embed.set_footer(icon_url=footer_icon,text=footer_name)
                #embed.add_field(name="Golden Razz Berry: ",inline=True, value=value_grazz)
                #embed.add_field(name="Repel: ",inline=True, value=value_repel)
                #embed.add_field(name="Starter: ",inline=True, value=value_start)
                #embed.add_field(name="Privacy: ",inline=True, value=value_priv)
                #embed.set_thumbnail(footer_icon)
                #await message.channel.send(embed=embed)


        if message.content.lower() == "lol":
            database = self.db.execute(f'SELECT Lol FROM Admin')
            database.fetchall()
            print(database)
            if database:
                if database[0][3] == 1:
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

        if message.author.id == bot_wl:
            
        
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
                            if "repel" in message.content:
                                await message.channel.send("<@"+str(sender)+"> Hey, your <:repel:1164286208822738967> boost expired!")
                        else: return
                        if database[0][2] == 1:
                            #print("grazz activated"+str(database[0][2]))
                            if "goldenrazz" in message.content:
                                await message.channel.send("<@"+str(sender)+"> Hey, your <:grazz:1164341690442727464> boost expired!")
                        else: return
                

            #Rare Spawn Listener
        receiver_channel = 825958388349272106 #bot-testing channel
        log_channel = 1164544776985653319
        if "found a wild" in message.content:
            announce_channel = self.client.get_channel(receiver_channel)
            log_channel = self.client.get_channel(log_channel)
            if (len(message.embeds) > 0):
                __embed = message.embeds[0]
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
                database = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID={sender.id}')
                database = database.fetchall()
                if not database:
                    self.db.execute(f'INSERT INTO Toggle (USER_ID) VALUES ({sender.id})')
                    self.db.commit()
                    await log_channel.send(str(sender)+" is now in the database. "+str(sender.id))
                    await message.channel.send(f"Is this your first visit here? Welcome! I've added you to my database. Check ```/toggle``` for more info.")
                


        if message.author.id == bot_wl:
            if (len(message.embeds) > 0):
                _embed=message.embeds[0]
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
                self.db.execute(f'INSERT or REPLACE INTO Dex VALUES ({dex},{name},{type1_semi},{type2_semi},{b_hp},{b_atk},{b_def},{b_spatk},{b_spdef},{b_spd},{legendary},{shiny},{golden},{mega},{rarity},{imageurl})')
                self.db.commit()
        # Only wotks in specific channels!
        # channel_ids = [825817765432131615, 825813023716540429, 890255606219431946, 1161018942555422792, 827510854467584002]
        # if message.channel.id in channel_ids:
        
        channel_ids = [1163743648744226886, 827510854467584002] #test-spawns
        receiver_channel = 825958388349272106 #bot-testing channel
        if message.channel.id in channel_ids:
            print("Message received")
            if message.author.id == bot_wl:
                announce_channel = self.client.get_channel(receiver_channel)
                #Legendary Embed HEX #a007f8 160, 7, 248
                #Shiny Embed HEX #fe98cb 254, 152, 203
                #Event Excl HEX #e9270b 233, 39, 11
                #SR HEX #f8f407
                #R HEX  #fb8908
                #UC HEX #13b4e7
                #C HEX  #0855fb
                embedc = ["#0855fb","#13b4e7","#fb8908","#f8f407","#a007f8", "#fe98cb" , "#e9270b"]
                if "found a wild" in message.content:
                    await message.channel.send("Thats a spawn")
                    if (len(message.embeds) > 0):
                        _embed = message.embeds[0]
                        color = _embed.color
                        # value = color.value
                        # await message.channel.send(value)
                        # await message.channel.send(color)
                        # await message.channel.send(str(color))

                        if str(color) in embedc:
                            author_icurl = _embed.author.icon_url
                            thumb = _embed.image.url
                            await message.channel.send("I see you...")
                            embedded=disnake.Embed(
                                title=(
                                    
                                ), color=color,description=(
                                    
                                ),
                            )
                            embedded.set_author(
                                name=(str(sender.display_name)+" just found a cool Pokémon!"), icon_url=author_icurl
                            )
                            embedded.set_image(url=thumb)
                            await announce_channel.send(embed=embedded)
                            await announce_channel.send("This will be an embed in the future")
                        
                    else: await message.channel.send("Wrong color")
                        
                if (len(message.embeds) > 0):
                    _embed = message.embeds[0]
                    if message.content != None:
                        await message.channel.send("Text: "+message.content)
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