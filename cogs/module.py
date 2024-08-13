import asyncio
import datetime
import os
import disnake
from disnake.ext import commands
import sqlite3
from sqlite3 import connect

import pytz
from  utility.rarity_db import poke_rarity, embed_color
from utility.embed import Custom_embed
from utility.drop_chance import drop_pos, rare_calc, ball_used_low, ball_used_high
import random
from utility.all_checks import Basic_checker
import pandas
import openpyxl

class Modules(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")

    async def darktest(self, message):
        if message.reference:
            ref_msg = await message.channel.fetch_message(message.reference.message_id)
            sender = ref_msg.author
        elif message.interaction:
            sender = message.interaction.author
        if sender.id == 475664587736481792 or sender.id == 352224989367369729:
            #print("Sjaap battle - testing for Dark mons.")
            if len(message.embeds)>0:
                emb = message.embeds[0]
                #print("Has an embed.")
                if emb.description:
                    #print("Has a description.")
                    opponent = emb.description.split("challenged ")[1]
                    opponent = opponent.split("**")[1]
                    #print(opponent)
                    mons = emb.description.split(opponent)[2]
                    #print(mons)
                    mon = [mons.split(":")[1], mons.split(":")[3], mons.split(":")[5]]
                    #print(mon)
                    #await message.channel.send(mon)
                    desc = ""
                    i = 1
                    for entry in mon:
                        dex = self.db.execute(f'SELECT DexID, Name, Type_1, Type_2 FROM Dex WHERE DexID = {entry}')
                        dex = dex.fetchone()
                        #print(dex)
                        if dex[2] == "darktype" or dex[3] == "darktype":
                            desc += f"Team-number {i}: {dex[1]} is a Dark type Pokémon.\n"
                        i = i + 1
                    if desc != "":
                        await message.reply(f"<@{sender.id}>\n{desc}")

    async def averagecoins(self, message):
        if message.reference:
            ref_msg = await message.channel.fetch_message(message.reference.message_id)
            sender = ref_msg.author
        elif message.interaction:
            sender = message.interaction.author
        if len(message.embeds)>0:
            emb = message.embeds[0]
            if emb.footer.text:
                coin = emb.footer.text.split(" earned ")[1]
                coin = coin.split(" ")[0]
                if "," in coin:
                    coin.replace(",", "")
                try:
                    self.db.execute(F"UPDATE average SET coins = coins + {int(coin)}, catch_count = catch_count + 1 WHERE UserID = {sender.id}")
                    self.db.commit()
                except:
                    self.db.execute(f"INSERT UserID = {sender.id}, username = '{sender.name}', catch_count = 1, coins = {int(coin)} INTO average")
                    self.db.commit()
    async def resetaverage(self):
        conn = sqlite3.connect('database.db')
        df = pandas.read_sql_query("SELECT * FROM average ORDER BY catch_count DESC", conn)
        file_path = "/tmp/exported_data.xlsx"
        df.to_excel(file_path,index=False,engine='openpyxl')
        conn.close()
        channel = self.client.get_channel(1272981076419149886)
        await channel.send(file=disnake.File(file_path))
        self.db.execute(f"DELETE * FROM average")
        self.db.commit()
        os.remove(file_path)
    async def averagetimer(self):
        while True:
            cet = pytz.timezone('CET')
            now = datetime.datetime.now(cet)
            days_until_monday = (7-now.weekday())%7
            if days_until_monday == 0 and now.hour >= 14:
                days_until_monday = 7 
            next_monday = now + datetime.timedelta(days=days_until_monday)
            next_monday_at_2pm = cet.localize(datetime.datetime(next_monday.year, next_monday.month, next_monday.day, 14, 0, 0))
            time_until = next_monday_at_2pm-now
            print(f"Setting a LB Timer for {time_until.total_seconds()} seconds.")
            await asyncio.sleep(time_until.total_seconds())
            await asyncio.create_task(self.resetaverage(self))


def setup(client):
    client.add_cog(Modules(client))