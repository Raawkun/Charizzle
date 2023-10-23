import asyncio
from disnake.embeds import Embed

# config
import time
import datetime
from datetime import datetime

# class embed
class Custom_embed:

    def __init__(self, client, title = None, description = None, colour = None, footer = None, thumb = None):
        # bot
        self.client = client

        # embed
        self.title = title
        self.description = description
        self.colour = colour
        self.footer = footer
        self.thumb = thumb

    async def setup_embed(self):
        # init
        embed = Embed()

        # setting up
        if(self.title != None):
            embed.title = self.title
        
        if(self.description != None):
            embed.description = self.description
        
        if(self.colour != None):
            embed.colour = self.colour
        else:
            embed.colour = 0x807ba6
        
        if(self.footer != None):
            embed.set_footer(text=self.footer)
        else:
            embed.set_footer(text=f'{self.client.user.display_name}',icon_url=f'{self.client.user.avatar}')
        
        if(self.thumb != None):
            embed.set_thumbnail(url = self.thumb)
        else:
            embed.set_thumbnail(url = f'{self.client.user.avatar}')
        
        return(embed)