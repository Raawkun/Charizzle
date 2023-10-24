import datetime
import disnake
from disnake.ext import commands
import sqlite3
from sqlite3 import connect
from  utility.rarity_db import poke_rarity
from utility.embed import Custom_embed

class On_Edit(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")

    current_time = datetime.datetime.utcnow()
    timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):

        
        receiver_channel = 825958388349272106
        current_time = datetime.datetime.utcnow()
        timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
        announce = self.client.get_channel(receiver_channel)
        if before.author.id == 664508672713424926:
            if (len(before.embeds) > 0):
                try:
                    _embed = after.embeds[0]
                except:
                    print("Message edited. No Embed")
                data = self.db.execute(f'SELECT * FROM Dex WHERE Img_url = "{_embed.image.url}"')
                data = data.fetchall()
                if before.reference:
                    ref_msg = await before.channel.fetch_message(before.reference.message_id)
                    sender = ref_msg.author.display_name
                elif before.interaction:
                    ref_msg = before.interaction.user
                    sender = ref_msg.display_name
                
                color = _embed.color
                ##### Rare Spawn #####
                Rare_Spawns = ["Event", "Legendary", "Shiny"]
                if _embed.description:
                    if "caught a" in _embed.description:
                        raremon = data[0][14]
                        if raremon in Rare_Spawns or _embed.color == 0xe9270b:
                            raremon = poke_rarity[(data[0][14])]
                            description_text = f"Original message: [Click here]({before.jump_url})\n"
                            embed = disnake.Embed(title=raremon+" **"+data[0][1]+"** \nDex: #"+str(data[0][0]), color=color,description=description_text)
                            embed.set_author(name=(sender+" just caught a:"), icon_url=_embed.author.icon_url)
                            embed.set_image(_embed.image.url)
                            embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                            await announce.send(embed=embed)
                    if "broke out" in _embed.description:
                        raremon = data[0][14]
                        if raremon in Rare_Spawns or _embed.color == 0xe9270b:
                            raremon = poke_rarity[(data[0][14])]
                            description_text = f"Original message: [Click here]({before.jump_url})\n"
                            embed = disnake.Embed(title=raremon+" **"+data[0][1]+"** \nDex: #"+str(data[0][0]), color=color,description=description_text)
                            embed.set_author(name=(sender+" almost caught a:"), icon_url=_embed.author.icon_url)
                            embed.set_image(_embed.image.url)
                            embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                            await announce.send(embed=embed)
                    




def setup(client):
    client.add_cog(On_Edit(client))