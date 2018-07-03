import logging
import os
import random
import re
import time

import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix=('a.', 'A.'))

# replace with your own id
owner_id = '239212486673301505'

def is_owner(ctx):
    print(ctx.message.author.id)
    return ctx.message.author.id == owner_id

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    for server in bot.servers:
        print(server)

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        await bot.send_message(ctx.message.channel, content='This command is on a %.2fs cooldown' % error.retry_after)
    raise error  # re-raise the error so all the errors will still show up in console


@bot.command(pass_context=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def color(ctx: commands.Context, color=None):
    colors = {
        "red": "FF0000",
        "maroon": "800000",
        "yellow": "FFFF00",
        "olive": "808000",
        "lime": "00FF00",
        "green": "008000",
        "aqua": "00FFFF",
        "teal": "008080",
        "blue": "0000FF",
        "navy": "000080",
        "pink": "FF00FF",
        "purple": "800080",
        "white": "FFFFFF",
        "silver": "C0C0C0",
        "gray": "808080",
        "black": "000001",
        "default": "000000"
    }

    if color in colors:
        color = colors[color]
    if color == None:
        color = discord.Color(random.randint(0x000000, 0xFFFFFF))
    elif len(color) == 6:
        color = discord.Color(int(f"0x{color}", 0))
    elif len(color) == 7:
        color = discord.Color(int(f"0x{color[1:]}", 0))
    await ctx.bot.edit_role(ctx.message.server, ctx.message.author.top_role, color=color)
    await bot.say("Changed role color.")

@bot.command(pass_context=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def role(ctx: commands.Context, *args):
    name = " "

    if args:
        name = " ".join(args)

    if name != "@everyone" and ctx.message.author.top_role.name != "@everyone":
        print(ctx.message.author.top_role.name, "@everyone")
        print(type(ctx.message.author.top_role.name), type("@everyone"))
        await ctx.bot.edit_role(ctx.message.server, ctx.message.author.top_role, name=name)
        await bot.say("Changed role name to: " + name)

@bot.command()
async def colorcodes():
    await bot.say("https://htmlcolorcodes.com/")

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


@bot.command(aliases=['twit', 'tw'])
async def twitter(username):
    page_source = requests.get('https://www.twitter.com/' + username).text
    soup = BeautifulSoup(page_source, 'lxml')
    posts = soup.find_all(class_='tweet-timestamp js-permalink js-nav js-tooltip')
    urls = []

    for post in posts:

        print(post.get('href'))
        link_username = re.findall('/(.*?)/status/', post.get('href'))
        print(link_username[0])
        if username.lower() == link_username[0].lower():
            urls.append('https://www.twitter.com' + post.get('href'))

    url = random.choice(urls)

    await bot.say(url)


@bot.command(aliases=['insta', 'ig'])
async def instagram(username, *args):
    print(username)
    page_source = requests.get('https://www.instagram.com/' + username).text

    srcs = re.findall('"shortcode":"(.*?)","', page_source)

    urls = []

    if srcs:
        for src in srcs:
            urls.append('https://www.instagram.com/p/' + src)
            print(src)

        if args:
            for arg in args:
                if arg == 'r' or arg == 'random':
                    url = random.choice(urls)
                elif arg.isdigit():
                    url = urls[int(arg) - 1]
        else:
            url = urls[0]

        await bot.say(url)
    else:
        await bot.say("Profile doesn't exist or private.")

    print(len(urls))

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


@bot.command(name='8ball')
async def _8ball():
    responses = [
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
        "Don't count on it",
        'My reply is no',
        'My sources say no',
        'Outlook not so good',
        'Very doubtful'
    ]
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


def load_token() -> str:
    token_file = open('token', 'r')
    token = token_file.read()
    token_file.close()

    return token


@bot.command(name='reload', pass_context=True)
@commands.check(is_owner)
async def _reload(ctx, module):
    bot.unload_extension(module)
    bot.load_extension(module)


def main(bot: commands.Bot) -> None:
    token = load_token()
    bot.load_extension('cogs.runescape')
    bot.run(token)


if __name__ == '__main__':
    main(bot)
