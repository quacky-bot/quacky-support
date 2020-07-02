import discord
from discord.ext import commands

def admin():
    async def predicate(ctx):
        bot = ctx.bot
        quacky_guild = bot.get_guild(665378018310488065)
        quacky_member = quacky_guild.get_member(ctx.author.id)
        quacky_devrole = quacky_guild.get_role(665381175958962215)
        quacky_adminrole = quacky_guild.get_role(665423523308634113)
        if quacky_member is None:
            return False
        elif quacky_adminrole in quacky_member.roles:
            return True
        else:
            return False

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
            await ctx.send(f'<:check:678014104111284234> Reloaded all of the bot\'s commands successfully.')
            print(f'+=+=+=+=+=+=+=+ {ctx.author} has reloaded Quacky Support +=+=+=+=+=+=+=+')
        else:
            self.bot.reload_extension(cog)
            await ctx.send(f'<:check:678014104111284234> Reloaded the **{cog}** cog.')
            print(f'+=+=+=+=+=+=+=+ Quacky Support: {ctx.author} has reloaded {cog} +=+=+=+=+=+=+=+')


    @commands.command(usage='[channel] <message>')
    @admin()
    async def say(self, ctx, channel, message=None):
        """ Make's the Bot Say a Message! """
        fail = False
        channel1 = channel
        if channel.__contains__('<') and channel.__contains__('>') and channel.__contains__('#'):
            channel1 = channel.replace('<', '')
            channel1 = channel1.replace('>', '')
            channel1 = channel1.replace('#', '')
            try:
                channel1 = ctx.guild.get_channel(int(channel1))
            except:
                fail = True
        else:
            try:
                channel1 = ctx.guild.get_channel(int(channel1))
            except:
                fail = True
        if fail == True:
            await ctx.channel.last_message.delete()
            return await ctx.send(channel)
        else:
            if message is None:
                return await ctx.send(f'**:bangbang: ERROR :bangbang:**\nmessage is a required argument that is missing.')
            await channel1.send(message)
            await ctx.channel.last_message.add_reaction('\U00002705')

    @commands.command()
    @admin()
    async def shutdown(self, ctx):
        """ Shutdown the Bot. """
        await ctx.send('Ok, Shutting down now. Bye!')
        await self.bot.change_presence(activity=discord.Game(type=0, name='Shutting Down'), status=discord.Status.dnd)
        await self.bot.logout()

    @commands.command()
    @admin()
    async def dm(self, ctx, user, *, message):
        """ Makes the Bot DM Someone. """
        user1 = user
        user2 = user
        if user.__contains__('<') and user.__contains__('>') and user.__contains__('@'): # If User is Mentioned
            user1 = user.replace('<', '')
            user1 = user1.replace('>', '')
            user1 = user1.replace('@', '')
            user1 = user1.replace('!', '')
            try:
                user1 = ctx.guild.get_member(int(user1))
            except:
                user1 = None
        else:
            user1 = discord.utils.get(ctx.guild.members, name=user) # Else Just Search

        if user2 == user and user1 == None: # If search fails, search via userid
            try:
                user1 = ctx.guild.get_member(int(user))
            except:
                user1 = None

        if user1 is None:
            return await ctx.send(f'**:bangbang: ERROR :bangbang:**\nI cannot find that user!')
        try:
            await user1.send(message)
            await ctx.send(f":white_check_mark: Sent a DM to **{user1}**")
        except discord.Forbidden:
            await ctx.send('**:bangbang: ERROR :bangbang:**\nI am unable to DM that user.')

    @commands.command()
    @admin()
    async def status(self, ctx, activity, *, status):
        """ Changes the bot's playing status. """
        if activity == 'playing' or activity == 'game':
            await self.bot.change_presence(activity=discord.Game(type=0, name=status), status=discord.Status.online)
            game = 'Playing'
        elif activity == 'listen' or activity == 'listening':
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status), status=discord.Status.online)
            game = 'Listening To'
        elif activity == 'watching' or activity == 'watch':
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status), status=discord.Status.online)
            game = 'Watching'
        elif activity == 'stream' or activity == 'streaming' or activity == 'twitch':
            await self.bot.change_presence(activity=discord.Streaming(name='on Twitch', url=status), status=discord.Status.online)
            game = 'Streaming'
        else:
            return await ctx.send(f'**:bangbang: ERROR :bangbang:\nactivity must be one of the following:\n> playing\n> listening\n> watching\n> streaming')
        safe_status = discord.utils.escape_markdown(status, as_needed=True, ignore_links=True)
        await ctx.send(f":white_check_mark: Successfully changed the bot's status to **{game} {safe_status}**")

def setup(bot):
    bot.add_cog(Admin(bot))
