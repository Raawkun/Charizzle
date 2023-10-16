from typing import Any
import disnake
from disnake.ext import commands
import asyncio
from sqlite3 import connect
from disnake import Option, OptionChoice, OptionType, ApplicationCommandInteraction
from configparser import SafeConfigParser

# Zeichen zum Kopieren: [ ] { }

class Coms(commands.Cog):

    SafeConfigParser.read('settings.ini')

    def __init__(self, client):
        self.client = client

#Database initialization, needed in every file with db
    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")

#Creation of the table in the db
    @commands.command()
    async def toggledb(self, ctx):
        self.db.execute(f'''
                        CREATE TABLE IF NOT EXISTS Toggle(
                            Ref INTEGER AUTO_INCREMENT PRIMARY KEY,
                            User_ID INTEGER,
                            Switch1 INTEGER DEFAULT 0,
                            Switch2 INTEGER DEFAULT 0,
                            Switch3 INTEGER DEFAULT 0,
                            )
                        ''')
        self.db.commit()
        await ctx.send("Done")

    @commands.slash_command(
        name="toggle",
        description="Toggle commands",
        options=[
            Option(
                name="switch",
                description="Choose a switch to toggle",
                type=3,
                choices=[
                    OptionChoice("Squirtle", "squirtle"),
                    OptionChoice("Charmander", "charmander"),
                    OptionChoice("Annoy", "annoy"),
                    OptionChoice("Lol", "lol"),
                ],
                required=True
            ),   
        ],)
    async def _toggle(self, ctx, switch = None):
        await ctx.respomse.defer()
        parser = SafeConfigParser()
        parser.read('settings.ini')
        if switch == "squirtle":
            if parser.get('squirtle') == 1:
                parser.set('squirtle', 0)
            else: parser.set('squirtle', 1)
        elif switch == "charmander":
            if parser.get('charmander') == 1:
                parser.set('charmander', 0)
            else: parser.set('charmander', 1)
        elif switch == "annoy":
            if parser.get('annoy') == 1:
                parser.set('annoy', 0)
            else: parser.set('annoy', 1)
        elif switch == "lol":
            if parser.get('lol') == 1:
                parser.set('lol', 0)
            else: parser.set('lol', 1)
    

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
        annoy_id = int(input_id)
        amounts = try_amount
        SafeConfigParser.set('client_id', annoy_id)
        SafeConfigParser.set('attempts', amounts)
        await ctx.send(f"Changed the ID!")

    


    @commands.slash_command(
            name="test",
            description="Just getting a badge!!")
    async def _test(self, ctx):
            await ctx.response.defer()
            await ctx.send(f"Now I have my badge!!!")



def setup(client):
    client.add_cog(Coms(client))