import discord, json, datetime
from discord.ext import commands

def admin():
    async def predicate(ctx):
        return ctx.author.id == 345457928972533773 or ctx.author.id == 443217277580738571
    return commands.check(predicate)

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @admin()
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
            self.bot.reload_extension(f'cogs.{cog}')
            await ctx.send(f'<:check:678014104111284234> Reloaded the **{cog}** cog.')
            print(f'+=+=+=+=+=+=+=+ Quacky Support: {ctx.author} has reloaded {cog} +=+=+=+=+=+=+=+')

    @commands.command()
    @admin()
    async def shutdown(self, ctx):
        """ Shutsdown the bot. """
        await ctx.send('Shutting down... Goodbye!')
        await self.bot.change_presence(activity=discord.Game(type=0, name='Shutting Down...'), status=discord.Status.dnd)
        await self.bot.logout()

    @commands.command()
    @admin()
    @commands.guild_only()
    async def sadd(self, ctx, *, user):
        """ Add Someone Permission to Apply for Support Team """
        user = await searching.user(self, ctx, 'give access to apply for Support Team', user)
        if isinstance(user1, discord.Message):
            return
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
    @admin()
    @commands.guild_only()
    async def sdemote(self, ctx, user, *, reason):
        """ Demote a Staff Member! """
        user = await searching.user(self, ctx, 'demote', user)
        if isinstance(user1, discord.Message):
            return
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

    @commands.command()
    @admin()
    @commands.guild_only()
    async def spromote(self, ctx, *, user):
        user = await searching.user(self, ctx, 'promote', user)
        if isinstance(user1, discord.Message):
            return
        helper = ctx.guild.get_role(690239278277591043)
        support = ctx.guild.get_role(729735292734406669)
        mod = ctx.guild.get_role(665423380207370240)
        staff = ctx.guild.get_role(665423057430511626)
        warn = ''
        if mod in user.roles:
            return await ctx.send(f'<:redx:678014058590502912> I cannot promote {user.display_name} as they are already the highest rank!')
        elif support in user.roles:
            new_rank = 'Mod'
            await user.add_roles(mod, reason=f'Promoted by {ctx.author} ({ctx.author.id})')
            await user.remove_roles(helper, reason=f'Promoted by {ctx.author} ({ctx.author.id})')
            embed = discord.Embed(title='You\'ve Been Promoted :tada:', colour=discord.Colour(7506394), description=f'Hey {user.name} :tada:\nThe Quacky Administrators have decided that you deserve a promotion!\nYou\'ve been promoted to Moderator Rank!\n[Pleaese Read about Being a Moderator.](https://quacky.js.org/staff/promoted)\nThanks and Congradulations :smiley:')
        elif helper in user.roles:
            new_rank = 'Support Team'
            await user.add_roles(support, reason=f'Promoted by {ctx.author} ({ctx.author.id})')
            embed = discord.Embed(title='You\'ve Been Promoted :tada:', colour=discord.Colour(7506394), description=f'Hey {user.name} :tada:\nThe Quacky Administrators have decided that you deserve a promotion!\nYou\'ve been promoted to Support Team Rank!\n[Please Read about Managing Support Tickets](https://quacky.js.org/staff/tickets) and [Re-Read the Moderation Policy.](https://quacky.js.org/staff/moderation)\nThanks and Congradulations :smiley:')
        elif staff in user.roles:
            await user.add_roles(helper, reason=f'Promoted by {ctx.author} ({ctx.author.id})')
            return await ctx.send(f'<:check:678014104111284234> Added the Helper Role to **{user.display_name}**.')
        else:
            return await ctx.send(f'<:redx:678014058590502912> {user.display_name} is not a Staff Member!')
        embed.set_author(name=f'Quacky Bot Administrators', icon_url=f'https://quacky.js.org/files/avatar.png')
        embed.set_image(url=f'https://quacky.js.org/files/eevee-evolve.gif')
        try:
            await user.send(embed=embed)
        except discord.errors.HTTPException:
            warn = f'\n:warning: I can\'t send DMs to {user.display_name}! Please make sure to notify them of their promotion.'
        await ctx.send(f'<:check:678014104111284234> Promoted **{user.display_name}** to {new_rank}.{warn}')

    @commands.command(aliases=['activitytest'])
    @admin()
    @commands.guild_only()
    async def atest(self, ctx):
        """ Runs a Staff Activity Test! """
        channel = ctx.guild.get_channel(665426967692181514)
        emoji = self.bot.get_emoji(678014104111284234)
        embed = discord.Embed(title='Staff Activity Test', description=f"React with {emoji} to this message to show that you're active!\nYou have 2 days before you're demoted.", color=discord.Colour(0xFFB42B))
        embed.set_thumbnail(url="https://quacky.elixi.re/i/5t4r.gif?raw=1")
        msg = await channel.send(embed=embed)
        await msg.pin()
        await msg.add_reaction(emoji)
        File = open('/root/Support/Files/misc.json').read()
        data = json.loads(File)
        data['activity'] = [msg.id, f'{(datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%m/%d %H:%M")}']
        with open('/root/Support/Files/misc.json', 'w') as f:
            json.dump(data, f, indent=2)
        if ctx.channel != channel:
            await ctx.message.add_reaction(emoji)

def setup(bot):
    bot.add_cog(Admin(bot))
