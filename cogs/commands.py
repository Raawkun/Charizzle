import math
import random
from typing import Any
import disnake
from disnake.ext import commands
import asyncio
from sqlite3 import connect
from disnake import Message, Option, OptionChoice, OptionType, ApplicationCommandInteraction
import json
import datetime
import time
from utility.all_checks import Basic_checker
from utility.embed import Custom_embed, Auction_embed
from utility.rarity_db import counts, countnumber, min_increase
from utility.rarity_db import poke_rarity, embed_color, chambers, thresholds
from utility.id_lists import unpinnables
from googlesearch import search
from PIL import Image, ImageDraw, ImageSequence
from io import BytesIO
import imageio
import aiohttp

# Zeichen zum Kopieren: [ ] { }

class Coms(commands.Cog):

#Database initialization, needed in every file with db
    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")



    current_time = datetime.datetime.utcnow()
    timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')

    async def errorlog(self, error, author, guild, channel):
        footer = f"{datetime.datetime.utcnow()}"
        desc = f"{guild.name}, <#{channel}>, <@{author.id}>"
        _emb = await Auction_embed(self.client,footer=footer, description=desc).setup_embed()
        _emb.add_field(name="Error:",value=error)
        errcha = self.client.get_channel(1210143608355823647)
        await errcha.send(embed=_emb)

    ############## Server configuration
    @commands.check(Basic_checker().check_admin)
    @commands.command()
    async def setup(self, ctx, defo:str = None, mode:str = None, *args):
        guild = ctx.guild
        print(args[0])
        channel = int(args[0])
        if defo == None:
            title = f"{self.client.user.display_name}'s Setup"
            desc = f"This command is to setup {self.client.user.display_name}'s various feeds or pings.\n"
            desc += f"The following can be set up in this server at the moment.\n\n**Functions:**\n"
            desc += f"> * __Changelog__: {self.client.user.display_name}'s updates.\n"
            desc += f"> * Usage: ``changelog [set/remove] [channel id]``\n"
            desc += f"> * __PokéMeow Rare Spawns__: A solid feed for Meow spawns.\n> * Usage: ``rarespawn [set/remove] [channel id]``\n"
            desc += f"> * __Psycord Outbreaks & Wild Spawns__: If you have the outbreak feed from Psycord set up in your server, you can get pings when a certain Pokémon has an outbreak and there can be pings whenever a wild Pokémon gets spawned due to server activity.\n"
            desc += f"> * Usage: ``outbreaks [add/remove] [channel id]`` for outbreak pings.\n> * Usage: ``outbreaks [role] [role id]``"
            desc += f"> * __Psycord Flex Channel__: Custom made starboard for Psycord. Usable with replying ``flex`` on a Psycord message.\n> * Usage: ``psyflex [set/remove] [channel id]``\n\n\n*Parameters in [] are mandatory.*"

            _emb = await Auction_embed(self.client,title=title, description=desc).setup_embed()

            await ctx.reply(embed = _emb)
        elif defo == "changelog":
            if mode == "add" or mode == "set":
                try:
                    log = self.client.get_channel(channel)
                    self.db.execute(f'UPDATE Admin SET Changelog = {args[0]} WHERE Server_ID = {guild.id}')
                    self.db.commit()
                    _emb = await Auction_embed(self.client, description=f"<@{ctx.author.id} has set up this channel to receive <@{self.client.user.id}>'s update logs.").setup_embed()
                    await log.send(embed=_emb)
                    await ctx.reply(f"Successfully set <#{args[0]}> as your changelog channel for me.")
                except Exception as e:
                    asyncio.create_task(self.errorlog(e, ctx.author, guild, args[0]))
                    await ctx.reply("Please enter a Channel ID.")
            elif mode == "remove" or mode == "delete":
                self.db.execute(f'UPDATE Admin SET Changelog = NULL WHERE Server_ID = {guild.id}')
                self.db.commit()
                await ctx.reply(f"I've removed changelog updates from this server.")
            else:
                await ctx.reply()
        elif defo == "rarespawn":
            if mode == "add" or mode == "set":
                try:
                    log = self.client.get_channel(channel)
                    self.db.execute(f'UPDATE Admin SET RareSpawn = {channel} WHERE Server_ID = {guild.id}')
                    self.db.commit()
                    _emb = await Auction_embed(self.client, description=f"<@{ctx.author.id}> has set up this channel to receive PokéMeow rare spawns.").setup_embed()
                    await log.send(embed=_emb)
                    await ctx.reply(f"Successfully set <#{args[0]}> as your rare spawn channel for PokéMeow.")
                except Exception as e:
                    asyncio.create_task(self.errorlog(e, ctx.author, guild, args[0]))
                    await ctx.reply("Please enter a Channel ID.")
            elif mode == "remove" or mode == "delete":
                self.db.execute(f'UPDATE Admin SET RareSpawn = NULL WHERE Server_ID = {guild.id}')
                self.db.commit()
                await ctx.reply(f"I've removed PokéMeow rare spawn updates from this server.")
            else:
                await ctx.reply()
        elif defo == "psyflex":
            if mode == "add" or mode == "set":
                try:
                    log = self.client.get_channel(channel)
                    self.db.execute(f'UPDATE Admin SET PsyFlex = {channel} WHERE Server_ID = {guild.id}')
                    self.db.commit()
                    _emb = await Auction_embed(self.client, description=f"<@{ctx.author.id}> has set up this channel to receive Psycord flex messages. ``flex`` is the command to use for that.").setup_embed()
                    await log.send(embed=_emb)
                    await ctx.reply(f"Successfully set <#{args[0]}> as your flex channel for Psycord.")
                except Exception as e:
                    asyncio.create_task(self.errorlog(e, ctx.author, guild, args[0]))
                    await ctx.reply("Please enter a Channel ID.")
            elif mode == "remove" or mode == "delete":
                self.db.execute(f'UPDATE Admin SET PsyFlex = NULL WHERE Server_ID = {guild.id}')
                self.db.commit()
                await ctx.reply(f"I've removed Psycord flex posts from this server.")
            else:
                await ctx.reply()
        elif defo == "outbreaks":
            if mode == "add" or mode == "set":
                try:
                    log = self.client.get_channel(channel)
                    print(log)
                    self.db.execute(f'UPDATE Admin SET PsyhuntFeed = {args[0]} WHERE Server_ID = {guild.id}')
                    self.db.commit()
                    _emb = await Auction_embed(self.client, description=f"<@{ctx.author.id}> has set up this channel to check for Psycord outbreaks.").setup_embed()
                    await log.send(embed=_emb)
                    await ctx.reply(f"Successfully set <#{args[0]}> as your Psycord outbreaks feed channel.")
                except Exception as e:
                    asyncio.create_task(self.errorlog(e, ctx.author, guild, args[0]))
                    await ctx.reply("Wrong usage, please refer back to the command usage.")
            elif mode == "role":
                try:
                    log = guild.get_role(channel)
                    self.db.execute(f'UPDATE Admin SET PsyhuntRole = {args[0]} WHERE Server_ID = {guild.id}')
                    self.db.commit()
                    _emb = await Auction_embed(self.client, description=f"<@{ctx.author.id}> has set up <@&{args[0]}> to ping for Psycord spawns.").setup_embed()
                    await ctx.reply(embed=_emb)
                except Exception as e:
                    asyncio.create_task(self.errorlog(e, ctx.author, guild, args[0]))
                    await ctx.reply("Please enter a Channel ID.")
            elif mode == "remove" or mode == "delete":
                self.db.execute(f'UPDATE Admin SET PsyhuntFeed = NULL WHERE Server_ID = {guild.id}')
                self.db.commit()
                await ctx.reply(f"I've removed psycord outbreak pings from this server.")
            else:
                await ctx.reply()
        else:
            await ctx.reply()

    @commands.command()
    async def dm(self, ctx, userid, *args):
        try:
            int(userid)
            print(userid)
        except ValueError:
            print("ValueError")
        if userid.startswith("<@") and userid.endswith(">"):
            print("Starting with mention, "+userid)
            userid = userid.split("<@")[1]
            userid = userid.split(">")[0]
            userid = int(userid)
            print(userid)
        else:
            print(userid)
            userid = ctx.guild.get_member(int(userid))
            print(userid)
            userid = userid.id
            print("Its a name...")

        user = ctx.guild.get_member(userid)
        msg = " ".join(args)
        await user.send(msg)

    @commands.check(Basic_checker().check_server)
    @commands.check(Basic_checker().check_admin)
    @commands.command()
    async def spring(self, ctx):
        exclude = ["IPC-Trainer", "PAR Trainer", "Trial Member", "Clan Friend", "Botz", "Clan Treasury", "PAR Friends", "Straymons Member"]
        members = ctx.guild.members
        await ctx.send("Calculating...")
        role = disnake.utils.get(ctx.guild.roles, name="Stranger?")
        print(role)
        with open("springclean.txt", "w") as file:

            for entry in members:
                has_role = any(role.name in exclude for role in entry.roles)
                if not has_role and entry.bot == False:
                    print(entry.display_name)
                    await entry.add_roles(role)
                    file.write(f"Name: {entry.display_name} - ID: {entry.id}, joined: {entry.joined_at}, roles: {entry.roles}\n")

            pass

        await ctx.reply(content="Here is the file for the spring cleaning.",file=disnake.File(file, filename="springclean.txt"))


    @commands.command()
    async def toggle(self, ctx):
        current_time = datetime.datetime.now()
        timestamp = current_time.strftime('%Y-%m-%d %H:%M')
        user_id = ctx.author.id
        database = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {user_id}')
        database = database.fetchone()
        author_url = "https://cdn.discordapp.com/emojis/1153729922620215349.webp?size=96&quality=lossless"
        author_name = ctx.author.display_name
        gengar_bot = self.client.get_user(1161011648585285652)
        footer_icon = gengar_bot.display_avatar.url
        footer_name = gengar_bot.display_name+" I "+timestamp
        emo_yes = ":white_check_mark:"
        emo_no = ":x:"
        emo_ping = ":bell:"
        emo_sile = ":no_bell:"
        color = 0x807ba6
        if database:
            if database[2] == 1:
                value_grazz = emo_yes
            else:
                value_grazz = emo_no
            if database[3] == 1:
                value_repel = emo_yes
            else:
                value_repel = emo_no
            if database[4] == 1:
                value_start = emo_yes
            else:
                value_start = emo_no
            if database[5] == 1:
                value_link = emo_yes
            else:
                value_link = emo_no
            if database[6] == 0:
                value_rem = "Text style"
            elif database[6] == 1:
                value_rem = "Emote Style"
            if database[10] == 1:
                value_spawn = emo_yes
            elif database[10] == 0:
                value_spawn = emo_no
            if database[0][11] == 1:
                value_fish = emo_yes
            elif database[11] == 0:
                value_fish = emo_no
            if database[12] == 1:
                value_battle = emo_yes
            elif database[12] == 0:
                value_battle = emo_no
            if database[13] == 1:
                value_quest = emo_yes
            elif database[13] == 0:
                value_quest = emo_no
            if database[14] == 1:
                value_questr = emo_yes + emo_sile
            elif database[14] == 0:
                value_questr = emo_no
            elif database[4] == 2:
                value_questr = emo_yes + emo_ping
            if database[15] == 1:
                value_other = emo_yes
            elif database[15] == 0:
                value_other = emo_no
            if database[16] == 0:
                value_ping = emo_ping
            else:
                value_ping = emo_sile
            embed = disnake.Embed(
                title="**Settings**", color=color, description="Here you can see your current toggle settings. \nChangeable via ``/toggle`` \n\nThe current settings are:"
            )
            embed.set_author(icon_url=author_url,name=author_name)
            embed.set_footer(icon_url=footer_icon,text=footer_name)
            embed.add_field(name="Golden Razz Berry/Honey: ",inline=True, value=value_grazz)
            embed.add_field(name="Repels: ",inline=True, value=value_repel)
            embed.add_field(name="Starter: ",inline=True, value=value_start)
            embed.add_field(name="Reminder Mode: ", inline=True, value=value_rem)
            embed.add_field(name="Pings: ", inline=True, value=value_ping)
            embed.add_field(name="",inline=True, value="")
            embed.add_field(name="Spawn: ", inline=True, value=value_spawn)
            embed.add_field(name="Fish: ", inline=True, value=value_fish)
            embed.add_field(name="Battle: ", inline=True, value=value_battle)
            embed.add_field(name="Quest Command: ", inline=True, value=value_quest)
            embed.add_field(name="Next Quest: ", inline=True, value=value_questr)
            embed.add_field(name="Other Commands: ", inline=True, value=value_other)

            embed.set_thumbnail(footer_icon)
            await ctx.send(embed=embed)

    @commands.command()
    async def faq(self, ctx):
        await ctx.send("The FAQ Channel is here: <#1161686361091350608>")

    @commands.command()
    async def hunt(self, ctx, mode:str = None, mon = None,amount:int = None):
        staff = 837611415070048277
        staff = ctx.guild.get_role(837611415070048277)
        if mode == None:
            desc = f"Placeholder.\nUse either ``add, delete,reset,list,clear,show,active``."
            await ctx.reply(desc)
        elif mode == "add":
            if staff not in ctx.author.roles:
                await ctx.reply("Unauthorized try to access that command. You have no power here.")
            else:
                if mon == None:
                    await ctx.reply("Please insert a Pokémon Name or ID.")
                else:
                    try:
                        if int(mon) == True:
                            dex = self.db.execute(f'SELECT * FROM Dex WHERE DexID = {mon}')
                            dex = dex.fetchone()
                    except:
                        mon = mon.capitalize()
                        mon = mon+" "
                        dex = self.db.execute(f'SELECT * FROM Dex WHERE Name = "{mon}"')
                        dex = dex.fetchone()
                    if amount == None:
                        amount = thresholds[dex[14]]
                    hunts = self.db.execute(f'SELECT * FROM HuntMons')
                    hunts = hunts.fetchall()
                    i = 0
                    for entry in hunts:
                        if dex[1] in entry[1]:
                            await ctx.reply("That Pokémon is currently hunted.")
                            i = 1
                    if i == 0:
                        self.db.execute(f'INSERT INTO HuntMons VALUES ({dex[0]}, "{dex[1]}", {amount})')
                        self.db.commit()
                        self.db.execute(f'ALTER TABLE HuntMembers ADD {dex[1]} INT')
                        self.db.commit()
                        await ctx.reply(f'Added **{dex[1]}** to the hunt, current threshold is **{amount}**')
        elif mode == "delete":
            if staff not in ctx.author.roles:
                await ctx.reply("Unauthorized try to access that command. You have no power here.")
            else:
                if mon == None:
                    await ctx.reply("Please insert a Pokémon Name or ID.")
                else:
                    if int(mon):
                        dex = self.db.execute(f'SELECT * FROM Dex WHERE DexID = {mon}')
                        dex = dex.fetchone()
                    else:
                        mon = mon.capitalize()
                        dex = self.db.execute(f'SELECT * FROM Dex WHERE Name = "{mon}"')
                        dex = dex.fetchone()
                    hunts = self.db.execute(f'SELECT * FROM HuntMons')
                    hunts = hunts.fetchall()
                    i = 0
                    print(dex)
                    print(hunts)
                    for entry in hunts:
                        if dex[1] in entry[1]:
                            self.db.execute(f'DELETE FROM HuntMons WHERE MonID = {dex[0]}')
                            self.db.commit()
                            self.db.execute(f'ALTER TABLE HuntMembers DROP {dex[1]}')
                            self.db.commit()
                            await ctx.reply(f"Deleted {dex[1]} from the hunt table.")
        elif mode == "clear" or mode == "reset":
            if staff not in ctx.author.roles:
                await ctx.reply("Unauthorized try to access that command. You have no power here.")
            else:
                self.db.execute(f'DELETE FROM HuntMons')
                self.db.commit()
                self.db.execute(f'DELETE FROM HuntMembers')
                self.db.commit()
                await ctx.reply(f"Cleared the whole hunt table.")
        elif mode == "list" or mode == "show" or mode == "active":
            hunts = self.db.execute(f'SELECT * FROM HuntMons')
            hunts = hunts.fetchall()
            if hunts:
                desc = "\n"
                for entry in hunts:
                    desc += f"> * {entry[1]}, minimum amount: {entry[2]}\n"
                _embed = await Auction_embed(self.client,title="**Current Hunts**", description=desc).setup_embed()
                await ctx.reply(embed=_embed)
            else:
                await ctx.reply("There are no hunts at the moment.")



    @commands.command()
    async def calc(self, ctx, operation:str):
        await ctx.send(eval(operation))

    @commands.command()
    async def random(self, ctx, message = None):
        try:
            message = ctx.message.content.split()[1]
        except: message = None
        #print(str(message))
        gengar_bot = self.client.get_user(1161011648585285652)
        footer_icon = gengar_bot.display_avatar.url
        footer_name = "Mega Gengar"
        if message == "hunt":
            roll1 = random.randint(1, 479)
            database1 = self.db.execute(f'SELECT * FROM Dex WHERE DexID = {roll1}')
            database1 = database1.fetchall()
            roll2 = random.randint(1, 479)
            while roll2 == roll1:
                roll2 = random.randint(1, 479)
            database2 = self.db.execute(f'SELECT * FROM Dex WHERE DexID = {roll2}')
            database2 = database2.fetchall()
            #print(roll1)
            #print(roll2)
            monname = database1[0][1]
            monurl = database1[0][15]
            monrare = database1[0][14]
            embed = disnake.Embed(title="Your first Pokémon is **"+str(roll1)+"**.", color=0x807ba6)
            embed.set_footer(icon_url=footer_icon,text=footer_name)
            embed.set_author(name="PNG (Pokémon Number Generator)",icon_url="https://cdn.discordapp.com/emojis/862641822404050964.png")
            embed.set_image(monurl)
            embed.add_field(name=(monname), inline=True,value=("Dex Number: "+str(roll1)+"\n\nRarity: "+monrare+"\n\n"))
            await ctx.send(embed=embed)
            embed2 = disnake.Embed(title="Your second Pokémon is **"+str(roll2)+"**.", color=0x807ba6)
            embed2.set_author(name="PNG (Pokémon Number Generator)",icon_url="https://cdn.discordapp.com/emojis/862641822404050964.png")
            monname = database2[0][1]
            monurl = database2[0][15]
            monrare = database2[0][14]
            embed2.set_footer(icon_url=footer_icon,text=footer_name)
            embed2.set_image(monurl)
            embed2.add_field(name=(monname), inline=True,value=("Dex Number: "+str(roll2)+"\n\nRarity: "+monrare))

            await ctx.send(embed=embed2)

        else:
            roll1 = random.randint(1, 914)
            database1 = self.db.execute(f'SELECT * FROM Dex WHERE DexID = {roll1}')
            database1 = database1.fetchall()
            monname = database1[0][1]
            monurl = database1[0][15]
            monrare = database1[0][14]
            embed = disnake.Embed(title="Your Pokémon is **"+str(roll1)+"**.", color=0x807ba6)
            embed.set_footer(icon_url=footer_icon,text=footer_name)
            embed.set_author(name="PNG (Pokémon Number Generator)",icon_url="https://cdn.discordapp.com/emojis/862641822404050964.png")
            embed.set_image(monurl)
            #print(roll1)
            embed.add_field(name=(monname), inline=True,value=("Dex Number: "+str(roll1)+"\n\nRarity: "+monrare))
            await ctx.send(embed=embed)



    @commands.command()
    async def joined(self, ctx, member: disnake.Member):
        """Says when a member joined."""
        await ctx.send(f"{member.name} joined in {member.joined_at}")

    @commands.command()
    async def test(self, ctx):
        await ctx.send(f"I'm alive!!! {ctx.author.name}")

    @commands.command(aliases=["tc","topc"])
    async def topcount(self, ctx, message = None):
        cat = ["event","fullodd","legendary","item","goldenfish","shinyfish","legendaryfish","goldenexp","shinyexp","legendaryexp","icon"]
        if message:
            if message in cat:
                data = self.db.execute(f'SELECT * FROM Counter ORDER BY {message} DESC')
                data = data.fetchall()
                e = countnumber[message]
                embed = await Custom_embed(self.client,title=f"Top Count Leaderboard",description=f"Top 5 Leaderboard in "+counts[message]).setup_embed()

                embed.add_field(name="Place:",value="1.\n2.\n3.\n4.\n5.")
                embed.add_field(name="Username",value="<@"+str(data[0][0])+">\n"+"<@"+str(data[1][0])+">\n"+"<@"+str(data[2][0])+">\n"+"<@"+str(data[3][0])+">\n"+"<@"+str(data[4][0])+">")
                embed.add_field(name="Amount",value=str(data[0][e])+"\n"+str(data[1][e])+"\n"+str(data[2][e])+"\n"+str(data[3][e])+"\n"+str(data[4][e]))
                await ctx.send(embed=embed)
            if message == "total":
                embed = await Custom_embed(self.client,title=f"Top Count Leaderboard",description=f"Top 5 Leaderboard in total").setup_embed()
                i = 0
                while i <= 4:
                    data = self.db.execute(f'SELECT * FROM Counter ORDER BY {cat[i]} DESC')
                    data = data.fetchall()
                    #print(cat[i])
                    e = countnumber[cat[i]]
                    fieldname = counts[cat[i]]
                    #print(fieldname)
                    embed.add_field(name=fieldname,value="",inline=False)
                    embed.add_field(name="Place:",value="1.\n2.\n3.\n4.\n5.")
                    embed.add_field(name="Username",value="<@"+str(data[0][0])+">\n"+"<@"+str(data[1][0])+">\n"+"<@"+str(data[2][0])+">\n"+"<@"+str(data[3][0])+">\n"+"<@"+str(data[4][0])+">")
                    embed.add_field(name="Amount",value=str(data[0][e])+"\n"+str(data[1][e])+"\n"+str(data[2][e])+"\n"+str(data[3][e])+"\n"+str(data[4][e]))
                    i+=1
                await ctx.send(embed=embed)
                embed = await Custom_embed(self.client,title=f"Top Count Leaderboard",description=f"Top 5 Leaderboard in total").setup_embed()
                while i >= 5 and i <=9:
                    data = self.db.execute(f'SELECT * FROM Counter ORDER BY {cat[i]} DESC')
                    data = data.fetchall()
                    #print(cat[i])
                    e = countnumber[cat[i]]
                    fieldname = counts[cat[i]]
                    embed.add_field(name=fieldname,value="",inline=False)
                    embed.add_field(name="Place:",value="1.\n2.\n3.\n4.\n5.")
                    embed.add_field(name="Username",value="<@"+str(data[0][0])+">\n"+"<@"+str(data[1][0])+">\n"+"<@"+str(data[2][0])+">\n"+"<@"+str(data[3][0])+">\n"+"<@"+str(data[4][0])+">")
                    embed.add_field(name="Amount",value=str(data[0][e])+"\n"+str(data[1][e])+"\n"+str(data[2][e])+"\n"+str(data[3][e])+"\n"+str(data[4][e]))
                    i+=1
                await ctx.send(embed=embed)
        else:
            embed = await Custom_embed(self.client,title=f"Wrong Usage",description=f"Sorry, wrong parameter.").setup_embed()
            embed.add_field(name="Valid parameter for ``topcount``:",value="event, fullodd, legendary, item, goldenfish, shinyfish, legendaryfish, goldenexp, shinyexp, legendaryexp, icon\n''total'' prints a summary for every category.")
            embed.add_field(name="__Aliases:__",value="``topc`` or ``tc``",inline=False)
            await ctx.send(embed=embed)



    @commands.command()
    async def toggledb(self, ctx):
        self.db.execute(f'''
                        CREATE TABLE IF NOT EXISTS Events(
                        User_ID INTEGER,
                        Buyin INTEGER,
                        Points INTEGER DEFAULT 0,
                        ItemsUsed INTEGER DEFAULT 0,
                        Items INTEGER DEFAULT 0
                        )
                        ''')
        self.db.commit()
        print("Dex_DB created")
        await ctx.send("Done")

    @commands.command()
    async def pin(self, ctx, message_id: int = None):
        checker = 1
        if message_id == None:
            #print("No ID given")
            if ctx.message.reference:
                message_id = ctx.message.reference.message_id
            #print("Ref id is "+str(message_id))
            else:
                await ctx.send("Please use a message ID or answer to a message.")
                checker = 0
        if checker == 1:
            ref_msg = await ctx.channel.fetch_message(message_id)
            #print(ref_msg)
            if ctx.channel.id not in unpinnables:
                #print("Channel is ok")
                message = ref_msg
                await message.pin()

    @commands.command()
    async def unpin(self, ctx, message_id: int = None):
        checker = 1
        if message_id == None:
            #print("No ID given")
            if ctx.message.reference:
                message_id = ctx.message.reference.message_id
            else:
                await ctx.send("Please use a message ID or answer to a message.")
                checker = 0
        if checker == 1:
            ref_msg = await ctx.channel.fetch_message(message_id)
            #print(ref_msg)
            if ctx.channel.id not in unpinnables:
                emoji = ':white_check_mark:'
                await ctx.message.add_reaction(emoji)
                #print("Channel is ok")
                message = ref_msg
                await message.unpin()

    @commands.check(Basic_checker().check_management)
    @commands.command()
    async def rare(self, ctx, id: int):
        receiver_channel = 825950637958234133
        announce = self.client.get_channel(receiver_channel)
        overseen = await ctx.channel.fetch_message(id)
        if overseen:
            Rare_Spawns = ["Event", "Legendary", "Shiny","Golden"]
            if "from completing challenge" in overseen.content:
                    if overseen.reference:
                        ref_msg = await overseen.channel.fetch_message(overseen.reference.message_id)
                        sender = ref_msg.author
                    elif overseen.interaction:
                        sender = overseen.interaction.author
                    print(f'{sender.display_name} won a chamber.')
                    nite = overseen.content.split("<:")[1]
                    item = nite.split(":")[0]
                    print(f'{item}, {chambers[item]}')
                    number = nite.split(":")[1]
                    number = number.split(">")[0]
                    dex = self.db.execute(f'SELECT * FROM Dex WHERE DexID = {chambers[item]}')
                    dex = dex.fetchone()
                    print(dex[1])
                    current_time = overseen.created_at
                    timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
                    description_text = f"Original message: [Click here]({overseen.jump_url})\n"
                    embed = disnake.Embed(title=f"{sender.display_name} was able to claim a **{item.capitalize()}**",description=description_text)
                    embed.set_author(name=(f'{sender.display_name}'+" won in a megachamber!"),icon_url=f"https://cdn.discordapp.com/emojis/{number}.webp?size=96&quality=lossless")
                    embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                    embed.set_image(dex[15])
                    await announce.send(embed=embed)
            if len(overseen.embeds) > 0:
                _embed = overseen.embeds[0]
                print(overseen)
                user = _embed.author.name.split(" ")[1]
                print(user)
                user = user.split("!")[0]
                print(user)
                user = ctx.guild.get_member_named(user)
                print(user)
                if "broke out" or "caught a " in _embed.description:
                    data = self.db.execute(f'SELECT * FROM Dex WHERE Img_url = "{_embed.image.url}"')
                    data = data.fetchall()
                    raremon = data[0][14]
                    print(raremon)
                    ball = _embed.description.split(" with a")[1]
                    ball = ball.split("!")[0]
                    ball = ball.split(" ")[1]
                    print(ball)
                    #print(_embed.color)
                    color = str(_embed.color)
                    #print(color)
                    if raremon in Rare_Spawns or color == '#ea260b':
                        raremon = poke_rarity[(data[0][14])]
                        current_time = overseen.created_at
                        timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
                        print(timestamp)
                        description_text = f"Original message: [Click here]({overseen.jump_url})\n"
                        embed = await Custom_embed(self.client, title=raremon+" **"+data[0][1]+"** \nDex: #"+str(data[0][0]),description=description_text,colour=_embed.color).setup_embed()
                        embed.set_author(name=(user.display_name+" just caught a:"), icon_url=_embed.author.icon_url)
                        embed.set_image(_embed.image.url)
                        embed.set_thumbnail(url=None)

                        embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                        await announce.send(embed=embed)
                        await ctx.send("Check <#825950637958234133>",embed=embed)
                    else:
                        await ctx.send(f'{data[0][1]} is not rare enough to be posted. If you think this is wrong, ping Blue Flame.')

            elif "'s trainer icon!" in overseen.content:
                print(overseen.content)
                current_time = overseen.created_at
                timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
                iconname = overseen.content.split("unlocked ")[1]
                icon = iconname.split(":")[2]
                icon = icon.split(">")[0]
                print(icon)
                iconname = iconname.split(":")[1]
                print(iconname)
                iconname = iconname.replace("_"," ")
                iconname = iconname.title()
                print(iconname)
                authorid = overseen.content.split("@")[1]
                authorid = int(authorid.split(">")[0])
                user = self.client.get_user(authorid)
                thumburl = "https://cdn.discordapp.com/emojis/"
                icon = str(icon)
                thumburl = thumburl+icon
                thumburl = thumburl+".webp?size=96&quality=lossless"
                print(thumburl)
                current_time = overseen.created_at
                timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
                description_text = f"Original message: [Click here]({overseen.jump_url})\n"
                embed = await Custom_embed(self.client,description="**"+iconname+"** was viciously defeated and dropped their icon.\n"+description_text,thumb=thumburl).setup_embed()
                embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                embed.set_author(name=f'{self.client.get_user(authorid).display_name}'" just found a new icon!", icon_url="https://cdn.discordapp.com/emojis/766701189260771359.webp?size=96&quality=lossless")
                await announce.send(embed=embed)

            elif "used a code to claim" in overseen.content:
                if overseen.reference:
                    ref_msg = await overseen.channel.fetch_message(overseen.reference.message_id)
                    sender = ref_msg.author
                elif overseen.interaction:
                    sender = overseen.interaction.author
                monname = overseen.content.split("**")[1]
                monname = monname+" "
                await ctx.send('``'+monname+'``')
                print(monname)
                data = self.db.execute(f'SELECT * FROM Dex WHERE Name LIKE "{monname}"')
                data = data.fetchall()
                #print(data)
                url = data[0][15]
                #print(url)
                monname = data[0][1]
                print(monname)
                current_time = overseen.created_at
                timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
                description_text = f"Original message: [Click here]({overseen.jump_url})\n"
                embed = await Custom_embed(self.client,thumb=url,description=sender.display_name+" just claimed a **"+monname+"** from a code.\n"+description_text).setup_embed()
                embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                embed.set_author(name=f'{sender.display_name}'" just redeemed a code!", icon_url="https://cdn.discordapp.com/emojis/671852541729832964.webp?size=240&quality=lossless")
                await announce.send(embed=embed)

        else:
            await ctx.send("Please reply to a message.")

    @commands.check(Basic_checker().check_server)
    @commands.check(Basic_checker().check_admin)
    @commands.command(aliases=["bl", "blackl"])
    async def blacklist(self, ctx, action: str = None, userid: int = None):
        if userid != None:
            db = self.db.execute(f'SELECT * FROM Blacklist WHERE UserID = {userid}')
            db = db.fetchall()
            user = await self.client.getch_user(userid)
        if action == "add":
            if db:
                await ctx.send(user.name+" is already on the blacklist.")
            elif userid == None:
                await ctx.send("Please mention a valid user id next time.")
            elif not db:
                self.db.execute(f'INSERT INTO Blacklist VALUES ({userid})')
                self.db.commit()
                await ctx.send(user.name+" was added to the blacklist.")
        if action == "remove":
            if db:
                self.db.execute(f'DELETE FROM Blacklist WHERE UserID = {userid}')
                self.db.commit()
                await ctx.send(user.name+" was removed from the blacklist.")
            elif userid == None:
                await ctx.send("Not sure who to remove here - maybe add a user id next time?")
            elif not db:
                await ctx.send("Sorry, but "+user.name+" isn't on the blacklist.")
        if action == None:
            db = self.db.execute(f'SELECT * FROM Blacklist')
            db = db.fetchall()
            if len(db) >= 1:
                print(len(db))
                msg = "**Usernames:**\n"
                i = 1
                for row in db:
                    print(i)
                    user = await self.client.getch_user(db[i-1][0])
                    print(user)
                    msg += user.name+"\n"
                    i+=1
            else:
                msg = "{Empty}"
            embed = await Custom_embed(self.client,title="Blacklist", description=msg,thumb=None).setup_embed()
            await ctx.send(embed=embed)

    #484x484 pfp
    #start 0 321 or 4 326
    @commands.check(Basic_checker().check_management)
    @commands.command()
    async def pic(self, ctx, userid = None):
        if userid == None:
            userid = ctx.author
        else:
            if "@" in userid:
                userid = userid.split("@")[1]
                userid = userid.split(">")[0]
            userid = await self.client.getch_user(int(userid))

        victory = Image.open("pictures/victory_hall.png")

        asset = userid.avatar.with_size(128)
        #print(asset)
        asset = await asset.read()
        data = BytesIO(asset)
        pfp = Image.open(data)

        pfp = pfp.resize((484,484))
        victory.paste(pfp, (326,4))
        victory.save("pictures/victory.png")

        await ctx.send(file=disnake.File("pictures/victory.png"))

    @commands.command()
    async def flex(self, ctx, number: int = None):
        flex = self.db.execute(f'SELECT * FROM Admin WHERE Server_ID = {ctx.guild.id}')
        flex = flex.fetchone()
        if flex[10] != 0:
            flexchannel = int(flex[10])
            flexchannel = self.client.get_channel(flexchannel)
            if number == None:
                if ctx.message.reference:
                    spawn = ctx.message.reference.message_id
                    spawn = await ctx.channel.fetch_message(spawn)
                    _embed = spawn.embeds[0]
                    await ctx.message.reply(f"Done! Check <#{flexchannel.id}> to see the result!")
                    await flexchannel.send(f'Original Message: [Click here]({spawn.jump_url})',embed=_embed)
                else:
                    await ctx.send("Please answer to a message or use its ID.")
            elif number != None:
                spawn = await ctx.channel.fetch_message(number)
                _embed = spawn.embeds[0]
                await ctx.message.reply(f"Done! Check <#{flexchannel.id}> to see the result!")
                await flexchannel.send(f'Original Message: [Click here]({spawn.jump_url})',embed=_embed)
        else:
            await ctx.message.reply("Your server has not yet setup a flex channel for psycord spawns. Please ask your server admin about it.")

    @commands.command()
    async def code(self, ctx, *lines):
        code_channel = 1213234583949021255
        channel = self.client.get_channel(code_channel)
        cod = ' '.join(lines)
        firsthalf = cod.split("Expires")[0]
        secondhalf = cod.split(firsthalf)[1]
        #print(firsthalf)
        #print(secondhalf)
        cod = firsthalf+"\n"+secondhalf
        #print(cod)
        if "Expires on:" in cod:
            #print("Its in")
            await ctx.message.delete()
            oldmsg = self.db.execute(f'SELECT * FROM Admin')
            oldmsg = oldmsg.fetchone()
            try:
                oldmsg = await channel.fetch_message(oldmsg[7])
                await oldmsg.delete()
            except Exception as e:
                print(e)
            _embed = await Auction_embed(self.client,title="**New Code**",description=cod).setup_embed()
            _embed.set_author(name=f'{ctx.author.display_name} sponsored a code!',icon_url=ctx.author.display_avatar)
            thx = await ctx.send(f"Thx for gifting a code! Check <#{code_channel}>!")
            first = await channel.send(embed=_embed)
            react = self.client.get_emoji(825954837384265770)
            await first.add_reaction(react)
            desc = "<:GengarHeart:1153729922620215349> To submit a code in here just use the command: ``mcode message``\n \n<:GengarHeart:1153729922620215349> React to the <:hype:825954837384265770> Emote if you've claimed the code!\n"
            _membed = await Auction_embed(self.client,title="**How to donate:**",description=desc).setup_embed()
            msg = await channel.send(embed=_membed)
            id = msg.id
            self.db.execute(f'UPDATE Admin SET Stickymsg = {id}')
            self.db.commit()
            await asyncio.sleep(5)
            await thx.delete()
        else:
            await ctx.send("Please paste the whole message from ``/drops``.")

    @commands.check(Basic_checker().check_management)
    @commands.command()
    async def tester(self, ctx, number: int):
        data = self.db.execute(f'SELECT * FROM Dex WHERE DexID = {number}')
        data = data.fetchall()
        print(data[0][15])
        msg = data[0][15]

        pic = Image.open("pictures/tester.png",'r')

        async with aiohttp.ClientSession() as session:
            async with session.get(msg) as response:
                gif_data = await response.read()

        new_gif_frame = []

        gif_data = imageio.get_reader(BytesIO(gif_data), 'GIF')

        for gif_frame in gif_data:
            new_frame = pic.copy()
            new_frame.paste(Image.fromarray(gif_frame).resize((250,250)), (530,50), Image.fromarray(gif_frame).resize((250,250)).convert('RGBA'))
            new_gif_frame.append(new_frame)

        print(gif_data.get_meta_data())

        new_gif_byte_array = BytesIO()
        new_gif_frame[0].save(
            new_gif_byte_array,
            save_all=True,
            append_images=new_gif_frame[1:],
            format='GIF',
            duration=gif_data.get_meta_data()["duration"]
        )

        new_gif_byte_array.seek(0)
        await ctx.send(file=disnake.File(new_gif_byte_array, 'combined_image.gif'))


        # first_frame = Image.fromarray(gif_data[0])



        # tester = Image.open("pictures/tester.png")
        # monframe = first_frame.resize((250, 250))
        # tester.paste(monframe, (530, 50))
        # tester.save("pictures/tested.png")

        # await ctx.send(file=disnake.File("pictures/tested.png"))

    @commands.command(aliases=["buddy","stats"])
    async def bud(self, ctx, user = None):
        if "@" in user:
            #print(user)
            user = user.split("@")[1]
            user = user.split(">")[0]
            user = int(user)
            #print(user)
            buddy = ctx.guild.get_member(user)
            #print(buddy)
            roles = buddy.roles
            leng = len(roles)
            leng = leng-1
            tr = roles[leng]
            #print(tr)
            col = tr.colour
            #print(col)
            exp = random.randint(0,1250000)
            level = int(((4*exp)/5)**(1/3))
            embed = await Custom_embed(self.client, thumb=None, colour=col,title="**Level**: "+str(level)+"\n**Total EXP**: "+str(exp)+"\n**Item**: None").setup_embed()
            embed.add_field(name="Type",value=f"<@&{tr.id}>")
            fship = random.randint(0,10)
            descheart = ""
            if fship > 0:
                calc = math.floor(fship/2)
                descheart += "<:fullheart:1197574322907250708>"*calc
                if calc%2 == 1:
                    descheart += "<:halfheart:1278102327617785909>"
                    calc += 1
                calc = 5-calc
                descheart += "<:emptyheart:1278102303974359141>"*calc
            embed.add_field(name="Friendship",value=descheart)
            atk = random.randint(0,14)
            deff = random.randint(0,14)
            hp = random.randint(0,14)
            spe = random.randint(0,14)
            #print(roles)
            for role in roles:
                if role.name == "Management":
                    atk = 20
                    deff = 20
                    hp = 20
                    spe = 20

            if atk > 0 and atk < 5:
                starsatk = "<:star0:1197574311200960672><:star0:1197574311200960672><:star0:1197574311200960672><:star0:1197574311200960672>"
            elif atk >= 5 and atk < 10:
                starsatk = "<:star1:1197574299553366188><:star0:1197574311200960672><:star0:1197574311200960672><:star0:1197574311200960672>"
            elif atk >= 10 and atk < 15:
                starsatk = "<:star1:1197574299553366188><:star1:1197574299553366188><:star0:1197574311200960672><:star0:1197574311200960672>"
            else:
                starsatk = "<:star1:1197574299553366188><:star1:1197574299553366188><:star1:1197574299553366188><:star1:1197574299553366188>"
            if deff > 0 and deff < 5:
                starsdef = "<:star0:1197574311200960672><:star0:1197574311200960672><:star0:1197574311200960672><:star0:1197574311200960672>"
            elif deff >= 5 and deff < 10:
                starsdef = "<:star1:1197574299553366188><:star0:1197574311200960672><:star0:1197574311200960672><:star0:1197574311200960672>"
            elif deff >= 10 and deff < 15:
                starsdef = "<:star1:1197574299553366188><:star1:1197574299553366188><:star0:1197574311200960672><:star0:1197574311200960672>"
            else:
                starsdef = "<:star1:1197574299553366188><:star1:1197574299553366188><:star1:1197574299553366188><:star1:1197574299553366188>"
            if hp > 0 and hp < 5:
                starshp = "<:star0:1197574311200960672><:star0:1197574311200960672><:star0:1197574311200960672><:star0:1197574311200960672>"
            elif hp >= 5 and hp < 10:
                starshp = "<:star1:1197574299553366188><:star0:1197574311200960672><:star0:1197574311200960672><:star0:1197574311200960672>"
            elif hp >= 10 and hp < 15:
                starshp = "<:star1:1197574299553366188><:star1:1197574299553366188><:star0:1197574311200960672><:star0:1197574311200960672>"
            else:
                starshp = "<:star1:1197574299553366188><:star1:1197574299553366188><:star1:1197574299553366188><:star1:1197574299553366188>"
            if spe > 0 and spe < 5:
                starsspe = "<:star0:1197574311200960672><:star0:1197574311200960672><:star0:1197574311200960672><:star0:1197574311200960672>"
            elif spe >= 5 and spe < 10:
                starsspe = "<:star1:1197574299553366188><:star0:1197574311200960672><:star0:1197574311200960672><:star0:1197574311200960672>"
            elif spe >= 10 and spe < 15:
                starsspe = "<:star1:1197574299553366188><:star1:1197574299553366188><:star0:1197574311200960672><:star0:1197574311200960672>"
            else:
                starsspe = "<:star1:1197574299553366188><:star1:1197574299553366188><:star1:1197574299553366188><:star1:1197574299553366188>"
            msg = ("ATK ["+str(atk)+"] "+starsatk+" DEF ["+str(deff)+"] "+starsdef+"\nHP ["+str(hp)+"] "+starshp+" SPE ["+str(spe)+"] "+starsspe)
            msg = msg+("\nSPA ["+str(atk)+"] "+starsatk+" SPD ["+str(deff)+"] "+starsdef)
            embed.add_field(name="Buddy IVs",value=msg,inline=False)
            embed.set_image(buddy.display_avatar.url)
            await ctx.send(embed=embed)
            #print(buddy)
        elif user == int:
            print(user)
            buddy = ctx.guild.get_member(user)
            print(buddy)
            print(buddy.roles)
        elif user == None:
            print(user)
        else:
            print(user)

    @commands.command(aliases=["psy", "ph"])
    async def psyhunt(self, ctx, mode:str = None, *args):
        args = [s.lower() for s in args]
        mon = " ".join(args)
        #print(mon)
        if mode == None:
            await ctx.send("Placeholder.\nPlease use either ``list, add, delete, clear``.")
        elif mode.lower() == "list":
            hunts = self.db.execute(f'SELECT * FROM PsyHunt WHERE UserID = {ctx.author.id}')
            hunts = hunts.fetchall()
            if hunts == None:
                await ctx.reply("You're not hunting for any outbreaks.")
            else:
                desc = "you're currently hunting "
                if len(hunts) == 1:
                    desc += hunts[0][1]
                    print(hunts[0][1].title())
                else:
                    print(hunts)
                    i = 0
                    for entry in hunts:
                        if i == len(hunts):
                            desc += f'{entry[1].title()}.'
                        else:
                            desc += f'{entry[1].title()}, '
                        i += 1
                await ctx.reply(f"{ctx.author.display_name }, {desc}")
        elif mode.lower() == "add":
            if mon == None:
                await ctx.reply("Please specify a suitable Pokémon to hunt.")
            else:
                hunts = self.db.execute(f'SELECT * FROM PsyHunt WHERE UserID = {ctx.author.id}')
                hunts = hunts.fetchall()
                i = 0
                for entry in hunts:
                    if mon in entry[1]:
                        await ctx.reply("You're already looking for that Pokémon.")
                        i = 1
                if i == 0:
                    self.db.execute(f'INSERT INTO PsyHunt (UserID, Mon, ServerID) VALUES ({ctx.author.id}, "{mon}", {ctx.guild.id})')
                    self.db.commit()
                    await ctx.reply(f"{ctx.author.display_name}, I've added {mon.title()} to your Outbreak hunting list.")
        elif mode.lower() == "delete" or mode.lower() == "remove":
            if mon == None:
                await ctx.send("Please specify a suitable entry from your hunt list to delete.")
            else:
                hunts = self.db.execute(f'SELECT * FROM PsyHunt WHERE UserID = {ctx.author.id}')
                hunts = hunts.fetchall()
                for entry in hunts:
                    if mon in entry[1]:
                        self.db.execute(f'DELETE FROM PsyHunt WHERE Mon = "{mon}" AND UserID = {ctx.author.id}')
                        self.db.commit()
                        await ctx.send(f"{ctx.author.display_name}, {mon.title()} is now deleted from your Psycord huntlist.")
        elif mode.lower() == "clear":
            self.db.execute(f'DELETE FROM PsyHunt WHERE UserID = {ctx.author.id}')
            self.db.commit()
            await ctx.reply(f"Successfully cleared your Psycord outbreak hunts, {ctx.author.display_name}.")
        else:
            await ctx.reply("Wrong usage, either use ``list, add, delete, clear``.")

    @commands.check(Basic_checker().check_admin)
    @commands.command()
    async def readout(self, ctx, mid:int = None, mode:str = None):
        checker = 1
        if mid == None:
            if ctx.message.reference:
                mid = ctx.message.reference.message_id
            else:
                await ctx.send("Please use a message ID or answer to a message.")
                checker = 0
        if checker == 1:
            ref_msg = await ctx.channel.fetch_message(mid)
            desc = f"Name:{ref_msg.author.display_name}\nID: {ref_msg.author.id}\nContent: \n```{ref_msg.content}\n```"
            if mode == "embed":
                if (len(ref_msg.embeds) > 0):
                    _embed = ref_msg.embeds[0]
                    if ref_msg.content != None:
                        if _embed.description != None:
                            desc +=("```Desc:\n")
                            desc +=(f"{_embed.description}```\n")
                        if _embed.footer != None:
                            desc +=("```Footer:\n")
                            desc +=(f"{_embed.footer.text}```\n")
                        if _embed.title != None:
                            desc +=("```Title:")
                            desc +=(f"{_embed.title}```\n")
                        if _embed.fields != None:
                            desc +=("```Fields:")
                            desc +=(f"{_embed.fields}```\n")
                        if _embed.image != None:
                            desc +=("```Image:")
                            desc +=(f"{_embed.image.url}```\n")
                        if _embed.thumbnail.url != None:
                            desc +=("```Thumb:")
                            desc +=(f"{_embed.thumbnail.url}```\n")
                        if _embed.author.name != None:
                            desc +=("```Author:")
                            desc +=(f"{_embed.author.name}\n")
                            desc +=(f"{_embed.author.icon_url}```\n")
                        if _embed.color != None:
                            desc +=(f"```Color:\n")
                            desc +=(f"{_embed.color}```")
            await ctx.reply(desc)

    @commands.command()
    async def invite(self, ctx):
        user = ctx.author
        request = self.client.get_channel(1220801181123870932)
        dm = ctx.guild.get_member(user.id)
        desc = f"**{user.display_name}**, <@{user.id}>\n"
        desc += f"From Server {ctx.guild.name} - {ctx.guild.id}, requested an invitation link."
        _emb = await Auction_embed(self.client, title="**Invitation Request**",description=desc).setup_embed()
        _emb.set_thumbnail(url=ctx.guild.icon.url)
        _emb.set_image(url=user.display_avatar)
        await dm.send("I've send your request to get approved. You'll receive a DM with an invite link from me, if the request gets approved.")
        await ctx.reply("Request send. Please check your DMs.")
        await request.send(embed=_emb)

    @commands.check(Basic_checker().check_if_it_is_me)
    @commands.command()
    async def testmode(self, ctx):
        db = self.db.execute(f"SELECT TestMode FROM Admin WHERE Server_ID = {ctx.guild.id}")
        db = db.fetchone()
        if db[0] == 1:
            self.db.execute(f"UPDATE Admin SET TestMode = 0 WHERE Server_ID = {ctx.guild.id}")
            self.db.commit()
            await ctx.reply("Testmode deactivated.")
        else:
            self.db.execute(f"UPDATE Admin SET TestMode = 1 WHERE Server_ID = {ctx.guild.id}")
            self.db.commit()
            await ctx.reply("Testmode activated.")

    @commands.command(aliases=["avg","average"])
    async def averagecheck(self, ctx, userid:str = None):
        #print(userid)
        if userid == None:
            userid = ctx.author.id
            #print(userid)
        elif "@" in userid:
            userid = (userid.split("@")[1]).split(">")[0]
            #print(userid)
        userid = int(userid)
        try:
            db = self.db.execute(f"SELECT avg_coins, catch_count FROM average WHERE UserID = {userid}")
            db = db.fetchone()
            avg = db[0]
            catches = db[1]
        except:
            avg = 0
            catches = 0
        user = ctx.guild.get_member(userid)
        await ctx.reply(f"The current average stats for {user.name}:\n**{avg}** coins in **{catches}** catches.\n*Stats reset each Monday 2pm CET*")

    @commands.check(Basic_checker().check_if_it_is_me)
    @commands.command()
    async def dbcleaner(self, ctx):
        self.db.execute(f'''
    CREATE TABLE IF NOT EXISTS totalaverage (
        UserID INTEGER PRIMARY KEY,  -- UserID as the primary key (automatically unique)
        username TEXT NOT NULL,      -- Username as a string (TEXT type)
        catch_count INTEGER DEFAULT 0,  -- Catch count as an integer, default value 0
        coins INTEGER DEFAULT 0        -- Coins as an integer, default value 0
    )
''')
        self.db.commit()
            

def setup(client):
    client.add_cog(Coms(client))