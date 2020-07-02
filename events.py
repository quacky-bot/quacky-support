import discord, json
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready():
        # (activity=discord.Game(name="a game"))
        # (activity=discord.Streaming(name="My Stream", url=my_twitch_url))
        # (activity=discord.Activity(type=discord.ActivityType.listening, name="a song"))
        # (activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"))
        await client.change_presence(activity=discord.Game(type=0, name=f'with Code'), status=discord.Status.online)
        print(f'"{client.user.name}" is ready to use.')

    @commands.Cog.listener()
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.ExtensionNotLoaded) or isinstance(error, commands.ExtensionAlreadyLoaded) or isinstance(error, commands.ExtensionFailed) or isinstance(error, commands.ExtensionNotFound) or isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'**:bangbang: ERROR :bangbang:**\n{error}')
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send('**:bangbang: ERROR :bangbang:**\nThis command cannot be used in DMs!')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f'**:bangbang: ERROR :bangbang:**\nYou do not have the required permissions to do that command.\nMissing Permission: `{error.missing_perms}`')
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f'**:bangbang: ERROR :bangbang:**\nI do not have the required permissions to do that command.\nMissing Permission: `{error.missing_perms}`')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(':x: You don\'t have permission to do this command!')
        else:
            await ctx.send(f'**:bangbang: ERROR :bangbang:**\n{error}\n*This seems to be an error with the code. Please contact the bot owner about this!*')
