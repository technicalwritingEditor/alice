import random
import csv
import discord
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
async def rs(username='Kevintf'):
    csv_f = requests.get('http://services.runescape.com/m=hiscore_oldschool/index_lite.ws?player=' + username).text

    reader = csv.reader(csv_f.splitlines(), delimiter=',')

    rs = [
        'Overall',
        'Attack',
        'Defense',
        'Strength',
        'Hitpoints',
        'Ranged',
        'Prayer',
        'Magic',
        'Cooking',
        'Woodcutting',
        'Fletching',
        'Fishing',
        'Firemaking',
        'Crafting',
        'Smithing',
        'Mining',
        'Herblore',
        'Agility',
        'Thieving',
        'Slayer',
        'Farming',
        'Runecraft',
        'Hunter',
        'Construction',
        'Clue Scrolls (easy)',
        'Clue Scrolls (medium)',
        'Clue Scrolls (all)',
        None,
        None,
        'Clue Scrolls (hard)',
        None,
        None,
        None
    ]

    count = 0
    data = []

    for row in reader:
        row.append(rs[count])
        count += 1
        data.append(row)

    o_data = ''

    for rank, level, xp, skill in data:
        o_data += skill + ' ' + rank + ' ' + level + ' ' + xp + '\n'
        if 'Construction' in skill:
            break

    await bot.say('```css\n' + username + '\n\nSkill  | Rank | Level |  XP\n' + o_data + '```')


@bot.command()
async def coin(*args):
    cmc = requests.get(
        'https://api.coinmarketcap.com/v1/ticker/').json()

    symb = 'btc'
    num = 1
    called_help = False

    for arg in args:
        if any(char.isdigit() for char in arg):
            num = float(arg)
        elif arg == '--help' or arg == '-h':
            embed = discord.Embed(title='coin -h, --help ', color=discord.Color(0x6d689b))
            embed.add_field(name='__a.coin__', value='default values are 1 btc\n-> `a.coin`\n----> 1 BTC = $8805.74 USD', inline=False)
            embed.add_field(name='__a.coin num__', value='default symbol is btc\n-> `a.coin .4`\n----> 0.4 BTC = $3515.60 USD', inline=False)
            embed.add_field(name='__a.coin symb__', value='symb can be any of the ticker symbols from the top 100 on [coinmarketcap](http://coinmarketcap.com).\n`-> a.coin ETH`\n----> 1 ETH = $868.05 USD', inline=False)
            embed.add_field(name='__a.coin num symb__', value='-> `a.coin 2.45 xmr`\n----> 2.45 XMR = $607.84 USD', inline=False)
            await bot.say(embed=embed)
            called_help = True
        else:
            symb = arg

    for coin in cmc:
        if str(coin['symbol']).lower() == symb.lower():
            symb_price = round(float(coin['price_usd']) * num, 2)
            symb_price = f'{symb_price:.2f}'

    '''if usd == 'usd':
        print(arg, btc_price)
        usd_price = arg / round(float(btc[0]['price_usd']))
        usd_price = f'{usd_price:.4f}'
        arg = f'{arg:.2f}'
        await bot.say(str(arg) + ' USD = ' + str(usd_price) + ' BTC')
    else:'''

    if not called_help:
        await bot.say(
            str(num) + ' ' + symb.upper() + ' = $' + str(symb_price) + ' USD')


bot.run(token)
