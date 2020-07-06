import discord, json, time, asyncio
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 2.0, BucketType.user)
    async def ping(self, ctx):
        """ Ping Pong! Check the Bot's Latency. """
        start = time.perf_counter()
        message = await ctx.send(f":ping_pong: Pong!\nHeartbeat :heart: {round(self.bot.latency * 1000)}ms")
        end = time.perf_counter()
        await message.edit(content=f"{message.content}\nEdit Message <:Edit_Feature:690660539373846549> {round((end - start) * 1000)}ms")

    @commands.command(aliases=['updaterank'])
    @commands.cooldown(1, 300.0, BucketType.user)
    async def rankupdate(self, ctx):
        """ Updates your Roles in the Quacky Support Server to Match your Quacky Badges. """
        guild = self.bot.get_guild(665378018310488065)
        member = guild.get_member(ctx.author.id)
        File = open('/root/Quacky/Files/badges.json').read()
        data = json.loads(File)
        total = 0
        rank = 0
        for x in data['error']:
            if x['id'] == member.id:
                total = x['total']
        for a in data['donator']:
            if a['id'] == member.id:
                rank = a['rank']
        if member.id in data['special']:
            special = guild.get_role(689520201259417682)
            await member.add_roles(special, reason=f'Has Special Badge')
        donator = guild.get_role(690234363648016443)
        if rank == 3:
            mega = guild.get_role(690234610462097504)
            await member.add_roles(mega, donator, reason=f'Has MEGA Badge')
        elif rank == 2:
            mvp = guild.get_role(690234421294530657)
            await member.add_roles(mvp, donator, reason=f'Has MVP Badge')
        elif rank == 1:
            vip = guild.get_role(665423079454801930)
            await member.add_roles(vip, donator, reason=f'Has VIP Badge')
        if total >= 5:
            bug = guild.get_role(729501130723426334)
            await member.add_roles(bug, reason=f'Has Found {total} Bugs with Quacky')
        await ctx.send('<:check:678014104111284234> Updated your Roles in the Quacky Support Server.')

    @commands.command()
    @commands.cooldown(1, 300.0, BucketType.user)
    async def cleardata(self, ctx):
        msg = await ctx.send(f'Are you sure you want to do this, {ctx.author.mention}?\nThis will clear your error, donator, and special badge(s). __**THERE IS NO UNDO!**__')
        checkmark = self.bot.get_emoji(678014104111284234)
        redx = self.bot.get_emoji(678014058590502912)
        await msg.add_reaction(checkmark)
        await msg.add_reaction(redx)
        def check(reaction, user):
            if ctx.author == user:
                if reaction.emoji == checkmark:
                    return True
                elif reaction.emoji == redx:
                    return True
                else:
                    return False
            else:
                return False
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            return await msg.edit(content=f'~~{msg.content}~~\n\nYou took too long to react to the message!')
        else:
            if reaction.emoji == redx:
                return await ctx.send(f'Ok, I won\'t clear your data.')

        File = open('/root/Quacky/Files/badges.json').read()
        data = json.loads(File)
        error = data['error']
        donator = data['donator']
        special = data['special']
        for x in error:
            if x['id'] == ctx.author.id:
                error.remove(x)
        for a in donator:
            if a['id'] == ctx.author.id:
                donator.remove(a)
        if ctx.author.id in special:
            special.remove(ctx.author.id)
        with open('/root/Quacky/Files/badges.json', 'w') as f:
            json.dump(data, f, indent=4)
        guild = self.bot.get_guild()
        ctx_member = guild.get_member(ctx.author.id)
        await ctx.send('<:check:678014104111284234> Cleared your Quacky Data!\nIf you would like to sync your roles with your badges do `!rankupdate`')

    @commands.command()
    @commands.is_owner()
    @commands.cooldown(1, 2.0, BucketType.user)
    async def halp(self, ctx, *, command=None):
        """ Sends this message. """
        about = f"Hi! I'm the Quacky Support Bot.\nI'm here for Support Tickets, Moderation, and Badge Changes."
        try:
            command = command.lower()
        except:
            command = None
        if command is None:
            admincog = self.bot.get_cog('Admin')
            misccog = self.bot.get_cog('Misc')
            modcog = self.bot.get_cog('Moderation')
            ticketcog = self.bot.get_cog('Ticket')
            admin = []
            misc = []
            moderation = []
            ticket = []
            for command in self.bot.commands:
                appendtext = f'**-{command.name}** - {command.short_doc}'
                if command.enabled == False:
                    appendtext = f'~~{appendtext}~~'
                if command.hidden == True:
                    pass
                elif command.cog == admincog:
                    admin.append(appendtext)
                elif command.cog == misccog:
                    misc.append(appendtext)
                elif command.cog == modcog:
                    moderation.append(appendtext)
                elif command.cog == ticketcog:
                    ticket.append(appendtext)
            admin.sort()
            misc.sort()
            moderation.sort()
            ticket.sort()
            admin = '\n'.join(admin)
            misc = '\n'.join(misc)
            moderation = '\n'.join(moderation)
            ticket = '\n'.join(ticket)
            embed = discord.Embed(title=f'Quacky Support\'s Commands', colour=discord.Colour(16750848), description=f'{about}')
            embed.add_field(name='Misc Commands', value=f'{moderation}')
            embed.add_field(name='VC Commands', value=f'{voice}')
            embed.add_field(name='Misc Commands', value=f'{misc}')
            embed.add_field(name='Fun Commands', value=f'{fun}')
            embed.add_field(name='Role Commands', value=f'{roles}')
            embed.set_footer(text='If you would like to learn more about me do -about')
            quacky_guild = self.bot.get_guild(665378018310488065)
            quacky_member = quacky_guild.get_member(ctx.author.id)
            if quacky_member is not None:
                quacky_totalroles = quacky_member.roles
                support = quacky_guild.get_role(729735292734406669)
                mod = quacky_guild.get_role(665423380207370240)
                admin = quacky_guild.get_role(665423523308634113)
                if admin in quacky_totalroles and ctx.guild is not None:
                    embed.add_field(name='Staff Commands', value='If you want to see your Staff Commands, run this command in DMs.')
                elif admin in quacky_totalroles and ctx.guild is None:
                    embed.add_field(name=f'Admin Commands', value=f'{admin_cmds}')
                elif mod in quacky_totalroles:
                    embed.add_field(name=f'Moderator Commands', value=f'{mod_cmds}')
                elif support in quacky_totalroles:
                    embed.add_field(name=f'Helper Commands', value=f'{beta_cmds}')# @todo Finish the Help Command - Manual Adding for Support Tickets :(
            await ctx.send(embed=embed)
        elif command == 'fun' or command == 'misc' or command == 'moderation' or command == 'roles' or command == 'voice':
            cog = self.bot.get_cog(f'{command.capitalize()}')
            cogcmds = cog.get_commands()
            cmds = []
            for x in cogcmds:
                appendtext = f'**-{x}** - {x.short_doc}'
                if x.enabled == False:
                    appendtext = f'~~{appendtext}~~'
                if x.hidden == True:
                    pass
                else:
                    cmds.append(f'{appendtext}')
            cmds.sort()
            cmds = '\n'.join(cmds)
            embed = discord.Embed(title=f'Quacky Bot\'s Commands', colour=discord.Colour(16750848), description=f'{about}')
            embed.add_field(name=f'{command.capitalize()} Commands', value=f'{cmds}')
            embed.set_footer(text='If you would like to learn more about me do -about')
            await ctx.send(embed=embed)
        else:
            command1 = self.bot.get_command(f'{command}')
            if command1 is None:
                return await ctx.send(f'<:redx:678014058590502912> `{command}` is not a valid command!')
            else:
                command = command1
            if command.usage is None:
                params = []
                for f in command.clean_params:
                    params.append(command.clean_params.get(f))
                params = list(params)
                new_params = []
                for x in params:
                    x = str(x)
                    x = x.replace('<Parameter ', '')
                    x = x.replace('"', '')
                    x = x.replace('>', '')
                    new_params.append(x)
                final_params = []
                for a in new_params:
                    if a.__contains__('='):
                        a = a.split('=')
                        a = a.pop(0)
                        final_params.append(f'[{a}]')
                    else:
                        final_params.append(f'<{a}>')
                arguments = ' '.join(final_params)
            else:
                arguments = command.usage
            admincog = self.bot.get_cog('Admin')
            if command.aliases == []:
                embed = discord.Embed(title=f'-{command.name} {arguments}', colour=discord.Colour(7506394), description=f'{command.help}')
            else:
                aliases = '|'.join(command.aliases)
                aliases = f'[{command.name}|{aliases}]'
                embed = discord.Embed(title=f'-{aliases} {arguments}', colour=discord.Colour(7506394), description=f'{command.help}')
            if command.cog == admincog:
                quacky_guild = self.bot.get_guild(665378018310488065)
                quacky_member = quacky_guild.get_member(ctx.author.id)
                if quacky_member is not None:
                    quacky_totalroles = quacky_member.roles
                    staffrole = quacky_guild.get_role(665423057430511626)
                    if staffrole in quacky_totalroles:
                        await ctx.author.send(embed=embed)
                        if ctx.guild is not None:
                            await ctx.send(f':mailbox_with_mail: Check your DMs!')
                    else:
                        await ctx.send(f'<:redx:678014058590502912> You don\'t have permission to see the Help Menu for the `{command}` command.')
                else:
                    await ctx.send(f'<:redx:678014058590502912> You don\'t have permission to see the Help Menu for the `{command}` command.')
            else:
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Misc(bot))
