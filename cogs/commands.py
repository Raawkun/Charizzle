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
#    @commands.slash_command(
#        name="toggle",
#        description="Toggle commands",
#        options=[
#            Option(
#                name="switch",
#                description="Choose a switch to toggle",
#                type=3,
#                choices=[
#                    OptionChoice("Squirtle", "squirtle"),
#                    OptionChoice("Charmander", "charmander"),
#                    OptionChoice("Annoy", "annoy"),
#                ],
#                required=True
#            ),   
#        ],)
#    async def _toggle(self, ctx, switch = None):
#        await ctx.response.defer()
#        database = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {ctx.author.id}')
#        database = database.fetchall()
#        for row in database:
#            if switch == "squirtle" and row[2] == 0:
#                self.db.execute(f'UPDATE Toggle SET Switch1 = 1 WHERE User_ID = {ctx.author.id}')
#                self.db.commit()
#                await ctx.send("Toggled on")
#            elif switch == "squirtle" and row[2] == 1:
#                self.db.execute(f'UPDATE Toggle SET Switch1 = 0 WHERE User_ID = {ctx.author.id}')
#                self.db.commit()
#                await ctx.send("Toggled off")
#            elif switch == "annoy" and row[3] == 0:
#                self.db.execute(f'UPDATE Toggle SET Switch3 = 1 WHERE User_ID = {ctx.author.id}')
#                self.db.commit()
#                await ctx.send("Toggled on")

    @commands.command()
    async def toggle(ctx, input: str):
        enabled = " is enabled."
        disabled = " is disabled."

        with open("config.json", "r") as config_file:
            config_data = json.load(config_file)

        authorized_users = [837611415070048277]
        sender = disnake.Message.author

        if authorized_users in disnake.Message.author.get_role:
            if input == "squirtle":
                if config_data.get('squirtle') == 1:
                    config_data['squirtle'] = 0
                    print("SQUIRTLE"+disabled)
                    await ctx.message.send(input+disabled)
                else: 
                    config_data['squirtle'] = 1
                    print("SQUIRTLE"+enabled)
                    await ctx.message.send(input+enabled)
            elif input == "charmander":
                if config_data.get('charmander') == 1:
                    config_data['charmander'] = 0
                    print("CHARMANDER"+disabled)
                    await ctx.message.send(input+disabled)
                else: 
                    config_data['charmander'] = 1
                    print("CHARMANDER"+enabled)
                    await ctx.message.send(input+enabled)
            elif input == "lol":
                if config_data.get('lol') == 1:
                    config_data['lol'] = 0
                    print("LOL"+disabled)
                    await ctx.message.send(input+disabled)
                else: 
                    config_data['lol'] = 1
                    print("LOL"+enabled)
                    await ctx.message.send(input+enabled)
            elif input == "annoy":
                if config_data.get('annoy') == 1:
                    config_data['annoy'] = 0
                    print("ANNOY"+disabled)
                    await ctx.message.send(input+disabled)
                else: 
                    config_data['annoy'] = 1
                    print("ANNOY"+enabled)
                    await ctx.message.send(input+enabled)

            else:
                await ctx.message.send("Wrong input.")

        else: 
            await ctx.message.send("You don't have enough power to access this.")


    @commands.command()
    async def add(self, ctx, left: int, right: int):
        """Adds two numbers together."""
        await ctx.send(left + right)

    @commands.command()
    async def vers(self, ctx):
        vers1 = str("1.0.0.2")
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
                        CREATE TABLE IF NOT EXISTS Toggle(
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
        await ctx.send("Done")


def setup(client):
    client.add_cog(Coms(client))