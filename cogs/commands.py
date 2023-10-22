import random
from typing import Any
import disnake
from disnake.ext import commands
import asyncio
from sqlite3 import connect
from disnake import Message, Option, OptionChoice, OptionType, ApplicationCommandInteraction
import json
import sqlite3

# Zeichen zum Kopieren: [ ] { }

class Coms(commands.Cog):

#Database initialization, needed in every file with db
    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")
        


    @commands.command()
    async def toggle(self, ctx):
        user_id = ctx.author.id
        database = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {user_id}')
        database = database.fetchall()
        author_url = "https://cdn.discordapp.com/emojis/1153729922620215349.webp?size=96&quality=lossless"
        author_name = ctx.author.display_name
        gengar_bot = self.client.get_user(1161011648585285652)
        footer_icon = gengar_bot.display_avatar.url
        footer_name = "Mega Gengar"
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
            embed.set_footer(icon_url=footer_icon,text=footer_name)
            embed.add_field(name="Golden Razz Berry: ",inline=True, value=value_grazz)
            embed.add_field(name="Repel: ",inline=True, value=value_repel)
            embed.add_field(name="Starter: ",inline=True, value=value_start)
            embed.add_field(name="Privacy: ",inline=True, value=value_priv)
            embed.set_thumbnail(footer_icon)
            await ctx.send(embed=embed)

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
    async def vers(self, ctx):
        vers1 = str("1.0.0.3")
        await ctx.send(vers1)

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


    @commands.command()
    async def annoy(self, ctx, input_id, try_amount):
            with open("config.json", "r") as config_file:
                config_data = json.load(config_file)
            
            if disnake.message.author.id == [352224989367369729]:
                if input_id != int:
                    await ctx.message.send("Please input a user ID.")
                else: annoy_id = input_id
                if try_amount != int:
                    await ctx.message.send("Please input a number")
                else: amounts = try_amount
            
                config_data['client_id'] = annoy_id
                config_data['attempts'] = amounts
                await ctx.message.send(f"Changed the ID!")
            else: await ctx.message.send("Not allowed to use this command.")

    



    @commands.command()
    async def toggledb(self, ctx, input: str):
        if "dex" in input:
            self.db.execute(f'''
                            CREATE TABLE IF NOT EXISTS Dex(
                            DexID INTEGER PRIMARY KEY,
                            Name TEXT,
                            Type_1 TEXT,
                            Type_2 TEXT,
                            Hp INTEGER,
                            Attack INTEGER,
                            Defence INTEGER,
                            Sp_atk INTEGER,
                            Sp_def INTEGER,
                            Speed INTEGER,
                            Legendary BOOLEAN,
                            Shiny BOOLEAN,
                            Golden BOOLEAN,
                            Mega BOOLEAN,
                            Rarity TEXT,
                            Img_url TEXT
                            )
                            ''')
            self.db.commit()
            print("Dex_DB created")
        elif "toggle" in input:
            self.db.execute(f'''
                            CREATE TABLE IF NOT EXISTS Toggle (
                            Ref INTEGER AUTO_INCREMENT PRIMARY KEY,
                            User_ID INT,
                            Grazz INT DEFAULT 1,
                            Repel INT DEFAULT 1,
                            Starter INT DEFAULT 1,
                            Privacy INT DEFAULT 0
                            )
                            ''')
            self.db.commit()
            print("Toggle_DB created")
        elif "admin" in input:
            self.db.execute(f'''
                            CREATE TABLE IF NOT EXISTS Admin (
                            Ref INTEGER AUTO_INCREMENT PRIMARY KEY,
                            User_ID INTEGER DEFAULT 352224989367369729,
                            Stfu INT DEFAULT 1,
                            Lol INT DEFAULT 1
                            )
            ''')
            self.db.commit()
            print("Admin_DB created")
        await ctx.send("Done")
        



def setup(client):
    client.add_cog(Coms(client))