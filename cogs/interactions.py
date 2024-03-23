import disnake
from disnake.ext import commands

class Interactions(commands.Cog):

    @commands.Cog.listener()
    async def on_interaction(interaction: disnake.Interaction):
        if isinstance(interaction, disnake.MessageInteraction):
            print(interaction.data.content)
    
def setup(client):
    client.add_cog(Interactions(client))