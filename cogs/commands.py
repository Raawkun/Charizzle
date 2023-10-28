import random
from typing import Any
import disnake
from disnake.ext import commands
import asyncio
from sqlite3 import connect
from disnake import Message, Option, OptionChoice, OptionType, ApplicationCommandInteraction
import json
import sqlite3
import datetime
from utility.all_checks import Basic_checker
from utility.embed import Custom_embed
from utility.rarity_db import counts, countnumber

# Zeichen zum Kopieren: [ ] { }

class Coms(commands.Cog):

#Database initialization, needed in every file with db
    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")

    
    
    current_time = datetime.datetime.utcnow()
    timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
        


    @commands.command()
    async def toggle(self, ctx):
        current_time = datetime.datetime.now()
        timestamp = str("<t:"+{int(current_time.timestamp)}+":R>")
        user_id = ctx.author.id
        database = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {user_id}')
        database = database.fetchall()
        author_url = "https://cdn.discordapp.com/emojis/1153729922620215349.webp?size=96&quality=lossless"
        author_name = ctx.author.display_name
        gengar_bot = self.client.get_user(1161011648585285652)
        footer_icon = gengar_bot.display_avatar.url
        footer_name = "Mega Gengar "+timestamp
        emo_yes = ":white_check_mark:"
        emo_no = ":x:"
        color = 0x807ba6
        if database:
            if database[0][2] == 1:
                value_grazz = emo_yes
            else: 
                value_grazz = emo_no
            if database[0][3] == 1:
                value_repel = emo_yes
            else:
                value_repel = emo_no
            if database[0][4] == 1:
                value_start = emo_yes
            else: 
                value_start = emo_no
            if database[0][5] == 1:
                value_priv = emo_yes
            else:
                value_priv = emo_no
            embed = disnake.Embed(
                title="**Settings**", color=color, description="Here you can see your current toggle settings. \nChangeable via ``/toggle`` \n\nThe current settings are:"
            )
            embed.set_author(icon_url=author_url,name=author_name)
            embed.set_footer(icon_url=footer_icon,text=(footer_name+" I "+timestamp))
            embed.add_field(name="Golden Razz Berry: ",inline=True, value=value_grazz)
            embed.add_field(name="Repel: ",inline=True, value=value_repel)
            embed.add_field(name="Starter: ",inline=True, value=value_start)
            embed.add_field(name="Privacy: ",inline=True, value=value_priv)
            embed.set_thumbnail(footer_icon)
            await ctx.send(embed=embed)

    @commands.check(Basic_checker().check_management)
    @commands.command()
    async def huntadd(self, ctx):
        def check(m):
            return m.author == ctx.author
        await ctx.send("Please enter the Pokémon ID.")
        try:
            first_response = await self.client.wait_for('message', check=check, timeout=30)
            first_integer = int(first_response.content)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond.")
            return
        except ValueError:
            await ctx.send("That's not a valid integer.")
            return
        
        await ctx.send("Please enter threshold.")
        try:
            second_response = await self.client.wait_for('message', check=check, timeout=30)
            second_integer = int(second_response.content)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond.")
            return
        except ValueError:
            await ctx.send("That's not a valid integer.")
            return
        
        data = self.db.execute(f'SELECT * FROM Dex WHERE DexID = {first_integer}')
        data = data.fetchall()
        embed = disnake.Embed(title="Chosen Hunt Pokémon:", description="**"+str(data[0][1])+"**\nDex #"+str(first_integer)+"\n\nThreshold: "+str(second_integer), color=0x807ba6)
        embed.set_image(data[0][15])

        await ctx.send("Is this correct? yes/no", embed=embed)
        try:
            third_response = await self.client.wait_for('message',check=check, timeout=30)
            third_answer = str(third_response)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond.")
            return
        if "yes" in third_response.content.lower():
            self.db.execute(f'INSERT INTO Hunt (DexID, Name, Threshold) VALUES ({first_integer}, "{data[0][1]}", {second_integer})')
            self.db.commit()
            await ctx.send("Pokémon added. Check ``hunt`` for your current hunt goals")
        if "no" in third_response.content.lower():
            await ctx.send("Wow. Start again & this time do it better.")

    @commands.check(Basic_checker().check_management)
    @commands.command()
    async def huntremove(self, ctx):
        def check(m):
            return m.author == ctx.author
        await ctx.send("Please enter the Pokémon ID of the hunt you want to remove")
        try:
            first_response = await self.client.wait_for('message', check=check, timeout=30)
            first_integer = int(first_response.content)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond.")
            return
        except ValueError:
            await ctx.send("That's not a valid integer.")
            return
        
        await ctx.send(str(first_integer)+" should really be removed? Yes/No")
        try:
            second_response = await self.client.wait_for('message', check=check, timeout=30)
            second_answer = str(first_response.content)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond.")
            return
        
        if "yes" in second_response.content.lower():
            self.db.execute(f'DELETE FROM Hunt WHERE DexID = {first_integer}')
            self.db.commit()
            await ctx.send("Entry cleared.")
        if "no" in second_response.content.lower():
            await ctx.send("Smh. Make up your mind.")

    @commands.check(Basic_checker().check_management)
    @commands.command()
    async def huntclear(self, ctx):
        def check(m):
            return m.author == ctx.author
        await ctx.send("Do you really want to reset **the whole** hunt table? Yes/No")
        try:
            first_response = await self.client.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond.")
            return
        if "yes" in first_response.content.lower():
            self.db.execute(F'DELETE FROM Hunt')
            self.db.commit()
            await ctx.send("Hunt table cleared.")
        if "no" in first_response.content.lower():
            await ctx.send("Knew it.")


    @commands.command()
    async def hunt(self, ctx):
        data = self.db.execute(f'SELECT * FROM Hunt')
        data = data.fetchall()
        max = self.db.execute(f'SELECT Count(*) FROM Hunt')
        max = max.fetchone()[0]
        #max = max.rowcount
        #print(max)
        if data:
            embed = disnake.Embed(description="Current Hunt Pokémon",color=0x807ba6)
            embed.set_author(name="ᵖᵃʳᵃˡʸᵐᵖᶤᶜˢ Hunt System")
            embed.set_footer(text=f'{self.client.user.display_name}',icon_url=f'{self.client.user.avatar}')
            guild = ctx.guild
            embed.set_thumbnail(url=guild.icon)
            #print("0x807ba6")
            i = 0
            while i < (max):
                #print("First i is:"+str(i))
                embed.add_field(name=("**"+str(data[i][1])+"**with threshold of "+str(data[i][2])),value="",inline=False)
                #embed.add_field(name=" ",value=" ",inline=True)
                #print("Added embed")
                i+=1
                #print(i)
            
            await ctx.send(embed=embed)
        else:
            await ctx.send("There is no hunt event at the moment.")



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
    async def master(self, ctx):
        try:
            await ctx.send(f"My trainer is Blue Flames.")
        except Exception as e:
            await ctx.send(f"Error: {str(e)}")

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


    @commands.check(Basic_checker().check_management)
    @commands.command()
    async def eventset(self, ctx):
        data = self.db.execute(f'SELECT * FROM Admin')
        data = data.fetchall()
        announce = self.client.get_channel(917890289652346911)
        log = self.client.get_channel(1166470108068188200)
        if data[0][4] == 0:
            self.db.execute(f'UPDATE Admin SET Event = 1')
            self.db.commit()
            await ctx.send(f'{self.client.user.display_name}'+"'s Event is now active!")
            await announce.send("Ignore me, thats a test")
            await log.send("**Event started**")
        if data[0][4] == 1:
            self.db.execute(f'UPDATE Admin SET Event = 0')
            self.db.commit()
            data = self.db.execute(f'SELECT * FROM Events')
            data = data.fetchall()
            embed = await Custom_embed(self.client,title="Event Leaderboard").setup_embed()
            #
            # Placeholder for table
            #                               
            await ctx.send("Ended the event. Check <#917890289652346911> for the leaderboard table.")
            await log.send("**Event ended**")
            await announce.send("Test message")
            # self.db.execute(f'DELETE FROM Events')
            # self.cb.commit()
    
    @commands.command(aliases=["ex"])
    async def feed(self,ctx, message = None):
        sender = ctx.author.id
        print(sender)
        data = self.db.execute(f'SELECT * FROM Events WHERE User_ID = {sender}')
        data = data.fetchall()
        if message == None:
            #print("No extra input")
            if data:
                if data[0][4] == 0:
                    await ctx.send("Oh no! Looks like there are not enough cookies in your bag!")
                else:
                    newamount = data[0][4]-1
                    self.db.execute(f'UPDATE Events SET ItemsUsed = ItemsUsed + 1, Items = Items - 1 WHERE User_ID = {sender}')
                    self.db.commit()
                    await ctx.send("That was yummy! You have "+f'{newamount}'+" cookies left right now.")
        elif message == "all":
            if data:
                self.db.execute(f'UPDATE Events SET ItemsUsed = ItemsUsed + Items, Items == 0 WHERE User_ID = {sender}')
                self.db.commit()
                await asyncio.sleep(0.5)
                await ctx.send("That was yummy! You have 0 cookies left right now.")
        elif int(message) > 0:
            print(message)
            reducer = int(message)
            if data:
                if reducer > data[0][4]:
                    await ctx.send("Oh no! Looks like there are not enough cookies in your bag!")
                else:
                    self.db.execute(f'UPDATE Events SET ItemsUsed = ItemsUsed + {reducer}, Items = Items - {reducer} WHERE User_ID = {sender}')
                    self.db.commit()
                    newamount = data[0][4]-reducer
                    await ctx.send("That was yummy! You have "+f'{newamount}'+" cookies left right now.")

    @commands.command(aliases=["inv","inventory"])
    async def bag(self,ctx):
        dataad = self.db.execute(f'SELECT * FROM Admin')
        dataad = dataad.fetchall()
        if dataad[0][4] == 1:
            database_table = self.db.execute(f"SELECT * FROM Events WHERE User_ID = {ctx.author.id}")
            database_table = database_table.fetchall()
            if database_table == None:
                msg ="Your inventory is empty."
            else:
                msg = "Lava Cookies: "+f'{database_table[0][4]}'+" <:lavacookie:1167592527570935922>"
        else:
            msg = "Your inventory is empty."
            
        embed = await Custom_embed(self.client,title=f'{ctx.author.display_name}'"'s Item Bag",thumb="https://www.pokewiki.de/images/e/ec/Pyrobeutel2.png",description=msg).setup_embed()
        await ctx.send(embed=embed)


    @commands.command()
    async def event(self, ctx):
        dataad = self.db.execute(f'SELECT * FROM Admin')
        dataad = dataad.fetchall()
        if dataad[0][4] == 1:
            msg = "# - Points - User\n"
            database_table = self.db.execute(f"SELECT * FROM Events WHERE NOT Points = 0 ORDER BY Points DESC, ItemsUsed DESC")
            database_table = database_table.fetchall()
            if database_table:
                i = 1
                for row in database_table:
                    msg += (f'#{i:02} {str(row[2]).ljust(7)} - {str(ctx.guild.get_member(row[0])).ljust(7)}\n')
                    i += 1
                embed = await Custom_embed(self.client, title="Event Leaderboard",description=f'```{msg}```').setup_embed()
                await ctx.send(embed=embed)
        else:
            await ctx.send("There's no "+f'{self.client.user.display_name}'+" event running at the moment. Please check <#917890289652346911>.")
        

def setup(client):
    client.add_cog(Coms(client))