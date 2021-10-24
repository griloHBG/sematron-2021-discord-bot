# bot.py
# following https://realpython.com/how-to-make-a-discord-bot-python/
import os

import numpy as np
from discord.ext.commands import Context
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

class jokenpo_helper:
    choices = [ 'pedra', 'papel', 'tesoura']
    choices_parser = { "pedra":"pedra",
                "\U0001faa8":"pedra",
                "papel": "papel",
                "📰": "papel",
                "🗞️": "papel",
                "🧻": "papel",
                "tesoura": "tesoura",
                "✂️": "tesoura", # o caracter depois da ✂ NÃO é um espaço!!
                }
    result = {'pedra':{'pedra':'empate',
                       'papel':'perdeu',
                       'tesoura':'venceu',
                       },
              'papel':{'pedra':'venceu',
                       'papel':'empate',
                       'tesoura':'perdeu',
                       },
              'tesoura':{'pedra':'perdeu',
                       'papel':'venceu',
                       'tesoura':'empate',
                       },
              }
    '''
    user point of view!
                        user
                pedra   papel   tesou
        pedra   emp     venceu  perdeu
    bot papel   perdeu  emp     venceu
        tesou   venceu  perdeu  emp
    '''
    emoji = {'pedra':':rock:',
             'papel':':roll_of_paper:',
             'tesoura':':scissors:',
             }
    draw_emojis = [':wink:', ':slight_smile:', ':stuck_out_tongue_closed_eyes:', ':smirk_cat:', ':cowboy:', ]

    help_string_with_formatting =   f"Ok. Vou te ensinar como jogar Jokenpo (https://pt.wikipedia.org/wiki/Pedra,_papel_e_tesoura)\n" \
                    f"Você precisa escolher entre **pedra** (ou :rock:), **papel** (ou :newspaper: ou :newspaper2: ou :roll_of_paper:), ou **tesoura** (ou :scissors:)\n" \
                    f"Aí, depois que você me mandar sua escolha, vou fazer a minha escolha (eu juro que eu não vou roubar :p )\n" \
                    f"E então vou declarar o resultado\n" \
                    f"A regra de quem venceu é assim:\n" \
                    f"**Pedra** :rock: vence de :scissors: **Tesoura**\n" \
                    f"**Tesoura** :scissors: vence de :newspaper: **Papel**\n" \
                    f"**Papel** :newspaper: vence de :rock: **Pedra**\n" \
                    f"\n" \
                    f"Se escolhermos a mesma opção, teremos um empate!\n"

    help_string_without_formatting =   f"Ok. Vou te ensinar como jogar Jokenpo (https://pt.wikipedia.org/wiki/Pedra,_papel_e_tesoura)\n" \
                               f"Você precisa escolher entre pedra (ou :rock:), papel (ou :newspaper: ou :newspaper2: ou :roll_of_paper:), ou tesoura (ou :scissors:)\n" \
                               f"Aí, depois que você me mandar sua escolha, vou fazer a minha escolha (eu juro que eu não vou roubar :p )\n" \
                               f"E então vou declarar o resultado\n" \
                               f"A regra de quem venceu é assim:\n" \
                               f"Pedra vence de Tesoura\n" \
                               f"Tesoura vence de Papel\n" \
                               f"Papel vence de Pedra\n" \
                               f"\n" \
                               f"Se escolhermos a mesma opção, teremos um empate!\n"

    brief = "Escolha pedra, papel ou tesoura e vamos jogar jokenpo!"

    ranking_board={"player_id":{"player":0,"bot":0}}

    @classmethod
    def player_won(cls, player_name_id:str): #exemplo de player_name_id: Grilo#1234
        if player_name_id in cls.ranking_board.keys():
            cls.ranking_board[player_name_id]["player"] += 1
        else:
            cls.ranking_board[player_name_id] = {"player":0,"bot":0}
            cls.ranking_board[player_name_id]["player"] = 1
            cls.ranking_board[player_name_id]["bot"] = 0

    @classmethod
    def draw(cls, player_name_id:str): #exemplo de player_name_id: Grilo#1234
        if not player_name_id in cls.ranking_board.keys():
            cls.ranking_board[player_name_id] = {"player":0,"bot":0}

    @classmethod
    def player_lost(cls, player_name_id:str): #exemplo de player_name_id: Grilo#1234
        if player_name_id in cls.ranking_board.keys():
            cls.ranking_board[player_name_id]["bot"] += 1
        else:
            cls.ranking_board[player_name_id] = {"player":0,"bot":0}
            cls.ranking_board[player_name_id]["player"] = 0
            cls.ranking_board[player_name_id]["bot"] = 1

