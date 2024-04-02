from sqlite3 import connect
import disnake
from disnake.ext import commands
from disnake import Message, Option, OptionChoice, OptionType, ApplicationCommandInteraction
import asyncio
import datetime
from utility.embed import Custom_embed, Auction_embed
from utility.all_checks import Basic_checker
from utility.rarity_db import counts, countnumber
from utility.info_dict import embed_color,cmds,functions,info,events

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
                    #OptionChoice("Reminder Off","reminder0"),
                    #OptionChoice("Reminder On, no Ping","reminder1"),
                    #OptionChoice("Reminder On, with Ping","reminder2"),
                    OptionChoice("All Reminders Emote only off", "emoreminder0"),
                    OptionChoice("All Reminders Emote only on", "emoreminder1"),
                    OptionChoice("Spawn Reminder Off","spreminder0"),
                    OptionChoice("Spawn Reminder On, no Ping","spreminder1"),
                    OptionChoice("Spawn Reminder On, with Ping","spreminder2"),
                    OptionChoice("Fish Reminder Off","fireminder0"),
                    OptionChoice("Fish Reminder On, no Ping","fireminder1"),
                    OptionChoice("Fish Reminder On, with Ping","fireminder2"),
                    OptionChoice("Battle Reminder Off","bareminder0"),
                    OptionChoice("Battle Reminder On, no Ping","bareminder1"),
                    OptionChoice("Battle Reminder On, with Ping","bareminder2"),
                    OptionChoice("Quest Command Reminder Off","qureminder0"),
                    OptionChoice("Quest Command Reminder On, no Ping","qureminder1"),
                    OptionChoice("Quest Command Reminder On, with Ping","qureminder2"),
                    OptionChoice("New Quest Reminder Off","qtreminder0"),
                    OptionChoice("New Quest Reminder On, no Ping","qtreminder1"),
                    OptionChoice("New Quest Reminder On, with Ping","qtreminder2"),
                    OptionChoice("Other Reminder Off","otreminder0"),
                    OptionChoice("Other Reminder On, no Ping","otreminder1"),
                    OptionChoice("Other Reminder On, with Ping","otreminder2")
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
                await ctx.send("Toggled on.", ephemeral= True)
            elif switch == "grazz" and row[2] == 1:
                self.db.execute(f'UPDATE Toggle SET Grazz = 0 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled off.", ephemeral= True)
            elif switch == "repel" and row[3] == 0:
                self.db.execute(f'UPDATE Toggle SET Repel = 1 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled on.", ephemeral= True)
                
            elif switch == "repel" and row[3] == 1:
                self.db.execute(f'UPDATE Toggle SET Repel = 0 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled off.", ephemeral= True)
                
            elif switch == "starter" and row[4] == 0:
                self.db.execute(f'UPDATE Toggle SET Starter = 1 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled on.", ephemeral= True)
            elif switch == "starter" and row[4] == 1:
                self.db.execute(f'UPDATE Toggle SET Starter = 0 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled off.", ephemeral= True)
            elif switch == "emoreminder0":
                self.db.execute(f'UPDATE Toggle SET Reminder = 0 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled your reminders to text style.", ephemeral= True)
            elif switch == "emoreminder1":
                self.db.execute(f'UPDATE Toggle SET Reminder = 1 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled your reminder to emote style.", ephemeral= True)
            # elif switch == "reminder0":
            #     self.db.execute(f'UPDATE Toggle SET Reminder = 0 WHERE User_ID = {ctx.author.id}')
            #     self.db.commit()
            #     await ctx.send("Toggled your reminders off.", ephemeral= True)
            # elif switch == "reminder1":
            #     self.db.execute(f'UPDATE Toggle SET Reminder = 1 WHERE User_ID = {ctx.author.id}')
            #     self.db.commit()
            #     await ctx.send("Toggled reminders on, but I wont ping you.", ephemeral= True)
            # elif switch == "reminder2":
            #     self.db.execute(f'UPDATE Toggle SET Reminder = 2 WHERE User_ID = {ctx.author.id}')
            #     self.db.commit()
            #     await ctx.send("Toggled reminders on, and I will ping you.", ephemeral= True)
            elif switch == "spreminder0":
                self.db.execute(f'UPDATE Toggle SET ToggleSpawn = 0 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled your spawn reminders off.", ephemeral= True)
            elif switch == "spreminder1":
                self.db.execute(f'UPDATE Toggle SET ToggleSpawn = 1 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled spawn reminders on, but I wont ping you.", ephemeral= True)
            elif switch == "spreminder2":
                self.db.execute(f'UPDATE Toggle SET ToggleSpawn = 2 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled spawn reminders on, and I will ping you.", ephemeral= True)
            elif switch == "fireminder0":
                self.db.execute(f'UPDATE Toggle SET ToggleFish = 0 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled your fish reminders off.", ephemeral= True)
            elif switch == "fireminder1":
                self.db.execute(f'UPDATE Toggle SET ToggleFish = 1 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled fish reminders on, but I wont ping you.", ephemeral= True)
            elif switch == "fireminder2":
                self.db.execute(f'UPDATE Toggle SET ToggleFish = 2 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled fish reminders on, and I will ping you.", ephemeral= True)
            elif switch == "bareminder0":
                self.db.execute(f'UPDATE Toggle SET ToggleBattle = 0 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled your battle reminders off.", ephemeral= True)
            elif switch == "bareminder1":
                self.db.execute(f'UPDATE Toggle SET ToggleBattle = 1 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled battle reminders on, but I wont ping you.", ephemeral= True)
            elif switch == "bareminder2":
                self.db.execute(f'UPDATE Toggle SET ToggleBattle = 2 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled battle reminders on, and I will ping you.", ephemeral= True)
            elif switch == "qureminder0":
                self.db.execute(f'UPDATE Toggle SET ToggleQuest = 0 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled your quest command reminders off.", ephemeral= True)
            elif switch == "qureminder1":
                self.db.execute(f'UPDATE Toggle SET ToggleQuest = 1 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled quest command reminders on, but I wont ping you.", ephemeral= True)
            elif switch == "qureminder2":
                self.db.execute(f'UPDATE Toggle SET ToggleQuest = 2 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled quest command reminders on, and I will ping you.", ephemeral= True)
            elif switch == "qtreminder0":
                self.db.execute(f'UPDATE Toggle SET ToggleQuestTimer = 0 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled your new quest reminders off.", ephemeral= True)
            elif switch == "qtreminder1":
                self.db.execute(f'UPDATE Toggle SET ToggleQuestTimer = 1 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled new quest reminders on, but I wont ping you.", ephemeral= True)
            elif switch == "qtreminder2":
                self.db.execute(f'UPDATE Toggle SET ToggleQuestTimer = 2 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled new quest reminders on, and I will ping you.", ephemeral= True)
            elif switch == "otreminder0":
                self.db.execute(f'UPDATE Toggle SET ToggleOthers = 0 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled your other reminders off.", ephemeral= True)
            elif switch == "otreminder1":
                self.db.execute(f'UPDATE Toggle SET ToggleOthers = 1 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled other reminders on, but I wont ping you.", ephemeral= True)
            elif switch == "otreminder2":
                self.db.execute(f'UPDATE Toggle SET ToggleOthers = 2 WHERE User_ID = {ctx.author.id}')
                self.db.commit()
                await ctx.send("Toggled other reminders on, and I will ping you.", ephemeral= True)


    @commands.slash_command(name="event", description="Shows the current Leaderboard, if there's an event.")
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
        
    @commands.slash_command(name="bag", description="Take a look into your bag.")
    async def bag(self, ctx):
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

    @commands.slash_command(name="feed", description="Give a Cookie to Mega Gengar.")
    async def feed(self,ctx,amount = None):
        sender = ctx.author.id
        print(sender)
        data = self.db.execute(f'SELECT * FROM Events WHERE User_ID = {sender}')
        data = data.fetchall()
        if amount == None:
            #print("No extra input")
            if data:
                if data[0][4] == 0:
                    await ctx.send("Oh no! Looks like there are not enough cookies in your bag!")
                else:
                    newamount = data[0][4]-1
                    self.db.execute(f'UPDATE Events SET ItemsUsed = ItemsUsed + 1, Items = Items - 1 WHERE User_ID = {sender}')
                    self.db.commit()
                    await ctx.send("That was yummy! You have "+f'{newamount}'+" cookies left right now.")
        elif amount == "all":
            if data:
                self.db.execute(f'UPDATE Events SET ItemsUsed = ItemsUsed + Items, Items == 0 WHERE User_ID = {sender}')
                self.db.commit()
                await asyncio.sleep(0.5)
                await ctx.send("That was yummy! You have 0 cookies left right now.")
        elif int(amount) > 0:
            print(amount)
            reducer = int(amount)
            if data:
                if reducer > data[0][4]:
                    await ctx.send("Oh no! Looks like there are not enough cookies in your bag!")
                else:
                    self.db.execute(f'UPDATE Events SET ItemsUsed = ItemsUsed + {reducer}, Items = Items - {reducer} WHERE User_ID = {sender}')
                    self.db.commit()
                    newamount = data[0][4]-reducer
                    await ctx.send("That was yummy! You have "+f'{newamount}'+" cookies left right now.")

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

    # @commands.slash_command(name="hunt",description="Shows you the current hunt targets during a hunt event.")
    # async def hunt(self, ctx):
        # data = self.db.execute(f'SELECT * FROM Hunt')
        # data = data.fetchall()
        # max = self.db.execute(f'SELECT Count(*) FROM Hunt')
        # max = max.fetchone()[0]
        # #max = max.rowcount
        # #print(max)
        # if data:
        #     embed = disnake.Embed(description="Current Hunt Pokémon",color=0x807ba6)
        #     embed.set_author(name="ᵖᵃʳᵃˡʸᵐᵖᶤᶜˢ Hunt System")
        #     embed.set_footer(text=f'{self.client.user.display_name}',icon_url=f'{self.client.user.avatar}')
        #     guild = ctx.guild
        #     embed.set_thumbnail(url=guild.icon)
        #     #print("0x807ba6")
        #     i = 0
        #     while i < (max):
        #         #print("First i is:"+str(i))
        #         embed.add_field(name=("**"+str(data[i][1])+"**with threshold of "+str(data[i][2])),value="",inline=False)
        #         #embed.add_field(name=" ",value=" ",inline=True)
        #         #print("Added embed")
        #         i+=1
        #         #print(i)
            
        #     await ctx.send(embed=embed)
        # else:
        #     await ctx.send("There is no hunt event at the moment.")
        
    @commands.slash_command(name="faq", description="Quickest way to the faq")
    async def _faq(self, ctx):
        await ctx.send("The FAQ Channel is here: <#1161686361091350608>",ephemeral=True)
        
    @commands.slash_command(name="info", description="Important informations about the bot and its functions.",options=
                [Option(
                name="switch",
                description="Choose a switch to know more.",
                type=3,
                choices=[
                    OptionChoice("Commands", "cmnds"),
                    OptionChoice("Functions", "functions"),
                    OptionChoice("Event", "event")
                ],
                required=False
            ), ],
            )
    async def _info(self,ctx,switch = None):
        await ctx.response.defer()
        embed = disnake.Embed(description=f'{self.client.user.display_name}'+" overview",color = embed_color)
        embed.set_footer(text=f'{self.client.user.display_name}', icon_url=f'{self.client.user.avatar}')
        embed.set_thumbnail(url=embed.footer.icon_url)
        if switch == "cmnds":
            embed.add_field(name="**__Toggle__**",value=cmds["toggle"],inline=False)
            embed.add_field(name="**__Random__**", value=cmds["random"],inline=False)
            embed.add_field(name="**__Clan Hunts__**", value=cmds["hunt"],inline=False)
            embed.add_field(name="**__Top Count__**",value=cmds["topcount"], inline=False)
            embed.add_field(name=" ", value=" ",inline=False)
            embed.add_field(name="Miscellanous Cmds", value=cmds["misc"],inline=False)
            await ctx.send(embed=embed)
        elif switch == "functions":
            embed.add_field(name="**__Boost notifier__**",value=functions["boost"],inline=False)
            embed.add_field(name="**__Rare Spawns__**",value=functions["rare"],inline=False)
            embed.add_field(name="**__Reminders__**",value=functions["remind"], inline=False)
            embed.add_field(name=" ", value=" ",inline=False)
            embed.add_field(name="Miscellanous Functions",value=functions["misc"], inline=False)
            await ctx.send(embed=embed)
        elif switch == "event":
            embed.add_field(name="**__Events__**",value=events["event"],inline=False)
            embed.add_field(name="**__Possible Activites__**",value=events["active"],inline=False)
            embed.add_field(name="**__Point System__**",value=events["points"],inline=False)
            embed.add_field(name="**__Feeding__**",value=events["feed"],inline=False)
            embed.add_field(name=" ", value=" ",inline=False)
            embed.add_field(name="Commands",value=events["cmd"])
            await ctx.send(embed=embed)
        else:
            embed.add_field(name="**__Info Panel__**",value=info["text"])
            await ctx.send(embed=embed)
    
    @commands.check(Basic_checker().check_admin)
    @commands.slash_command(name="setup", description="First setup of the bot (can be changed later too ofc).", 
                            options=[Option(name="mode", description="What you want to set up.", choices=[OptionChoice("Gengar Changelog","chlo"), OptionChoice("Meow Rare Spawn","rasp"), OptionChoice("Psycord Outbreak Channel", "outbr"), OptionChoice("Psycord Wild Spawn Ping", "role")], required=False),
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
            desc += f"> * __Psycord Outbreaks & Wild Spawns__: If you have the outbreak feed from Psycord set up in your server, you can get pings when a certain Pokémon has an outbreak and there can be pings whenever a wild Pokémon gets spawned due to server activity.\n"
            desc += f"> * Usage: ``outbreaks [set/delete] [channel id]`` for outbreak pings.\n> * Usage: ``outbreaks [role] [role id]``\n\n\n*Parameters in [] are mandatory.*"

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
        elif mode == "outbr":
            if set == "set":
                try:
                    log = self.client.get_channel(ID)
                    print(log)
                    self.db.execute(f'UPDATE Admin SET PsyhuntFeed = {ID} WHERE Server_ID = {guild.id}')
                    self.db.commit()
                    _emb = await Auction_embed(self.client, description=f"<@{ctx.author.id}> has set up this channel to check for Psycord outbreaks.").setup_embed()
                    await log.send(embed=_emb)
                    await ctx.send(f"Successfully set <#{ID}> as your Psycord outbreaks feed channel.")
                except Exception as e:
                    asyncio.create_task(self.errorlog(e, ctx.author, guild, ID))
                    await ctx.send("Wrong usage, please refer back to the command usage.")
            elif set == "delete":
                self.db.execute(f'UPDATE Admin SET PsyhuntFeed = NULL WHERE Server_ID = {guild.id}')
                self.db.commit()
                await ctx.send(f"I've removed psycord outbreak pings from this server.")
            else:
                await ctx.send()
        elif mode == "role":
            if set == "set":
                try:
                    log = guild.get_role(ID)
                    self.db.execute(f'UPDATE Admin SET PsyhuntRole = {ID} WHERE Server_ID = {guild.id}')
                    self.db.commit()
                    _emb = await Auction_embed(self.client, description=f"<@{ctx.author.id}> has set up <@&{ID}> to ping for Psycord spawns.").setup_embed()
                    await ctx.send(embed=_emb)
                except Exception as e:
                    asyncio.create_task(self.errorlog(e, ctx.author, guild, ID))
                    await ctx.send("Please enter a valid Role ID.")
            elif set == "delete":
                self.db.execute(f'UPDATE Admin SET PsyhuntRole = NULL WHERE Server_ID = {guild.id}')
                self.db.commit()
                await ctx.send(f"I've removed psycord wild spawn pings from this server.")
        else:
            await ctx.send()
        
        
            
def setup(client):
    client.add_cog(SlashComs(client))