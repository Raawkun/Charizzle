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

    enabled = " is enabled."
    disabled = " is disabled."

    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    def __init__(self, client):
        self.client = client

#Database initialization, needed in every file with db
    def __init__(self, client):
        self.client = client
        self.db = connect("pokemon.db")

#Creation of the table in the db
#    @commands.command()
#    async def toggledb(self, ctx):
#        self.db.execute(f'''
#                        CREATE TABLE IF NOT EXISTS Toggle(
#                            Ref INTEGER AUTO_INCREMENT PRIMARY KEY,
#                            User_ID INTEGER,
#                            Switch1 INTEGER DEFAULT 0,
#                            Switch2 INTEGER DEFAULT 0,
#                            Switch3 INTEGER DEFAULT 0,
#                            )
#                        ''')
#        self.db.commit()
#        await ctx.send("Done")

#Toggle command from Pr1nce
    @commands.slash_command(
        name="toggle",
        description="Toggle bot actions",
        options=[
            Option(
                name="switch",
                description="Choose a switch to toggle",
                type=3,
                choices=[
                    OptionChoice("Grazz", "grazz"),
                    OptionChoice("Repel", "repel"),
                    OptionChoice("Starter", "starter"),
                    OptionChoice("Privacy", "privacy")
                ],
                required=True
            ),   
        ],)
    async def _toggle(self, ctx, switch = None):
        await ctx.response.defer()
        database = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {ctx.author.id}')
        database = database.fetchall()
        for row in database:
            if switch == "grazz" and row[3] == 0:
                self.db.execute(f'UPDATE Toggle SET Grazz = 1 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled on")
            elif switch == "grazz" and row[3] == 1:
                self.db.execute(f'UPDATE Toggle SET Grazz = 0 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled off")
            elif switch == "repel" and row[4] == 0:
                self.db.execute(f'UPDATE Toggle SET Repel = 1 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled on")
                
            elif switch == "repel" and row[4] == 1:
                self.db.execute(f'UPDATE Toggle SET Repel = 0 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled off")
                
            elif switch == "starter" and row[5] == 0:
                self.db.execute(f'UPDATE Toggle SET Starter = 1 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled on")
            elif switch == "starter" and row[5] == 1:
                self.db.execute(f'UPDATE Toggle SET Starter = 0 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled off")
            elif switch == "privacy" and row[6] == 0:
                self.db.execute(f'UPDATE Toggle SET Privacy = 1 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled on")
            elif switch == "privacy" and row[6] == 1:
                self.db.execute(f'UPDATE Toggle SET Privacy = 0 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled off")

    @commands.slash_command(
        name="admin",
        description="Toggle admin stuff",
        options=[
            Option(
                name="switch",
                description="Choose a switch to toggle",
                type=3,
                choices=[
                    OptionChoice("Stfu", "stfu"),
                    OptionChoice("Lol", "lol")
                ],
                required=True
            ),   
        ],)
    async def _admin(self, ctx, swtich = None):
        await ctx.response.defer()
        database = self.db.execute(f'SELECT * FROM Admin WHERE User_ID = {ctx.author.id}')
        database = database.fetchall()
        if ctx.author.id == self.db.execute(f'SELECT User_ID FROM Admin'):
            for row in database:
                if swtich == "stfu" and row[2] == 0:
                    self.db.execute(f'UPDATE Admin SET Stfu = 1 WHERE User_ID = {ctx.author.id}')
                    self.db.commit()
                    await ctx.send("Toggled on", hidden=True)
                elif swtich == "stfu" and row[2] == 1:
                    self.db.execute(f'UPDATE Admin SET Stfu = 0 WHERE User_ID = {ctx.author.id}')
                    self.db.commit()
                    await ctx.send("Toggled off", hidden=True)
                elif swtich == "lol" and row[3] == 0:
                    self.db.execute(f'UPDATE Admin SET Lol = 1 WHERE User_ID = {ctx.author.id}')
                    self.db.commit()
                    await ctx.send("Toggled on", hidden=True)
                    
                elif swtich == "lol" and row[3] == 1:
                    self.db.execute(f'UPDATE Admin SET Lol = 0 WHERE User_ID = {ctx.author.id}')
                    self.db.commit()
                    await ctx.send("Toggled off", hidden=True)
        else: await ctx.send("You're not my Trainer, I do no obey to you! <:blastoise_smug:835196079586148443>", hidden=True)



    @commands.command()
    async def calc(self, ctx, input: int):
        """Adds two numbers together."""
        await ctx.send(input)

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

    


    @commands.slash_command(
            name="test",
            description="Just getting a badge!!")
    async def _test(self, ctx):
            await ctx.response.defer()
            await ctx.send(f"Now I have my badge!!!")

    @commands.command()
    async def toggledb(self, ctx):
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
        self.db.execute(f'''
                        CREATE TABLE IF NOT EXISTS Toggle(
                        Ref INTEGER AUTO_INCREMENT PRIMARY KEY,
                        User_ID INT,
                        Username TEXT,
                        Grazz BOOLEAN DEFAULT 1,
                        Repel BOOLEAN DEFAULT 1,
                        Starter BOOLEAN DEFAULT 1,
                        Privacy BOOLEAN DEFAULT 0,
                        )
                        ''')
        self.db.commit()
        self.db.execute(f'''
                        CREATE TABLE IF NOT EXISTS Admin(
                        User_ID INTEGER DEFAULT 352224989367369729,
                        Stfu BOOLEAN DEFAULT 1,
                        Lol BOOLEAN DEFAULT 1
                        )
        ''')
        await ctx.send("Done")
        



def setup(client):
    client.add_cog(Coms(client))