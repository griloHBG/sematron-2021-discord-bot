# bot.py
import os

import discord
from dotenv import load_dotenv

import numpy as np

import re

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    msg = message.content

    two_digits_regex = re.compile(r'\d\d[!?]$')

    if two_digits_regex.match(msg):
        response = np.random.choice(brooklyn_99_quotes)
        await message.channel.send(response)

    # print(msg, "fora")
    #
    # num_list = [chr(n+ord('0')) for n in range(10)]
    #
    # if len(msg) == 3:
    #     #if msg[-1] == "!" or msg[-1] == "?":
    #     if msg[-1] in ["!", "?"]:
    #         if msg[0] in num_list and msg[1] in num_list:
    #             response = np.random.choice(brooklyn_99_quotes)
    #             print(msg, "dentro")
    #             await message.channel.send(response)



client.run(TOKEN)