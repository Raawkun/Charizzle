import os
import random
import disnake
from disnake.ext import commands
import asyncio
import re
import pytz
import main
from sqlite3 import connect
from main import client
from utility.rarity_db import poke_rarity, chambers
from utility.egglist import eggexcl
from utility.drop_chance import drop_pos, buyin
from utility.info_dict import rem_emotes, emote_list, embed_color
import aiomysql
import datetime
from utility.embed import Custom_embed, Auction_embed
from cogs.module import Modules
from utility.db_config import db_config

# Zeichen zum Kopieren: [ ] { }


class Listener(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")
        self.dv = connect("dataverse.db")

    async def errorlog(self, error, message,author):
        footer = f"{datetime.datetime.utcnow()}"
        desc = f"{message.guild.name}, <#{message.channel}>, <@{author.id}>\n[Original Message.]({message.jump_url})"
        _emb = await Auction_embed(self.client,footer=footer, description=desc).setup_embed()
        _emb.add_field(name="Error:",value=error)
        errcha = self.client.get_channel(1210143608355823647)
        await errcha.send(embed=_emb)
    promo_item = "none"
    exclusives = []

    
    async def get_db_connection(self):
        return await aiomysql.connect(host=db_config["host"],user=db_config["user"],password=db_config["password"],db=db_config["db"])
    
    async def load_promo(self):
        conn = await self.get_db_connection()
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT Current_Item FROM Stuff")
            result = await cursor.fetchone()
            await conn.ensure_closed()
        self.promo_item = result[0]
        print(f"Loaded promo item: {self.promo_item}")
        
    async def load_excl(self):
        conn = await self.get_db_connection()
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT ID FROM Exclusives")
            result = await cursor.fetchall()
            await conn.ensure_closed()
        for entry in result:
            self.exclusives.append(entry[0])
        print(f"Loaded exclusives: {self.exclusives}")
    
    async def dawndusk(self):
        rem_channel = self.client.get_channel(827306503866155008)
        east = pytz.timezone("America/New_York")
        while True:
            now = datetime.datetime.now(east)
        
            c_6am = now.replace(hour=6, minute=0)
            c_6pm = now.replace(hour=18, minute=0)
            if now == c_6am or now == c_6pm:
                desc = f"<@&1338742032809590786>\nIts time! Go get your stones!"
                if now == c_6am:
                    desc += "Current Stone: <:dawn_stone:1339193944575053865> Dawn Stone"
                else:
                    desc += "Current Stone: <:dusk_stone:1339193992176472267> Dusk Stone"
                await rem_channel.send(desc)
                wait_sec = 12*60*60
            else:
                c_6am = now.replace(hour=6, minute=0,second=0)
                c_6pm = now.replace(hour=18, minute=0,second=0)
                if now < c_6am:
                    next = c_6am
                elif now < c_6pm:
                    next = c_6pm
                else:
                    next = c_6am + datetime.timedelta(days=1)
                wait_sec = (next-now).total_seconds()
            print(f"Next stone coming in {wait_sec/60} minutes.")
            await asyncio.sleep(wait_sec)
            
            
        
    async def _quest_reminder(self,channelid, user_id, waiter,reminder, link, emote):
        print(f"quest_reminder started for {user_id} waiting for {waiter} seconds.")
        channel = self.client.get_channel(channelid)
        self.db.execute(f'UPDATE Toggle SET Timer = 1 WHERE User_ID = {user_id}')
        self.db.commit()
        await asyncio.sleep(waiter)
        #print("slept enough.")
        if link == 0:
            link = ";quest"
        else:
            link = f'</quest info:1015311085517156475>'
        if emote == 1:
            if link == 0:
                link = ""
            desc = f'{rem_emotes["remind"]} - <@{user_id}> {rem_emotes["next"]}{rem_emotes["quest"]} {link}'
        else:
            desc = f'{rem_emotes["remind"]} - <@{user_id}>, your next {link} is ready!'
        if reminder == 1:
            await channel.send(desc, allowed_mentions = disnake.AllowedMentions(users=False))
        elif reminder == 2:
            await channel.send(desc)
        self.db.execute(f'UPDATE Toggle SET QuestTime = 0, Channel = 0, Timer = 0 WHERE User_ID = {user_id}')
        self.db.commit()

    
    async def _changelog(self):
        log = self.client.get_channel(1210143608355823647)
        current_time = datetime.datetime.utcnow()
        timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
        timestamp = "At UTC "+timestamp
        print("Changelog check!")
        try:
            print("Opening that file!")
            with open("changelog.txt", 'r') as file:
            # Read the content of the file
                file_content = file.read()
                print(file_content)
            # Check if the file contains any words
            
            if any(word.isalpha() for word in file_content.split()):
                # If the file contains words, send the content in a message
                channels = self.db.execute(f'SELECT Changelog FROM Admin WHERE Changelog != 0')
                channels = channels.fetchall()
                #print(channels)
                for entry in channels:
                    #print(entry)
                    entry = int(entry[0])
                    channel = self.client.get_channel(entry)
                    await channel.send(f"Time for a new changelog! Get ready:\n```\n{file_content}\n```\nAnd that's all for today!")
                with open("changelog_old.txt", "a") as oldfile:
                    old_content = f"\n\n{timestamp}\n{file_content}"
                    oldfile.write(old_content)
                file ="changelog.txt"
                os.remove(file)
                
            else:
               exit
        except Exception as e:
            #await log.send(f'Changelog Error: {e}')
            return

    #events
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'We have logged in {self.client.user}! ID: {self.client.user.id}')
        print("------")
        print(datetime.datetime.now())
        await self.client.change_presence(activity=disnake.Activity(type=disnake.ActivityType.watching, name="the changelog."))
        await asyncio.create_task(self.load_promo())
        await asyncio.create_task(self.load_excl())
        asyncio.create_task(self.dawndusk())
        asyncio.create_task(self._changelog())
        asyncio.create_task(Modules.averagetimer(self))
        reminders = self.db.execute(f'SELECT * FROM Toggle WHERE QuestTime >= 1 ORDER BY QuestTime ASC')
        reminders = reminders.fetchall()
        #print(reminders)
        for row in reminders:
            channelid = row[8]
            self.db.execute(f'UPDATE Toggle SET Timer = 0 WHERE Channel = {channelid}')
            self.db.commit()
            #print(row[9])
            #print("theres at least one row")
            #print(channelid)
            current_time = datetime.datetime.timestamp(datetime.datetime.now())
            #print(current_time)
            waiter = row[7]
            #print(waiter)
            userid = row[1]
            if waiter > current_time:
                waiter = waiter-current_time
                #print(waiter)
                if row[14] == 1:
                    reminder = 1
                elif row[14] == 2:
                    reminder = 2
                if row[6] == 1:
                    emote = 0
                else:
                    emote = 1
                if row[5] == 0:
                    link = 0
                else:
                    link = 1
                
                await asyncio.create_task(self._quest_reminder(channelid, userid, waiter, reminder, link, emote))
            elif waiter < current_time:
                self.db.execute(f'UPDATE Toggle SET Channel = 0, QuestTime = 0, Timer = 0 WHERE User_ID = {userid}')
                self.db.commit()
        print("Time do to ghost stuff!")
            
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        id = guild.id
        self.db.execute(f'INSERT INTO Admin (Server_ID) VALUES ({id})')
        self.db.commit()
        log = self.client.get_channel(1164544776985653319)
        await log.send(f"A new **server**! {guild.name} with the ID of {id}. ")
        ### Setup msg
        desc = f"This command is to setup {self.client.user.display_name}'s various feeds or pings.\n"
        desc += f"The following can be set up in this server at the moment.\n\n**Functions:**\n"
        desc += f"> * __Changelog__: {self.client.user.display_name}'s updates.\n"
        desc += f"> * Usage: ``changelog [set/remove] [channel id]``\n"
        desc += f"> * __PokéMeow Rare Spawns__: A solid feed for Meow spawns.\n> * Usage: ``rarespawn [set/remove] [channel id]``\n"
     
        _emb = disnake.Embed(title=f"{self.client.user.display_name}'s Setup",description=desc,colour=0x807ba6)
        _emb.set_footer(text=f'Provided by {self.client.user.display_name}',icon_url=f'{self.client.user.avatar}')
        text = f"Thanks for choosing <@{self.client.user.id}>!"
        try:
            default = guild.system_channel
            await default.send(text,embed=_emb)
        except:
            async for entry in guild.audit_logs(action=disnake.AuditLogAction.bot_add):
                if entry.target == self.user:
                    inviter_id = entry.user.id
                    inviter_id = guild.get_member_named(inviter_id)
                    await inviter_id.send(text,embed=_emb)
                    return
            

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        id = guild.id
        self.db.execute(f'DELETE FROM Admin WHERE Server_ID = {id}')
        self.db.commit()
        log = self.client.get_channel(1164544776985653319)
        await log.send(f"One **server** less! {guild.name} with the ID of {id}. ")


    @commands.Cog.listener()
    async def on_member_join(self, member):
        id = member.guild.id
        if id == 825813023716540426: #Paralympic
            desc= f"Welcome to ᵖᵃʳᵃˡʸᵐᵖᶤᶜˢ <@{member.id}>.\nTo get full access to the server, get verified in <#998249646923202610>!\n"
            desc += f"If you are here to join the clan, then please post your `;stats` in <#825836268332122122> and make sure you read the pins in there for clan requirements.\n"
            desc += f"If you're a member of a partnered clan, please head to <#825836268332122122> and use ``;clan``.\n"
            desc += f"Have a read of <#885070641638825984> for information on the server including the rules.\n"
            desc += f"Happy hunting!"
            channel = self.client.get_channel(825836238951022602)
            await channel.send(desc)
        if id == 1227320623567736924: #PokeTour
            # Welcome msg
            desc = f"Welcome to {member.guild.name}, <@{member.id}>!"
            channel = member.guild.system_channel
            await channel.send(desc)
            roles = [1227356364624498760, 1227356782335230002, 1227356761007329330, 1227358972965687335]
            for entry in roles:
                role = member.guild.get_role(entry)
                await member.add_roles(role)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        if guild.id == 1227320623567736924: #PokeTour
            desc = f"We say good-bye to <@{member.id}>, I hope they find inner peace. - {member.id}"
            await member.guild.system_channel.send(desc)
    

    @commands.Cog.listener()
    async def on_message(self, message):
        # This function will be called whenever a message is sent in a server where the bot is a member.
        # You can add your custom logic here.
        if message.author == self.client.user:
            return  # Ignore messages sent by the bot itself.
        meow = 664508672713424926
        #Meow ID & KarpGuru
        karp = 922248409350549564
        celadon = 1080049677518508032
        myself = 352224989367369729
        
        current_time = datetime.datetime.utcnow()
        timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
        
        if message.author.bot and message.author.id != meow and message.author.id != karp and message.author.id != 1209829454667317288 and message.author.id != 865576698137673739:
            return
            
        if "happy" in message.content.lower():
            if "birthday" in message.content.lower():
                if "1161011648585285652" in message.content.lower() or "gengar" in message.content.lower():
                    if current_time.day == 9 and current_time.month == 10:
                        await message.reply(f"Thx <@{message.author.id}>! And happy spooky season! :ghost: ")
                    else:
                        next_bd = datetime.datetime(current_time.year+1, 9,10,tzinfo=current_time.tzinfo)
                        next = next_bd - current_time
                        await message.reply(f"Thx <@{message.author.id}>, but my birthday is October 9th, so in {next.days} days.")
        elif "hbd" in message.content.lower():
            if "1161011648585285652" in message.content.lower() or "gengar" in message.content.lower():
                if current_time.day == 9 and current_time.month == 10:
                    await message.reply(f"Thx <@{message.author.id}>! And happy spooky season! :ghost: ")
                else:
                    next_bd = datetime.datetime(current_time.year+1, 9,10,tzinfo=current_time.tzinfo)
                    next = next_bd - current_time
                    await message.reply(f"Thx <@{message.author.id}>, but my birthday is October 9th, so in {next.days} days.")
                
        if message.content.lower() == "trygoogle":
            await message.delete()
            await message.channel.send("https://tenor.com/bUYzH.gif")
        #Open to every Channel!
        if message.content == "^-^":
            await message.channel.send("https://media.tenor.com/LC5ripTgbHkAAAAC/kyogre-kyogresmile.gif")

        if message.content.lower() == "stfu":
            await message.reply("No u.",allowed_mentions = disnake.AllowedMentions(replied_user=False))


        if message.content.lower() == "lol":
            await message.reply("Rofl.", allowed_mentions = disnake.AllowedMentions(replied_user=False))

        if message.author.id == karp:
            if "our general chat" in message.content.lower():
                username = message.content
                username = username.split(">")[0]
                username = int(username.split("@")[1])
                username = self.client.get_user(username)
                username = username.display_name
                #print(username+" welcomed")
                await message.channel.send("Hey, "+username)
                await message.channel.send("<a:welcome1:1130245046025846814><a:welcome2:1130245098983137323>")
            if "here is some info for new people" in message.content.lower():
                id = message.content.split("<@")[1]
                id = id.split(">")[0]
                desc = f"Hi <@{id}>! Congrats on joining this awesome clan!\nI'm {self.client.user.display_name} and here to help you to grind as easy & efficient as possible!\nYou may know bots like MeowHelper from other servers - don't worry, I'm way more reliable!\n\n"
                desc += f"My main work here is to remind you when your PokéMeow command cooldowns are done - and I can either remind with or without pings.\nIf you want to know more about my functions and command, check out ``mInfo``or </info:1177325264351543447>.\n\n"
                desc += f"Have a good time here! <:GengarHeart:1153729922620215349>"
                emb = await Auction_embed(self.client, title="Welcome!", description=desc).setup_embed()
                await message.channel.send(embed=emb)


        database = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {message.author.id}')
        database = database.fetchone()
        if database:
            if database[4] == 1:
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

        ########Rare Spawn Listener 825958388349272106 #bot-testing channel
        receiver_channel = self.db.execute(f'SELECT * FROM Admin WHERE Server_ID = {message.guild.id}') # rare-spawns
        receiver_channel = receiver_channel.fetchone()
        #print(receiver_channel)
        receiver_channel = int(receiver_channel[4])
        log_channel = 1164544776985653319
        if message.author.id == meow:
            if message.reference:
                ref_msg = await message.channel.fetch_message(message.reference.message_id)
                sender = ref_msg.author
            elif message.interaction:
                sender = message.interaction.author
            announce_channel = self.client.get_channel(receiver_channel)
            log_chn = self.client.get_channel(log_channel)
            if ", your egg is ready to hatch" in message.content.lower():
                if "incubator" in message.content.lower():
                    await message.reply(f"</egg hatch-incubator:1015311084594405485>")
                else:
                    await message.reply(f"</egg hatch:1015311084594405485>")
            if "oh? you found a" in message.content.lower():
                item = message.content.split("found a <:")[1]
                item = item.split(":")[0]
                if item == self.promo_item:
                    await message.reply(f"Oh wow - looks like you've found a promo item! Congratulations!")
            if "won the battle!" in message.content.lower():
                if self.promo_item in message.content.lower():
                    await message.reply(f"Oh wow - looks like you've found a promo item! Congratulations!")
            if "used a code to claim" in message.content:
                monname = message.content.split("**")[1]
                print(monname)
                data = self.db.execute(f'SELECT * FROM Dex WHERE Name = "{monname}"')
                data = data.fetchone()
                #print(data)
                url = data[15]
                #print(url)
                monname = data[1]
                print(monname)
                current_time = message.created_at
                timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
                desc_text = f"\nOriginal message: [Click here]({message.jump_url})\n"
                embed = await Custom_embed(self.client,thumb=url,description=sender.display_name+" just claimed a **"+monname+"** from a code.\n"+desc_text).setup_embed()
                embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                embed.set_author(name=f'{sender.display_name}'" just redeemed a code!", icon_url="https://cdn.discordapp.com/emojis/671852541729832964.webp?size=240&quality=lossless")
                await announce_channel.send(embed=embed)
            if "You ate a" in message.content:
                await asyncio.sleep(3)
                datarem = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {sender.id}')
                datarem = datarem.fetchone()
                if datarem[15] == 1:
                    if datarem[5] == 1:
                        link = '</give fun-item:1015311084812501028>'
                    else:
                        link = ";give"
                    if datarem[6]==0:
                        desc = f'{rem_emotes["remind"]} - <@{sender.id}>, you can now use {link} again.'
                    else:
                        if datarem[5] == 0:
                            link = ""
                        desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["give"]} {link}'
                    
                    if datarem[16] == 0:
                        await message.channel.send(desc, allowed_mentions = disnake.AllowedMentions(users = False))
                    else:
                        await message.channel.send(desc)
                    
            if "s trainer icon!" in message.content:
                iconname = message.content.split("unlocked ")[1]
                icon = iconname.split(":")[2]
                icon = icon.split(">")[0]
                iconname = iconname.split(":")[1]
                iconname = iconname.replace("_"," ")
                iconname = iconname.title()
                authorid = message.content.split("@")[1]
                authorid = int(authorid.split(">")[0])
                user = self.client.get_user(authorid)
                thumburl = "https://cdn.discordapp.com/emojis/"
                icon = str(icon)
                thumburl = thumburl+icon
                thumburl = thumburl+".webp?size=96&quality=lossless"
                print(thumburl)
                desc_text = f"Original message: [Click here]({message.jump_url})\n"
                embed = await Custom_embed(self.client,thumb=thumburl,description="**"+iconname+"** was viciously defeated and dropped their icon.\n"+desc_text).setup_embed()
                embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                embed.set_author(name=f'{self.client.get_user(authorid).display_name}'" just found a new icon!", icon_url="https://cdn.discordapp.com/emojis/766701189260771359.webp?size=96&quality=lossless")
                await announce_channel.send(embed=embed)
                await log_chn.send(user.name+" found an icon")
                await log_chn.send("Its "+iconname)
            if "from completing challenge" in message.content:
                print(f'{sender.display_name} won a chamber.')
                nite = message.content.split("<:")[1]
                item = nite.split(":")[0]
                try:
                    if chambers[item]:
                        print(f'{item}, {chambers[item]}')
                        number = nite.split(":")[1]
                        number = number.split(">")[0]
                        dex = self.db.execute(f'SELECT * FROM Dex WHERE DexID = {chambers[item]}')
                        dex = dex.fetchone()
                        print(dex[1])
                        current_time = message.created_at
                        timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
                        description_text = f"Original message: [Click here]({message.jump_url})\n"
                        embed = disnake.Embed(title=f"{sender.display_name} was able to claim a **{item.capitalize()}**",description=description_text)
                        embed.set_author(name=(f'{sender.display_name}'+" won in a megachamber!"),icon_url=f"https://cdn.discordapp.com/emojis/{number}.webp?size=96&quality=lossless")
                        embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                        embed.set_image(dex[15])
                        await announce_channel.send(embed=embed)
                except Exception as e:
                    print(f"No valid Chamber, its too easy: {e}")
            if message.content:
                #print("Aha, some content")
                if "your catch bot" in message.content.lower():
                    #print("Aha, catchbotting in message")
                    await asyncio.sleep(8)
                    datarem = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {sender.id}')
                    datarem = datarem.fetchone()
                    if datarem[15] == 1:
                        if datarem[5] == 0:
                            link = ";catchbot"
                        else:
                            link = "</catchbot view:1015311084422434824>"
                        if datarem[6] == 0:
                            desc = f'{rem_emotes["remind"]} - <@{sender.id}>, you can now use your {link} again.'
                            #desc = desc[::-1]
                        else:
                            if datarem[5] == 0:
                                link = ""
                            desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["catchbot"]} {link}'
                        if datarem[16] == 0:
                            await message.channel.send(desc, allowed_mentions = disnake.AllowedMentions(users = False))
                        else:
                            await message.channel.send(desc)
                if "holding an egg" in message.content.lower() or "egg is not ready" in message.content.lower():
                    await asyncio.sleep(5)
                    datarem = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {sender.id}')
                    datarem = datarem.fetchall()
                    if datarem[0][15] == 1:
                        if datarem[0][6] == 0:
                            desc = f'{rem_emotes["remind"]} - <@{sender.id}>, you can now use ;egg again.'
                            #desc = desc[::-1]
                        else:
                            desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["egg"]}'
                        await message.channel.send(desc, allowed_mentions = disnake.AllowedMentions(users = False))
                    elif datarem[0][15] == 2:
                        if datarem[0][6] == 0:
                            desc = f'{rem_emotes["remind"]} - <@{sender.id}>, you can now use ;egg again.'
                            #desc = desc[::-1]
                        else:
                            desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["egg"]}'
                        await message.channel.send(desc)           
            if (len(message.embeds) > 0):
                _embed = message.embeds[0]
                color = _embed.color
                #print(_embed.author.name)
                Rare_Spawned = ["Event", "Legendary", "Shiny", "Golden"]
                if _embed.author:
                    if "Special Golden" in _embed.author.name:
                        try:
                            item = _embed.description.split("3x <:")[1]
                            item = item.split(":")[0]
                            if item != self.promo_item:
                                print(f"New Promo Item: {item}")
                                self.promo_item = item
                                conn = await self.get_db_connection()
                                async with conn.cursor() as cursor:
                                    await cursor.execute(f"UPDATE Stuff SET Current_Item = '{item}'")
                                    await conn.commit()
                                    await conn.ensure_closed()
                        except Exception as e:
                            print(f";Promo Error: {e}")
                            print(Exception.args)
                    if "Research Lab" in _embed.author.name:
                        try:
                            desc = _embed.description
                            current_points = desc.split("Research Points**: ")[1]
                            current_points = int((current_points.split("**")[0]).replace(",", ""))
                            valuables = desc.split("(")
                            nuggets = int(valuables[1].split(")")[0])
                            big_nuggets = int(valuables[2].split(")")[0])
                            pearls = int(valuables[3].split(")")[0])
                            big_pearls = int(valuables[4].split(")")[0])
                            stars = int(valuables[5].split(")")[0])
                            comet = int(valuables[6].split(")")[0])
                            if nuggets > 10:
                                big_nuggets = big_nuggets + (nuggets//10)
                                nuggets = nuggets%10
                            if pearls > 10:
                                big_pearls = big_pearls + (pearls//10)
                                pearls = pearls%10
                            coins = (nuggets*2000)+(pearls*2000)+(big_nuggets*30000)+(big_pearls*30000)+(stars*15000)+(comet*60000)
                            rp = (nuggets*1)+(pearls*1)+(big_nuggets*15)+(big_pearls*15)+(stars*10)+(comet*25)
                            description_text = f'If you exchange all your Nuggets for Big Nuggets and Pearls for Big Pearls beforehand, you should get\n\nPokeCoins: {coins:,} {emote_list["coins"]}\nRP: {rp:,} {emote_list["rp"]}\n\nTotal RP after exchange: {(current_points+rp):,} {emote_list["rp"]}'
                            footer_text = f"This calculation does not check for owned relics or fossils."
                            embed = disnake.Embed(title="Your current exchangeable valuables:",timestamp=current_time,color=embed_color, description=description_text)
                            embed.set_author(name="Research Calculation Centre") 
                            embed.set_footer(text=footer_text)
                            embed.set_thumbnail(url="https://media.discordapp.net/attachments/1088391118384807997/1308177781703708684/IMG_9481.jpg?ex=673cfeff&is=673bad7f&hm=42cb718ff77260db27caaf10c8a2dd3037ff0b5f25418d0c2b6f50cb1b2c72d1&")
                            await message.reply(embed=embed)
                        except Exception as e:
                            print(f"Research Lab Error: {e}")
                    if "Global Market " in _embed.author.name:
                        print("Market going on")
                        try:
                            if _embed.footer.text:
                                if "#" in _embed.footer.text:
                                    number = _embed.footer.text.split("#")[1]
                                    number = int(number.split(" ")[0])
                                    #print(number)
                                    datdex = self.db.execute(f'SELECT * FROM Dex WHERE DexID = {number}')
                                    datdex = datdex.fetchone()
                                    #print(datdex[0][1])
                                    current_time = int(datetime.datetime.timestamp(datetime.datetime.now()))
                                    if "amount for sale" in _embed.description.lower():
                                        price = _embed.description.split("PokeCoin")[2]
                                        lowprice = price.split(" ")[1]
                                        lowprice = int(lowprice.replace(",", ""))
                                        amount = int(price.split(" ")[5])
                                    else:
                                        for entry in _embed.fields:
                                            if entry.name == "Price each":
                                                #print(entry.value)
                                                price = entry.value.split("`")[1]
                                                #print(price)
                                                lowprice = int(price.replace(",", ""))
                                            if entry.name == "Amount Remaining":
                                                amount = entry.value.split("`")[1]
                                                amount = int((amount.split(" ")[0]).replace(",", ""))
                                    #print(lowprice)
                                    #print(amount)
                                    self.db.execute(f'UPDATE Dex Set LowestVal = {lowprice}, UpdateTime = {current_time}, Amount = {amount} WHERE DexID = {datdex[0]}')
                                    self.db.commit()
                        except Exception as e:
                            asyncio.create_task(self.errorlog(e, message=message, author=sender))
                        await asyncio.sleep(3)
                        datarem = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {sender.id}')
                        datarem = datarem.fetchone()
                        if datarem[15] == 1:
                            if datarem[5] == 0:
                                link = ";market"
                            else:
                                link = "</market view:1015311085307445255>"
                            if datarem[6] == 0:
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}>, you can now use {link} again.'
                                #desc = desc[::-1]
                            else:
                                if datarem[5] == 0:
                                    link =""
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["market"]} {link}'
                            if datarem[16] == 0:
                                await message.channel.send(desc, allowed_mentions = disnake.AllowedMentions(users = False))
                            else:
                                await message.channel.send(desc)
                    if "Counters" in _embed.author.name:
                        if _embed.fields:
                            for field in _embed.fields:
                                if field.name == "Counter • Pokemon/Thing":
                                    i=0
                                    eventshiny = field.value.split(" • ")[i]
                                    eventshiny = eventshiny.replace(",", "")
                                    eventshiny = int(eventshiny)
                                    i+=1
                                    print(eventshiny)
                                    fullodds = field.value.split(" • ")[i]
                                    fullodds = fullodds.split("\n")[1]
                                    fullodds = fullodds.replace(",", "")
                                    i+=1
                                    fullodds = int(fullodds)
                                    print(fullodds)
                                    legendary = field.value.split(" • ")[i]
                                    legendary = legendary.split("\n")[1]
                                    legendary = legendary.replace(",", "")
                                    i+=1
                                    legendary = int(legendary)
                                    print(legendary)
                                    item = field.value.split(" • ")[i]
                                    item = item.split("\n")[1]
                                    item = item.replace(",", "")
                                    i+=1
                                    item = int(item)
                                    print(fullodds)
                                    fgolden = field.value.split(" • ")[i]
                                    fgolden = fgolden.split("\n")[1]
                                    fgolden = fgolden.replace(",", "")
                                    i+=1
                                    fgolden = int(fgolden)
                                    print(fgolden)
                                    fshiny = field.value.split(" • ")[i]
                                    fshiny = fshiny.split("\n")[1]
                                    fshiny = fshiny.replace(",", "")
                                    i+=1
                                    fshiny = int(fshiny)
                                    print(fshiny)
                                    flegend= field.value.split(" • ")[i]
                                    flegend = flegend.split("\n")[1]
                                    flegend = flegend.replace(",", "")
                                    i+=1
                                    flegend = int(flegend)
                                    print(flegend)
                                    egolden = field.value.split(" • ")[i]
                                    egolden = egolden.split("\n")[1]
                                    egolden = egolden.replace(",", "")
                                    i+=1
                                    egolden = int(egolden)
                                    print(egolden)
                                    eshiny = field.value.split(" • ")[i]
                                    eshiny = eshiny.split("\n")[1]
                                    eshiny = eshiny.replace(",", "")
                                    i+=1
                                    eshiny = int(eshiny)
                                    print(eshiny)
                                    elegend = field.value.split(" • ")[i]
                                    elegend = elegend.split("\n")[1]
                                    elegend = elegend.replace(",", "")
                                    i+=1
                                    elegend = int(elegend)
                                    print(elegend)
                                    icon = field.value.split(" • ")[i]
                                    icon = icon.split("\n")[1]
                                    icon = icon.replace(",", "")
                                    i+=1
                                    icon = int(icon)
                                    print(icon)
                                    data = self.db.execute(f'SELECT * FROM Counter WHERE User_ID = ({sender.id})')
                                    data = data.fetchall()
                                    if data:
                                        print("Fetched it?")
                                        self.db.execute(f'UPDATE Counter SET event = ({eventshiny}), fullodd = {fullodds}, legendary = {legendary}, item = {item}, goldenfish = {fgolden}, shinyfish = {fshiny}, legendaryfish = {flegend}, goldenexp = {egolden}, shinyexp = {eshiny}, legendaryexp = {elegend}, icon = {icon} WHERE User_ID = ({sender.id})')
                                        self.db.commit()
                                    else:
                                        
                                        self.db.execute(f'INSERT INTO Counter VALUES ({sender.id},{eventshiny},{fullodds},{legendary},{item},{fgolden},{fshiny},{flegend},{egolden},{eshiny},{elegend},{icon})')
                                        self.db.commit()
                                        print("New in")

  
                if "found a wild" in message.content:
                    log_channel = self.client.get_channel(log_channel)
                    if (len(message.embeds) > 0):
                        #Check if reaction or interaction
                        
                            #print(sender)
                        ## Checking for a User in Database, if not, initializing
                        databaserep = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID={sender.id}')
                        databaserep = databaserep.fetchall()
                        if not databaserep:
                            self.db.execute(f'INSERT INTO Toggle (USER_ID) VALUES ({sender.id})')
                            self.db.commit()
                            await log_channel.send(str(sender)+" is now in the database. "+str(sender.id))
                            await message.channel.send(f"Is this your first visit here? Welcome! I've added you to my database. Check ``/info`` for more info.")
                        Rare_Spawns = ["Event", "Legendary", "Shiny","Golden"]
                        _embed = message.embeds[0]
                        data = self.db.execute(f'SELECT * FROM Dex WHERE Img_url = "{_embed.image.url}"')
                        data = data.fetchone()
                        ######## Repel/Grazz notifier
                        #print(database)
                        if databaserep:
                            if databaserep[0][3] == 1:
                                # boost = "boost expired!"
                                # hey = "Hey, your"
                                # boost = boost[::-1]
                                # hey = hey[::-1]
                                # user = f'<@{str(sender.id)}>'
                                #print("repel activated"+str(database[0][3]))
                                if "super_repel" in message.content and "boost" in message.content:
                                    if databaserep[0][6]==0:
                                        #await message.channel.send(f"{boost} <:superrepel:1165230878474113025> {hey} {user}")
                                        desc=f'{rem_emotes["remind"]} - <@{sender.id}> Hey, your {rem_emotes["superrepel"]} boost expired!'
                                    else:
                                        desc=f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["superrepel"]}'
                                    await message.channel.send(desc)
                                if "max_repel" in message.content and "boost" in message.content:
                                    if databaserep[0][6]==0:
                                        #await message.channel.send(f"{boost} <:superrepel:1165230878474113025> {hey} {user}")
                                        desc=f'{rem_emotes["remind"]} - <@{sender.id}> Hey, your {rem_emotes["maxrepel"]} boost expired!'
                                    else:
                                        desc=f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["maxrepel"]}'
                                    await message.channel.send(desc)
                                if ":repel" in message.content and "boost" in message.content:
                                    if databaserep[0][6]==0:
                                        #await message.channel.send(f"{boost} <:superrepel:1165230878474113025> {hey} {user}")
                                        desc=f'{rem_emotes["remind"]} - <@{sender.id}> Hey, your {rem_emotes["repel"]} boost expired!'
                                    else:
                                        desc=f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["repel"]}'
                                    await message.channel.send(desc)
                                if ":fluffy" in message.content:
                                    if databaserep[0][6]==0:
                                        #await message.channel.send(f"{boost} <:superrepel:1165230878474113025> {hey} {user}")
                                        desc=f'{rem_emotes["remind"]} - <@{sender.id}> Hey, your {rem_emotes["fluffy"]} boost expired!'
                                    else:
                                        desc=f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["fluffy"]}'
                                    await message.channel.send(desc)
                                if ":pokedoll" in message.content:
                                    if databaserep[0][6]==0:
                                        #await message.channel.send(f"{boost} <:superrepel:1165230878474113025> {hey} {user}")
                                        desc=f'{rem_emotes["remind"]} - <@{sender.id}> Hey, your {rem_emotes["pokedoll"]} boost expired!'
                                    else:
                                        desc=f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["pokedoll"]}'
                                    await message.channel.send(desc)
                                if ":poketoy" in message.content:
                                    if databaserep[0][6]==0:
                                        #await message.channel.send(f"{boost} <:superrepel:1165230878474113025> {hey} {user}")
                                        desc=f'{rem_emotes["remind"]} - <@{sender.id}> Hey, your {rem_emotes["poketoy"]} boost expired!'
                                    else:
                                        desc=f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["poketoy"]}'
                                    await message.channel.send(desc)
                            else: return
                            if databaserep[0][2] == 1:
                                # boost = "boost expired!"
                                # hey = "Hey, your"
                                # boost = boost[::-1]
                                # hey = hey[::-1]
                                # user = f'<@{str(sender.id)}>'
                                #print("grazz activated"+str(database[0][2]))
                                if "goldenrazz" in message.content and "boost" in message.content:
                                    if databaserep[0][6]==0:
                                        #await message.channel.send(f"{boost} <:superrepel:1165230878474113025> {hey} {user}")
                                        desc=f'{rem_emotes["remind"]} - <@{sender.id}> Hey, your {rem_emotes["grazz"]} boost expired!'
                                    else:
                                        desc=f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["grazz"]}'
                                    await message.channel.send(desc)
                                if "honey" in message.content and "boost" in message.content:
                                    if databaserep[0][6]==0:
                                        #await message.channel.send(f"{boost} <:superrepel:1165230878474113025> {hey} {user}")
                                        desc=f'{rem_emotes["remind"]} - <@{sender.id}> Hey, your {rem_emotes["honey"]} boost expired!'
                                    else:
                                        desc=f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["honey"]}'
                                    await message.channel.send(desc)
                            else: return

                    
                        await asyncio.sleep(8.8)
                        datarem = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {sender.id}')
                        datarem = datarem.fetchone()
                        if datarem[10] == 1:
                            # desc = "again."
                            # desc = desc[::-1]
                            # desc1=str(sender.display_name)+", you can now use "
                            # desc1=desc1[::-1]
                            # await message.channel.send(f"{desc} </pokemon:1015311085441654824> {desc1}")
                            if datarem[5] == 0:
                                link = ";p"
                            else:
                                link = "</pokemon:1015311085441654824>"
                            if datarem[6]==0:
                                desc=f'{rem_emotes["remind"]} - <@{sender.id}>, you can now use {link} again.'
                            else:
                                if datarem[5] == 0:
                                    link = ""
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["spawn"]} {link}'
                            if datarem[16] == 1:
                                await message.channel.send(desc)
                            else:
                                await message.channel.send(desc, allowed_mentions = disnake.AllowedMentions(users = False))
                if _embed.description:
                    if "cast a" in _embed.description:
                        await asyncio.sleep(24.2)
                        datarem = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {sender.id}')
                        datarem = datarem.fetchone()
                        if datarem[11] == 1:
                            if datarem[5] == 0:
                                link = ";fish"
                            else:
                                link = "</fish spawn:1015311084812501026>"
                            if datarem[6]==0:
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}>, you can use {link} again.'
                            else:
                                if datarem[5] == 0:
                                    link = ""
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["fish"]} {link}'
                            if datarem[16] == 1:
                                await message.channel.send(desc)
                            else:
                                await message.channel.send(desc, allowed_mentions = disnake.AllowedMentions(users = False))
                    
                    if "from a swap" in _embed.description:
                        await asyncio.sleep(6)
                        datarem = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {sender.id}')
                        datarem = datarem.fetchall()
                        if datarem[0][15] == 1:
                            
                            if datarem[0][6]==0:
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}>, you can now ;swap again.'
                            else:
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["swap"]}'
                            await message.channel.send(desc, allowed_mentions = disnake.AllowedMentions(users = False))
                        elif datarem[0][15] == 2:
                            if datarem[0][6]==0:
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}>, you can now ;swap again.'
                            else:
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["swap"]}'
                            await message.channel.send(desc)
                if _embed.title:
                    if "quests for rewards!" in _embed.title:
                        #print("Quest screen from "+sender.display_name)
                        datarem = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {sender.id}')
                        datarem = datarem.fetchone()
                        await asyncio.sleep(6)
                        if datarem[13] == 1:
                            if datarem[5] == 0:
                                link = ";quest"
                            else:
                                link = "</quest info:1015311085517156475>"
                            if datarem[6]==0:
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}>, you can now check your {link} again.'
                            else:
                                if datarem[5] == 0:
                                    link =""
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["quest"]} {link}'
                            if datarem[16] == 0:
                                await message.channel.send(desc, allowed_mentions = disnake.AllowedMentions(users = False))
                            else:
                                await message.channel.send(desc)
                        if _embed.footer:
                            if "Next quest in" in _embed.footer.text:
                                #print("Oh, a quest?")
                                msg = _embed.footer.text
                                msg = msg.split(": ")[1]
                                #print(msg)
                                hours = int(msg.split(" H")[0])*60*60
                                #print(hours)
                                minutes = msg.split("H ")[1]
                                minutes = int(minutes.split(" M")[0])*60
                                #print(minutes)
                                seconds = msg.split("M ")[1]
                                seconds = int(seconds.split(" S")[0])
                                #print(seconds)
                                waiter = hours+minutes+seconds
                                #print(waiter)
                                datarem = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {sender.id}')
                                datarem = datarem.fetchone()
                                if datarem[14] != 0:
                                    if datarem[7] != 0:
                                        print("Already a timer running")
                                    else:
                                        print("Oh, a new timer")
                                        q_time = int(datetime.datetime.timestamp(datetime.datetime.now()))-8
                                        print(q_time)
                                        q_time = q_time+waiter
                                        channelid = message.channel.id
                                        self.db.execute(f'UPDATE Toggle SET QuestTime = {q_time}, Channel = {channelid} WHERE User_ID = {sender.id}')
                                        self.db.commit()
                                        q_time = str(q_time)
                                        if datarem[14] == 1:
                                            remind = 1
                                        elif datarem[14] == 2:
                                            remind = 2
                                        if datarem[6] == 0:
                                            emote = 0
                                        else: 
                                            emote = 1
                                        if datarem[5] == 0:
                                            link = 0
                                        else:
                                            link = 1
                                        if datarem[9] == 0:
                                            minutes = int(waiter/60)
                                            if datarem[6] == 1:
                                                desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["quest"]}:alarm_clock::white_check_mark:'
                                            elif datarem[6] == 0:
                                                desc = str(sender.display_name)+", I've set a timer for "+str(minutes)+" minutes."
                                            if datarem[14] == 1:
                                                await message.channel.send(desc, allowed_mentions= disnake.AllowedMentions(users=False))
                                            elif datarem[14] == 2:
                                                await message.channel.send(desc)
                                            await asyncio.create_task(self._quest_reminder(channelid, sender.id, waiter,remind, link, emote))
                        
                if _embed.author.name:
                    if "catchbot" in _embed.author.name.lower():
                        #print("Aha, catchbotting in name")
                        await asyncio.sleep(5)
                        datarem = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {sender.id}')
                        datarem = datarem.fetchone()
                        if datarem[15] == 1:
                            if datarem[5] == 0:
                                link = ";catchbot"
                            else:
                                link = "</catchbot view:1015311084422434824>"
                            if datarem[6] == 0:
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}>, you can now use your {link} again.'
                                #desc = desc[::-1]
                            else:
                                if datarem[5] == 0:
                                    link = ""
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["catchbot"]} {link}'
                            if datarem[16] == 0:
                                await message.channel.send(desc, allowed_mentions = disnake.AllowedMentions(users = False))
                            else:
                                await message.channel.send(desc)
                
                
                if _embed.footer.text:
                    if "current event ends: " in _embed.footer.text.lower():
                        for field in _embed.fields:
                            if "event-exclusives" in field.name.lower():
                                print(field)
                                mons = field.value.split("\n")
                                names = {}
                                for entry in mons:
                                    name = entry.split(" ")[1]
                                    id = entry.split(":")[1]
                                    names.update({id:name})
                                conn = await self.get_db_connection()
                                async with conn.cursor() as cursor:
                                    await cursor.execute("DELETE FROM Exclusives")
                                    await conn.commit()
                                    for entry in names:
                                        await cursor.execute(f"INSERT INTO Exclusives VALUES ({entry},'{names[entry]}')")
                                    await conn.commit()
                                    await conn.ensure_closed()
                                await self.load_excl()
                    if "battle starts in" in _embed.footer.text.lower():
                        #print("Aha, battling.")
                        if "xmas steven** to a battle" in _embed.description.lower():
                            asyncio.create_task(Modules.adamannpc(self, message))
                        #asyncio.create_task(Modules.darktest(self, message))
                        await asyncio.sleep(59)
                        datarem = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {sender.id}')
                        datarem = datarem.fetchone()
                        if datarem[12] == 1:
                            if datarem[5] == 0:
                                link = ";battle"
                            else:
                                link = "</battle:1015311084422434819>"
                            if datarem[6]==0:
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}>, you can now {link} again.'
                            else:
                                if datarem[5] == 0:
                                    link = ""
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["battle"]} {link}'
                            if datarem[16] == 0:
                                await message.channel.send(desc, allowed_mentions = disnake.AllowedMentions(users = False))
                            else:
                                await message.channel.send(desc)
                    if "buddy help" in _embed.footer.text.lower() or "move help" in _embed.footer.text.lower():
                        #print("Buddy Window")
                        await asyncio.sleep(5)
                        datarem = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {sender.id}')
                        datarem = datarem.fetchone()
                        if datarem[15] == 1:
                            if datarem[5] == 0:
                                if "move" in _embed.footer.text.lower():
                                    link = ";moves"
                                else:
                                    link = ";buddy"
                            else:
                                if "move" in _embed.footer.text.lower():
                                    link = "</moves view:1015311085441654817>"
                                else:
                                    link = "</buddy current-buddy:1015311084422434823>"
                            #print(link)
                            if datarem[6]==0:
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}>, you can now use {link} again.'
                            else:
                                if datarem[5] == 0:
                                    link =""
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["buddy"]} {link}'
                            if datarem[16] == 0:
                                await message.channel.send(desc, allowed_mentions = disnake.AllowedMentions(users = False))
                            else:
                                await message.channel.send(desc)

                        

                if _embed.author.name:
                    if "Egg Centre" in _embed.author.name:
                        await asyncio.sleep(5)
                        datarem = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {sender.id}')
                        datarem = datarem.fetchone()
                        if datarem[15] == 1:
                            if datarem[5] == 0:
                                link = ";egg"
                            else:
                                link = "</egg status:1015311084594405485>"
                            if datarem[6]==0:
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}>, you can now use {link} again.'
                            else:
                                if datarem[5] == 0:
                                    link=""
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["egg"]} {link}'
                            if datarem[16] == 0:
                                await message.channel.send(desc, allowed_mentions = disnake.AllowedMentions(users = False))
                            else:
                                await message.channel.send(desc)
                    if "hatched" in _embed.author.name:
                        if message.reference:
                            ref_msg = await message.channel.fetch_message(message.reference.message_id)
                            if "incubator" in ref_msg.content:
                                await message.reply(f"</egg use-incubator:1015311084594405485>")
                            else:
                                await message.reply(f"</egg hold:1015311084594405485>")
                        elif message.interaction:
                            ref_msg = message.interaction
                            if "incubator" in ref_msg.name:
                                await message.reply(f"</egg use-incubator:1015311084594405485>")
                            else:
                                await message.reply(f"</egg hold:1015311084594405485>")
                        data_egg = self.db.execute(f'SELECT * FROM Dex WHERE Img_url = "{_embed.image.url}"')
                        data_egg = data_egg.fetchone()
                        sender = ref_msg.author
                        raremon = poke_rarity[(data_egg[14])]
                        description_text = f"Original message: [Click here]({message.jump_url})\n"
                        #print(Rare_Spawned)
                        #Rare_Spawned = ["Golden","Event", "Legendary", "Shiny", "Rare", "SuperRare"]
                        if data_egg[14] in Rare_Spawned or str(data_egg[0]) in eggexcl:
                            print("Its in the one list!")
                            print(str(data_egg[0]))
                            embed = disnake.Embed(title=raremon+" **"+data_egg[1]+"** \nDex: #"+str(data_egg[0]), color=color,description=description_text)
                            embed.set_author(name=(sender.display_name+" just hatched an exclusive:"),icon_url="https://cdn.discordapp.com/emojis/689325070015135745.gif?size=96&quality=lossless")
                            embed.set_image(_embed.image.url)
                            embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                            await announce_channel.send(embed=embed)

                        await asyncio.sleep(5)
                        datarem = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {sender.id}')
                        datarem = datarem.fetchone()
                        if datarem[15] == 1:
                            if datarem[5] == 0:
                                link = ";egg"
                            else:
                                link = "</egg status:1015311084594405485>"
                            if datarem[6]==0:
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}>, you can now use {link} again.'
                            else:
                                if datarem[5] == 0:
                                    link=""
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["egg"]} {link}'
                            if datarem[16] == 0:
                                await message.channel.send(desc, allowed_mentions = disnake.AllowedMentions(users = False))
                            else:
                                await message.channel.send(desc)

                        
                    if "opened " in _embed.author.name:
                        if _embed.image:
                            #print("Theres a spawn")
                            data_box = self.db.execute(f'SELECT * FROM Dex WHERE Img_url = "{_embed.image.url}"')
                            data_box = data_box.fetchall()
                            sender = ref_msg.author.display_name
                            #Rare_Spawned = ["Event", "Legendary", "Shiny", "Rare", "SuperRare","Common","Uncommon","Golden"]
                            raremon = poke_rarity[(data_box[0][14])]
                            if data_box[0][14] in Rare_Spawned:
                                #print("Rare enough")
                                description_text = " "
                                if "Pokemon received" in _embed.description:
                                    mons = _embed.description.split("total):\n")[1]
                                    #print(mons)
                                    mons = mons.split(">")
                                    unused = mons.pop()
                                    #print(mons)
                                    description_text = "Pokemon received:\n"
                                    for entry in mons:
                                        monid = entry.split(":")[1]
                                        #print(monid)
                                        monid = int(monid)
                                        dex = self.dv.execute(f'SELECT * FROM SpawnEmotes WHERE DexID = {monid}')
                                        dex = dex.fetchone()
                                        description_text += f'<:{monid}:{dex[3]}> '
                                        
                                description_text += f"\nOriginal message: [Click here]({message.jump_url})\n"
                                embed = disnake.Embed(title=raremon+" **"+data_box[0][1]+"** \nDex: #"+str(data_box[0][0]), color=color,description=description_text)
                                embed.set_author(name=(sender+" just unboxed a:"),icon_url="https://cdn.discordapp.com/emojis/784865588207157259.gif?size=96&quality=lossless")
                                embed.set_image(_embed.image.url)
                                embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                                await announce_channel.send(embed=embed)
                    if "PokeMeow Swaps" in _embed.author.name:
                        data_sw = self.db.execute(f'SELECT * FROM Dex WHERE Img_url = "{_embed.image.url}"')
                        data_sw = data_sw.fetchone()
                        sender = ref_msg.author.display_name
                        raremon = poke_rarity[(data_sw[14])]
                        #Rare_Spawned = ["Event", "Shiny", "Legendary", "SuperRare", "Rare", "Uncommon", "Common","Golden"]
                        description_text = f"Original message: [Click here]({message.jump_url})\n"
                        if data_sw[14] in Rare_Spawned:
                            embed = disnake.Embed(title=raremon+" **"+data_sw[1]+"** \nDex: #"+str(data_sw[0]), color=color,description=description_text)
                            embed.set_author(name=(sender+" just swapped for a:"),icon_url="https://cdn.discordapp.com/emojis/869901886080315392.webp?size=96&quality=lossless")
                            embed.set_image(_embed.image.url)
                            embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                            await announce_channel.send(embed=embed)
                if _embed.description:
                    if message.reference:
                        ref_msg = await message.channel.fetch_message(message.reference.message_id)
                    elif message.interaction:
                        ref_msg = message.interaction
                    if "claimed a <:Golden" in _embed.description:
                        data_pr = self.db.execute(f'SELECT * FROM Dex WHERE Img_url = "{_embed.image.url}"')
                        data_pr = data_pr.fetchall()
                        logging = 1083131761451606096
                        logging = self.client.get_channel(logging)
                        try:
                            await logging.send(embed=message.embed)
                        except:
                            logging.send("NO message to log")
                        try:
                            await logging.send(_embed.description)
                        except:
                            logging.send("How's there no description???")
                        #print(data_pr[0][14])
                        raremon = poke_rarity[(data_pr[0][14])]
                        description_text = f"Original message: [Click here]({message.jump_url})\n"
                        embed = disnake.Embed(title=raremon+" **"+data_pr[0][1]+"** \nDex: #"+str(data_pr[0][0]), color=color,description=description_text)
                        embed.set_author(name=(f'{sender.display_name}'+" just claimed a:"),icon_url="https://cdn.discordapp.com/emojis/676623920711073793.webp?size=96&quality=lossless")
                        embed.set_image(_embed.image.url)
                        embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                        await announce_channel.send(embed=embed)
                    if "returned with" in _embed.description:
                        # await message.channel.send(_embed.description)
                        description_text = f"Original message: [Click here]({message.jump_url})\n"
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
                            embed.set_author(name=(sender+"'s catchbot brought a:"),icon_url="https://cdn.discordapp.com/emojis/1167818560752603196.webp?size=96&quality=lossless")
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
        log = self.client.get_channel(log_channel)
        if message.author.id == meow:
            if (len(message.embeds) > 0):
                _embed=message.embeds[0]
                if message.reference:
                    try:
                        ref_msg = await message.channel.fetch_message(message.reference.message_id)  # Command with ;
                        sender = ref_msg.author
                        #print("Ref")
                    except:
                        ref_msg = message.interaction #Command with /
                        sender = ref_msg.author
                if _embed.description:
                    try:
                        if "version" in _embed.description:
                            #print("Version in it")
                            dex=_embed.author.name.split(" #")[1]
                            #print(dex)
                            name=_embed.author.name.split(" #")[0]
                            #print(name)
                            try:
                                data = self.db.execute(f'SELECT * FROM Dex WHERE DexID = {dex}')
                                data = data.fetchone()
                                #await log.send(data)
                                val = data[17]
                                time = data[18]
                                amount = data[19]
                            except:
                                #await log.send(data)
                                val = 0
                                time = 0
                                amount = 0
                            for field in _embed.fields:
                                if field.name == "Dex Number":
                                    #print(field.value)
                                    region = field.value.split("> ")[1]
                                    #print(region)
                                    region = region.split(" ")[0]
                                    #print(region)
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
                            self.db.execute(f'INSERT or REPLACE INTO Dex VALUES ({dex},"{name}","{type1_semi}","{type2_semi}",{b_hp},{b_atk},{b_def},{b_spatk},{b_spdef},{b_spd},{legendary},{shiny},{golden},{mega},"{rarity}","{imageurl}","{region}",{val},{time},{amount})')
                            self.db.commit()
                            #print("Its in the dex now")
                    except Exception as e: 
                        print("Dex for db: ")
                        print(e)
                
                    try:
                        if "version" in _embed.description:
                            _embed=message.embeds[0]
                            dex=_embed.author.name.split("#")[1]
                            #print(dex)
                            dexdat = self.db.execute(f'SELECT * FROM Dex WHERE DexID = {dex}')
                            dexdat = dexdat.fetchall()
                            if dexdat[0][17] >=2:
                                #print("Was updated.")
                                lowest = f'{dexdat[0][17]:,}'
                                #print(lowest)
                                amount = f'{dexdat[0][19]:,}'
                                #print(amount)
                                time = str(dexdat[0][18])
                                #print(time)
                                msg = "Lowest Price: "+lowest+"\nAmount: "+amount+"\nLast Update: <t:"+time+":f>"
                                #print(msg)
                                thumb = _embed.thumbnail.url
                                embed = await Custom_embed(self.client,title=dexdat[0][1]+" #"+str(dexdat[0][0]),description=msg,thumb=thumb).setup_embed()
                                await message.channel.send(embed=embed)
                    except Exception as e: 
                        dex=_embed.author.name
                        print("Market after dex: "+str(dex)+" - "+sender.display_name)
                        print(e)
        # Only works in specific channels!
        # channel_ids = [825817765432131615, 825813023716540429, 890255606219431946, 1161018942555422792, 827510854467584002]
        # if message.channel.id in channel_ids:
    
            

                
                

#------------------------------------- Testing area---------------------------------------------------------------------------------------------#


#1037323228961579049     825958388349272106 bot testing
        channel_ids = [1083131761451606096, 827510854467584002] #test-spawns
        receiver_channel = 1211296331717410856 #debug
        if message.channel.id == receiver_channel:
            if message.author.id == meow:
                await message.channel.send("Message received: "+message.author.display_name)
                log = self.client.get_channel(receiver_channel)
                print("message")
                if (len(message.embeds) > 0):
                    print("embed")
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
                        await message.channel.send("Thumbnail:")
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


def setup(client):
    client.add_cog(Listener(client))
