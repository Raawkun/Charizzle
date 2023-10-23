
# dependancies
import asyncio
import disnake

#time
import time
import datetime
from datetime import datetime, timedelta

import random

# basic checker
class Basic_checker:
    """
    Manages the basic checks.
    """

    async def check_admin(self, ctx):
        if ctx.author.guild_permissions.administrator:
            return True
        
        await ctx.send("You need to have admin rights to use this command.", ephemeral=True)
        return False

    async def check_management(self, ctx):
        management_role_name = "Management"  # Replace with the actual role name
        
        for role in ctx.author.roles:
            if role.name == management_role_name:
                return True
        
        await ctx.send("You need to have the 'Management' role to use this command.", ephemeral=True)
        return False

    async def check_server(self, ctx):
        if ctx.guild.id == 825813023716540426:
            return True
        await ctx.send("Sorry, this only works in the Paralympics server.", ephemeral=True)
        return(False)
    
    async def check_if_it_is_me(self, ctx):
        if ctx.user.id == 427135226066501642:
            return(True)
        else:
            await ctx.send(f"Sorry, only Pr1nc3✯ can use this command", ephemeral=True)
            return(False)

    async def check_station_channel(self, ctx):
        if ctx.channel.id == 1079409997496193145:
            return(True)
        else:
            await ctx.send("You can't use that in here, you must go to <#1079409997496193145>", ephemeral=True)
            return(False)