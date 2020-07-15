import discord
from discord.ext import commands

def admin():
    async def predicate(ctx):
        bot = ctx.bot
        quacky_guild = bot.get_guild(665378018310488065)
        quacky_member = quacky_guild.get_member(ctx.author.id)
        quacky_adminrole = quacky_guild.get_role(665423523308634113)
        if quacky_member is None:
            return False
        elif quacky_adminrole in quacky_member.roles:
            return True
        else:
            return False
    return commands.check(predicate)

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @admin()
    async def reload(self, ctx, *, cog='all'):
        """ Reloads the bot's commands. """
        if cog == 'all':
            self.bot.reload_extension('admin')
            self.bot.reload_extension('misc')
            self.bot.reload_extension('moderation')
            self.bot.reload_extension('events')
            self.bot.reload_extension('ticket')
            await ctx.send(f'<:check:678014104111284234> Reloaded all of the bot\'s commands successfully.')
            print(f'+=+=+=+=+=+=+=+ {ctx.author} has reloaded Quacky Support +=+=+=+=+=+=+=+')
        else:
            self.bot.reload_extension(cog)
            await ctx.send(f'<:check:678014104111284234> Reloaded the **{cog}** cog.')
            print(f'+=+=+=+=+=+=+=+ Quacky Support: {ctx.author} has reloaded {cog} +=+=+=+=+=+=+=+')

    @commands.command()
    @admin()
    async def test(self, ctx):
        self.bot.load_extension('ticket')

    @commands.command()
    @admin()
    async def shutdown(self, ctx):
        """ Shutsdown the bot. """
        await ctx.send('Shutting down... Goodbye!')
        await self.bot.change_presence(activity=discord.Game(type=0, name='Shutting Down...'), status=discord.Status.dnd)
        await self.bot.logout()

def setup(bot):
    bot.add_cog(Admin(bot))
