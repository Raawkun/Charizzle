import datetime
import disnake
from disnake.ext import commands
import sqlite3
from sqlite3 import connect

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
                _embed = after.embeds[0]
                data = self.db.execute(f'SELECT * FROM Dex WHERE Img_url = "{_embed.image.url}"')
                data = data.fetchall()
                try: 
                    ref_msg = await before.channel.fetch_message(before.reference.message_id)
                except:
                    ref_msg = await before.channel.fetch_message(before.interaction.id)
                sender = ref_msg.author.display_name
                color = _embed.color
                if "caught" in _embed.description:
                    print("Caughted")
                    raremon = data[0][14]
                    print(raremon)
                    print(data[0][1])
                    Rare_Spawns = ["Event", "Legendary", "Shiny"]
                    if raremon in Rare_Spawns or _embed.color == 0xe9270b:
                        description_text = f"Original message: [Click here]({ref_msg.jump_url})\n"
                        embed = disnake.Embed(title=raremon+" **"+data[0][1]+"** \nDex: #"+str(data[0][0]), color=color,description=description_text)
                        embed.set_author(name=(sender+" just spawned a:"), icon_url=_embed.author.icon_url)
                        embed.set_image(_embed.image.url)
                        embed.set_footer(text=(f'{self.client.user.display_name}'+" | at UTC "f'{timestamp}'), icon_url=f'{self.client.user.avatar}')
                        await announce.send(embed=embed)




def setup(client):
    client.add_cog(On_Edit(client))