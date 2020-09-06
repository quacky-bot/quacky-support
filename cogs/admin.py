import discord, json
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, *, cog='all'):
        """ Reloads the bot's commands. """
        if cog == 'all':
            self.bot.reload_extension('cogs.admin')
            self.bot.reload_extension('cogs.misc')
            self.bot.reload_extension('cogs.moderation')
            self.bot.reload_extension('cogs.events')
            self.bot.reload_extension('cogs.ticket')
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
    @commands.guild_only()
    async def sadd(self, ctx, *, user: discord.Member):
        """ Add Someone Permission to Apply for Support Team """
        File = open('/root/Quacky/Files/misc.json').read()
        data = json.loads(File)
        if user.id in data['sapply']:
            return await ctx.send('<:redx:678014058590502912> **{user.display_name}** was already eligible to be a Support Team member!')
        data['sapply'].append(user.id)
        with open('/root/Quacky/Files/misc.json', 'w') as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title='You\'ve Been Promoted!', description=f'Hello {user.name} :tada:\nYou now have the chance to Apply to be a Support Team Member!\nIf you would like to apply DM Me the `!sapply` command and we will begin the application process.', color=discord.Colour(0x00BDFF))
        embed.set_author(name='Quacky Bot Administrators', icon_url='https://quacky.js.org/files/avatar.png')
        warn = ''
        try:
            await user.send(embed=embed)
        except discord.errors.HTTPException:
            warn = f'\n:warning: I can\'t send DMs to {user.display_name}! Please make sure to notify them of their promotion.'
        await ctx.send(f'<:check:678014104111284234> **{user.display_name}** can now apply to be a Support Team member!{warn}')

    @commands.command()
    @commands.is_owner()
    @commands.guild_only()
    async def sdemote(self, ctx, user: discord.Member, *, reason):
        """ Demote a Staff Member! """
        helper = ctx.guild.get_role(690239278277591043)
        support = ctx.guild.get_role(729735292734406669)
        mod = ctx.guild.get_role(665423380207370240)
        staff = ctx.guild.get_role(665423057430511626)
        warn = ''
        if mod in user.roles:
            await user.remove_roles(mod, reason=f'{ctx.author} - Demote Command\nReason: {reason}')
            await user.add_roles(support, reason=f'{ctx.author} - Demote Command\nReason: {reason}')
            old_rank = 'Moderator'
            new_rank = 'Support Team Member'
        elif support in user.roles:
            await user.remove_roles(support, reason=f'{ctx.author} - Demote Command\nReason: {reason}')
            await user.add_roles(helper, reason=f'{ctx.author} - Demote Command\nReason: {reason}')
            old_rank = 'Support Team Member'
            new_rank = 'Helper'
        elif helper in user.roles:
            await user.remove_roles(staff, helper, reason=f'{ctx.author} - Demote Command\nReason: {reason}')
            embed = discord.Embed(title='You\'ve Been Demoted', description=f'Hello {user.name},\nSadly, the Quacky Administrators have decided to remove you from the Staff Team.\n**Reason:** {reason}', color=discord.Colour(0xC70039))
            embed.set_author(name='Quacky Bot Administrators', icon_url='https://quacky.js.org/files/avatar.png')
            try:
                await user.send(embed=embed)
                return await ctx.send(f'<:check:678014104111284234> Removed **{user.display_name}** from the Staff Team.')
            except discord.errors.HTTPException:
                return await ctx.send(f'<:check:678014104111284234> Removed **{user.display_name}** from the Staff Team.\n:warning: I can\'t send DMs to {user.display_name}! Please make sure to notify them of their demotion.')
        elif staff in user.roles:
            await user.remove_roles(staff, reason=f'{ctx.author} - Demote Command\nReason: {reason}')
            return await ctx.send(f'<:check:678014104111284234> Removed the Staff Role from **{user.display_name}**.')
        else:
            return await ctx.send(f'<:redx:678014058590502912> **{user.display_name}** is not a Staff Member and cannot be demoted!')

        embed = discord.Embed(title='You\'ve Been Demoted', description=f'Hello {user.name},\nSadly, the Quacky Administrators have decided to demote you from {old_rank} to {new_rank}.\n**Reason:** {reason}', color=discord.Colour(0xC70039))
        embed.set_author(name='Quacky Bot Administrators', icon_url='https://quacky.js.org/files/avatar.png')
        try:
            await user.send(embed=embed)
        except discord.errors.HTTPException:
            warn = f'\n:warning: I can\'t send DMs to {user.display_name}! Please make sure to notify them of their demotion.'
        await ctx.send(f'<:check:678014104111284234> Demoted **{user.display_name}** to {new_rank}.{warn}')


def setup(bot):
    bot.add_cog(Admin(bot))
