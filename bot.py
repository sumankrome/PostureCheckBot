import discord
from discord.ext import commands, tasks
from discord import app_commands
import response
import images

class BotClient(discord.Client):
    def __init__(self, intents: discord.Intents, timer):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

        self.timer = timer
        self.isStarted = False
        self.atUsers = []

def run_discord_bot():
    TOKEN = "MTE2OTAxNzA3MTM3NjU0MzgwNQ.GghfTB.7AImnySydeajBCeFrc0kYC4XuTwk-bMGBtIXxg"
    
    bot = BotClient(intents=discord.Intents.all(), timer = 5)

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user} (ID: {bot.user.id})')
        print('------')
        await bot.tree.sync()

    @bot.tree.command(name="set_timer", description="Give time to the timer in minutes")
    @app_commands.describe(timer = "Give time to the timer in minutes: ")
    async def set_timer(interaction: discord.Integration, timer: str):
        try:
            timer = float(timer)
            await interaction.response.send_message(f"{interaction.user.name} has set the timer to {timer} minutes")
            response.set_timer(bot, timer)
            task_loop.change_interval(seconds=float(bot.timer))
        except ValueError:
            await interaction.response.send_message(f"Please input a number.")

    @bot.tree.command(name="start_posture", description="Starts the timer")
    async def start_timer(interaction: discord.integrations):
        if(bot.isStarted == False):
            await interaction.response.send_message(f"{interaction.user.name} has started the Posture Reminder")
            response.start_timer(bot)
            await task_loop.start(interaction.channel)
            bot.atUsers = []
        else:
            await interaction.response.send_message(f"Posture Reminder has already been started")

    @bot.tree.command(name="stop_posture", description="Stop the timer")
    async def stop_timer(interaction: discord.integrations):
        if(bot.isStarted == True):
            await interaction.response.send_message(f"{interaction.user.name} has stopped the Posture Reminder")
            response.stop_timer(bot)
            task_loop.stop()
        else:
            await interaction.response.send_message(f"Posture Reminder has not been started")
            
    @bot.tree.command(name="mention", description="Mention me with the Posture Reminder")
    async def mention(interaction: discord.integrations):
        inList = False
        for i in bot.atUsers:
            if (i == interaction.user.mention):
                inList = True
                bot.atUsers.remove(i)
            
        if(inList):
            await interaction.response.send_message(f"{interaction.user.name} will no longer be @'d", ephemeral=True)
        else:
            await interaction.response.send_message(f"{interaction.user.name} will now be @'d", ephemeral=True)
            bot.atUsers.append(interaction.user.mention)

    @tasks.loop(seconds=bot.timer)
    async def task_loop(channel):
        print("CHECKING")
        print(f"Timer is at {bot.timer}")
        usersToAt = ""
        for i in bot.atUsers:
            usersToAt = usersToAt + f" {i}"
        await channel.send("CHECK YOUR F-ING POSTURE" + usersToAt)
        await channel.send(images.choose_random_image())

    bot.run(TOKEN)