from sqlite3 import connect
import disnake
from disnake.ext import commands
from disnake import Message, Option, OptionChoice, OptionType, ApplicationCommandInteraction
import asyncio
import datetime
from utility.embed import Custom_embed, Auction_embed
from utility.all_checks import Basic_checker
from utility.rarity_db import counts, countnumber
from utility.info_dict import embed_color,cmds,functions,info

class SlashComs(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")

    async def errorlog(self, error, author, guild, channel):
        footer = f"{datetime.datetime.utcnow()}"
        desc = f"{guild.name}, <#{channel}>, <@{author.id}>"
        _emb = await Auction_embed(self.client,footer=footer, description=desc).setup_embed()
        _emb.add_field(name="Error:",value=error)
        errcha = self.client.get_channel(1210143608355823647)
        await errcha.send(embed=_emb)

    @commands.slash_command(
            name="test",
            description="Just getting a badge!!")
    async def _test(self, ctx):
            await ctx.response.defer()
            await ctx.send(f"Now I have my badge!!!")

    @commands.check(Basic_checker.check_if_it_is_me)
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


    @commands.slash_command(name="topcount",description="Shows a leaderboard for different ;count stats")
    async def topcount(self, ctx, category = None):
        cat = ["event","fullodd","legendary","item","goldenfish","shinyfish","legendaryfish","goldenexp","shinyexp","legendaryexp","icon"]
        if category:
            if category in cat:
                data = self.db.execute(f'SELECT * FROM Counter ORDER BY {category} DESC')
                data = data.fetchall()
                e = countnumber[category]
                embed = await Custom_embed(self.client,title=f"Top Count Leaderboard",description=f"Top 5 Leaderboard in "+counts[category]).setup_embed()

                embed.add_field(name="Place:",value="1.\n2.\n3.\n4.\n5.")
                embed.add_field(name="Username",value="<@"+str(data[0][0])+">\n"+"<@"+str(data[1][0])+">\n"+"<@"+str(data[2][0])+">\n"+"<@"+str(data[3][0])+">\n"+"<@"+str(data[4][0])+">")
                embed.add_field(name="Amount",value=str(data[0][e])+"\n"+str(data[1][e])+"\n"+str(data[2][e])+"\n"+str(data[3][e])+"\n"+str(data[4][e]))
                await ctx.send(embed=embed)
            if category == "total":
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
        
    @commands.slash_command(name="faq", description="Quickest way to the faq")
    async def _faq(self, ctx):
        await ctx.send("The FAQ Channel is here: <#1161686361091350608>",ephemeral=True)
        
    
    @commands.check(Basic_checker().check_admin)
    @commands.slash_command(name="setup", description="First setup of the bot (can be changed later too ofc).", 
                            options=[Option(name="mode", description="What you want to set up.", choices=[OptionChoice("Gengar Changelog","chlo"), OptionChoice("Meow Rare Spawn","rasp")], required=False),
                                Option(name="set", description="Wether to set it up or delete.", type=3, choices=[OptionChoice("Set", "set"), OptionChoice("Delete","delete")], required=False),
                                Option(name="id", description="Channel/Role ID", type=3, required=False),
                                
                                    ])
    
    async def _setup(self, ctx, mode = None, set = None, id = None):
        guild = ctx.guild
        if id != None:
            ID = int(id)
        if id == None:
            ID = ctx.channel.id
        if mode == None:
            title = f"{self.client.user.display_name}'s Setup"
            desc = f"This command is to setup {self.client.user.display_name}'s various feeds or pings.\n"
            desc += f"The following can be set up in this server at the moment.\n\n**Functions:**\n"
            desc += f"> * __Changelog__: {self.client.user.display_name}'s updates.\n"
            desc += f"> * Usage: ``changelog [set/delete] [channel id]``\n"
            desc += f"> * __PokéMeow Rare Spawns__: A solid feed for Meow spawns.\n> * Usage: ``rarespawn [set/delete] [channel id]``\n"
            
            _emb = await Auction_embed(self.client,title=title, description=desc).setup_embed()

            await ctx.send(embed = _emb)
        elif mode == "chlo":
            if set == "set":
                try:
                    log = self.client.get_channel(ID)
                    self.db.execute(f'UPDATE Admin SET Changelog = {ID} WHERE Server_ID = {guild.id}')
                    self.db.commit()
                    _emb = await Auction_embed(self.client, description=f"<@{ctx.author.id}> has set up this channel to receive <@{self.client.user.id}>'s update logs.").setup_embed()
                    await log.send(embed=_emb)
                    await ctx.send(f"Successfully set <#{ID}> as your changelog channel for my updates.")
                except Exception as e:
                    asyncio.create_task(self.errorlog(e, ctx.author, guild, ID))
                    await ctx.send("Please enter a Channel ID.")
            elif set == "delete":
                self.db.execute(f'UPDATE Admin SET Changelog = NULL WHERE Server_ID = {guild.id}')
                self.db.commit()
                await ctx.send(f"I've removed changelog updates from this server.")
            else:
                await ctx.send()
        elif mode == "rasp":
            if set == "set":
                try:
                    log = self.client.get_channel(ID)
                    self.db.execute(f'UPDATE Admin SET RareSpawn = {ID} WHERE Server_ID = {guild.id}')
                    self.db.commit()
                    _emb = await Auction_embed(self.client, description=f"<@{ctx.author.id}> has set up this channel to receive PokéMeow rare spawns.").setup_embed()
                    await log.send(embed=_emb)
                    await ctx.send(f"Successfully set <#{ID}> as your rare spawn channel for PokéMeow.")
                except Exception as e:
                    asyncio.create_task(self.errorlog(e, ctx.author, guild, ID))
                    await ctx.send("Please enter a Channel ID.")
            elif set == "delete":
                self.db.execute(f'UPDATE Admin SET RareSpawn = NULL WHERE Server_ID = {guild.id}')
                self.db.commit()
                await ctx.send(f"I've removed PokéMeow rare spawn updates from this server.")
            else:
                await ctx.send()
        else:
            await ctx.send()
        
        
            
def setup(client):
    client.add_cog(SlashComs(client))