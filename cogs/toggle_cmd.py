from datetime import datetime
from sqlite3 import connect
import disnake

from cogs import commands

toggles = ["Grazz","Repel","Starter","Linked","Emotes","ToggleSpawn","ToggleFish","ToggleBattle","ToggleQuest","ToggleQuestTimer","ToggleOthers","Ping"]
functions = ["Grazz", "Repel","Starter","Linked","Emotes","Ping"]
reminders = ["ToggleSpawn","ToggleFish","ToggleBattle","ToggleQuest","ToggleQuestTimer","ToggleOthers"]
#Reminder Buttons
class Remd_Buttons(disnake.ui.Button):
    def __init__(self, user_id):
        super().__init__(label="Reminder", style=disnake.ButtonStyle.primary,custom_id=f"rmd_button_{user_id}")
        self.user_id = user_id
        self.db = connect("database.db")

    async def callback(self, interaction:disnake.MessageInteraction):
        if interaction.user.id != self.user_id:
            exit
        data = self.db.execute(f"SELECT ToggleSpawn,ToggleFish,ToggleBattle,ToggleQuest,ToggleQuestTimer,ToggleOthers FROM Toggle WHERE User_ID = {self.user_id}")
        data = data.fetchone()
        view = FunctionView(self.user_id)
        i = 0
        for item in view.children:
            if isinstance(item, disnake.ui.Button):
                if data[i] == 1:
                    item.style = disnake.ButtonStyle.green
                else:
                    item.style = disnake.ButtonStyle.red
                i+=1
        await interaction.response.edit_message(view=view)

#Function Buttons
class Fnct_Buttons(disnake.ui.Button):
    def __init__(self, user_id):
        super().__init__(label="Functions", style=disnake.ButtonStyle.primary,custom_id=f"fnc_button_{user_id}")
        self.user_id = user_id
        self.db = connect("database.db")

    async def callback(self, interaction: disnake.MessageInteraction):
        if interaction.user.id != self.user_id:
            exit
        data = self.db.execute(f"SELECT Grazz, Repel, Starter, Linked, Emotes, Ping FROM Toggle WHERE User_ID = {self.user_id}")
        data = data.fetchone()
        view = FunctionView(self.user_id)
        i = 0
        for item in view.children:
            if isinstance(item, disnake.ui.Button):
                if data[i] == 1:
                    item.style = disnake.ButtonStyle.green
                else:
                    item.style = disnake.ButtonStyle.red
                i+=1
        await interaction.response.edit_message(view=view)
            
class RazzButton(disnake.ui.Button):
    def __init__(self, user_id,entry):
        super().__init__(label="Home", style=disnake.ButtonStyle.primary,custom_id=f"toggle_button_{user_id}_{entry}")
        self.user_id = user_id
        self.entry = entry
        self.db = connect("database.db")

    async def callback(self, interaction: disnake.MessageInteraction):
        if interaction.user.id != self.user_id:
            exit
        
        if interaction.component.custom_id == self.custom_id:
            view = disnake.ui.View.from_message(interaction.message)
            for item in view.children:
                if isinstance(item, disnake.ui.Button):
                    if item.custom_id == self.custom_id:
                        if item.style == disnake.ButtonStyle.green:
                            item.style = disnake.ButtonStyle.red
                            self.db.execute(f"UPDATE Toggle SET {self.entry} == 0 WHERE User_ID = {self.user_id}")
                            if self.entry == "Linked":
                                msg = f"Deactivated linked slash commands in the notification."
                            elif self.entry == "Emotes":
                                msg = f"Deactivated emote-only notifications."
                            else:
                                msg = f"Deactivated that notification."
                        else:
                            item.style = disnake.ButtonStyle.green
                            self.db.execute(f"UPDATE Toggle SET {self.entry} == 1 WHERE User_ID = {self.user_id}")
                            if self.entry == "Linked":
                                msg = f"Activated linked slash commands in the notification."
                            elif self.entry == "Emotes":
                                msg = f"Activated emote-only notifications."
                            else:
                                msg = f"Activated that notification."
                        self.db.commit()
        await interaction.response.edit_message(msg,view=view)

