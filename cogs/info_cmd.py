from sqlite3 import connect
import disnake
import asyncio
from disnake.ext import commands
import datetime
from utility.embed import Custom_embed

class Info_Cmd(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")

    
    
    current_time = datetime.datetime.utcnow()
    timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')

    @commands.command()
    async def info(self, ctx, message = None):
        embed = disnake.Embed(description=f'{self.client.user.display_name}'+" overview",color = 0x807ba6)
        embed.set_footer(text=f'{self.client.user.display_name}', icon_url=f'{self.client.user.avatar}')
        embed.set_thumbnail(url=embed.footer.icon_url)
        if message:
            if message in ["commands","cmds","Commands","Cmds"]:
                embed.add_field(name="**__Toggle__**",value="> ``toggle`` - to see your current settings.\n> ``/toggle`` - for enabling/disabling certain functions.",inline=False)
                embed.add_field(name="**__Random__**", value="> ``random`` - a rng for Pokémon.",inline=False)
                embed.add_field(name="**__Clan Hunts__**", value="> ``hunt`` - for checking the current hunt.",inline=False)
                embed.add_field(name="**__Top Count__**",value="> ``topcount`` to check valid parameter; will show the most catches since last encounter")
                embed.add_field(name=" ", value=" ",inline=False)
                embed.add_field(name="Miscellanous Cmds", value="> ``calc`` - enter a formula to get a result.\n> ``joined`` - find out when you entered the server.\n> ``test`` - Well, a test command.",inline=False)
                await ctx.send(embed=embed)
            elif message in ["functions","Functions"]:
                embed.add_field(name="**__Boost notifier__**",value="> Offers different kinds of notifiers when boosts (Repels, Grazz, Honey) are expired in a spawn.\n> You can toggle them on/off via ``/toggle``.",inline=False)
                embed.add_field(name="**__Rare Spawns__**",value="> Posts rare spawns, exclusive hatches and much more into <#825950637958234133> - go check it out!",inline=False)
                embed.add_field(name=" ", value=" ",inline=False)
                embed.add_field(name="Miscellanous Functions",value="> This bot is a fun project. That's why there are fun responses to certain catchphrases, right now these catchphrases are 'lol', 'stfu' and the names of the kanto starters.\n> Last one can be disabled via ``/toggle`` ")
                await ctx.send(embed=embed)
        else:
            embed.add_field(name="**__Info Panel__**",value="Welcome to the "f'{self.client.user.display_name}'" Info Panel. Below you'll find sections you can trigger with the command.\n\nAvailable Info Pages:\n* **Commands** \n* **Functions** \n")
            await ctx.send(embed=embed)
        


def setup(client):
    client.add_cog(Info_Cmd(client))