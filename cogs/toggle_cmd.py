import datetime
from sqlite3 import connect
import disnake

from disnake.ext import commands

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
        try:
            await interaction.response.defer()
            if interaction.user.id != self.user_id:
                exit
            data = self.db.execute(f"SELECT ToggleSpawn,ToggleFish,ToggleBattle,ToggleQuest,ToggleQuestTimer,ToggleOthers FROM Toggle WHERE User_ID = {self.user_id}")
            data = data.fetchone()
            view = ReminderView(self.user_id)
            i = 0
            for item in view.children:
                if isinstance(item, disnake.ui.Button):
                    if item.label in reminders:
                        if data[i] == 1:
                            item.style = disnake.ButtonStyle.green
                        else:
                            item.style = disnake.ButtonStyle.red
                        i+=1
            await interaction.edit_original_response(view=view)
        except Exception as e:
            print(e)

class RemButton(disnake.ui.Button):
    def __init__(self, user_id,entry):
        super().__init__(label=f"{entry}", style=disnake.ButtonStyle.primary,custom_id=f"toggle_button_{user_id}_{entry}")
        self.user_id = user_id
        self.entry = entry
        self.db = connect("database.db")

    async def callback(self, interaction: disnake.MessageInteraction):
        try:
            await interaction.response.defer()
            if interaction.user.id != self.user_id:
                exit
            data = self.db.execute(f"SELECT ToggleSpawn,ToggleFish,ToggleBattle,ToggleQuest,ToggleQuestTimer,ToggleOthers FROM Toggle WHERE User_ID = {self.user_id}")
            data = data.fetchone()
            i=0
            if interaction.component.custom_id == self.custom_id:
                view = ReminderView(self.user_id)
                for item in view.children:
                    if isinstance(item, disnake.ui.Button):
                        if item.label in reminders:
                            if data[i] == 1:
                                item.style = disnake.ButtonStyle.green
                            else:
                                item.style = disnake.ButtonStyle.red
                            i+=1
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
            await interaction.edit_original_response(msg,view=view)
        except Exception as e:
            print(e)

#Function Buttons
class Fnct_Buttons(disnake.ui.Button):
    def __init__(self, user_id):
        super().__init__(label="Functions", style=disnake.ButtonStyle.primary,custom_id=f"fnc_button_{user_id}")
        self.user_id = user_id
        self.db = connect("database.db")

    async def callback(self, interaction: disnake.MessageInteraction):
        try:
            await interaction.response.defer()
            if interaction.user.id != self.user_id:
                exit
            data = self.db.execute(f"SELECT Grazz, Repel, Starter, Linked, Emotes, Ping FROM Toggle WHERE User_ID = {self.user_id}")
            data = data.fetchone()
            view = FunctionView(self.user_id)
            i = 0
            for item in view.children:
                if isinstance(item, disnake.ui.Button):
                    if item.label in functions:
                        if data[i] == 1:
                            item.style = disnake.ButtonStyle.green
                        else:
                            item.style = disnake.ButtonStyle.red
                        i+=1
            await interaction.edit_original_response(view=view)
        except Exception as e:
            print(e)
            
class FuncButton(disnake.ui.Button):
    def __init__(self, user_id,entry):
        super().__init__(label=f"{entry}", style=disnake.ButtonStyle.primary,custom_id=f"toggle_button_{user_id}_{entry}")
        self.user_id = user_id
        self.entry = entry
        self.db = connect("database.db")

    async def callback(self, interaction: disnake.MessageInteraction):
        try:
            await interaction.response.defer()
            if interaction.user.id != self.user_id:
                exit
            data = self.db.execute(f"SELECT Grazz, Repel, Starter, Linked, Emotes, Ping FROM Toggle WHERE User_ID = {self.user_id}")
            data = data.fetchone()
            i=0
            if interaction.component.custom_id == self.custom_id:
                view = FunctionView(self.user_id)
                for item in view.children:
                    if isinstance(item, disnake.ui.Button):
                        if item.label in functions:
                            if data[i] == 1:
                                item.style = disnake.ButtonStyle.green
                            else:
                                item.style = disnake.ButtonStyle.red
                            i+=1
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
            await interaction.edit_original_response(msg,view=view)
        except Exception as e:
            print(e)

class BackButton(disnake.ui.Button):
    def __init__(self,user_id):
        super().__init__(label="Back", style=disnake.ButtonStyle.primary,custom_id=f"back_button_{user_id}")
        self.user_id = user_id

    async def callback(self, interaction: disnake.MessageInteraction):
        await interaction.response.defer()
        if interaction.user.id != self.user_id:
            exit
        try:
            view = ToggleView(self.user_id)
            await interaction.edit_original_response(view=view)
        except Exception as e:
            print(e)

class ReminderView(disnake.ui.View):
    def __init__(self, user_id):
        super().__init__()
        self.add_item(BackButton(user_id))
        for entry in reminders:
            self.add_item(RemButton(user_id,entry))

class FunctionView(disnake.ui.View):
    def __init__(self, user_id):
        super().__init__()
        self.add_item(BackButton(user_id))
        for entry in functions:
            self.add_item(FuncButton(user_id,entry))

class ToggleView(disnake.ui.View):
    def __init__(self, user_id):
        super().__init__()
        self.add_item(Remd_Buttons(user_id))
        self.add_item(Fnct_Buttons(user_id))

class Toggle_Cmd(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db = connect("database.db")

    current_time = datetime.datetime.now()
    timestamp = current_time.strftime('%Y-%m-%d %H:%M')

    @commands.command()
    async def toggle(self, ctx):
        try:
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
                
                embed = disnake.Embed(
                    title="**Settings**", color=color, description="Here you can see your current toggle settings. \nChangeable via ``/toggle`` \n\nThe current settings are:"
                )
                embed.set_author(icon_url=author_url,name=author_name)
                embed.set_footer(icon_url=footer_icon,text=footer_name)
                
                embed.set_thumbnail(footer_icon)
                await ctx.send(embed=embed,view=ToggleView(user_id=ctx.author.id))
        except Exception as e:
            print(f"{e}")

def setup(client):
    client.add_cog(Toggle_Cmd(client))