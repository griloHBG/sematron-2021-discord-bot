# bot.py
# following https://realpython.com/how-to-make-a-discord-bot-python/
import os

from discord.ext.commands.bot import Bot
from dotenv import load_dotenv
from numpy import random

import discord
intents = discord.Intents.default()
intents.members = True

import requests
import json
import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            print("TO NA GUILDA DA SEMATRON, CAMBADA! UHUL!11!")

            print(
                f'{bot.user} is connected to the following guild:\n'
                f'{guild.name}(id: {guild.id})'
            )

            members = '\n - '.join([member.name for member in guild.members])
            print(f'Guild Members:\n - {members}')
            print(guild.members)


@bot.command(name='99', help='Frases aleatórias advindas do seriado Brooklin 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

timeapi_url = lambda spec_list : f"http://worldtimeapi.org/api/timezone/{'/'.join(spec_list)}"
timeapihelp_url = "http://worldtimeapi.org/timezones"

@bot.command(name="hora", help=f'Passe como argumento regiões e subregiões para ficar sabendo o horário atual de lá!\nLista de lugares:\n{timeapihelp_url}\nExemplo:\n!hora Brazil Sao_Paulo', brief='Retorna o horário atual de alguma parte do mundo usando a API do WorldTime')
async def get_current_datetime(ctx, *region):
    if len(region) > 3:
        await ctx.send(f"Né por nada não... mas vc tá passando `{len(region)}` especificações de região...\n"
                       f"O máximo é 3.\n"
                       f"Dá uma olhada aqui nas regiões disponíveis:"
                       f"_{timeapihelp_url}_")
        return
    elif len(region) < 1:
        await ctx.send(f"Né por nada não... mas vc tá passando `{len(region)}` especificações de região...\n"
                       f"Tem que ter pelo menos 1.\n"
                       f"Dá uma olhada aqui nas regiões disponíveis:"
                       f"_{timeapihelp_url}_")
        return
    if isinstance(region, str):
        region = region.split('/')

    current_url = timeapi_url(region)
    await ctx.send(f"Buscando datetime com essa url:\n**{current_url}**")

    response = requests.request("GET", url=current_url)

    if response.status_code == 200:
        data = json.loads(response.text)
        current_datetime = datetime.datetime.fromisoformat(data['datetime'])
        await ctx.send(f"{', '.join(region)}: {current_datetime}")
    elif response.status_code == 404:
        await ctx.send(f"Não deu bom procurar por {', '.join(region)} não..."
                       f"Dá uma olhada aqui nas regiões disponíveis:"
                       f"_{timeapihelp_url}_")


bot.run(TOKEN)