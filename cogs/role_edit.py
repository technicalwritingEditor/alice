import random

import discord
from discord.ext import commands


class RoleEdit:
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rolecolor(self, ctx, color=None):
        """Change the color of your role
        Basic color names are supported
        Use the hex color code to get the exact color you want
        Use https://htmlcolorcodes.com/ to find a color

        Examples:
        a.rolecolor green
        a.rolecolor #110A2E
        a.rolecolor 6F59CC 
        """
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

        if ctx.message.author.top_role.name != "squad":
            if color in colors:
                color = colors[color]
            if color == None:
                color = discord.Color(random.randint(0x000000, 0xFFFFFF))
            elif len(color) == 6:
                color = discord.Color(int(f"0x{color}", 0))
            elif len(color) == 7:
                color = discord.Color(int(f"0x{color[1:]}", 0))

            await ctx.bot.edit_role(ctx.message.server, ctx.message.author.top_role, color=color)
            await self.bot.say("Changed role color.")

    
    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rolename(self, ctx: commands.Context, *name):
        """Change the name of your role

        Example:
        a.rolename alice
        """
        name = " "

        if name:
            name = " ".join(name)

        if name != "@everyone" and ctx.message.author.top_role.name != "@everyone" and ctx.message.author.top_role.name != "squad":
            print(ctx.message.author.top_role.name, "@everyone")
            print(type(ctx.message.author.top_role.name), type("@everyone"))
            await ctx.bot.edit_role(ctx.message.server, ctx.message.author.top_role, name=name)
            await self.bot.say("Changed role name to: " + name)

def setup(bot: commands.bot) -> None:
    bot.add_cog(RoleEdit(bot))
