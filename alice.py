import csv
import random
import urllib
import logging

import discord
import requests
from discord.ext import commands

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix=('a.', 'A.'))

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
async def roll(*args):
    stop = 100
    help_menu = False
    for arg in args:
        if arg == '-h' or arg == '--help':
            help_menu = True
        elif arg:
            stop = int(arg)

    if not help_menu:
        num = random.randrange(1, stop + 1)
        await bot.say(num)
    else:
        embed = discord.Embed(title='roll -h, --help ', color=discord.Color(0x6d689b))
        embed.add_field(name='__a.roll__', value='roll a random number between 1 and 100. place a number in front of a.roll to roll between 1 and x.\nex. `a.roll 10` to roll between 1 and 10', inline=False)
        await bot.say(embed=embed)


@bot.command()
async def rs(*args):
    print(args)
    long = False
    three = False
    username = []
    for arg in args:
        if arg == '--long' or arg == '-l':
            long = True
            three = False
        elif arg == '-3':
            three = True
            long = False
        else:
            username.append(arg)

    if username:
        username = ' '.join(username)
    else:
        username = 'Kevintf'
    csv_f = requests.get(
        'http://services.runescape.com'
        '/m=hiscore_oldschool/index_lite.ws?player=' + username).text

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

    # username = '[' + username + '](http://services.runescape.com/m=hiscore_oldschool/hiscorepersonal.ws?user1=' + username + ')'

    # if 'kevintf' in username.lower():
    #     username = ':heart: ' + username + ' :heart:'
    # else:
    #     username = ':small_blue_diamond: ' + username + ' :small_blue_diamond:'

    embed = discord.Embed(color=discord.Color(0x6d689b))

    username_parse = urllib.parse.quote_plus(username)

    embed.set_author(name=username, url='http://services.runescape.com/m=hiscore_oldschool/hiscorepersonal.ws?user1=' + username_parse, icon_url='https://raw.githubusercontent.com/cheazy/alice/master/img/runescape.png')

    ordered_rs = [
        'Attack',
        'Hitpoints',
        'Mining',
        'Strength',
        'Agility',
        'Smithing',
        'Defense',
        'Herblore',
        'Fishing',
        'Ranged',
        'Thieving',
        'Cooking',
        'Prayer',
        'Crafting',
        'Firemaking',
        'Magic',
        'Fletching',
        'Woodcutting',
        'Runecraft',
        'Slayer',
        'Farming',
        'Construction',
        'Hunter',
        'Overall'
    ]

    del data[-9:]
    text_data = ''
    count = 1
    space_gap = 0

    for rank, level, xp, skill in data:
        # o_data += skill + ' ' + rank + ' ' + level + ' ' + xp + '\n'
        if not ordered_rs:
            break

        for rank, level, xp, skill in data:
            if skill == ordered_rs[0] and ordered_rs:
                if skill == 'Attack':
                    # skill = ':crossed_swords:'
                    skill_icon = '<:attack:412729368536940544>'
                elif skill == 'Defense':
                    # skill = ':shield:'
                    skill_icon = '<:defense:412729368574427136>'
                elif skill == 'Strength':
                    # skill = ':fist:'
                    skill_icon = '<:strength:412729746666029123>'
                elif skill == 'Hitpoints':
                    # skill = ':heart:'
                    skill_icon = '<:hitpoints:412729368633147392>'
                elif skill == 'Ranged':
                    # skill = ':bow_and_arrow:'
                    skill_icon = '<:ranged:412729368427888662>'
                elif skill == 'Prayer':
                    # skill = ':pray:'
                    skill_icon = '<:prayer:412729368364974094>'
                elif skill == 'Magic':
                    # skill = ':sparkles:'
                    skill_icon = '<:magic:412729368817696768>'
                elif skill == 'Agility':
                    # skill = ':runner:'
                    skill_icon = '<:agility:412729368364974102>'
                elif skill == 'Thieving':
                    # skill = ':man_with_turban::skin-tone-5:' + skill
                    skill_icon = '<:thieving:412729368843124736>'
                elif skill == 'Fishing':
                    # skill = ':fishing_pole_and_fish:'
                    skill_icon = '<:fishing:412729368507580427>'
                elif skill == 'Farming':
                    # skill = ':seedling:'
                    skill_icon = '<:farming:412729368205328395>'
                elif skill == 'Woodcutting':
                    # skill = ':evergreen_tree:'
                    skill_icon = '<:woodcutting:412729368776015872>'
                elif skill == 'Hunter':
                    # skill = ':monkey:'
                    skill_icon = '<:hunter:412729368671027200>'
                elif skill == 'Construction':
                    # skill = ':classical_building:'
                    skill_icon = '<:construct:412729368528289822>'
                elif skill == 'Herblore':
                    # skill = ':mushroom:'
                    skill_icon = '<:herblore:412729368608243713>'
                elif skill == 'Firemaking':
                    # skill = ':fire:'
                    skill_icon = '<:firemaking:412729368461312001>'
                elif skill == 'Cooking':
                    # skill = ':pizza:'
                    skill_icon = '<:cook:412729368205328386>'
                elif skill == 'Mining':
                    # skill = ':pick:'
                    skill_icon = '<:mining:412729368637603852>'
                elif skill == 'Overall':
                    # skill = ':bar_chart:'
                    skill_icon = '<:total:412729368675221526>'
                elif skill == 'Runecraft':
                    # skill = ':full_moon:'
                    skill_icon = '<:runecraft:412729368704581632>'
                elif skill == 'Crafting':
                    # skill = ':hammer_pick:'
                    skill_icon = '<:crafting:412729368532746240>'
                elif skill == 'Fletching':
                    # skill = ':sagittarius:'
                    skill_icon = '<:fletching:412729368469831685>'
                elif skill == 'Slayer':
                    # skill = ':japanese_ogre:'
                    skill_icon = '<:slayer:412729368654118944>'
                elif skill == 'Smithing':
                    # skill = ':hammer:'
                    skill_icon = '<:smithing:412729368696061952>'
                # embed.add_field(name=skill, value='⠀⠀⠀⠀' + level)

                space_gap = 15 - len(skill)
                if skill == 'Agility':
                    space_gap += 2
                elif skill == 'Defense':
                    space_gap -= 1
                elif skill == 'Fishing':
                    space_gap += 2
                elif skill == 'Prayer':
                    space_gap += 2
                elif skill == 'Firemaking':
                    space_gap -= 2
                elif skill == 'Runecraft':
                    space_gap -= 1
                elif skill == 'Hunter':
                    space_gap += 1

                if len(level) == 1:
                    space_gap += 3

                # print(skill, space_gap)
                if level == '99':
                    level = '__99__'
                elif level == '2277':
                    level = '__2277__'

                if count == 3 and three:
                    text_data += skill_icon + ' ' + level + ' ' + skill + '\n'
                    count = 1      
                elif (count == 2 or long) and not three:
                    text_data += skill_icon + ' ' + level + ' ' + skill + '\n'
                    count = 1
                else:
                    text_data += skill_icon + ' ' + level + ' ' + skill + ' ' * space_gap
                    count += 1
                embed.description = text_data
                ordered_rs.pop(0)
                break

    await bot.say(embed=embed)


@bot.command()
async def coin(*args):
    cmc = requests.get(
        'https://api.coinmarketcap.com/v1/ticker/').json()

    symb = 'btc'
    num = 1
    called_help = False

    for arg in args:
        if any(char.isdigit() for char in arg):
            for char in arg:
                if char == 'k' or char == 'K':
                    arg = float(arg[:-1]) * 1000
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

    if num == 1:
        num = ''

    if not called_help:
        await bot.say(
            str(num) + ' ' + symb.upper() + ' = $' + str(symb_price) + ' USD')


bot.run(token)
