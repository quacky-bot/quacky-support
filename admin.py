import discord
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
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
    @commands.is_owner()
    async def shutdown(self, ctx):
        """ Shutsdown the bot. """
        await ctx.send('Shutting down... Goodbye!')
        await self.bot.change_presence(activity=discord.Game(type=0, name='Shutting Down...'), status=discord.Status.dnd)
        await self.bot.logout()

    @commands.command()
    @commands.is_owner()
    async def sadd(self, ctx, *, user: discord.Member):
        """ Add Someone Permission to Apply for Support Team """
        File = open('/root/Quacky/Files/misc.json').read()
        data = json.loads(File)
        if user.id in data['sapply']:
            return await ctx.send('<:redx:678014058590502912> You\'re not eligible to apply for Support Team.')
        data['sapply'].append(user.id)
        with open('/root/Quacky/Files/misc.json', 'w') as f:
            json.dump(data, f, indent=4)

def setup(bot):
    bot.add_cog(Admin(bot))
