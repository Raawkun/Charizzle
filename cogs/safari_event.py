import asyncio
import datetime
from sqlite3 import connect
import disnake
from disnake.ext import commands
import pictures
from PIL import Image


async def errorlog(self, error, message,author):
        footer = f"{datetime.datetime.utcnow()}"
        desc = f"{message.guild.name}, <#{message.channel}>, <@{author.id}>\n[Original Message.]({message.jump_url})"
        _emb = disnake.Embed(footer=footer, description=desc)
        _emb.add_field(name="Error:",value=error)
        errcha = self.client.get_channel(1210143608355823647)
        await errcha.send(embed=_emb)

class LureButton(disnake.ui.Button):
    def __init__(self, user_id,row):
        super().__init__(label="Lure", style=disnake.ButtonStyle.primary,custom_id=f"lure_button_{user_id}"),row=row
        self.user_id = user_id
        self.db = connect("database.db")

    async def callback(self, interaction: disnake.MessageInteraction):
        try:
            await interaction.defer()
            if interaction.user.id != self.user_id:
                exit
        except Exception as e:
            await asyncio.create_task(errorlog(e,interaction.user.id))

class BallButton(disnake.ui.Button):
    def __init__(self, user_id,row):
        super().__init__(label="Lure", style=disnake.ButtonStyle.primary,custom_id=f"lure_button_{user_id}",row=row)
        self.user_id = user_id
        self.db = connect("database.db")

    async def callback(self, interaction: disnake.MessageInteraction):
        try:
            await interaction.defer()
            if interaction.user.id != self.user_id:
                exit
        except Exception as e:
            await asyncio.create_task(errorlog(e,interaction.user.id))

class FleeButton(disnake.ui.Button):
    def __init__(self, user_id,row):
        super().__init__(label="Lure", style=disnake.ButtonStyle.primary,custom_id=f"lure_button_{user_id}",row=row)
        self.user_id = user_id
        self.db = connect("database.db")

    async def callback(self, interaction: disnake.MessageInteraction):
        try:
            await interaction.defer()
            if interaction.user.id != self.user_id:
                exit
        except Exception as e:
            await asyncio.create_task(errorlog(e,interaction.user.id))

class StoneButton(disnake.ui.Button):
    def __init__(self, user_id,row):
        super().__init__(label="Lure", style=disnake.ButtonStyle.primary,custom_id=f"lure_button_{user_id}",row=row)
        self.user_id = user_id
        self.db = connect("database.db")

    async def callback(self, interaction: disnake.MessageInteraction):
        try:
            await interaction.defer()
            if interaction.user.id != self.user_id:
                exit
        except Exception as e:
            await asyncio.create_task(errorlog(e,interaction.user.id))

class SafariView(disnake.ui.View):
    def __init__(self, user_id):
        super().__init__()
        row = 1
        self.add_item(LureButton(user_id,row))
        self.add_item(StoneButton(user_id,row))
        row = 2
        self.add_item(BallButton(user_id,row))
        self.add_item(FleeButton(user_id,row))


async def SafariEvent(self, message, db, user):
    try:
        name,pic,speed = db[1],db[15],db[9]
        desc = f"You've encountered a wild **{name}** in the Safari Zone!"
        emb = disnake.Embed(description=desc,color=disnake.Colour.dark_green())
        backside = Image.open("pictures/trainerback.png","r")
        emb.set_thumbnail(file=backside)
        emb.set_author(name="Gengars Safari Event")
        emb.set_image(url=pic)
        await message.channel.reply(embed=emb,view=SafariView)
    except Exception as e:
        await asyncio.create_task(errorlog(e, user.id))



class SafariEvent(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")

    current_time = datetime.datetime.now()
    timestamp = current_time.strftime('%Y-%m-%d %H:%M')


    @commands.command()
    async def safari(self,id):
        return



    def setup(client):
        client.add_cog(SafariEvent(client))