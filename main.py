# bot.py
# following https://realpython.com/how-to-make-a-discord-bot-python/
import os
import re

import discord
from dotenv import load_dotenv
from numpy import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            print("TO NA GUILDA DA SEMATRON, CAMBADA! UHUL!11!")

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Eae {member.name}! Bora regaçar o rolê!'
    )

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

    calc_re = re.compile(r'[\+\-]?\d+(\.\d+)?[\+\-\*\/][\+\-]?\d+(\.\d+)?')

    if message.content == '99!':
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)
    elif calc_re.fullmatch(message.content):
        response = eval(message.content)
        await message.channel.send(response)
    elif message.content[0:6] == "!expr ":
        try:
            response = eval(message.content[6:])
        except Exception as e:
            response = repr(e)
        await message.channel.send(response)



client.run(TOKEN)