class ReminderView(disnake.ui.View):
    def __init__(self, user_id):
        super().__init__()
        for entry in reminders:
            self.add_item(RazzButton(user_id,entry))

class FunctionView(disnake.ui.View):
    def __init__(self, user_id):
        super().__init__()
        for entry in functions:
            self.add_item(RazzButton(user_id,entry))

class ToggleView(disnake.ui.View):
    def __init__(self, user_id):
        super().__init__()
        self.add.item()
        self.add_item(Fnct_Buttons(user_id))

class Toggle_Cmd(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")

    current_time = datetime.datetime.now()
    timestamp = current_time.strftime('%Y-%m-%d %H:%M')

    @commands.command()
    async def toggle(self, ctx):
        user_id = ctx.author.id
        database = self.db.execute(f'SELECT * FROM Toggle WHERE User_ID = {user_id}')
        database = database.fetchone()
        author_url = "https://cdn.discordapp.com/emojis/1153729922620215349.webp?size=96&quality=lossless"
        author_name = ctx.author.display_name
        gengar_bot = self.client.get_user(1161011648585285652)
        footer_icon = gengar_bot.display_avatar.url
        footer_name = gengar_bot.display_name+" I "+self.timestamp
        emo_yes = ":white_check_mark:"
        emo_no = ":x:"
        emo_ping = ":bell:"
        emo_sile = ":no_bell:"
        color = 0x807ba6
        if database:
            if database[2] == 1:
                value_grazz = emo_yes
            else:
                value_grazz = emo_no
            if database[3] == 1:
                value_repel = emo_yes
            else:
                value_repel = emo_no
            if database[4] == 1:
                value_start = emo_yes
            else:
                value_start = emo_no
            if database[5] == 1:
                value_link = emo_yes
            else:
                value_link = emo_no
            if database[6] == 0:
                value_rem = "Text style"
            elif database[6] == 1:
                value_rem = "Emote Style"
            if database[10] == 1:
                value_spawn = emo_yes
            elif database[10] == 0:
                value_spawn = emo_no
            if database[0][11] == 1:
                value_fish = emo_yes
            elif database[11] == 0:
                value_fish = emo_no
            if database[12] == 1:
                value_battle = emo_yes
            elif database[12] == 0:
                value_battle = emo_no
            if database[13] == 1:
                value_quest = emo_yes
            elif database[13] == 0:
                value_quest = emo_no
            if database[14] == 1:
                value_questr = emo_yes + emo_sile
            elif database[14] == 0:
                value_questr = emo_no
            elif database[4] == 2:
                value_questr = emo_yes + emo_ping
            if database[15] == 1:
                value_other = emo_yes
            elif database[15] == 0:
                value_other = emo_no
            if database[16] == 0:
                value_ping = emo_ping
            else:
                value_ping = emo_sile
            embed = disnake.Embed(
                title="**Settings**", color=color, description="Here you can see your current toggle settings. \nChangeable via ``/toggle`` \n\nThe current settings are:"
            )
            embed.set_author(icon_url=author_url,name=author_name)
            embed.set_footer(icon_url=footer_icon,text=footer_name)
            embed.add_field(name="Golden Razz Berry/Honey: ",inline=True, value=value_grazz)
            embed.add_field(name="Repels: ",inline=True, value=value_repel)
            embed.add_field(name="Starter: ",inline=True, value=value_start)
            embed.add_field(name="Reminder Mode: ", inline=True, value=value_rem)
            embed.add_field(name="Pings: ", inline=True, value=value_ping)
            embed.add_field(name="",inline=True, value="")
            embed.add_field(name="Spawn: ", inline=True, value=value_spawn)
            embed.add_field(name="Fish: ", inline=True, value=value_fish)
            embed.add_field(name="Battle: ", inline=True, value=value_battle)
            embed.add_field(name="Quest Command: ", inline=True, value=value_quest)
            embed.add_field(name="Next Quest: ", inline=True, value=value_questr)
            embed.add_field(name="Other Commands: ", inline=True, value=value_other)
            embed.set_thumbnail(footer_icon)
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Toggle_Cmd(client))