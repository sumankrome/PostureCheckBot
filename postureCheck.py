async def start_timer(bot, interaction):
    print("Started Timer")
    if interaction.user not in bot.atUsers:
        bot.atUsers.append(interaction.user)
    await interaction.response.send_message(f"{interaction.user.name} has started the Posture Reminder")
    bot.isStarted = True
    bot.count = 0

async def stop_timer(bot, interaction):
    print("Stopped Timer")
    await interaction.response.send_message(f"{interaction.user.name} has stopped the Posture Reminder")
    bot.isStarted = False
    bot.task_loop.stop()

async def set_timer(bot, interaction, time):
    await interaction.response.send_message(f"{interaction.user.name} has set the timer to {time} minutes")
    print(f"Set timer to {time} minutes")
    bot.timer = time

postureCheckHelp = """• To use this bot, you will need to be in a voice call. Join VC and start this bot with /start_posture.
• You can add more people to the mention list by using /posture_mention.
• You can change the frequency in which you get the Posture Check by using /set_timer.
• You can stop the posture check with /stop_posture.
• The Posture Check will stop either when the mention list is empty or everyone in the mention list leave the voice chat."""