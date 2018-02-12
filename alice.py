import random

import requests
from discord.ext import commands

bot = commands.Bot(command_prefix='a.')

token_file = open('token', 'r')
token = token_file.read()
token_file.close()


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def roll(stop=100):
    num = random.randrange(1, stop + 1)
    await bot.say(num)


@bot.command()
async def btc(arg=1.0, usd=''):
    btc = requests.get(
        'https://api.coinmarketcap.com/v1/ticker/bitcoin/').json()

    btc_price = round(float(btc[0]['price_usd']) * arg, 2)
    btc_price = f'{btc_price:.2f}'

    if usd == 'usd':
        print(arg, btc_price)
        usd_price = arg / round(float(btc[0]['price_usd']))
        usd_price = f'{usd_price:.4f}'
        arg = f'{arg:.2f}'
        await bot.say(str(arg) + ' USD = ' + str(usd_price) + ' BTC')
    else:
        await bot.say(str(arg) + ' BTC = $' + str(btc_price) + ' USD')


bot.run(token)
