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
from utility.id_lists import safari_id
from cogs.safari_event import SafariEvent
import random
from utility.all_checks import Basic_checker
from cogs.listener import Listener

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
                return
            if before.pinned == after.pinned:
                ##### Rare Spawn #####
                Rare_Spawns = ["Event", "Legendary", "Shiny","Golden"]
                #Rare_Spawns = ["Event", "Legendary", "Shiny", "Rare", "SuperRare","Golden"]
                if (len(before.embeds) > 0):
                    #print("Edit with Embed")
                    befembed = before.embeds[0]
                    if "may continue playing" in after.content.lower():
                        emoji = "<:GengarClap:1338134716397916233>"
                        await after.add_reaction(emoji)
                        return
                    if (len(after.embeds) > 0):
                        _embed = after.embeds[0]
                        color = _embed.color
                        #print("After embed")
                    else:
                        return
                    if _embed.description:
                        if "fished out a" in _embed.description:
                            #print("Fishyyyy")
                            try:
                                data = self.db.execute(f'SELECT * FROM Dex WHERE Img_url = "{_embed.image.url}"')
                                data = data.fetchone()
                            except:
                                try:
                                    name = _embed.description.split("**")[3]
                                    data = self.db.execute(f'SELECT * FROM Dex WHERE Name = "{name}"')
                                    data = data.fetchone()
                                except:
                                    await before.channel.send("It seems this Pokémon is not in my database - could you please add it with checking its ``/pokedex entry``?")
                                    return
                            if data[11] == 1:
                                await before.channel.send("Watch out! This one is a <:shin:1165314036909494344> Pokémon!")
                            elif data[12]:
                                await before.channel.send("Watch out! This one is a <:gold:1165319370801692786> Pokémon!")
                    if _embed.footer.text:
                        if "pokemon roll" in _embed.footer.text.lower():
                            #print("There's been a roll")
                            try:
                                data = self.db.execute(f'SELECT * FROM Dex WHERE Img_url = "{_embed.image.url}"')
                                data = data.fetchone()
                                raremon = data[14]
                                #print(f"{data[1]} - {data[14]}")
                            except:
                                try:
                                    name = _embed.description.split("**")[1]
                                    data = self.db.execute(f'SELECT * FROM Dex WHERE Name = "{name}"')
                                    data = data.fetchone()
                                    raremon = data[14]
                                except:
                                    await before.channel.send("It seems this Pokémon is not in my database - could you please add it with checking its ``/pokedex entry``?")
                                    return
                            if before.reference:
                                ref_msg = await before.channel.fetch_message(before.reference.message_id)
                                sender = ref_msg.author
                            elif before.interaction:
                                ref_msg = before.interaction.user
                                sender = ref_msg
                            if raremon in Rare_Spawns or data[0] in Listener.exclusives:
                                #print("Theres a rare spawn.")
                                description_text = " "
                                if "caught a" in _embed.description:
                                    #print(f"Something got caught; {data[1]}")
                                    if "retrieved a" in _embed.description:
                                        #Rare_Spawns = ["Event", "Legendary", "Shiny", "Rare","Common", "Uncommon", "SuperRare","Golden"]
                                        item = _embed.description.split("retrieved")[1]
                                        item = item.split("**")[1]
                                        #print(item)
                                        description_text = f"<:held_item:1213754494266122280> **It held onto a {item}**.\n"
                                    if "token" in _embed.footer.text:
                                        author = sender.display_name+" just reeled in a:"
                                    else:
                                        author = sender.display_name+" just caught a:"

                                if "broke out" in _embed.description:
                                    #print(f"Something broke out; {data[1]}")
                                    author = sender.display_name+" almost caught a:"
                                    
                                                    
                                if "ran away" in _embed.description:
                                    #print(f"Something ran away; {data[1]}")
                                    author = sender.display_name+" was too slow for:"
                                raremon = poke_rarity[(data[14])]
                                description_text += f"Original message: [Click here]({before.jump_url})\n"
                                embed = disnake.Embed(title=raremon+" **"+data[1]+"** \nDex: #"+str(data[0]), color=color,description=description_text)
                                embed.set_author(name=author, icon_url=_embed.author.icon_url)
                                embed.set_image(_embed.image.url)
                                embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                                await announce.send(embed=embed)
                                emoji = '🔔'
                                await after.add_reaction(emoji)
                                return

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



def setup(client):
    client.add_cog(On_Edit(client))