import asyncio
import math
import random
from sqlite3 import connect
from disnake.ext import commands

from utility.drop_chance import rare_calc, drop_pos, ball_used_high, ball_used_low,buyin,standard_rate


class Events(commands.Cog):
    
    def __init__(self, client):
            self.client = client
            self.db = connect("database.db")

    async def messageProcess(self, message):
        if message.reference:
            ref_msg = await message.channel.fetch_message(message.reference.message_id)
            sender = ref_msg.author
        elif message.interaction:
            ref_msg = message.interaction.user
            sender = ref_msg
        timestamp = message.created_at()
        guild = message.guild
        author, desc, footer, img, color, title, thumb,emb = None
        if (len(message.embeds)>0):
            emb = message.embeds[0]
            if emb.author.name:
                author = emb.author.name
            if emb.description:
                desc = emb.description
            if emb.footer:
                footer = emb.footer.text
            if emb.image:
                img = emb.image.link
            if emb.color:
                color = emb.color
            if emb.title:
                title = emb.title
            if emb.thumbnail:
                thumb = emb.thumbnail.url
        return(sender, timestamp, emb, img, guild, author, desc, footer, color, title, thumb)
            
    async def EventCheck(self, message):
        db = self.db.execute(f"SELECT Event FROM Admin WHERE Server_ID = {message.guild.id}")
        db = db.fetchone()
        if db[0] == 0:
            return
        else:
            user, timestamp, emb, img = await asyncio.create_task(self.messageProcess(message))
            buyin = await asyncio.create_task(self.BuyinCheck(user.id))
            if buyin == 1:
                itemdrop = await asyncio.create_task(self.ItemDropCheck(message, user, emb))

    async def BuyinCheck(self, user):
        db = self.db.execute(f"SELECT * FROM Events WHERE User_ID = {user.id}")
        db = db.fetchone()
        if db:
            if db[1] > buyin:
                return(1)
            else:
                return(0)
        else:
            return(1)
        
    async def ItemDropCheck(self, message, user, emb):
        dex = self.db.execute(f"SELECT * FROM Dex WHERE Img_url = '{emb.image.url}'")
        dex = dex.fetchone()
        if "caught a " in emb.description:
            ball = emb.description.split("with a ")[1]
            ball = ball.split("!")[0]
        method = drop_pos["battle"]
        if "water state" in emb.footer.text.lower():
            method = drop_pos["fish"]
        else:
            method = drop_pos["hunt"]
        if "hatched an" in emb.author.name:
            method = drop_pos["egg"]
        rarity = dex[13]
        ballbonus = ball_used_low[ball]
        rare = ["SuperRare", "Shiny", "Legendary", "Golden"]
        if rarity in rare:
            ballbonus = ball_used_high[ball]
        
        avg = ((method+rare_calc[rarity]+ballbonus)/3)
        red = math.log(1+avg)
        calc = standard_rate*(1 + red)*random.random()
        if calc > random.random():
            await message.channel.send(f"Oh?! {user.mention} - you've found a <:booster_pack:1261461055830491188> **Booster Pack**! You can open it with ``event open [qt]``")
            self.db.execute(f"UPDATE Events SET Items = Items + 1 WHERE User_ID = {user.id}")
            self.db.commit()
        else:
            return(0)




def setup(client):
    client.add_cog(Events(client))