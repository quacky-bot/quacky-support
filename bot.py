import discord, json
from discord.ext import commands
error_icon = 'https://cdn.discordapp.com/emojis/678014140203401246.png?v=1'
Client = discord.Client()
TOKEN = open('/root/Support/token.txt', 'r').read()
# TOKEN = open('/Users/duckmasteral/Documents/GitHub/quacky-support/token.txt').read()

initial_extensions = ['cogs.admin', 'cogs.moderation', 'cogs.misc', 'cogs.ticket', 'cogs.events', 'jishaku']

client = commands.Bot(command_prefix=commands.when_mentioned_or('!'), case_insensitive=True, allowed_mentions=discord.AllowedMentions(roles=False, everyone=False, users=False))

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            print(f'Quacky Support: {extension} could not be loaded!\n{type(e).__name__}: {e}')

client.run(TOKEN)
