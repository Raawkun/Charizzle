from sqlite3 import connect
import disnake
import asyncio
from disnake.ext import commands
import datetime
from utility.embed import Custom_embed
from utility.drop_chance import drop_pos, buyin
from utility.info_dict import embed_color, cmds, functions, events, info, psycord

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
                embed.add_field(name="**__Toggle__**",value=cmds["toggle"],inline=False)
                embed.add_field(name="**__Random__**", value=cmds["random"],inline=False)
                embed.add_field(name="**__Clan Hunts__**", value=cmds["hunt"],inline=False)
                embed.add_field(name="**__Top Count__**",value=cmds["topcount"], inline=False)
                embed.add_field(name=" ", value=" ",inline=False)
                embed.add_field(name="Miscellanous Cmds", value=cmds["misc"],inline=False)
                await ctx.send(embed=embed)
            elif message in ["functions","Functions","funct"]:
                embed.add_field(name="**__Boost notifier__**",value=functions["boost"],inline=False)
                embed.add_field(name="**__Rare Spawns__**",value=functions["rare"],inline=False)
                embed.add_field(name="**__Reminders__**",value=functions["remind"], inline=False)
                embed.add_field(name=" ", value=" ",inline=False)
                embed.add_field(name="Miscellanous Functions",value=functions["misc"], inline=False)
                await ctx.send(embed=embed)
            elif message in ["event", "events","ev","Event","Events", "Ev"]:
                embed.add_field(name="**__Events__**",value=events["event"],inline=False)
                embed.add_field(name="**__Possible Activites__**",value=events["active"],inline=False)
                embed.add_field(name="**__Point System__**",value=events["points"],inline=False)
                embed.add_field(name="**__Feeding__**",value=events["feed"],inline=False)
                embed.add_field(name=" ", value=" ",inline=False)
                embed.add_field(name="Commands",value=events["cmd"])
                await ctx.send(embed=embed)
            elif message in ["psy", "psycord","Psy","Psycord"]:
                embed.add_field(name="**__Outbreaks__**", value=psycord["outbreaks"], inline=False)
                embed.add_field(name="**__Wild Spawns__**",value=psycord["wild"], inline=False)
                embed.add_field(name="**__Leftover Codes__**",value=psycord["codes"], inline=False)
                embed.add_field(name="**__Flexing__**",value=psycord["flex"], inline=False)
        else:
            embed.add_field(name="**__Info Panel__**",value=info["text"])
            await ctx.send(embed=embed)
        


def setup(client):
    client.add_cog(Info_Cmd(client))