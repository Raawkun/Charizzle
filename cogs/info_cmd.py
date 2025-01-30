from sqlite3 import connect
import disnake
import asyncio
from disnake.ext import commands
import datetime
from utility.embed import Custom_embed
from utility.info_dict import embed_color, cmds, functions, info

async def info_cmd(self, ctx):
    embed = disnake.Embed(description=f'{ctx.me.display_name}'+" overview",colour=embed_color)
    embed.set_footer(text=f'{ctx.me.display_name}', icon_url=f'{ctx.me.avatar}')
    embed.set_thumbnail(url=embed.footer.icon_url)
    
    embed.add_field(name="**__Toggle__**",value=cmds["toggle"],inline=False)
    embed.add_field(name="**__Random__**", value=cmds["random"],inline=False)
    embed.add_field(name="**__Clan Hunts__**", value=cmds["hunt"],inline=False)
    embed.add_field(name="**__Top Count__**",value=cmds["topcount"], inline=False)
    embed.add_field(name=" ", value=" ",inline=False)
    embed.add_field(name="Miscellanous Cmds", value=cmds["misc"],inline=False)
    return(embed)

async def info_funct(self,ctx):
    embed = disnake.Embed(description=f'{self.client.user.display_name}'+" overview",color = embed_color)
    embed.set_footer(text=f'{self.client.user.display_name}', icon_url=f'{self.client.user.avatar}')
    embed.set_thumbnail(url=embed.footer.icon_url)
    
    embed.add_field(name="**__Boost notifier__**",value=functions["boost"],inline=False)
    embed.add_field(name="**__Rare Spawns__**",value=functions["rare"],inline=False)
    embed.add_field(name="**__Reminders__**",value=functions["remind"], inline=False)
    embed.add_field(name=" ", value=" ",inline=False)
    embed.add_field(name="Miscellaneous Functions",value=functions["misc"], inline=False)
    return(embed)

class CmdButton(disnake.ui.Button):
    def __init__(self, user_id):
        super().__init__(label="Commands", style=disnake.ButtonStyle.primary, custom_id=f"cmd_button_{user_id}")
        self.user_id = user_id

    async def callback(self, interaction: disnake.MessageInteraction):
        
        if interaction.user.id != self.user_id:
            exit
        
        msg = await info_cmd(self, interaction)
        await interaction.response.edit_message(embed=msg)

class FnctButton(disnake.ui.Button):
    def __init__(self, user_id):
        super().__init__(label="Functions", style=disnake.ButtonStyle.primary, custom_id=f"fnct_button_{user_id}")
        self.user_id = user_id

    async def callback(self, interaction: disnake.MessageInteraction):
        
        if interaction.user.id != interaction.message.interaction.author.id:
            exit
        msg = await asyncio.create_task(info_funct(self,interaction))
        await interaction.response.edit_message(msg)

class GuessView(disnake.ui.View):
    def __init__(self, user_id):
        super().__init__()
        self.add_item(CmdButton(user_id))
        self.add_item(FnctButton(user_id))

class Info_Cmd(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")

    
    current_time = datetime.datetime.utcnow()
    timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')

        

    @commands.command(aliases = ["Info"])
    async def info(self, ctx, message = None):
        embed = disnake.Embed(description=f'{self.client.user.display_name}'+" overview",color = embed_color)
        embed.set_footer(text=f'{self.client.user.display_name}', icon_url=f'{self.client.user.avatar}')
        embed.set_thumbnail(url=embed.footer.icon_url)
        if message:
            if message in ["commands","cmds","Commands","Cmds"]:
                try:
                    embed = await self.info_cmd()
                    await ctx.send(embed=embed,view=GuessView(ctx.author.id))
                except Exception as e:
                    print(e)
            elif message in ["functions","Functions","funct"]:
                try:
                    embed = await self.info_funct()
                    await ctx.send(embed=embed,view=GuessView(ctx.author.id))
                except Exception as e:
                    print(e)
        else:
            try:
                embed.add_field(name="**__Info Panel__**",value=info["text"])
                await ctx.send(embed=embed,view=GuessView(ctx.author.id))
            except Exception as e:
                print(e)


def setup(client):
    client.add_cog(Info_Cmd(client))