import random
import disnake
from disnake.ext import commands
import asyncio
import re
import main
from sqlite3 import connect
from main import client
from utility.rarity_db import poke_rarity, chambers
from utility.egglist import eggexcl
from utility.drop_chance import drop_pos, buyin
from utility.info_dict import rem_emotes
import datetime
from utility.embed import Custom_embed

# Zeichen zum Kopieren: [ ] { }

class Listener(commands.Cog):


    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")
        self.dv = connect("dataverse.db")
    
    async def _quest_reminder(self,channelid, user_id, waiter,reminder):
        print(f"quest_reminder started for {user_id} waiting for {waiter} seconds.")
        channel = self.client.get_channel(channelid)
        self.db.execute(f'UPDATE Toggle SET Timer = 1 WHERE User_ID = {user_id}')
        self.db.commit()
        await asyncio.sleep(waiter)
        print("slept enough.")
        if reminder == 1:
            await channel.send(f'{rem_emotes["remind"]} - <@{user_id}> , your next quest is ready!', allowed_mentions = disnake.AllowedMentions(users=False))
        elif reminder == 2:
            await channel.send(f'{rem_emotes["remind"]} - <@{user_id}>, your next quest is ready!')
        elif reminder == 3:
            await channel.send(f'{rem_emotes["remind"]} - <@{user_id}> {rem_emotes["next"]}{rem_emotes["quest"]}', allowed_mentions= disnake.AllowedMentions(users=False))
        elif reminder == 4:
            await channel.send(f'{rem_emotes["remind"]} - <@{user_id}> {rem_emotes["next"]}{rem_emotes["quest"]}')
        self.db.execute(f'UPDATE Toggle SET QuestTime = 0, Channel = 0, Timer = 0 WHERE User_ID = {user_id}')
        self.db.commit()

    async def _psycord_team(self):
        last = self.db.execute(f'SELECT TeamUpdate FROM Admin WHERE Server_ID = 825813023716540426')
        last = last.fetchone()
        last = last[0]
        print(f'Last Psycord Team Update: {last}')
        if (last+608400)>int(round(datetime.datetime.timestamp(datetime.datetime.utcnow()))+3600):
            waiter = (last+608400)-int(round(datetime.datetime.timestamp(datetime.datetime.utcnow()))+3600)
            print(f'Not ready, sleeping for {waiter}')
            await asyncio.sleep(waiter)
            channel = self.client.get_channel(1201300833304854538)
            await channel.send(f"<@&1199086710659760189>\nPlease use ``/team members`` in <#1201300833304854538> and scroll through the sites for the leaderboard.")
            self.db.execute(f'UPDATE Admin SET TeamUpdate = {last+608400} WHERE Server_ID = 825813023716540426')
            self.db.commit()
        else:
            channel = self.client.get_channel(1201300833304854538)
            await channel.send(f"<@&1199086710659760189>\nPlease use ``/team members`` in <#1201300833304854538> and scroll through the sites for the leaderboard.")

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
                print(channels)
                for entry in channels:
                    print(entry)
                    entry = int(entry[0])
                    channel = self.client.get_channel(entry)
                    await channel.send(f"Time for a new changelog! Get ready:\n```\n{file_content}\n```\nAnd that's all for today!")
                with open("changelog_old.txt",'r') as file:
                    old_content = file.read()
                    with open("changelog_old.txt", "w") as file:
                        old_content += f"\n\n{timestamp}\n{file_content}"
                        file.write(old_content)
                open("changelog.txt", "w")
                pass
                
            else:
               exit
        except FileNotFoundError:
            await log.send(f"File 'changelog.txt' not found.")

    #events
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'We have logged in {self.client.user}! ID: {self.client.user.id}')
        print("------")
        print(datetime.datetime.timestamp(datetime.datetime.now()))
        await self.client.change_presence(activity=disnake.Activity(type=disnake.ActivityType.watching, name="that mInfo"))
        asyncio.create_task(self._changelog())
        reminders = self.db.execute(f'SELECT * FROM Toggle WHERE QuestTime >= 1 ORDER BY QuestTime ASC')
        reminders = reminders.fetchall()
        #asyncio.create_task(self._psycord_team())
        print(reminders)
        for row in reminders:
            channelid = row[8]
            self.db.execute(f'UPDATE Toggle SET Timer = 0 WHERE Channel = {channelid}')
            self.db.commit()
            print(row[9])
            print("theres at least one row")
            print(channelid)
            current_time = datetime.datetime.timestamp(datetime.datetime.now())
            print(current_time)
            waiter = row[7]
            print(waiter)
            userid = row[1]
            if waiter > current_time:
                waiter = waiter-current_time
                print(waiter)
                print(waiter)
                if row[14] == 1:
                    reminder = 1
                    if row[6] == 0:
                        reminder = 3
                elif row[14] == 2:
                    reminder = 2
                    if row[6] == 0:
                        reminder = 4
                await asyncio.create_task(self._quest_reminder(channelid, userid, waiter, reminder))
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
        desc += f"> * __PokéMeow Rare Spawns__: A solid feed for Meow spawns.\n> * Usage: ``rarwspawn [set/remove] [channel id]``\n"
        desc += f"> * __Psycord Outbreaks & Wild Spawns__: If you have the outbreak feed from Psycord set up in your server, you can get pings when a certain Pokémon has an outbreak and there can be pings whenever a wild Pokémon gets spawned due to server activity.\n"
        desc += f"> * Usage: ``outbreaks [add/remove] [channel id]`` for outbreak pings.\n> * Usage: ``outbreaks [role] [role id]``\n\n\n*Parameters in [] are mandatory.*"

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
    async def on_member_join(self, member, guild):
        id = guild.id
        if id == 825813023716540426:
            db = self.db.execute(f'SELECT * FROM Blacklist WHERE UserID = {member.id}')
            db = db.fetchall()
            print(member.id)
            print(member.name)
            if db:
                try:
                    await member.send("Sorry, the server you were trying to join blacklisted you.\nThat's probably because you broke some server rules.")
                    await member.kick(reason="You're blacklisted on this server, because you broke the law.")
                except Exception as e:
                    print(e)
                    print(member.display_name+" "+str(member.id))
            else:
                desc= f"Welcome to ᵖᵃʳᵃˡʸᵐᵖᶤᶜˢ <@{member.id}>.\nTo get full access to the server, get verified in <#998249646923202610>!\n"
                desc += f"If you are here to join the clan, then please post your `;stats` in <#825836268332122122> and make sure you read the pins in there for clan requirements.\n"
                desc += f"If you're a member of a partnered clan, please head to <#825836268332122122> and use ``;clan``.\n"
                desc += f"Have a read of <#885070641638825984> for information on the server including the rules.\n"
                desc += f"Happy hunting!"
                channel = self.client.get_channel(825836238951022602)
                await channel.send(desc)

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
        
        if message.author.bot and message.author.id != meow and message.author.id != karp and message.author.id != 1209829454667317288 and message.author.id != 865576698137673739 and message.author.display_name != "Psycord Official #🚨・alerts":
            return
        
        if message.content.lower() == "trygoogle":
            await message.delete()
            await message.channel.send("https://tenor.com/bUYzH.gif")
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

        if message.author.id == 922248409350549564:
            if "our general chat" in message.content.lower():
                username = message.content
                username = username.split(">")[0]
                username = int(username.split("@")[1])
                username = self.client.get_user(username)
                username = username.display_name
                #print(username+" welcomed")
                await message.channel.send("Hey, "+username)
                await message.channel.send("<a:welcome1:1130245046025846814><a:welcome2:1130245098983137323>")

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

        ######## Psycord Outbreak Listener
        outbreaks = self.db.execute(f'SELECT * FROM Admin WHERE Server_ID = {message.guild.id}')
        outbreaks = outbreaks.fetchone()
        #print(outbreaks)
        if message.channel.id == int(outbreaks[2]): #Feed channel
            print("Feed channel")
            print(f'{message.guild.name}')
            if len(message.embeds) > 0:
                emb = message.embeds[0]
                if "Reported" in emb.title:
                    mon = emb.description.split("**")[1]
                    outb = mon.lower()
                    hunts = self.db.execute(f'SELECT * FROM PsyHunt WHERE Mon = "{outb}" AND ServerID = {message.guild.id}')
                    hunts = hunts.fetchall()
                    desc = f"An outbreak of **{mon}** started! Gather, fellow hunters! \n"
                    for entry in hunts:
                        desc += f'<@{entry[0]}> '
                    await message.channel.send(desc)
                    if "Prof. Oak" in emb.description:
                        mon = emb.description.split("**")[7]
                        print(mon)
                        outb = mon.lower()
                        hunts = self.db.execute(f'SELECT * FROM PsyHunt WHERE Mon = "{outb}" AND ServerID = {message.guild.id}')
                        hunts = hunts.fetchall()
                        desc = f"**{mon}** is the connected Pokémon for the current Outbreak! Let's purify! \n"
                        for entry in hunts:
                            desc += f'<@{entry[0]}> '
                        await message.channel.send(desc)
        
        if message.channel.id == 1199807047294795878: ##Psycord Channel
            if message.author.id == 865576698137673739:  
                log = self.client.get_channel(1221565506902032444)
                #await log.send(f"{message}\n>>>\n{message.content}")
                if len(message.embeds) > 0:
                    emb = message.embeds[0]
                    await log.send(embed=emb)
                    if "a wild " in emb.title.lower():
                        print("wild spawn")
                        await message.channel.send(f"A wild Pokémon spawned! <@&1217752336508784681>")
                        
                        
        if message.channel.id == 1201300833304854538: #Psycord Extra
            if message.author.id == 865576698137673739:
                #print(f"Message from {message.author}")
                #print(len(message.embeds))
                if len(message.embeds) > 0:
                    print("With embed")
                    _embed = message.embeds[0]
                    if "paralympics | members" in _embed.title.lower():
                        print("Members table")
                        counter = self.db.execute(f'SELECT * FROM Admin WHERE Server_ID = 825813023716540426')
                        counter = counter.fetchone()
                        if (round(datetime.datetime.timestamp(datetime.datetime.now))+3600)>(counter+608400):
                            desc = _embed.description
                            desc = desc.split["Total TBs"](1)
                            desc = desc.split[":"]
                            i = 0
                            for entry in desc:
                                if i % 2 == 0:
                                    name = entry.split["|"](0)
                                    try:
                                        old = self.db.execute(f'SELECT * FROM PsycordTeam WHERE User = "{name}"')
                                        old = old.fetchone()
                                        print(old)
                                        oldpoint = int(old[1])
                                        average = int(old[3])
                                        count = int(old[4])+1
                                    except:
                                        oldpoint = 0
                                        average = 0
                                        count = 1
                                    points = int(entry.split["|"](1)).replace(",", "")
                                    print(f'{name}, {points}')
                                    if average != 0:
                                        newavg = (average*count-1)+points
                                        average = newavg / (count+1)
                                    self.db.execute(f'INSERT or REPLACE INTO PsycordTeam VALUES ("{name}", {points}, {oldpoint}, {average}, {count})')
                                    self.db.commit()
                                    self.db.execute(f'UPDATE Admin SET TeamUpdate = {counter+608400}')
                                    self.db.commit()
                                    print(f"Next Update will be at {counter+608400}")
                

        ######## Straymon Checker
        if message.channel.id == 825836268332122122:
            if message.author.id == meow:
                if len(message.embeds) > 0:
                    _embed = message.embeds[0]
                    if "PokeMeow Clans" in _embed.author.name:
                        if "Welcome to" in _embed.description:
                            if "Straymons" in _embed.description:
                                if message.reference:
                                    ref_msg = await message.channel.fetch_message(message.reference.message_id)
                                elif message.interaction:
                                    ref_msg = message.interaction.author
                                member = ref_msg.author
                                target_role = 1203087005127548928
                                target_role = message.guild.get_role(target_role)
                                if target_role and target_role not in member.roles:
                                    await member.add_roles(target_role)
                                    await message.channel.send(f"Welcome, <@{member.id}>! I've added the <@&1203087005127548928> role to you", allowed_mentions = disnake.AllowedMentions(users = False, roles= False))
                                
        ########Rare Spawn Listener 825958388349272106 #bot-testing channel
        receiver_channel = self.db.execute(f'SELECT * FROM Admin WHERE Server_ID = {message.guild.id}') # rare-spawns
        receiver_channel = receiver_channel.fetchone()
        #print(receiver_channel)
        receiver_channel = int(receiver_channel[4])
        log_channel = 1164544776985653319
        if message.author.id == meow:
            announce_channel = self.client.get_channel(receiver_channel)
            log_chn = self.client.get_channel(log_channel)
            if "used a code to claim" in message.content:
                if message.reference:
                    ref_msg = await message.channel.fetch_message(message.reference.message_id)
                    sender = ref_msg.author
                elif message.interaction:
                    sender = message.interaction.author
                monname = message.content.split("**")[1]
                monname = monname+" "
                print(monname)
                data = self.db.execute(f'SELECT * FROM Dex WHERE Name LIKE "{monname}"')
                data = data.fetchall()
                #print(data)
                url = data[0][15]
                #print(url)
                monname = data[0][1]
                print(monname)
                current_time = message.created_at
                timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
                desc_text = f"\nOriginal message: [Click here]({message.jump_url})\n"
                embed = await Custom_embed(self.client,thumb=url,description=sender.display_name+" just claimed a **"+monname+"** from a code.\n"+desc_text).setup_embed()
                embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                embed.set_author(name=f'{sender.display_name}'" just redeemed a code!", icon_url="https://cdn.discordapp.com/emojis/671852541729832964.webp?size=240&quality=lossless")
                await announce_channel.send(embed=embed)
            if "You ate a" in message.content:
                if message.reference:
                    ref_msg = await message.channel.fetch_message(message.reference.message_id)
                    sender = ref_msg.author
                elif message.interaction:
                    sender = message.interaction.author
                await asyncio.sleep(3)
                datarem = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {sender.id}')
                datarem = datarem.fetchall()
                if datarem[0][15] == 1:
                    if datarem[0][6]==0:
                        desc = f'{rem_emotes["remind"]} - <@{sender.id}>, you can now use </give fun-item:1015311084812501028> again.'
                    else:
                        desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["give"]}'
                    await message.channel.send(desc, allowed_mentions = disnake.AllowedMentions(users = False))
                elif datarem[0][15] == 2:
                    if datarem[0][6]==0:
                        desc = f'{rem_emotes["remind"]} - <@{sender.id}>, you can now use </give fun-item:1015311084812501028> again.'
                    else:
                        desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["give"]}'
                    await message.channel.send(desc)
            if "s trainer icon!" in message.content:
                iconname = message.content.split("unlocked ")[1]
                icon = iconname.split(":")[2]
                icon = icon.split(">")[0]
                print(icon)
                iconname = iconname.split(":")[1]
                print(iconname)
                iconname = iconname.replace("_"," ")
                iconname = iconname.title()
                print(iconname)
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
                await log_chn.send(user+" found an icon")
                await log_chn.send("Its "+iconname)
            if "won the battle!" in message.content:
                #print("Battle won")
                dataev = self.db.execute(f'SELECT * FROM Admin')
                dataev = dataev.fetchall()
                if dataev[0][4] == 1:
                    username = message.content.split("**")[1]
                    username = message.guild.get_member_named(username)
                    #print(username)
                    #print(username.id)
                    data = self.db.execute(f'SELECT * FROM Events WHERE User_ID = {username.id}')
                    data = data.fetchall()
                    if data:

                        item_count = data[0][3]
                        battle_odds = ((1/(drop_pos["battle"])) * (1 + (0.01 * item_count)))
                        odds = 0
                        # if coin_type == "battle":
                        odds = battle_odds

                        roll = random.random()

                        if odds > roll:
                            await message.channel.send("You've found a <:lavacookie:1167592527570935922>! Feed it to me with ``feed``.")
                            old_amount = data[0][4]
                            new_amount = 1+old_amount
                            self.db.execute(f'UPDATE Events SET Items = {new_amount} WHERE User_ID = {username.id}')
                            self.db.commit()
            if "from completing challenge" in message.content:
                if message.reference:
                    ref_msg = await message.channel.fetch_message(message.reference.message_id)
                    sender = ref_msg.author
                elif message.interaction:
                    sender = message.interaction.author
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
            if message.reference:
                ref_msg = await message.channel.fetch_message(message.reference.message_id)
                sender = ref_msg.author
                # print(interaction_message)
            if message.interaction:
                ref_msg = message.interaction
                sender = ref_msg.author
            if message.content:
                #print("Aha, some content")
                if "your catch bot" in message.content.lower():
                    #print("Aha, catchbotting in message")
                    await asyncio.sleep(8)
                    datarem = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {sender.id}')
                    datarem = datarem.fetchall()
                    if datarem[0][15] == 1:
                        if datarem[0][6] == 0:
                            desc = f'{rem_emotes["remind"]} - <@{sender.id}>, you can now use your catchbot again.'
                            #desc = desc[::-1]
                        else:
                            desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["catchbot"]}'
                        await message.channel.send(desc, allowed_mentions = disnake.AllowedMentions(users = False))
                    elif datarem[0][15] == 2:
                        if datarem[0][6] == 0:
                            desc = f'{rem_emotes["remind"]} - <@{str(sender.id)}>, you can now use your catchbot again.'
                            #desc = desc[::-1]
                        else:
                            desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["catchbot"]}'
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
                    if "Global Market " in _embed.author.name:
                        print("Market going on")
                        if _embed.footer.text:
                            number = _embed.footer.text.split("#")[1]
                            number = int(number.split(" ")[0])
                            #print(number)
                            datdex = self.db.execute(f'SELECT * FROM Dex WHERE DexID = {number}')
                            datdex = datdex.fetchall()
                            #print(datdex[0][1])
                            current_time = int(datetime.datetime.timestamp(datetime.datetime.now()))
                            price = _embed.description.split("PokeCoin")[2]
                            lowprice = price.split(" ")[1]
                            lowprice = int(lowprice.replace(",", ""))
                            #print(lowprice)
                            amount = int(price.split(" ")[5])
                            #print(amount)
                            self.db.execute(f'UPDATE Dex Set LowestVal = {lowprice}, UpdateTime = {current_time}, Amount = {amount} WHERE DexID = {datdex[0][0]}')
                            self.db.commit()
                            await asyncio.sleep(3)
                            datarem = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {sender.id}')
                            datarem = datarem.fetchall()
                        if datarem[0][15] == 1:
                            if datarem[0][6] == 0:
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}>, you can now use ;market again.'
                                #desc = desc[::-1]
                            else:
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["market"]}'
                            await message.channel.send(desc, allowed_mentions = disnake.AllowedMentions(users = False))
                        elif datarem[0][15] == 2:
                            if datarem[0][6] == 0:
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}>, you can now use ;market again.'
                                #desc = desc[::-1]
                            else:
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["market"]}'
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
                        datarem = datarem.fetchall()
                        if datarem[0][10] == 1:
                            # desc = "again."
                            # desc = desc[::-1]
                            # desc1=str(sender.display_name)+", you can now use "
                            # desc1=desc1[::-1]
                            # await message.channel.send(f"{desc} </pokemon:1015311085441654824> {desc1}")
                            if datarem[0][6]==0:
                                desc=f'{rem_emotes["remind"]} - <@{sender.id}>, you can now use </pokemon:1015311085441654824> again.'
                            else:
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["spawn"]}'
                            await message.channel.send(desc, allowed_mentions = disnake.AllowedMentions(users = False))
                        elif datarem[0][10] == 2:
                            # user = f"<@{str(sender.id)}>"
                            # desc = "again."
                            # desc = desc[::-1]
                            # desc1=", you can now use "
                            # desc1=desc1[::-1]
                            # await message.channel.send(f"{desc} </pokemon:1015311085441654824> {desc1} {user}")
                            if datarem[0][6]==0:
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}>, you can now use </pokemon:1015311085441654824> again.'
                            else:
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["spawn"]}'
                            await message.channel.send(desc)
                if _embed.description:
                    if "cast out a" in _embed.description:
                        await asyncio.sleep(24.2)
                        datarem = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {sender.id}')
                        datarem = datarem.fetchall()
                        if datarem[0][11] == 1:
                            # desc = "again."
                            # desc = desc[::-1]
                            # desc1=str(sender.display_name)+", you can now use "
                            # desc1=desc1[::-1]
                            # await message.channel.send(f"{desc} </fish spawn:1015311084812501026> {desc1}")
                            if datarem[0][6]==0:
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}>, you can use</fish spawn:1015311084812501026> again.'
                            else:
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["fish"]}'
                            await message.channel.send(desc, allowed_mentions = disnake.AllowedMentions(users = False))
                        elif datarem[0][11] == 2:
                            # user = f"<@{str(sender.id)}>"
                            # desc = "again."
                            # desc = desc[::-1]
                            # desc1=", you can now use "
                            # desc1=desc1[::-1]
                            # await message.channel.send(f"{desc} </fish spawn:1015311084812501026> {desc1} {user}")
                            if datarem[0][6]==0:
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}>, you can now use </fish spawn:1015311084812501026> again.'
                            else:
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["fish"]}'
                            await message.channel.send(desc)
                    
                    if "from a swap" in _embed.description:
                        await asyncio.sleep(6)
                        datarem = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {sender.id}')
                        datarem = datarem.fetchall()
                        if datarem[0][15] == 1:
                            # desc = str(sender.display_name)+", you can now swap again."
                            # desc = desc[::-1]
                            if datarem[0][6]==0:
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}>, you can now ;swap again.'
                            else:
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["swap"]}'
                            await message.channel.send(desc, allowed_mentions = disnake.AllowedMentions(users = False))
                        elif datarem[0][15] == 2:
                            # user = f"<@{str(sender.id)}>"
                            # desc = ", you can now swap again."
                            # desc = desc[::-1]+user
                            if datarem[0][6]==0:
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}>, you can now ;swap again.'
                            else:
                                desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["swap"]}'
                            await message.channel.send(desc)
                if _embed.title:
                    if "quests for rewards!" in _embed.title:
                        #print("Quest screen from "+sender.display_name)
                        datarem = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {sender.id}')
                        datarem = datarem.fetchall()
                        await asyncio.sleep(6)
                        if datarem[0][6]==0:
                            desc = f'{rem_emotes["remind"]} - <@{sender.id}>, you can now check your quests again.'
                        else:
                            desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["quest"]}'
                        if datarem[0][13] == 1:
                            await message.channel.send(desc, allowed_mentions = disnake.AllowedMentions(users = False))
                        elif datarem[0][13] == 2:
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
                                datarem = datarem.fetchall()
                                if datarem[0][14] != 0:
                                    if datarem[0][7] != 0:
                                        print("Already a timer running")
                                    else:
                                        print("Oh, a new timer")
                                        q_time = int(datetime.datetime.timestamp(datetime.datetime.now()))-6
                                        print(q_time)
                                        q_time = q_time+waiter
                                        channelid = message.channel.id
                                        self.db.execute(f'UPDATE Toggle SET QuestTime = {q_time}, Channel = {channelid} WHERE User_ID = {sender.id}')
                                        self.db.commit()
                                        q_time = str(q_time)
                                        if datarem[0][14] == 1:
                                            remind = 1
                                        elif datarem[0][14] == 2:
                                            remind = 2
                                        if datarem[0][9] == 0:
                                            minutes = int(waiter/60)
                                            if datarem[0][6] == 0:
                                                desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["quest"]}:alarm_clock::two::regional_indicator_h:'
                                            elif datarem[0][6] == 1:
                                                desc = str(sender.display_name)+", I've set a timer for "+str(minutes)+" minutes."
                                            if datarem[0][14] == 1:
                                                await message.channel.send(desc, allowed_mentions= disnake.AllowedMentions(users=False))
                                            elif datarem[0][14] == 2:
                                                await message.channel.send(desc)
                                            await asyncio.create_task(self._quest_reminder(channelid, sender.id, waiter,remind))
                        
                if _embed.author.name:
                    if "catchbot" in _embed.author.name.lower():
                        #print("Aha, catchbotting in name")
                        await asyncio.sleep(5)
                        datarem = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {sender.id}')
                        datarem = datarem.fetchall()
                        if datarem[0][6]==0:
                            desc = f'{rem_emotes["remind"]} - <@{sender.id}>, you can use your ;catchbot again.'
                        else:
                            desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["catchbot"]}'
                        if datarem[0][15] == 1:
                            await message.channel.send(desc, allowed_mentions = disnake.AllowedMentions(users = False))
                        elif datarem[0][15] == 2:
                            await message.channel.send(desc)
                
                
                if _embed.footer.text:
                    if "battle will begin" in _embed.footer.text:
                        print("Aha, battling.")
                        await asyncio.sleep(59)
                        datarem = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {sender.id}')
                        datarem = datarem.fetchall()
                        if datarem[0][6]==0:
                            desc = f'{rem_emotes["remind"]} - <@{sender.id}>, you can now ;battle again.'
                        else:
                            desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["battle"]}'
                        if datarem[0][12] == 1:
                            await message.channel.send(desc, allowed_mentions = disnake.AllowedMentions(users = False))
                        elif datarem[0][12] == 2:
                            await message.channel.send(desc)
                    if "buddy help" in _embed.footer.text.lower() or "move help" in _embed.footer.text.lower():
                        print("Buddy Window")
                        await asyncio.sleep(5)
                        datarem = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {sender.id}')
                        datarem = datarem.fetchall()
                        if datarem[0][6]==0:
                            desc = f'{rem_emotes["remind"]} - <@{sender.id}>, you can now use'
                            if "move" in _embed.footer.text.lower():
                                desc += ";moves again."
                            else:
                                desc += ";buddy again."
                        else:
                            desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["buddy"]}'
                        if datarem[0][15] == 1:
                            await message.channel.send(desc, allowed_mentions = disnake.AllowedMentions(users = False))
                        elif datarem[0][15] == 2:
                            await message.channel.send(desc)

                        

                if _embed.author.name:
                    if "Egg Centre" in _embed.author.name:
                        await asyncio.sleep(5)
                        datarem = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {sender.id}')
                        datarem = datarem.fetchall()
                        if datarem[0][6]==0:
                            desc = f'{rem_emotes["remind"]} - <@{sender.id}>, you can now use ;egg again.'
                        else:
                            desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["egg"]}'
                        if datarem[0][15] == 1:
                            await message.channel.send(desc, allowed_mentions = disnake.AllowedMentions(users = False))
                        elif datarem[0][15] == 2:
                            await message.channel.send(desc)
                    if "hatched" in _embed.author.name:
                        data_egg = self.db.execute(f'SELECT * FROM Dex WHERE Img_url = "{_embed.image.url}"')
                        data_egg = data_egg.fetchall()
                        sender = ref_msg.author
                        raremon = poke_rarity[(data_egg[0][14])]
                        description_text = f"Original message: [Click here]({message.jump_url})\n"
                        #print(Rare_Spawned)
                        #Rare_Spawned = ["Golden","Event", "Legendary", "Shiny", "Rare", "SuperRare"]
                        if data_egg[0][14] in Rare_Spawned or str(data_egg[0][0]) in eggexcl:
                            print("Its in the one list!")
                            print(str(data_egg[0][0]))
                            embed = disnake.Embed(title=raremon+" **"+data_egg[0][1]+"** \nDex: #"+str(data_egg[0][0]), color=color,description=description_text)
                            embed.set_author(name=(sender.display_name+" just hatched an exclusive:"),icon_url="https://cdn.discordapp.com/emojis/689325070015135745.gif?size=96&quality=lossless")
                            embed.set_image(_embed.image.url)
                            embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                            await announce_channel.send(embed=embed)

                        dataev = self.db.execute(f'SELECT * FROM Admin')
                        dataev = dataev.fetchall()
                        if dataev[0][4] == 1:
                            print("Event active")
                            print("Egg hatched")

                            egg_odds = (1/drop_pos["egg"])
                            odds = egg_odds

                            roll = random.random()

                            if odds > roll:
                                print(sender)
                                print(sender.id)
                                data = self.db.execute(f'SELECT * FROM Events WHERE User_ID = {sender.id}')
                                data = data.fetchall()
                                if data:
                                    await message.channel.send(str(sender.display_name)+", you've found a <:lavacookie:1167592527570935922>! Feed it to me with ``feed``.")
                                    old_amount = data[0][4]
                                    new_amount = 1+old_amount
                                    self.db.execute(f'UPDATE Events SET Items = {new_amount} WHERE User_ID = {sender.id}')
                                    self.db.commit()
                        await asyncio.sleep(5)
                        datarem = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {sender.id}')
                        datarem = datarem.fetchall()
                        if datarem[0][6]==0:
                            desc = f'{rem_emotes["remind"]} - <@{sender.id}>, you can now use ;egg again.'
                        else:
                            desc = f'{rem_emotes["remind"]} - <@{sender.id}> {rem_emotes["egg"]}'
                        if datarem[0][15] == 1:
                            await message.channel.send(desc, allowed_mentions = disnake.AllowedMentions(users = False))
                        elif datarem[0][15] == 2:
                            await message.channel.send(desc)

                        
                    if "opened " in _embed.author.name:
                        print("Box opening")
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
                                    print(mons)
                                    mons = mons.split(">")
                                    unused = mons.pop()
                                    print(mons)
                                    description_text = "Pokemon received:\n"
                                    for entry in mons:
                                        monid = entry.split(":")[1]
                                        print(monid)
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
                        data_sw = data_sw.fetchall()
                        sender = ref_msg.author.display_name
                        raremon = poke_rarity[(data_sw[0][14])]
                        #Rare_Spawned = ["Event", "Shiny", "Legendary", "SuperRare", "Rare", "Uncommon", "Common","Golden"]
                        description_text = f"Original message: [Click here]({message.jump_url})\n"
                        if data_sw[0][14] in Rare_Spawned:
                            embed = disnake.Embed(title=raremon+" **"+data_sw[0][1]+"** \nDex: #"+str(data_sw[0][0]), color=color,description=description_text)
                            embed.set_author(name=(sender+" just swapped for a:"),icon_url="https://cdn.discordapp.com/emojis/869901886080315392.webp?size=96&quality=lossless")
                            embed.set_image(_embed.image.url)
                            embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                            await announce_channel.send(embed=embed)
                if _embed.description:
                    if "claimed a <:Golden" in _embed.description:
                        data_pr = self.db.execute(f'SELECT * FROM Dex WHERE Img_url = "{_embed.image.url}"')
                        data_pr = data_pr.fetchall()
                        logging = 1083131761451606096
                        logging = self.client.get_channel(logging)
                        try:
                            await logging.send(message)
                        except:
                            logging.send("NO message to log")
                        try:
                            await logging.send(_embed.description)
                        except:
                            logging.send("How's there no description???")
                        print(data_pr[0][14])
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


        data = self.db.execute(f'SELECT * FROM Admin') #Checks my Admin Toggle db
        data = data.fetchall()
        log = 1166470108068188200
        #Bot-testing = 825958388349272106, buy-in-sponsoring = 920260648045273088, Meow-grind 1 = 1037323228961579049
        if message.channel.id == 920260648045273088:  #Checks for the Bot-testing channel
            log = self.client.get_channel(1166470108068188200) #Setting up my log channel ^^
            if data[0][4] == 1: #If "Event" is turned on
                #print("Its active")
                if message.author.id == meow:
                    #print("From Meow")
                    if " PokeCoins!" in message.content: #Looking for oaid PokeCoins
                        #print("There are coins")
                        try:
                            ref_msg = await message.channel.fetch_message(message.reference.message_id)  # Command with ;
                            sender = ref_msg.author
                            #print("Ref")
                        except:
                            ref_msg = message.interaction #Command with /
                            sender = ref_msg.author
                            #print("Int")
                        amount = message.content.split("<:PokeCoin:666879070650236928> ")[1] #Splitting the msg of Meow after the Coin Emote
                        amount = amount.split(" ")[0] #Splitting it again at the Space behind the Number
                        #print(amount)
                        try:
                            amount = int(amount.replace(",", "")) #Replacing any , if there are any
                        except:
                            amount = int(amount)
                        if amount >= buyin: #Checking for a minimum amount
                            update = self.db.execute(f'SELECT * FROM Events WHERE User_ID = {sender.id}') #Connecting to the event db
                            update = update.fetchall()
                            if update: #Is the User in the db already?
                                #print("We know them!")
                                newamount = (update[0][1])+amount #Taking the old amount they paid in & putting the new onto that
                                print(newamount)
                                self.db.execute(f'UPDATE Events SET Buyin = {newamount} WHERE User_ID = {sender.id}') #Updating that dude
                                self.db.commit()
                                await message.channel.send("You were already bought in, your total is now "f'{newamount:,}')
                                await log.send(f'{sender}'+"'s entry got updated, +"+f'{amount}'+", now: "+f'{newamount}'+" -- "+f'{sender.id}')
                            else: #Not in the db? Must be new then
                                #print("Someone new")
                                self.db.execute(f'INSERT INTO Events VALUES ({sender.id}, {amount}, 0, 1, 0)')
                                self.db.commit()
                                await message.channel.send("You've entered this "+f'{self.client.user.display_name}'+"'s Event.")
                                await log.send(f'{sender}'+" paid "f'{amount}'" & joined this event. -- "+f'{sender.id}')


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
                            print("Version in it")
                            dex=_embed.author.name.split("#")[1]
                            #print(dex)
                            name=_embed.author.name.split("#")[0]
                            #print(name)
                            try:
                                data = self.db.execute(f'SELECT * FROM Dex WHERE DexID = {dex}')
                                data = data.fetchall()
                                #await log.send(data)
                                val = data[0][17]
                                time = data[0][18]
                                amount = data[0][19]
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
                        dex=_embed.author.name.split("#")[1]
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
