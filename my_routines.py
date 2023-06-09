from twitchio.ext import routines
from game import mini_game
import my_bot
import random

random_timer = random.randint(5, 45)

# Timers can be changed.
@routines.routine(wait_first=True, minutes=45)
async def follow_reminder():
    """Reminds the audience to follow the stream"""
    await my_bot.bot.connected_channels[0].send("Enjoying the stream? "
                                                "Make sure to drop a follow!")

@routines.routine(wait_first=True, minutes=30)
async def hydration_reminder():
    """Reminder to drink water"""
    random_response = ["When did you drink water last? Don't forget to hydrate.",
                       "Stop whatever you are doing and drink some water",
                       "Hey you! Go drink water :)",
    ]
    await my_bot.bot.connected_channels[0].send(random.choice(random_response))

@routines.routine(wait_first=True, minutes=25)
async def builds_reminder():
    """Reminder about build commands"""
    reminder = "Type #builds in chat to get my builds."
    await my_bot.bot.connected_channels[0].send(random.choice(reminder))


@routines.routine(wait_first=True, minutes=random_timer)
async def mini_typing_game():
    """A small game to get user input from the chat that repeats what the bot says
    the winner can be any of the first 3 people to type. it is completely random whether
    the first, second, or the third person is going to be the winner"""
    if not my_bot.bot.game_active:
        await my_bot.bot.connected_channels[0].send(my_bot.bot.game_word)
        my_bot.bot.game_active = True
        await mini_game.check_game_status()