@bot.command(name="jokenpo", help=jokenpo_helper.help_string_without_formatting, brief=jokenpo_helper.brief)
async def jokenpo(ctx:Context, user_choice:str):
    if not user_choice:
        await ctx.send(jokenpo_helper.help_string_with_formatting)
        return

    user_choice = user_choice.strip()

    if not user_choice in jokenpo_helper.choices_parser.keys():
        await ctx.send(jokenpo_helper.help_string_with_formatting)
        return

    player_name_id = str(ctx.author)

    user_choice = jokenpo_helper.choices_parser[user_choice]

    bot_choice = np.random.choice(jokenpo_helper.choices)

    result = jokenpo_helper.result[user_choice][bot_choice]

    if result == "venceu":
        jokenpo_helper.player_won(player_name_id)
        await ctx.send(f"Mas não é que você **venceu**?! :dizzy_face:\n"
                       f"Você escolheu {user_choice} {jokenpo_helper.emoji[user_choice]}, que vence de {bot_choice} {jokenpo_helper.emoji[bot_choice]}, que foi a minha esolha!\n"
                       f"Impressionante!\n"
                       f"Se você quiser um repeteco, bora lá! :smiley:\n")
    elif result == "empate":
        jokenpo_helper.draw(player_name_id)
        await ctx.send(f"Pensamos igual! hahaha\n"
                       f"Você e eu escolhemos {user_choice} {jokenpo_helper.emoji[user_choice]}, então deu **empate**!\n"
                       f"Não pode ficar empatado não!\n"
                       f"Tá a fim de outra?! {np.random.choice(jokenpo_helper.draw_emojis)}\n")
    elif result == "perdeu":
        jokenpo_helper.player_lost(player_name_id)
        await ctx.send(f"Eita! Ganhei! Você **perdeu**! HÁ! :partying_face:\n"
                       f"Você escolheu {user_choice} {jokenpo_helper.emoji[user_choice]}, que perde de {bot_choice} {jokenpo_helper.emoji[bot_choice]}, que foi a minha esolha!\n"
                       f"EH NÓÓÓIS!! HAHAHAH\n"
                       f"Nem sei se quero jogar outra vez. Gosto de sair ganhando!\n"
                       f":rofl:")
    else:
        await ctx.send(f"ERRO! QQ ACONTECEU?!\nresultado foi **{result}**")

    player_score = jokenpo_helper.ranking_board[player_name_id]['player']
    bot_score = jokenpo_helper.ranking_board[player_name_id]['bot']

    player_length = np.max([3, len(player_name_id)])
    score_length = np.max([len(str(player_score)), len(str(bot_score))])

    await ctx.send(f"Olha o nosso placar, {player_name_id}:\n"
                   f"```"
                   f"{player_name_id:{player_length}}: {player_score:{score_length}} ponto{'' if player_score == 1 else 's'}\n"
                   f"{'Bot':{player_length}}: {bot_score:{score_length}} ponto{'' if bot_score == 1 else 's'}\n"
                   f"```")

    if bot_score > player_score:
        await ctx.send(f"Ah... vc sabe né. Eu manjo demais! :rofl::rofl:")
    elif bot_score < player_score:
        await ctx.send(f"Bora jogar mais umas que vc vai ver se eu não mudo esse placar, hein?!")
    else:
        await ctx.send(f"Vc é pário duro hein! Mas acho que consigo! :stuck_out_tongue_closed_eyes:")



bot.run(TOKEN)