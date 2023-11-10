import datetime
import disnake
from disnake.ext import commands
import sqlite3
from sqlite3 import connect
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

        
        receiver_channel = 825950637958234133
        current_time = datetime.datetime.utcnow()
        timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
        announce = self.client.get_channel(receiver_channel)
        if before.author.id == 664508672713424926:
            
            ##### Rare Spawn #####
            Rare_Spawns = ["Event", "Legendary", "Shiny","Golden"]
            #Rare_Spawns = ["Event", "Legendary", "Shiny", "Rare", "SuperRare","Golden"]
            if (len(before.embeds) > 0):
                befembed = before.embeds[0]
                if befembed.description:
                    if "captcha" in befembed.description:
                        print("Captcha, rude")
                        return
                    else:
                        try:
                            _embed = after.embeds[0]
                            color = _embed.color
                        except:
                            print("Message edited. No Embed")
                        try:
                            data = self.db.execute(f'SELECT * FROM Dex WHERE Img_url = "{_embed.image.url}"')
                            data = data.fetchall()
                        except:
                            print("Message edited. Theres no image or no embed.")
                        if before.reference:
                            ref_msg = await before.channel.fetch_message(before.reference.message_id)
                            sender = ref_msg.author
                        elif before.interaction:
                            ref_msg = before.interaction.user
                            sender = ref_msg
                        
                        
                        if _embed.description:
                            if _embed.footer.text:
                                #print("Oh, a footer!")
                                
                                if "token" in _embed.footer.text:
                                    #print("Token")
                                    if "caught a" in _embed.description:
                                        raremon = data[0][14]
                                        ball = _embed.description.split(" with a")[1]
                                        ball = ball.split("!")[0]
                                        ball = ball.split(" ")[1]
                                        #print("Fish caught")
                                        if raremon in Rare_Spawns or _embed.color == 0xe9270b:
                                            raremon = poke_rarity[(data[0][14])]
                                            description_text = f"Original message: [Click here]({before.jump_url})\n"
                                            embed = disnake.Embed(title=raremon+" **"+data[0][1]+"** \nDex: #"+str(data[0][0]), color=color,description=description_text)
                                            embed.set_author(name=(sender.display_name+" just caught a:"), icon_url=_embed.author.icon_url)
                                            embed.set_image(_embed.image.url)
                                            embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                                            await announce.send(embed=embed)
                                        dataev = self.db.execute(f'SELECT * FROM Admin')
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
                                                    data = data.fetchall()
                                                    old_amount = data[0][4]
                                                    new_amount = 1+old_amount
                                                    self.db.execute(f'UPDATE Events SET Items = {new_amount} WHERE User_ID = {sender.id}')
                                                    self.db.commit()
                                        
                                    if "broke out" in _embed.description:
                                        raremon = data[0][14]
                                        ball = _embed.description.split(" out of the")[1]
                                        ball = ball.split("!")[0]
                                        ball = ball.split(" ")[1]
                                        if raremon in Rare_Spawns or _embed.color == 0xe9270b:
                                            raremon = poke_rarity[(data[0][14])]
                                            description_text = f"Original message: [Click here]({before.jump_url})\n"
                                            embed = disnake.Embed(title=raremon+" **"+data[0][1]+"** \nDex: #"+str(data[0][0]), color=color,description=description_text)
                                            embed.set_author(name=(sender.display_name+" almost caught a:"), icon_url=_embed.author.icon_url)
                                            embed.set_image(_embed.image.url)
                                            embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                                            await announce.send(embed=embed)
                                    if "ran away" in _embed.description:
                                        raremon = data[0][14]
                                        total = "Total"
                                        self.db.execute(f'UPDATE Stats SET Fled = Fled + 1 WHERE Ball = ?',(total))
                                        self.db.commit()
                                        if raremon in Rare_Spawns or _embed.color == 0xe9270b:
                                            raremon = poke_rarity[(data[0][14])]
                                            description_text = f"Original message: [Click here]({before.jump_url})\n"
                                            embed = disnake.Embed(title=raremon+" **"+data[0][1]+"** \nDex: #"+str(data[0][0]), color=color,description=description_text)
                                            embed.set_author(name=(sender.display_name+" was too slow for:"), icon_url=_embed.author.icon_url)
                                            embed.set_image(_embed.image.url)
                                            embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                                            await announce.send(embed=embed)
                                else:
                                    #print("No token")
                                    if "caught a" in _embed.description:
                                        raremon = data[0][14]
                                        ball = _embed.description.split(" with a")[1]
                                        ball = ball.split("!")[0]
                                        ball = ball.split(" ")[1]
                                        #print("Caught a mon")
                                        if raremon in Rare_Spawns or _embed.color == 0xe9270b:
                                            raremon = poke_rarity[(data[0][14])]
                                            description_text = f"Original message: [Click here]({before.jump_url})\n"
                                            embed = disnake.Embed(title=raremon+" **"+data[0][1]+"** \nDex: #"+str(data[0][0]), color=color,description=description_text)
                                            embed.set_author(name=(f'{sender.display_name}'+" just caught a:"), icon_url=_embed.author.icon_url)
                                            embed.set_image(_embed.image.url)
                                            embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                                            await announce.send(embed=embed)
                                        dataev = self.db.execute(f'SELECT * FROM Admin')
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
                                        raremon = data[0][14]
                                        ball = _embed.description.split(" out of the")[1]
                                        ball = ball.split("!")[0]
                                        ball = ball.split(" ")[1]
                                        if raremon in Rare_Spawns or _embed.color == 0xe9270b:
                                            raremon = poke_rarity[(data[0][14])]
                                            description_text = f"Original message: [Click here]({before.jump_url})\n"
                                            embed = disnake.Embed(title=raremon+" **"+data[0][1]+"** \nDex: #"+str(data[0][0]), color=color,description=description_text)
                                            embed.set_author(name=(f'{sender.display_name}'+" almost caught a:"), icon_url=_embed.author.icon_url)
                                            embed.set_image(_embed.image.url)
                                            embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                                            await announce.send(embed=embed)
                                    if "ran away" in _embed.description:
                                        raremon = data[0][14]
                                        if raremon in Rare_Spawns or _embed.color == 0xe9270b:
                                            raremon = poke_rarity[(data[0][14])]
                                            description_text = f"Original message: [Click here]({before.jump_url})\n"
                                            embed = disnake.Embed(title=raremon+" **"+data[0][1]+"** \nDex: #"+str(data[0][0]), color=color,description=description_text)
                                            embed.set_author(name=(sender.display_name+" was too slow for:"), icon_url=_embed.author.icon_url)
                                            embed.set_image(_embed.image.url)
                                            embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                                            await announce.send(embed=embed)
                            channels = [1028441789448867880, 1079152774622744726]
                            if before.channel.id in channels:
                                if "clan member information" in befembed.description.lower():
                                    #print("Member Info")
                                    i = 1
                                    while i <= 15:
                                        for field in befembed.fields:
                                            if field.name == "User":
                                                userid = field.value.split("\n")[i-1]
                                                rang = userid.split(" <@")[0]
                                                rang = int(rang.replace("**",""))
                                                #print(rang)
                                                userid = userid.split(" ")[1]
                                                userid = userid.split("@")[1]
                                                userid = int(userid.split(">")[0])
                                                #print(userid)
                                                username = self.client.get_user(userid)
                                                #print(username)
                                            if field.name == "Contributions":
                                                catches = field.value.split("\n")[i-1]
                                                catches = catches.split(" ")[1]
                                                catches = catches.replace(",", "")
                                                catches = int(catches.replace("**", ""))
                                        old = 0
                                        datamem = self.db.execute(f'SELECT * FROM Leaderboard WHERE User_ID = {userid}')
                                        datamem = datamem.fetchall()
                                        count = 0
                                        if datamem:
                                            if catches == datamem[0][2]:
                                                count = datamem[0][4]+1
                                            if catches != datamem[0][2]:
                                                old = datamem[0][2]
                                        self.db.execute(f'INSERT or REPLACE INTO Leaderboard (User_ID, Username, ThisWeek, LastWeek, SameWeek) VALUES ({userid},"{username}", {catches}, {old}, {count})')
                                        self.db.commit()
                                        self.db.execute(f'INSERT or REPLACE INTO Memberlist (Rang ,User_ID) VALUES ({rang}, {userid})')
                                        self.db.commit()
                                        i+=1



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
                        monnumber = monrare.split(":")[3]
                        monrare = monrare.split(":")[1]
                        print(f'{monnumber}'", "f'{monrare}')
                        #Rare_Spawns = ["Event", "Legendary", "Shiny", "Rare", "SuperRare","Golden","Uncommon"]
                        if monrare in Rare_Spawns:
                            if monrare == "Shiny":
                                monnumber += 1000
                            if monrare == "Golden":
                                monnumber += 9000
                            data = self.db.execute(f'SELECT * FROM Dex WHERE DexID = {monnumber}')
                            data = data.fetchall()
                            if "just caught a " in after.content:
                                raremon = poke_rarity[(data[0][14])]
                                description_text = f"Original message: [Click here]({before.jump_url})\n"
                                embed = disnake.Embed(title=raremon+" **"+data[0][1]+"** \nDex: #"+str(data[0][0]), color=embed_color[monrare],description=description_text)
                                embed.set_author(name=(f'{sender}'+" just discovered a:"), icon_url="https://cdn.discordapp.com/emojis/1072075141489623040.webp?size=96&quality=lossless")
                                embed.set_image(data[0][15])
                                embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                                await announce.send(embed=embed)
                                print("Explore: Caught it!")
                            elif "broke out" in after.content:
                                raremon = poke_rarity[(data[0][14])]
                                description_text = f"Original message: [Click here]({before.jump_url})\n"
                                embed = disnake.Embed(title=raremon+" **"+data[0][1]+"** \nDex: #"+str(data[0][0]), color=embed_color[monrare],description=description_text)
                                embed.set_author(name=(f'{sender}'+" almost caught a:"), icon_url="https://cdn.discordapp.com/emojis/1072075141489623040.webp?size=96&quality=lossless")
                                embed.set_image(data[0][15])
                                embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                                await announce.send(embed=embed)
                                print("Explore: Broke out")
                            elif "ran away" in after.content:
                                raremon = poke_rarity[(data[0][14])]
                                description_text = f"Original message: [Click here]({before.jump_url})\n"
                                embed = disnake.Embed(title=raremon+" **"+data[0][1]+"** \nDex: #"+str(data[0][0]), color=embed_color[monrare],description=description_text)
                                embed.set_author(name=(sender+" was too slow for:"), icon_url="https://cdn.discordapp.com/emojis/1072075141489623040.webp?size=96&quality=lossless")
                                embed.set_image(data[0][15])
                                embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                                await announce.send(embed=embed)
                                print("Explore: Ran away")




def setup(client):
    client.add_cog(On_Edit(client))