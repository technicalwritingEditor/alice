import random
import re

import lxml
import requests
from bs4 import BeautifulSoup
from discord.ext import commands


class Social:
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(aliases=["tw"])
    async def twitter(self, username, *args):
        """Twitter post lookup
        Add "-r" to the end for a random post (working on a better way to do this)
        
        Examples:
        a.twitter jagexash
        a.tw lainvolta -r
        """
        page_source = requests.get("https://www.twitter.com/" + username).text
        soup = BeautifulSoup(page_source, "lxml")
        posts = soup.find_all(class_="tweet-timestamp js-permalink js-nav js-tooltip")
        urls = []

        for post in posts:

            print(post.get("href"))
            link_username = re.findall("/(.*?)/status/", post.get("href"))
            print(link_username[0])
            if username.lower() == link_username[0].lower():
                urls.append("https://www.twitter.com" + post.get("href"))

        if args:
            for arg in args:
                if arg == "-r":
                    url = random.choice(urls)
                else:
                    url = urls[0]
        else:
            url = urls[0]

        await self.bot.say(url)


    @commands.command(aliases=["ig"])
    async def instagram(self, username, *args):
        """Instagram post lookup
        Add "-r" to the end for a random post (working on a better way to do this)
        
        Examples:
        a.instagram satokayo1226
        a.ig l_ovewave -r
        """
        print(username)
        page_source = requests.get("https://www.instagram.com/" + username).text

        srcs = re.findall('"shortcode":"(.*?)","', page_source)

        urls = []

        if srcs:
            for src in srcs:
                urls.append("https://www.instagram.com/p/" + src)
                print(src)

            if args:
                for arg in args:
                    if arg == "-r" or arg == "random":
                        url = random.choice(urls)
                    elif arg.isdigit():
                        url = urls[int(arg) - 1]
            else:
                url = urls[0]

            await self.bot.say(url)
        else:
            await self.bot.say("Profile doesn't exist or private.")

        print(len(urls))

def setup(bot: commands.bot) -> None:
    bot.add_cog(Social(bot))
