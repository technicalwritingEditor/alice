import csv
import urllib.parse

import discord
import requests
from discord.ext import commands


class Runescape:
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(aliases=['rs2', 'rs3'], pass_context=True)
    async def rs(self, ctx: commands.Context, *username):
        rs = ctx.message.content[2:5]
        username = ' '.join(username)
        hiscore_csv = get_hiscore_csv(username, rs=rs)
        reader = csv.reader(hiscore_csv.splitlines())

        hiscore_data = [
            ['Overall', '<:total:412729368675221526>'],
            ['Attack', '<:attack:412729368536940544>'],
            ['Defense', '<:defense:412729368574427136>'],
            ['Strength', '<:strength:412729746666029123>'],
            ['Hitpoints', '<:hitpoints:412729368633147392>'],
            ['Ranged', '<:ranged:412729368427888662>'],
            ['Prayer', '<:prayer:412729368364974094>'],
            ['Magic', '<:magic:412729368817696768>'],
            ['Cooking', '<:cook:412729368205328386>'],
            ['Woodcutting', '<:woodcutting:412729368776015872>'],
            ['Fletching', '<:fletching:412729368469831685>'],
            ['Fishing', '<:fishing:412729368507580427>'],
            ['Firemaking', '<:firemaking:412729368461312001>'],
            ['Crafting', '<:crafting:412729368532746240>'],
            ['Smithing', '<:smithing:412729368696061952>'],
            ['Mining', '<:mining:412729368637603852>'],
            ['Herblore', '<:herblore:412729368608243713>'],
            ['Agility', '<:agility:412729368364974102>'],
            ['Thieving', '<:thieving:412729368843124736>'],
            ['Slayer', '<:slayer:412729368654118944>'],
            ['Farming', '<:farming:412729368205328395>'],
            ['Runecraft', '<:runecraft:412729368704581632>'],
            ['Hunter', '<:hunter:412729368671027200>'],
            ['Construction', '<:construct:412729368528289822>'],
            ['Summoning', '<:summoning:413537893970083840>'],
            ['Dungeoneering', '<:dungeoneering:413537893924208640>'],
            ['Divination', '<:divination:413537204820901888>'],
            ['Invention', '<:invention:413537478859948052>']
            # ['Clue Scrolls (easy)'],
            # ['Clue Scrolls (medium)'],
            # ['Clue Scrolls (all)'],
            # [None],
            # [None],
            # ['Clue Scrolls (hard)'],
            # [None],
            # [None],
            # [None]
        ]

        for row_count, row in enumerate(reader):
            if rs == 'rs3':
                if row_count == 28:
                    break
                else:
                    hiscore_data[row_count].extend(row)
            else:
                # row 24+ is for rs3
                if row_count == 24:
                    del hiscore_data[-4:]
                    break
                else:
                    hiscore_data[row_count].extend(row)

        embed = discord.Embed(color=discord.Color(0x6d689b))
        username_parse = urllib.parse.quote_plus(username)

        if rs == 'rs3':
            embed_url = (
                'http://services.runescape.com/m=hiscore/compare?user1=' +
                username_parse
            )
        else:
            embed_url = (
                'http://services.runescape.com/m=hiscore_oldschool/'
                'hiscorepersonal.ws?user1=' + username_parse)

        embed.set_author(
            name=username,
            url=embed_url,
            icon_url='https://raw.githubusercontent.com/'
                     'cheazy/alice/master/img/rs/runescape.png'
        )

        description_text = ''
        space_gaps = {
            'Strength': -2,
            'Ranged': -2,
            'Woodcutting': -8,
            'Crafting': -1,
            'Agility': 1,
            'Runecraft': -3,
            'Construction': -5,
            'Dungeoneering': -9
        }

        for row_count, data in enumerate(hiscore_data):
            skill, icon, _rank, level, _xp = data
            space_gap = 23 - len(skill)
            if len(level) == 1:
                space_gap += 3
            if skill in space_gaps.keys():
                space_gap += space_gaps[skill]
            if level == '99':
                level = '__99__'
            elif level == '2277':
                level = '__2277__'
            elif level == '120':
                level = '__120__'

            if row_count % 2:
                description_text += (
                    icon + ' ' +
                    level + ' ' +
                    skill + ' ' * space_gap)
            else:
                description_text += (
                    icon + ' ' +
                    level + ' ' +
                    skill + '\n')

        embed.description = description_text
        await self.bot.say(embed=embed)


def get_hiscore_csv(username, rs='rs'):
    rs_string = ''
    if rs == 'rs ' or rs == 'rs2':
        rs_string = '_oldschool'

    payload = {'player': username}
    hiscore_csv: str = requests.get(
        'http://services.runescape.com'
        '/m=hiscore' + rs_string + '/index_lite.ws',
        params=payload).text

    return hiscore_csv


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Runescape(bot))
