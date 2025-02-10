import asyncio
import datetime
from sqlite3 import connect
import disnake
from disnake.ext import commands
import pictures
from PIL import Image


async def errorlog(self, error, message,author):
        footer = f"{datetime.datetime.now(datetime.timezone.utc)}"
        desc = f"{message.guild.name}, <#{message.channel}>, <@{author.id}>\n[Original Message.]({message.jump_url})"
        _emb = disnake.Embed(footer=footer, description=desc)
        _emb.add_field(name="Error:",value=error)
        errcha = self.client.get_channel(1210143608355823647)
        await errcha.send(embed=_emb)

class LureButton(disnake.ui.Button):
    def __init__(self, user_id,row,db):
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

class BallButton(disnake.ui.Button):
    def __init__(self, user_id,row,db):
        super().__init__(label="Ball", style=disnake.ButtonStyle.primary,custom_id=f"ball_button_{user_id}",row=row)
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
        super().__init__(label="Flee", style=disnake.ButtonStyle.primary,custom_id=f"fleelure_button_{user_id}",row=row)
        self.user_id = user_id
        self.db = connect("database.db")

    async def callback(self, interaction: disnake.MessageInteraction):
        try:
            await interaction.defer()
            if interaction.user.id != self.user_id:
                exit
            desc = f"You decided to run away from the wild **{self.db[1]}**\nYou got away safely."
            emb = disnake.Embed(title=f"{self.user_id.display_name} ran away.",color=disnake.Color.dark_grey())
            await interaction.edit_original_response(embed=emb)
        except Exception as e:
            await asyncio.create_task(errorlog(e,interaction.user.id))

class StoneButton(disnake.ui.Button):
    def __init__(self, user_id,row,db):
        super().__init__(label="Stone", style=disnake.ButtonStyle.primary,custom_id=f"stone_button_{user_id}",row=row)
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
    def __init__(self, user_id,speed):
        super().__init__()
        row = 1
        self.add_item(LureButton(user_id,row,speed))
        self.add_item(StoneButton(user_id,row,speed))
        row = 2
        self.add_item(BallButton(user_id,row,speed))
        self.add_item(FleeButton(user_id,row))


async def Safari(self, message, db, user):
    print("Safari running")
    try:
        name,pic = db[1],db[15]
        print(name)
        desc = f"You've encountered a wild **{name}** in the Safari Zone!"
        emb = disnake.Embed(description=desc,color=disnake.Colour.dark_green())
        backside = Image.open("pictures/trainerback.png","r")
        emb.set_thumbnail(file=disnake.File("pictures/trainerback.png"))
        emb.set_author(name="Gengars Safari Event")
        emb.set_image(url=pic)
        await message.reply(embed=emb,view=SafariView(user,db))
    except Exception as e:
        print(e)



class SafariEvent(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")

    current_time = datetime.datetime.now()
    timestamp = current_time.strftime('%Y-%m-%d %H:%M')


    @commands.command()
    async def testsafari(self, ctx, id: int):
        try:
            print(id)
            data = self.db.execute(f"SELECT * FROM Dex WHERE DexID = {id}")
            data = data.fetchone()
            print(data)
            await Safari(self,ctx,data,ctx.author)
        except Exception as e:
            await asyncio.create_task(errorlog(e, ctx.author.id))



def setup(client):
    client.add_cog(SafariEvent(client))