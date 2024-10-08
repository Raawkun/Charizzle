import asyncio
import datetime
import disnake
from disnake.ext import commands
import sqlite3
from sqlite3 import connect
from cogs.module import Modules
from  utility.rarity_db import poke_rarity, embed_color
from utility.embed import Custom_embed
from utility.drop_chance import drop_pos, rare_calc, ball_used_low, ball_used_high
import random
from utility.all_checks import Basic_checker

class On_Edit(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")

    current_time = datetime.datetime.utcnow()
    timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):

        # 825950637958234133
        receiver_channel = self.db.execute(f'SELECT * FROM Admin WHERE Server_ID = {before.guild.id}')
        receiver_channel = receiver_channel.fetchone()
        #print(receiver_channel)
        receiver_channel = int(receiver_channel[4])
        current_time = datetime.datetime.utcnow()
        timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
        if receiver_channel > 0:
            announce = self.client.get_channel(int(receiver_channel))
        log = self.client.get_channel(1210143608355823647)
        
        if before.author.id == 664508672713424926:  #Meow
            if before.pinned != after.pinned:
                print(f"{before.author.display_name} pinned a message.")
            if before.pinned == after.pinned:
                ##### Rare Spawn #####
                Rare_Spawns = ["Event", "Legendary", "Shiny","Golden"]
                #Rare_Spawns = ["Event", "Legendary", "Shiny", "Rare", "SuperRare","Golden"]
                if (len(before.embeds) > 0):
                    befembed = before.embeds[0]
                    guild = before.guild
                    if befembed.description:
                        if "captcha" in befembed.description:
                            #print("Captcha, rude")
                            return
                        else:
                            _embed = after.embeds[0]
                            color = _embed.color
                            try:
                                data = self.db.execute(f'SELECT * FROM Dex WHERE Img_url = "{_embed.image.url}"')
                                data = data.fetchone()
                            except:
                                await before.channel.send("It seems this Pokémon is not in my database - could you please add it with checking its ``/pokedex entry``?")
                            if before.reference:
                                ref_msg = await before.channel.fetch_message(before.reference.message_id)
                                sender = ref_msg.author
                            elif before.interaction:
                                ref_msg = before.interaction.user
                                sender = ref_msg
                            
                            
                            if _embed.description:
                                if _embed.footer.text:
                                    #print("No pins")
                                    #print("Oh, a footer!")
                                    if "fished out a" in _embed.description:
                                        if data[11] == 1:
                                            await before.channel.send("Watch out! This one is a <:shin:1165314036909494344> Pokémon!")
                                        elif data[12]:
                                            await before.channel.send("Watch out! This one is a <:gold:1165319370801692786> Pokémon!")
                                    if "token" in _embed.footer.text:
                                        #print("Token")
                                        if "caught a" in _embed.description:
                                            raremon = data[14]
                                            ball = _embed.description.split(" with a")[1]
                                            ball = ball.split("!")[0]
                                            ball = ball.split(" ")[1]
                                            #print("Fish caught")
                                            if raremon in Rare_Spawns or _embed.color == 0xe9270b:
                                                if receiver_channel > 0:
                                                    raremon = poke_rarity[(data[14])]
                                                    description_text = f"Original message: [Click here]({before.jump_url})\n"
                                                    embed = disnake.Embed(title=raremon+" **"+data[1]+"** \nDex: #"+str(data[0]), color=color,description=description_text)
                                                    embed.set_author(name=(sender.display_name+" just caught a:"), icon_url=_embed.author.icon_url)
                                                    embed.set_image(_embed.image.url)
                                                    embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                                                    anno = await announce.send(embed=embed)
                                                    emoji = '🔔'
                                                    await after.add_reaction(emoji)
                                            dataev = self.db.execute(f'SELECT * FROM Admin WHERE Server_ID = {guild.id}')
                                            dataev = dataev.fetchall()
                                            if dataev[0][4] == 1:
                                                dataev = self.db.execute(f'SELECT * FROM Events WHERE User_ID = {sender.id}')
                                                dataev = dataev.fetchall()
                                                if dataev:
                                                    used = dataev[0][3]
                                                    
                                                    #print(used)
                                                    #print(rare_calc[raremon])
                                                    if raremon in ["Common", "Uncommon", "Rare"]:
                                                        points = ((used * (random.uniform(0.5,1.2)))* (rare_calc[raremon]*random.uniform(0.85,1.15)) * (ball_used_low[ball]*random.random()))*(1000+(used*6))
                                                    else:
                                                        points = ((used * (random.uniform(0.5,1.2)))* (rare_calc[raremon]*random.uniform(0.85,1.15)) * (ball_used_high[ball]*random.random()))*(1000+(used*6))
                                                    #print(points)
                                                    points = round(points)
                                                    await before.channel.send("Your catch earned a score of **"f'{int(points):,}'"** points!")
                                                    if points > dataev[0][2]:
                                                        self.db.execute(f'UPDATE Events SET Points = {points} WHERE User_ID = {sender.id}')
                                                        self.db.commit()
                                                    item_count = dataev[0][3]
                                                    #print(item_count)
                                                    fish_odds = (1/drop_pos["fish"])
                                                    #print(fish_odds)
                                                    odds = 0
                                                    #if coin_type == "hunt":
                                                    odds = fish_odds

                                                    roll = random.random()

                                                    if odds > roll:
                                                        #print("Find coins")
                                                        await before.channel.send("You've found a <:lavacookie:1167592527570935922>! Feed it to me with ``feed``.")
                                                        data = self.db.execute(f'SELECT * FROM Events WHERE User_ID = {sender.id}')
                                                        data = data.fetchone()
                                                        old_amount = data[4]
                                                        new_amount = 1+old_amount
                                                        self.db.execute(f'UPDATE Events SET Items = {new_amount} WHERE User_ID = {sender.id}')
                                                        self.db.commit()
                                            
                                        if "broke out" in _embed.description:
                                            raremon = data[14]
                                            ball = _embed.description.split(" out of the")[1]
                                            ball = ball.split("!")[0]
                                            ball = ball.split(" ")[1]
                                            if raremon in Rare_Spawns or _embed.color == 0xe9270b:
                                                if receiver_channel > 0:
                                                    raremon = poke_rarity[(data[14])]
                                                    description_text = f"Original message: [Click here]({before.jump_url})\n"
                                                    embed = disnake.Embed(title=raremon+" **"+data[1]+"** \nDex: #"+str(data[0]), color=color,description=description_text)
                                                    embed.set_author(name=(sender.display_name+" almost caught a:"), icon_url=_embed.author.icon_url)
                                                    embed.set_image(_embed.image.url)
                                                    embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                                                    anno = await announce.send(embed=embed)
                                                    emoji = '🔔'
                                                    await after.add_reaction(emoji)
                                        if "ran away" in _embed.description:
                                            raremon = data[14]
                                            if raremon in Rare_Spawns or _embed.color == 0xe9270b:
                                                if receiver_channel > 0:
                                                    raremon = poke_rarity[(data[14])]
                                                    description_text = f"Original message: [Click here]({before.jump_url})\n"
                                                    embed = disnake.Embed(title=raremon+" **"+data[1]+"** \nDex: #"+str(data[0]), color=color,description=description_text)
                                                    embed.set_author(name=(sender.display_name+" was too slow for:"), icon_url=_embed.author.icon_url)
                                                    embed.set_image(_embed.image.url)
                                                    embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                                                    anno = await announce.send(embed=embed)
                                                    emoji = '🔔'
                                                    await after.add_reaction(emoji)
                                    else:
                                        #print("No token")
                                        if "caught a" in _embed.description:
                                            monname = _embed.description.split("**")[1]
                                            data = self.db.execute(f'SELECT * FROM Dex WHERE Name = "{monname}"')
                                            data = data.fetchone()
                                            #print(monname)
                                            #print(data)
                                            raremon = data[14]
                                            ball = _embed.description.split(" with a")[1]
                                            ball = ball.split("!")[0]
                                            ball = ball.split(" ")[1]
                                            #print("Caught a mon")
                                            color = str(_embed.color)
                                            asyncio.create_task(Modules.averagecoins(self, after))
                                            description_text = " "
                                            if "retrieved a" in _embed.description:
                                                #Rare_Spawns = ["Event", "Legendary", "Shiny", "Rare","Common", "Uncommon", "SuperRare","Golden"]
                                                item = _embed.description.split("retrieved")[1]
                                                item = item.split("**")[1]
                                                #print(item)
                                                description_text = f"<:held_item:1213754494266122280> **It held onto a {item}**.\n"
                                            if raremon in Rare_Spawns or color == '#ea260b':
                                                if receiver_channel > 0:
                                                    raremon = poke_rarity[(data[14])]
                                                    description_text += f"Original message: [Click here]({before.jump_url})\n"
                                                    embed = disnake.Embed(title=raremon+" **"+data[1]+"** \nDex: #"+str(data[0]), color=_embed.color,description=description_text)
                                                    embed.set_author(name=(f'{sender.display_name}'+" just caught a:"), icon_url=_embed.author.icon_url)
                                                    embed.set_image(_embed.image.url)
                                                    embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                                                    anno = await announce.send(embed=embed)
                                                    emoji = '🔔'
                                                    await after.add_reaction(emoji)
                                            dataev = self.db.execute(f'SELECT * FROM Admin WHERE Server_ID = {guild.id}')
                                            dataev = dataev.fetchall()
                                            if dataev[0][4] == 1:
                                                dataev = self.db.execute(f'SELECT * FROM Events WHERE User_ID = {sender.id}')
                                                dataev = dataev.fetchall()
                                                if dataev:
                                                    raremon = data[0][14]
                                                    used = dataev[0][3]
                                                    ball = _embed.description.split(" with a")[1]
                                                    ball = ball.split("!")[0]
                                                    ball = ball.split(" ")[1]
                                                    #print(used)
                                                    print(f'{raremon}'", "f'{rare_calc[raremon]}')
                                                    #print(rare_calc[raremon])
                                                    if raremon in ["Common", "Uncommon", "Rare"]:
                                                        points = ((used * (random.uniform(0.5,1.2)))* (rare_calc[raremon]*random.uniform(0.85,1.15)) * (ball_used_low[ball]*random.random()))*(1000+(used*6))
                                                    else:
                                                        points = ((used * (random.uniform(0.5,1.2)))* (rare_calc[raremon]*random.uniform(0.85,1.15)) * (ball_used_high[ball]*random.random()))*(1000+(used*6))
                                                        #print(points)
                                                    points = round(points)
                                                    await before.channel.send("Your catch earned a score of **"f'{int(points):,}'"** points!")
                                                    if points > dataev[0][2]:
                                                        self.db.execute(f'UPDATE Events SET Points = {points} WHERE User_ID = {sender.id}')
                                                        self.db.commit()


                                                    item_count = dataev[0][3]
                                                    #print(item_count)
                                                    hunt_odds = ((1/drop_pos["hunt"]))
                                                    #print(hunt_odds)
                                                    odds = 0
                                                    #if coin_type == "hunt":
                                                    odds = hunt_odds

                                                    roll = random.random()
                                                    #print(roll)
                                                    if odds > roll:
                                                        #print("Find coins")
                                                        await before.channel.send("You've found a <:lavacookie:1167592527570935922>! Feed it to me with ``feed``.")
                                                        data = self.db.execute(f'SELECT * FROM Events WHERE User_ID = {sender.id}')
                                                        data = data.fetchall()
                                                        old_amount = data[0][4]
                                                        new_amount = 1+old_amount
                                                        self.db.execute(f'UPDATE Events SET Items = {new_amount} WHERE User_ID = {sender.id}')
                                                        self.db.commit()
                                        if "broke out" in _embed.description:
                                            try:
                                                raremon = data[14]
                                            except Exception as e:
                                                #await log.send(embed=_embed)
                                                #await log.send(f"Error: {e}, {data}, {before.jump_url}")
                                                monname = _embed.description.split("**")[1]
                                                data = self.db.execute(f'SELECT * FROM Dex WHERE Name = "{monname}"')
                                                data = data.fetchone()
                                                #print(data[1])
                                                raremon = data[14]
                                            ball = _embed.description.split(" out of the")[1]
                                            ball = ball.split("!")[0]
                                            ball = ball.split(" ")[1]
                                            color = str(_embed.color)
                                            if raremon in Rare_Spawns or color == '#ea260b':
                                                if receiver_channel > 0:
                                                    raremon = poke_rarity[(data[14])]
                                                    description_text = f"Original message: [Click here]({before.jump_url})\n"
                                                    embed = disnake.Embed(title=raremon+" **"+data[1]+"** \nDex: #"+str(data[0]), color=_embed.color,description=description_text)
                                                    embed.set_author(name=(f'{sender.display_name}'+" almost caught a:"), icon_url=_embed.author.icon_url)
                                                    embed.set_image(_embed.image.url)
                                                    embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                                                    anno = await announce.send(embed=embed)
                                                    emoji = '🔔'
                                                    await after.add_reaction(emoji)
                                        if "ran away" in _embed.description:
                                            raremon = data[14]
                                            color = str(_embed.color)
                                            if raremon in Rare_Spawns or color == '#ea260b':
                                                if receiver_channel > 0:
                                                    raremon = poke_rarity[(data[14])]
                                                    description_text = f"Original message: [Click here]({before.jump_url})\n"
                                                    embed = disnake.Embed(title=raremon+" **"+data[1]+"** \nDex: #"+str(data[0]), color=_embed.color,description=description_text)
                                                    embed.set_author(name=(sender.display_name+" was too slow for:"), icon_url=_embed.author.icon_url)
                                                    embed.set_image(_embed.image.url)
                                                    embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                                                    anno = await announce.send(embed=embed)
                                                    emoji = '🔔'
                                                    await after.add_reaction(emoji)

            if ":map: Map:" in before.content:
                if "Steps today:" in after.content:
                    #print("Someone is stepping.")
                    if "found a " in before.content:
                        if before.reference:
                            ref_msg = await before.channel.fetch_message(before.reference.message_id)
                            sender = ref_msg.author
                        else:
                            sender = "A User"
                        #print("Theres a pokemon")
                        monrare = before.content.split("found a ")[1]
                        monname = monrare.split("**")[1]
                        monnumber = monrare.split(":")[3]
                        monrare = monrare.split(":")[1]
                        print(f'{monnumber}'", "f'{monrare}'", "f'{monname}')
                        #Rare_Spawns = ["Event", "Legendary", "Shiny", "Rare", "SuperRare","Golden","Uncommon"]
                        if monrare in Rare_Spawns:
                            monnumber = int(monnumber)
                            if monrare == "Shiny":
                                monnumber += 1000
                            if monrare == "Golden":
                                monnumber += 9000
                            monnumber = str(monnumber)
                            data = self.db.execute(f'SELECT * FROM Dex WHERE DexID = {monnumber}')
                            data = data.fetchone()
                            if "just caught a " in after.content:
                                if receiver_channel > 0:
                                    raremon = poke_rarity[(data[14])]
                                    description_text = f"Original message: [Click here]({before.jump_url})\n"
                                    embed = disnake.Embed(title=raremon+" **"+data[1]+"** \nDex: #"+str(data[0]), color=embed_color[monrare],description=description_text)
                                    embed.set_author(name=(f'{sender}'+" just discovered a:"), icon_url="https://cdn.discordapp.com/emojis/1072075141489623040.webp?size=96&quality=lossless")
                                    embed.set_image(data[15])
                                    embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                                    anno = await announce.send(embed=embed)
                                    
                                print("Explore: Caught it!")
                            elif "broke out" in after.content:
                                if receiver_channel > 0:
                                    raremon = poke_rarity[(data[14])]
                                    description_text = f"Original message: [Click here]({before.jump_url})\n"
                                    embed = disnake.Embed(title=raremon+" **"+data[1]+"** \nDex: #"+str(data[0]), color=embed_color[monrare],description=description_text)
                                    embed.set_author(name=(f'{sender}'+" almost caught a:"), icon_url="https://cdn.discordapp.com/emojis/1072075141489623040.webp?size=96&quality=lossless")
                                    embed.set_image(data[15])
                                    embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                                    anno = await announce.send(embed=embed)
                                    
                                print("Explore: Broke out")
                            elif "ran away" in after.content:
                                if receiver_channel > 0:
                                    raremon = poke_rarity[(data[14])]
                                    description_text = f"Original message: [Click here]({before.jump_url})\n"
                                    embed = disnake.Embed(title=raremon+" **"+data[1]+"** \nDex: #"+str(data[0]), color=embed_color[monrare],description=description_text)
                                    embed.set_author(name=(sender+" was too slow for:"), icon_url="https://cdn.discordapp.com/emojis/1072075141489623040.webp?size=96&quality=lossless")
                                    embed.set_image(data[15])
                                    embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                                    anno = await announce.send(embed=embed)
                                    
                                print("Explore: Ran away")

        if before.author.id == 865576698137673739: ## Psycord
            #if before.pinned == after.pinned:
            if len(after.embeds) > 0:
                print("An embed?")
                log = self.client.get_channel(1221565506902032444)
                emb = after.embeds[0]
                await log.send(f"Original message: [Click here]({after.jump_url})\n",embed=emb)
                if emb.title != None:
                    #await log.send(f"Original message: [Click here]({after.jump_url})\n",embed=emb)
                    if "a wild " in emb.title.lower():
                        if "caught" in emb.title.lower():
                            exit
                        for reaction in emb.reactions:
                            if reaction.me:
                                exit
                            else:
                                emoji = '🔔'
                                await after.add_reaction(emoji)
                                print("wild spawn")
                                await log.send(f"<@352224989367369729> Original message: [Click here]({after.jump_url})\n",embed=emb)
                                await after.channel.send(f"A wild Pokémon spawned! <@&1217752336508784681>")
            if (len(before.embeds) > 0):
                _embed = before.embeds[0]
                if _embed.title:
                    if "paralympics | members" in _embed.title.lower():
                        print("Members table")
                        counter = self.db.execute(f'SELECT * FROM Admin WHERE Server_ID = 825813023716540426')
                        counter = counter.fetchone()
                        counter = int(counter[9])
                        if int(round(datetime.datetime.timestamp(datetime.datetime.utcnow()))+3600)>(counter+608400):
                            #print(_embed.description)
                            desc = _embed.description.split("Total TBs")[1]
                            desc = desc.split("\n")
                            #print(desc)
                            for entry in desc:
                                #print(f"Entry: {entry}")
                                try:
                                    name = entry.split("|")[0]
                                    #print(name)
                                    if "🦁" in name:
                                        name = name.split("🦁")[1]
                                    elif "🐻" in name:
                                        name = name.split("🐻")[1]
                                    elif "🦊" in name:
                                        name = name.split("🦊")[1]
                                    elif "🐰" in name:
                                        name = name.split("🐰")[1]
                                    name = name.replace(" ", "")
                                    #print(f"Name: {name}")
                                    try:
                                        old = self.db.execute(f'SELECT * FROM PsycordTeam WHERE User = "{name}"')
                                        old = old.fetchone()
                                        #print(old)
                                        oldpoint = int(old[1])
                                        average = int(old[3])
                                        count = int(old[4])+1
                                    except:
                                        oldpoint = 0
                                        average = 0
                                        count = 1
                                    points = int((entry.split("|")[1].replace(",", "")).replace(" ", ""))
                                    print(f'{name}, {points}')
                                    if average != 0:
                                        newavg = (average*count-1)+points
                                        average = newavg / (count+1)
                                    elif average == 0 and count > 1:
                                        newavg = oldpoint+points
                                        average = int(round(newavg / 2))
                                    self.db.execute(f'INSERT or REPLACE INTO PsycordTeam VALUES ("{name}", {points}, {oldpoint}, {average}, {count})')
                                    self.db.commit()
                                    self.db.execute(f'UPDATE Admin SET TeamUpdate = {counter+608400}')
                                    self.db.commit()
                                    print(f"Next Update will be at {counter+608400}")
                                except Exception as e:
                                    print(e)


def setup(client):
    client.add_cog(On_Edit(client))