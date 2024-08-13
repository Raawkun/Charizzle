import datetime
import disnake
from disnake.ext import commands
import sqlite3
from sqlite3 import connect
from  utility.rarity_db import poke_rarity, embed_color
from utility.embed import Custom_embed
from utility.drop_chance import drop_pos, rare_calc, ball_used_low, ball_used_high
import random
from utility.all_checks import Basic_checker

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
    


def setup(client):
    client.add_cog(Modules(client))