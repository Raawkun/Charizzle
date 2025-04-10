import asyncio
import datetime
import math
import random
from sqlite3 import connect
import disnake
from disnake.ext import commands
import pictures
from PIL import Image


async def errorlog(self, error, message,author):
        footer = f"{datetime.datetime.now(datetime.timezone.utc)}"
        desc = f"{message.guild.name}, <#{message.channel}>, <@{author.id}>\n[Original Message.]({message.jump_url()})"
        _emb = disnake.Embed(footer=footer, description=desc)
        _emb.add_field(name="Error:",value=error)
        errcha = self.client.get_channel(1210143608355823647)
        await errcha.send(embed=_emb)

class LureButton(disnake.ui.Button):
    def __init__(self, user_id,row,data,angry,eating,cr,run,moves):
        super().__init__(label="Bait", style=disnake.ButtonStyle.primary,custom_id=f"lure_button_{user_id}",row=row)
        self.user_id,self.data, self.eating, self.moves= user_id, data, eating, moves
        self.run, self.angry, self.cr= run, angry, cr
        self.db = connect("database.db")

    async def callback(self, interaction: disnake.MessageInteraction):
        try:
            await interaction.response.defer()
            if interaction.user.id != self.user_id:
                exit
            self.eating += random.randint(1,5)
            if self.eating > 255:
                self.eating = 255
            self.cr = math.floor(self.cr/2)
            self.angry = 0
            desc = f"Wild {self.data[1]} is eating."
            self.run = int(self.run/2)
            self.moves +=1
            footer = f"Moves taken: {self.moves}"
            await interaction.edit_original_response(desc,attachments=[])
        except Exception as e:
            await errorlog(self, e, interaction, interaction.user)

class StoneButton(disnake.ui.Button):
    def __init__(self, user_id,row,data,angry,eating,cr,run ,moves):
        super().__init__(label="Rock", style=disnake.ButtonStyle.primary,custom_id=f"stone_button_{user_id}",row=row)
        self.user_id,self.data, self.eating, self.moves= user_id, data, eating, moves
        self.run, self.angry, self.cr= run, angry, cr
        self.db = connect("database.db")

    async def callback(self, interaction: disnake.MessageInteraction):
        try:
            await interaction.response.defer()
            if interaction.user.id != self.user_id:
                exit
            self.angry += random.randint(1,5)
            if self.angry > 255:
                self.angry = 255
            self.cr *=2
            if self.cr > 255:
                self.cr = 255
            self.eating = 0
            desc = f"Wild {self.data[1]} is angry."
            self.run = int(self.run*2)
            self.moves +=1
            footer = f"Moves taken: {self.moves}"
            await interaction.edit_original_response(desc,attachments=[])
        except Exception as e:
            await errorlog(self, e, interaction, interaction.user)

class BallButton(disnake.ui.Button):
    def __init__(self, user_id,row,data,angry,eating,cr,run, moves):
        super().__init__(label="Ball", style=disnake.ButtonStyle.primary,custom_id=f"ball_button_{user_id}",row=row)
        self.user_id,self.data, self.eating, self.moves= user_id, data, eating, moves
        self.run, self.angry, self.cr= run, angry, cr
        self.db = connect("database.db")

    async def callback(self, interaction: disnake.MessageInteraction):
        try:
            await interaction.response.defer()
            if interaction.user.id != self.user_id:
                exit
            if self.angry > 0:
                self.angry -= 1
            elif self.eating > 0:
                self.eating -= 1
            n = random.randint(1,150)
            desc = f"You've caught the wild **{self.data[1]}**! Congratulations!"
            try:
                self.db.execute(f"UPDATE Safari SET Caught = Caught+1 WHERE User_ID = {self.user_id.id}")
                self.db.commit()
            except:
                self.db.execute(f"INSERT INTO Safari (USer_ID) VALUES ({self.user_id.id})")
                self.db.commit()
            self.moves +=1
            footer = f"Moves taken: {self.moves}"
            await interaction.edit_original_response(desc,attachments=[])
        except Exception as e:
            await errorlog(self, e, interaction, interaction.user)

class FleeButton(disnake.ui.Button):
    def __init__(self, user_id,row,data):
        super().__init__(label="Flee", style=disnake.ButtonStyle.primary,custom_id=f"fleelure_button_{user_id}",row=row)
        self.user_id = user_id
        self.data = data

    async def callback(self, interaction: disnake.MessageInteraction):
        try:
            await interaction.response.defer()
            if interaction.user.id != self.user_id:
                exit
            desc = f"You decided to run away from the wild **{self.data[1]}**\nYou got away safely."
            emb = disnake.Embed(title=f"{self.user_id.display_name} ran away.",color=disnake.Color.dark_grey(),description=desc)
            await interaction.edit_original_response(content="",embed=emb,view=None,attachments=[])
        except Exception as e:
            await errorlog(self, e, interaction, interaction.user)


class SafariView(disnake.ui.View):
    def __init__(self, user_id,db,angry,eating,cr,run,moves):
        super().__init__()
        row = 1
        self.add_item(LureButton(user_id,row,db,angry,eating,cr,run,moves))
        self.add_item(StoneButton(user_id,row,db,angry,eating,cr,run,moves))
        row = 2
        self.add_item(BallButton(user_id,row,db,angry,eating,cr,run,moves))
        self.add_item(FleeButton(user_id,row,db))


async def Safari(self, message, db, user):
    #print("Safari running")
    try:
        name,pic = db[1],db[15]
        #print(name)
        desc = f"You've encountered a wild **{name}** in the Safari Zone!"
        emb = disnake.Embed(description=desc,color=disnake.Colour.dark_green())
        emb.set_image(file=disnake.File("pictures/trainerback.png"))
        emb.set_author(name="Gengars Safari Event")
        emb.set_thumbnail(url=pic)
        angry, eating, cr, moves = 0, 0, 0, 0
        run = 2*db[9]
        await message.reply(embed=emb,view=SafariView(user,db,angry,eating,cr,run,moves))
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
            #print(id)
            data = self.db.execute(f"SELECT * FROM Dex WHERE DexID = {id}")
            data = data.fetchone()
            #print(data)
            await Safari(self,ctx,data,ctx.author)
        except Exception as e:
            await asyncio.create_task(errorlog(e, ctx.author.id))



def setup(client):
    client.add_cog(SafariEvent(client))