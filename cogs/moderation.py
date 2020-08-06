import discord, json
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ohyeea(self, ctx):
        await ctx.send('y')

def setup(bot):
    bot.add_cog(Moderation(bot))
