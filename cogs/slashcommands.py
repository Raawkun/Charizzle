from sqlite3 import connect
import disnake
from disnake.ext import commands
from disnake import Message, Option, OptionChoice, OptionType, ApplicationCommandInteraction
import asyncio
from utility.embed import Custom_embed

class SlashComs(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")

    @commands.slash_command(
            name="test",
            description="Just getting a badge!!")
    async def _test(self, ctx):
            await ctx.response.defer()
            await ctx.send(f"Now I have my badge!!!")


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
            if switch == "grazz" and row[2] == 0:
                self.db.execute(f'UPDATE Toggle SET Grazz = 1 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled on")
            elif switch == "grazz" and row[2] == 1:
                self.db.execute(f'UPDATE Toggle SET Grazz = 0 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled off")
            elif switch == "repel" and row[3] == 0:
                self.db.execute(f'UPDATE Toggle SET Repel = 1 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled on")
                
            elif switch == "repel" and row[3] == 1:
                self.db.execute(f'UPDATE Toggle SET Repel = 0 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled off")
                
            elif switch == "starter" and row[4] == 0:
                self.db.execute(f'UPDATE Toggle SET Starter = 1 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled on")
            elif switch == "starter" and row[4] == 1:
                self.db.execute(f'UPDATE Toggle SET Starter = 0 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled off")
            elif switch == "privacy" and row[5] == 0:
                self.db.execute(f'UPDATE Toggle SET Privacy = 1 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled on")
            elif switch == "privacy" and row[5] == 1:
                self.db.execute(f'UPDATE Toggle SET Privacy = 0 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled off")



def setup(client):
    client.add_cog(SlashComs(client))