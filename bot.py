import discord
from discord.ext import tasks
from discord import app_commands
import postureCheck
import horoscope
import images
import os
from dotenv import load_dotenv

class BotClient(discord.Client):
    def __init__(self, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

        self.timer = 5
        self.isStarted = False
        self.atUsers = []
        self.count = 0

def run_discord_bot():
    load_dotenv()
    bot = BotClient(intents=discord.Intents.all())
    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user} (ID: {bot.user.id})')
        print('------')

    @bot.tree.command(name='sync', description='Owner only')
    async def sync(interaction: discord.integrations):
        if interaction.user.id == os.getenv('USERID'):
            await bot.tree.sync()
            print('Command tree synced.')
            await interaction.response.send_message('Bot has been synced', ephemeral=True)
        else:
            await interaction.response.send_message('You must be the owner to use this command!')

    ######################################       POSTURE BOT SECTION
    @bot.tree.command(name="set_timer", description="Give time to the timer in minutes") #Set Timer code
    @app_commands.describe(timer = "Give time to the timer in minutes: ")
    async def set_timer(interaction: discord.integrations, timer: str):
        try:
            timer = float(timer)
            await postureCheck.set_timer(bot, interaction, timer)
            task_loop.change_interval(seconds=float(bot.timer))
        except ValueError:
            await interaction.response.send_message(f"Please input a number.")

    @bot.tree.command(name="start_posture", description="Starts the timer") #Start Posture code
    async def start_timer(interaction: discord.integrations):
        if(bot.isStarted == False):
            await postureCheck.start_timer(bot, interaction)
            task_loop.start(interaction.channel)
        else:
            await interaction.response.send_message(f"Posture Reminder has already been started")

    @bot.tree.command(name="stop_posture", description="Stop the timer") #Stop Posture code
    async def stop_timer(interaction: discord.integrations):
        if(bot.isStarted == True):
            await postureCheck.stop_timer(bot, interaction)
            task_loop.stop()
        else:
            await interaction.response.send_message(f"Posture Reminder has not been started")

    @bot.tree.command(name="posture_mention", description="Mention me with the Posture Reminder") #Mention code
    @app_commands.describe(member='The member to remind')
    async def postureMention(interaction: discord.integrations, member: discord.Member):
        inList = False
        for i in bot.atUsers:
            if (i == member):
                inList = True
                bot.atUsers.remove(i)
            
        if(inList):
            await interaction.response.send_message(f"{member} will no longer be @'d")
        else:
            await interaction.response.send_message(f"{member} will now be @'d")
            bot.atUsers.append(member)

    @bot.tree.command(name="posture_help", description="Get help for how to use posture check") #Posture Help
    async def postureHelp(interaction: discord.integrations):
        await interaction.response.send_message(postureCheck.postureCheckHelp, ephemeral = True)

    @tasks.loop(seconds=bot.timer) #Loop code
    async def task_loop(channel):
        usersToAt = ""
        for i in bot.atUsers:
            if i.voice == None:
                bot.atUsers.remove(i)
            else:
                usersToAt = usersToAt + f" {i.mention}"

        if bot.atUsers == []:
            await channel.send("Since no one is mentioned AND/OR everyone that was mentioned is not in VC, posture check has been stopped.")
            bot.isStarted = False
            task_loop.stop()

        if bot.isStarted:
            print(f"Timer is at {bot.timer}")

            await channel.send("CHECK YOUR F-ING POSTURE" + usersToAt)
            await channel.send(images.choose_random_image())

            bot.count += 1
            print("This has run " + str(bot.count) + " times")

    ######################################       HOROSCOPE SECTION
    @bot.tree.command(name="horoscope", description="Get your daily Horoscope!")
    @app_commands.describe(sign="Sign to choose from")
    @app_commands.choices(sign=[
        app_commands.Choice(name='Aries', value="aries"),
        app_commands.Choice(name='Taurus', value="taurus"),
        app_commands.Choice(name='Gemini', value="gemini"),
        app_commands.Choice(name='Cancer', value="cancer"),
        app_commands.Choice(name='Leo', value="leo"),
        app_commands.Choice(name='Virgo', value="virgo"),
        app_commands.Choice(name='Libra', value="libra"),
        app_commands.Choice(name='Scorpio', value="scorpio"),
        app_commands.Choice(name='Sagittarius', value="sagittarius"),
        app_commands.Choice(name='Capricorn', value="capricorn"),
        app_commands.Choice(name='Aquarius', value="aquarius"),
        app_commands.Choice(name='Pisces', value="pisces"),
        app_commands.Choice(name='Info', value="info")
    ])
    async def gethoroscope(interaction: discord.integrations, sign: app_commands.Choice[str]):
        message = horoscope.get_horoscope(sign.value)
        await interaction.response.send_message(message)

    bot.run(os.getenv('DISCORD_TOKEN'))