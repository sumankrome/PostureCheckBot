def start_timer(bot):
    print("Started Timer")
    bot.isStarted = True

def stop_timer(bot):
    print("Stopped Timer")
    bot.isStarted = False

def set_timer(bot, time):
    print(f"Set timer to {time} minutes")
    bot.timer = time