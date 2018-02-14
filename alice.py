import csv
import random
import urllib
import logging
import re

import discord
import requests
from discord.ext import commands
import os

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
async def meme():
    memes_list = os.listdir('img/memes')
    meme = random.choice(memes_list)

    with open('img/memes/' + meme, 'rb') as f:
        await bot.upload(f)


@bot.command(aliases=['ava'], pass_context=True)
async def avatar(ctx: commands.Context, *args):
    username = None

    if args:
        username = ' '.join(args)

    if not username:
        await bot.say(ctx.message.author.avatar_url)
    else:
        members = ctx.message.author.server.members
        for member in members:
            print(member)
            if re.match('.*' + str(username.lower()) + '.*', member.name.lower()):
                if member.avatar_url:
                    await bot.say(member.avatar_url)
                    break
                else:
                    await bot.say(member.default_avatar_url)
                    break
            if member.nick is not None:
                if re.match('.*' + str(username.lower()) + '.*', member.nick.lower()):
                    if member.avatar_url:
                        await bot.say(member.avatar_url)
                        break
                    else:
                        await bot.say(member.default_avatar_url)
                        break


@bot.command(aliases=['insta', 'ig'])
async def instagram(username, *args):
    print(username)
    page_source = requests.get('https://www.instagram.com/' + username).text

    srcs = re.findall('"code":"(.*?)","', page_source)

    urls = []

    if srcs:
        for src in srcs:
            urls.append('https://www.instagram.com/p/' + src)
            print(src)

        if args:
            for arg in args:
                if arg == 'r' or arg == 'recent':
                    url = urls[0]
                elif arg.isdigit():
                    url = urls[int(arg) - 1]
        else:
            url = random.choice(urls)

        await bot.say(url)
    else:
        await bot.say("Profile doesn't exist or private.")

    print(len(urls))


@bot.command()
async def bonds():
    bonds_list = os.listdir('img/bonds')
    bonds = random.choice(bonds_list)

    with open('img/bonds/' + bonds, 'rb') as f:
        await bot.upload(f)


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
        embed = discord.Embed(title='roll', color=discord.Color(0x6d689b))
        embed.add_field(
            name='__a.roll__',
            value='roll a random number between 1 and 100. place a number in front of a.roll to roll between 1 and x.\nex. `a.roll 10` to roll between 1 and 10',
            inline=False)
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

    rs_unordered = [
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
        row.append(rs_unordered[count])
        count += 1
        data.append(row)

    embed = discord.Embed(color=discord.Color(0x6d689b))

    username_parse = urllib.parse.quote_plus(username)

    embed.set_author(
        name=username,
        url='http://services.runescape.com/m=hiscore_oldschool/hiscorepersonal.ws?user1=' + username_parse,
        icon_url='https://raw.githubusercontent.com/cheazy/alice/master/img/runescape.png')

    rs = {
        'Attack': '<:attack:412729368536940544>',
        'Hitpoints': '<:hitpoints:412729368633147392>',
        'Mining': '<:mining:412729368637603852>',
        'Strength': '<:strength:412729746666029123>',
        'Agility': '<:agility:412729368364974102>',
        'Smithing': '<:smithing:412729368696061952>',
        'Defense': '<:defense:412729368574427136>',
        'Herblore': '<:herblore:412729368608243713>',
        'Fishing': '<:fishing:412729368507580427>',
        'Ranged': '<:ranged:412729368427888662>',
        'Thieving': '<:thieving:412729368843124736>',
        'Cooking': '<:cook:412729368205328386>',
        'Prayer': '<:prayer:412729368364974094>',
        'Crafting': '<:crafting:412729368532746240>',
        'Firemaking': '<:firemaking:412729368461312001>',
        'Magic': '<:magic:412729368817696768>',
        'Fletching': '<:fletching:412729368469831685>',
        'Woodcutting': '<:woodcutting:412729368776015872>',
        'Runecraft': '<:runecraft:412729368704581632>',
        'Slayer': '<:slayer:412729368654118944>',
        'Farming': '<:farming:412729368205328395>',
        'Construction': '<:construct:412729368528289822>',
        'Hunter': '<:hunter:412729368671027200>',
        'Overall': '<:total:412729368675221526>'
    }

    del data[-9:]
    text_data = ''
    count = 1
    space_gap = 0

    level = 1

    for skill, icon in rs.items():
        for ranks_data, level_data, xp_data, skill_data in data:
            if skill == skill_data:
                level = level_data
                break

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

        if level == '99':
            level = '__99__'
        elif level == '2277':
            level = '__2277__'

        if count == 3 and three:
            text_data += icon + ' ' + level + ' ' + skill + '\n'
            count = 1
        elif (count == 2 or long) and not three:
            text_data += icon + ' ' + level + ' ' + skill + '\n'
            count = 1
        else:
            text_data += icon + ' ' + level + ' ' + skill + ' ' * space_gap
            count += 1
        embed.description = text_data

    await bot.say(embed=embed)


@bot.command(name='8ball')
async def _8ball():
    responses = (
        'It is certain',
        'It is decidedly so',
        'Without a doubt',
        'Yes definitely',
        'You may rely on it',
        'As I see it, yes',
        'Most likely',
        'Outlook good',
        'Yes',
        'Signs point to yes',
        'Reply hazy try again',
        'Ask again later',
        'Better not tell you now',
        'Cannot predict now',
        'Concentrate and ask again',
        'Don\'t count on it',
        'My reply is no',
        'My sources say no',
        'Outlook not so good',
        'Very doubtful'
    )
    response = random.choice(responses)
    await bot.say(response)


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
                if char.lower() == 'k':
                    arg = float(arg[:-1]) * 1000
            num = float(arg)
        elif arg == '--help' or arg == '-h':
            embed = discord.Embed(title='coin -h, --help ', color=discord.Color(0x6d689b))
            embed.add_field(
                name='__a.coin__',
                value='default values are 1 btc\n-> `a.coin`\n----> 1 BTC = $8805.74 USD', inline=False)
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
