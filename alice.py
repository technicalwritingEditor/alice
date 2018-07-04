import logging
import os
import random
import re
import time

import discord 
import requests
from discord.ext import commands

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix=("a.", "A."))

# replace with your own id
owner_id = "239212486673301505"

def is_owner(ctx):
    print(ctx.message.author.id)
    return ctx.message.author.id == owner_id

@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")

    await bot.change_presence(game=discord.Game(name="a.help"))

    for server in bot.servers:
        print(server)

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        await bot.send_message(ctx.message.channel, content="This command is on a %.2fs cooldown" % error.retry_after)
    raise error  # re-raise the error so all the errors will still show up in console


@bot.command(aliases=["ava"], pass_context=True)
async def avatar(ctx: commands.Context, *args):
    username = None

    if args:
        username = " ".join(args)

    if not username:
        await bot.say(ctx.message.author.avatar_url)
    else:
        members = ctx.message.author.server.members
        for member in members:
            print(member)
            if re.match(".*" + str(username.lower()) + ".*", member.name.lower()):
                if member.avatar_url:
                    await bot.say(member.avatar_url)
                    break
                else:
                    await bot.say(member.default_avatar_url)
                    break
            if member.nick is not None:
                if re.match(".*" + str(username.lower()) + ".*", member.nick.lower()):
                    if member.avatar_url:
                        await bot.say(member.avatar_url)
                        break
                    else:
                        await bot.say(member.default_avatar_url)
                        break


@bot.command()
async def roll(*args):
    stop = 100
    help_menu = False
    for arg in args:
        if arg == "-h" or arg == "--help":
            help_menu = True
        elif arg:
            stop = int(arg)

    if not help_menu:
        num = random.randrange(1, stop + 1)
        await bot.say(num)
    else:
        embed = discord.Embed(title="roll", color=discord.Color(0x6d689b))
        embed.add_field(
            name="__a.roll__",
            value="roll a random number between 1 and 100. place a number in front of a.roll to roll between 1 and x.\nex. `a.roll 10` to roll between 1 and 10",
            inline=False)
        await bot.say(embed=embed)


@bot.command(name="8ball")
async def _8ball():
    responses = [
        "It is certain",
        "It is decidedly so",
        "Without a doubt",
        "Yes definitely",
        "You may rely on it",
        "As I see it, yes",
        "Most likely",
        "Outlook good",
        "Yes",
        "Signs point to yes",
        "Don't count on it",
        "My reply is no",
        "My sources say no",
        "Outlook not so good",
        "Very doubtful"
    ]
    response = random.choice(responses)
    await bot.say(response)


@bot.command()
async def coin(*args):
    cmc = requests.get(
        "https://api.coinmarketcap.com/v1/ticker/").json()

    symb = "btc"
    num = 1
    called_help = False

    for arg in args:
        if any(char.isdigit() for char in arg):
            for char in arg:
                if char.lower() == "k":
                    arg = float(arg[:-1]) * 1000
            num = float(arg)
        elif arg == "--help" or arg == "-h":
            embed = discord.Embed(title="coin -h, --help ", color=discord.Color(0x6d689b))
            embed.add_field(
                name="__a.coin__",
                value="default values are 1 btc\n-> `a.coin`\n----> 1 BTC = $8805.74 USD", inline=False)
            embed.add_field(name="__a.coin num__", value="default symbol is btc\n-> `a.coin .4`\n----> 0.4 BTC = $3515.60 USD", inline=False)
            embed.add_field(name="__a.coin symb__", value="symb can be any of the ticker symbols from the top 100 on [coinmarketcap](http://coinmarketcap.com).\n`-> a.coin ETH`\n----> 1 ETH = $868.05 USD", inline=False)
            embed.add_field(name="__a.coin num symb__", value="-> `a.coin 2.45 xmr`\n----> 2.45 XMR = $607.84 USD", inline=False)
            await bot.say(embed=embed)
            called_help = True
        else:
            symb = arg

    for coin in cmc:
        if str(coin["symbol"]).lower() == symb.lower():
            symb_price = round(float(coin["price_usd"]) * num, 2)
            symb_price = f"{symb_price:.2f}"

    """if usd == "usd":
        print(arg, btc_price)
        usd_price = arg / round(float(btc[0]["price_usd"]))
        usd_price = f"{usd_price:.4f}"
        arg = f"{arg:.2f}"
        await bot.say(str(arg) + " USD = " + str(usd_price) + " BTC")
    else:"""

    if num == 1:
        num = ""

    if not called_help:
        await bot.say(
            str(num) + " " + symb.upper() + " = $" + str(symb_price) + " USD")


def load_token() -> str:
    token_file = open("token", "r")
    token = token_file.read()
    token_file.close()

    return token


@bot.command(name="reload", pass_context=True)
@commands.check(is_owner)
async def _reload(ctx, module):
    bot.unload_extension(module)
    bot.load_extension(module)


def main(bot: commands.Bot) -> None:
    token = load_token()
    bot.load_extension("cogs.runescape")
    bot.load_extension("cogs.role_edit")
    bot.load_extension("cogs.social")
    bot.run(token)


if __name__ == "__main__":
    main(bot)
