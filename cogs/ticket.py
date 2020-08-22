import discord, json, asyncio
from discord.ext import commands, tasks
from discord.ext.commands.cooldowns import BucketType
from io import BytesIO

def rank(rank):
    async def predicate(ctx):
        try:
            ticket_owner = ctx.channel.topic
        except:
            ticket_owner = ''
        ticket_owner = ticket_owner.replace('USERID: ', '')
        bot = ctx.bot
        guild = bot.get_guild(665378018310488065)
        support = guild.get_role(729735292734406669)
        mod = guild.get_role(665423380207370240)
        admin = guild.get_role(665423523308634113)
        ctx_member = guild.get_member(ctx.author.id)
        if rank == 'helper':
            if support in ctx_member.roles or ticket_owner == str(ctx.author.id) or mod in ctx_member.roles or admin in ctx_member.roles:
                return True
            else:
                return False
        elif rank == 'mod':
            if mod in ctx_member.roles or ticket_owner == str(ctx.author.id) or admin in ctx_member.roles:
                return True
            else:
                return False
        elif rank == 'admin':
            if admin in ctx_member.roles:
                return True
            else:
                return False
        elif rank == 'blacklist':
            File = open('/root/Support/Files/blacklist.json').read()
            data = json.loads(File)
            for x in data['ticket']:
                if x['id'] == ctx.author.id:
                    return False
            return True
        else:
            return False
    return commands.check(predicate)

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @rank('blacklist')
    @commands.cooldown(1, 300.0, BucketType.user)
    async def new(self, ctx, *, subject=None):
        """ Create a Ticket!
        Ticket Categories are Report, Question, and Other.
        To prevent spam, you can only make a ticket once every 5 minutes. """
        guild = self.bot.get_guild(665378018310488065)
        await ctx.channel.last_message.delete()
        mod = guild.get_role(665423380207370240)
        support_role = guild.get_role(729735292734406669)
        admin = guild.get_role(665423523308634113)
        staff_role = guild.get_role(665423057430511626)
        member1 = guild.get_member(ctx.author.id)
        category = self.bot.get_channel(723971770289488013)
        staff_request = False
        if subject == None:
            def check_msg(m):
                if ctx.author == m.author and ctx.channel == m.channel:
                    return True
                else:
                    return False
            m1 = await ctx.send('What\'s the Subject of your Support Ticket?')
            try:
                msg = await self.bot.wait_for('message', check=check_msg, timeout=60.0)
            except asyncio.TimeoutError:
                await ctx.send('<:redx:678014058590502912> You took too long to answer the question!')
                return
            subject = msg.content
            await m1.delete()
            await msg.delete()
            if subject.lower() == 'cancel':
                await ctx.send('<:redx:678014058590502912> Canceled Creating the Support Ticket.')
                return
        if staff_role in member1.roles:
            staff_msg_yes = '\n<:Staff:690664654736851014> - Staff Request'
        else:
            staff_msg_yes = ''
        react_msg = await ctx.send(f'**Identify Your Ticket\'s Topic:**\n:bangbang: - Report\n:grey_question: - Question{staff_msg_yes}\n:newspaper: - Other\n<:redx:678014058590502912> - Cancel Your Ticket Creation')
        bangbang = '\U0000203c'
        news = '\U0001f4f0'
        question = '\U00002754'
        staff_emoji = self.bot.get_emoji(690664654736851014)
        cancel_emoji = self.bot.get_emoji(678014058590502912)
        await react_msg.add_reaction(bangbang)
        await react_msg.add_reaction(question)
        if staff_role in member1.roles:
            await react_msg.add_reaction(staff_emoji)
        await react_msg.add_reaction(news)
        await react_msg.add_reaction(cancel_emoji)
        def check_react(reaction, user_react):
            if ctx.author == user_react:
                if reaction.emoji == bangbang or reaction.emoji == question or reaction.emoji == news or reaction.emoji == cancel_emoji:
                    return True
                elif reaction.emoji == staff_emoji and staff_role in member1.roles:
                    return True
                else:
                    return False
            else:
                return False
        try:
            reaction, user_react = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_react)
        except asyncio.TimeoutError:
            await ctx.send('<:redx:678014058590502912> You took too long to react to the message!')
            return
        else:
            if reaction.emoji == bangbang:
                m = []
                online = discord.Status.online
                for member in mod.members:
                    if member.is_on_mobile():
                        return
                    if member.status == online:
                        m.append(f'{member.mention}')
                for member in admin.members:
                    if member.is_on_mobile():
                        return
                    if member.status == online:
                        m.append(f'{member.mention}')
                content = ' '.join(m)
                content = f'{content} {ctx.author.mention}'
                ticket_prefix = 'report'
                topic = 'Report'
            elif reaction.emoji == question:
                content = ctx.author.mention
                ticket_prefix = 'question'
                topic = 'Question'
            elif reaction.emoji == news:
                content = ctx.author.mention
                ticket_prefix = 'ticket'
                topic = 'Other'
            elif reaction.emoji == staff_emoji:
                content = ctx.author.mention
                ticket_prefix = 'staff'
                topic = 'Staff Request'
                staff_request = True
            elif reaction.emoji == cancel_emoji:
                await ctx.send(f'<:check:678014104111284234> Canceled the Ticket Making Process.', delete_after=10)
                return await react_msg.delete()
            await react_msg.delete()
        channel = await guild.create_text_channel(f'{ticket_prefix}-{member1.display_name}', category=category, reason=f'{ctx.author} ({ctx.author.id}) - Ticket Creation', topic=f'USERID: {ctx.author.id}')
        await channel.set_permissions(guild.default_role, read_messages=False, reason=f'{ctx.author} ({ctx.author.id}) - Ticket Creation')
        await channel.set_permissions(ctx.author, read_messages=True, send_messages=True, manage_messages=False, reason=f'{ctx.author} ({ctx.author.id}) - Ticket Creation')
        if staff_request == False:
            await channel.set_permissions(support_role, read_messages=True, send_messages=True, reason=f'{ctx.author} ({ctx.author.id}) - Ticket Creation')
            embed = discord.Embed(title='Quacky Support', colour=discord.Colour(7506394), description=f'Hey {ctx.author.mention}! Thanks for making a support ticket.\nA Quacky Staff Member will respond to you as soon as possible.\nTopic: **{topic}**\nSubject: **{subject}**')
        elif staff_request == True:
            embed = discord.Embed(title='Quacky Staff Request', colour=discord.Colour(7506394), description=f'Hey {ctx.author.mention}! Thanks for making a staff request ticket.\nA Quacky Admin will respond to you as soon as possible.\nTopic: **{topic}**\nSubject: **{subject}**')
        embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        await channel.send(embed=embed)
        delcontent = await channel.send(f'{content}', delete_after=0.01)
        await ctx.send(f'<:check:678014104111284234> Created your Support Ticket --> {channel.mention}', delete_after=10)

    @commands.command()
    @commands.guild_only()
    @rank('helper')
    async def close(self, ctx, *, reason=None):
        """ Close a Ticket """
        if ctx.channel.category_id != 723971770289488013:
            return await ctx.send(f'<:redx:678014058590502912> You can only do this command in a Support Ticket.')
        ticket_owner = ctx.channel.topic
        ticket_owner = ticket_owner.replace('USERID: ', '')
        archive = ctx.guild.get_channel(729813211704066169)
        tuser = self.bot.get_user(int(ticket_owner))
        member = ctx.guild.get_member(ctx.author.id)
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages = False
        overwrite.read_messages = True
        await ctx.channel.last_message.delete()
        if reason == None:
            def check_msg(m):
                if ctx.author == m.author and ctx.channel == m.channel:
                    return True
                else:
                    return False
            m1 = await ctx.send('What\'s the reason for closing the ticket?')
            try:
                m2 = await self.bot.wait_for('message', check=check_msg, timeout=60.0)
            except asyncio.TimeoutError:
                return await ctx.send('<:redx:678014058590502912> You took too long to answer the question!')
            reason = m2.content
            await m1.delete()
            await m2.delete()
            if reason.lower() == 'cancel':
                return await ctx.send('<:redx:678014058590502912> Canceled Closing the Support Ticket.')
        msg = await ctx.send(f'<a:Loading:540153374763384852> Sending the Message and Updating Permissions...')
        try:
            await tuser.send(f'Your ticket has been closed by **{member.display_name}** with reason **{reason}**\nYou can read the chat history here: {msg.jump_url}')
        except:
            await ctx.send(f'{tuser.mention} your ticket has been closed by {member.display_name} with reason {reason}', delete_after=5)
        if ctx.channel.name.startswith('staff-'):
            await ctx.channel.edit(category=archive, reason=f'{ctx.author} ({ctx.author.id}) - Ticket Close Command', sync_permissions=False, position=0)
        else:
            await ctx.channel.edit(category=archive, reason=f'{ctx.author} ({ctx.author.id}) - Ticket Close Command', sync_permissions=True, position=0)
        await ctx.channel.set_permissions(tuser, overwrite=overwrite)
        await msg.edit(content=f':lock: Ticket Closed by **{member.display_name}**\nReason: **{reason}**')

    @commands.command()
    @commands.guild_only()
    @rank('mod')
    async def add(self, ctx, *, user):
        """ Add Someone to a Ticket """
        if ctx.channel.category_id != 723971770289488013:
            return await ctx.send(f'<:redx:678014058590502912> You can only do this command in a Support Ticket.')
        ctx_member = ctx.guild.get_member(ctx.author.id)
        starting_msg = ctx.channel.last_message
        user = user.lower()
        user1 = None
        embed_user = ctx.author
        u = []
        m = []
        failn = []
        faily = []
        def check(m):
            if ctx.author == m.author and ctx.channel == m.channel:
                try:
                    m1 = int(m.content)
                except:
                    faily.append('n')
                    return True
                message_0 = m1 - 1
                if message_0 >= users_len or m1 <= 0:
                    faily.append('n')
                    return True
                else:
                    failn.append('n')
                    return True
            else:
                faily.append('n')
                return False
        guildmem = ctx.guild.members
        for member in guildmem:
            name = f'{member.name}#{member.discriminator}'
            name = name.lower()
            dname = member.display_name
            dname = dname.lower()
            oname = member.name
            oname = oname.lower()
            if dname.__contains__(f'{user}') or name == (f'{user}') or oname.__contains__(f'{user}'):
                u.append(f'{member.mention}')
                m.append(f'{member.id}')
        if len(u) == 1:# If it returns only 1 member
            pop = m.pop(0)
            user1 = ctx.guild.get_member(int(pop))
        elif len(u) == 0:# If it returns 0 members
            if user.startswith('<@') and user.endswith('>'):
                user1 = user.replace('<', '')
                user1 = user1.replace('>', '')
                user1 = user1.replace('!', '')
                user1 = user1.replace('@', '')
                user1 = ctx.guild.get_member(int(user1))
            else:
                try:
                    user1 = ctx.guild.get_member(int(user))
                except:
                    user1 = None
                    pass
            if user1 == None:
                embed = discord.Embed(title='OOPS! An error has occurred >.<', colour=discord.Colour(0xff0000), description='I can not find that user!')
                embed.set_author(name=f'{embed_user}', icon_url=f'{embed_user.avatar_url}')
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/678014140203401246.png?v=1")
                embed.set_footer(text='If you need help please do the -support command.')
                await ctx.send(embed=embed)
                return
        elif len(u) >= 10:
            embed = discord.Embed(title='OOPS! An error has occurred >.<', colour=discord.Colour(0xff0000), description='Too many users found. Please be more specific.')
            embed.set_author(name=f'{embed_user}', icon_url=f'{embed_user.avatar_url}')
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/678014140203401246.png?v=1")
            embed.set_footer(text='If you need help please do the -support command.')
            await ctx.send(embed=embed)
            return
        else:# If it returns more than 1 member
            a = ['1']
            users_list = []
            for item in u:
                num = len(a)
                a.append('f')
                users_list.append(f'{num}. {item}')
            users_len = len(users_list)
            users_list = '\n'.join(users_list)# -- -- -- ADD RESULT TEXT BELOW -- -- --
            embed = discord.Embed(title='Multiple Members Found!', colour=discord.Colour(7506394), description=f'Please type the number that corresponds to the member you want to add to the ticket.\n{users_list}')
            embed.set_author(name=f'{embed_user}', icon_url=f'{embed_user.avatar_url}')
            msg2 = await ctx.send(embed=embed)
            try:
                msg = await self.bot.wait_for('message', check=check, timeout=60.0)
            except asyncio.TimeoutError:
                await ctx.send('<:redx:678014058590502912> You took too long to answer the question!')
                return
            if len(failn) >= 1:
                msg1 = int(msg.content)
                popnum = msg1 - 1
                user2 = m.pop(popnum)
                user1 = ctx.guild.get_member(int(user2))
            elif len(faily) >= 1:
                await ctx.send(f'<:redx:678014058590502912> Invalid Number.')
                return
        if discord.PermissionOverwrite.is_empty(ctx.channel.overwrites_for(user1)) == False:
            return await ctx.send('<:redx:678014058590502912> You can\'t add someone to the ticket if they\'ve already been added!')
        await ctx.channel.set_permissions(user1, read_messages=True)
        try:
            await user1.send(f'<:join:659881573012865084> You\'ve been added to **{ctx.channel.mention}** by **{ctx_member.display_name}.**')
        except:
            pass
        await starting_msg.delete()
        try:
            await msg2.delete()
            await msg.delete()
        except:
            pass
        await ctx.send(f'<:check:678014104111284234> **{ctx_member.display_name}** added **{user1.display_name}** to the channel.')

    @commands.command()
    @commands.guild_only()
    @rank('mod')
    async def remove(self, ctx, *, user):
        """ Remove Someone from a Ticket """
        if ctx.channel.category_id != 723971770289488013:
            return await ctx.send(f'<:redx:678014058590502912> You can only do this command in a Support Ticket.')
        ticket_owner = ctx.channel.topic
        ticket_owner = ticket_owner.replace('USERID: ', '')
        tuser = self.bot.get_user(int(ticket_owner))
        tmember = ctx.guild.get_member(int(ticket_owner))
        support = ctx.guild.get_role(729735292734406669)
        quacky_bot_role = ctx.guild.get_role(665409797885263882)
        ctx_member = ctx.guild.get_member(ctx.author.id)
        starting_msg = ctx.channel.last_message
        user = user.lower()
        user1 = None
        embed_user = ctx.author
        u = []
        m = []
        failn = []
        faily = []
        def check(m):
            if ctx.author == m.author and ctx.channel == m.channel:
                try:
                    m1 = int(m.content)
                except:
                    faily.append('n')
                    return True
                message_0 = m1 - 1
                if message_0 >= users_len or m1 <= 0:
                    faily.append('n')
                    return True
                else:
                    failn.append('n')
                    return True
            else:
                faily.append('n')
                return False
        guildmem = ctx.guild.members
        for member in guildmem:
            name = f'{member.name}#{member.discriminator}'
            name = name.lower()
            dname = member.display_name
            dname = dname.lower()
            oname = member.name
            oname = oname.lower()
            if dname.__contains__(f'{user}') or name == (f'{user}') or oname.__contains__(f'{user}'):
                u.append(f'{member.mention}')
                m.append(f'{member.id}')
        if len(u) == 1:# If it returns only 1 member
            pop = m.pop(0)
            user1 = ctx.guild.get_member(int(pop))
        elif len(u) == 0:# If it returns 0 members
            if user.startswith('<@') and user.endswith('>'):
                user1 = user.replace('<', '')
                user1 = user1.replace('>', '')
                user1 = user1.replace('!', '')
                user1 = user1.replace('@', '')
                user1 = ctx.guild.get_member(int(user1))
            else:
                try:
                    user1 = ctx.guild.get_member(int(user))
                except:
                    user1 = None
                    pass
            if user1 == None:
                embed = discord.Embed(title='OOPS! An error has occurred >.<', colour=discord.Colour(0xff0000), description='I can not find that user!')
                embed.set_author(name=f'{embed_user}', icon_url=f'{embed_user.avatar_url}')
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/678014140203401246.png?v=1")
                embed.set_footer(text='If you need help please do the -support command.')
                await ctx.send(embed=embed)
                return
        elif len(u) >= 10:
            embed = discord.Embed(title='OOPS! An error has occurred >.<', colour=discord.Colour(0xff0000), description='Too many users found. Please be more specific.')
            embed.set_author(name=f'{embed_user}', icon_url=f'{embed_user.avatar_url}')
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/678014140203401246.png?v=1")
            embed.set_footer(text='If you need help please do the -support command.')
            await ctx.send(embed=embed)
            return
        else:# If it returns more than 1 member
            a = ['1']
            users_list = []
            for item in u:
                num = len(a)
                a.append('f')
                users_list.append(f'{num}. {item}')
            users_len = len(users_list)
            users_list = '\n'.join(users_list)# -- -- -- ADD RESULT TEXT BELOW -- -- --
            embed = discord.Embed(title='Multiple Members Found!', colour=discord.Colour(7506394), description=f'Please type the number that corresponds to the member you want to remove from the ticket.\n{users_list}')
            embed.set_author(name=f'{embed_user}', icon_url=f'{embed_user.avatar_url}')
            msg2 = await ctx.send(embed=embed)
            try:
                msg = await self.bot.wait_for('message', check=check, timeout=60.0)
            except asyncio.TimeoutError:
                await ctx.send('<:redx:678014058590502912> You took too long to answer the question!')
                return
            if len(failn) >= 1:
                msg1 = int(msg.content)
                popnum = msg1 - 1
                user2 = m.pop(popnum)
                user1 = ctx.guild.get_member(int(user2))
            elif len(faily) >= 1:
                await ctx.send(f'<:redx:678014058590502912> Invalid Number.')
                return
        if user1 == tmember:
            return await ctx.send(f'<:redx:678014058590502912> You can\'t remove the Ticket Owner from the ticket!')
        elif support in user1.roles:
            return await ctx.send(f'<:redx:678014058590502912> You cannot remove another Support Team Member from the Ticket!')
        elif quacky_bot_role in user1.roles or user1.id == 235148962103951360:
            return await ctx.send(f'<:redx:678014058590502912> You cannot remove this bot. It has permission to see every channel.')
        elif discord.PermissionOverwrite.is_empty(ctx.channel.overwrites_for(user1)):
            return await ctx.send(f'<:redx:678014058590502912> {user1.display_name} hasn\'t been added to the Ticket!')
        await ctx.channel.set_permissions(user1, overwrite=None)
        await starting_msg.delete()
        try:
            await msg2.delete()
            await msg.delete()
        except:
            pass
        await ctx.send(f'<:check:678014104111284234> **{ctx_member.display_name}** removed **{user1.display_name}** from the channel.')

    @commands.command()
    @commands.guild_only()
    @rank('helper')
    async def rename(self, ctx, *, prefix):
        """ Rename a Ticket's Prefix """
        if ctx.channel.category_id != 723971770289488013:
            return await ctx.send(f'<:redx:678014058590502912> You can only do this command in a Support Ticket.')
        ticket_owner = ctx.channel.topic
        ticket_owner = ticket_owner.replace('USERID: ', '')
        tuser = self.bot.get_user(int(ticket_owner))
        tmember = ctx.guild.get_member(int(ticket_owner))
        ctx_member = ctx.guild.get_member(ctx.author.id)
        starting_msg = ctx.channel.last_message
        await ctx.channel.edit(name=f'{prefix}-{tmember.display_name}')
        await ctx.send(f'<:check:678014104111284234> **{ctx_member.display_name}** renamed the channel to **{ctx.channel.name}**')
        await starting_msg.delete()

    @commands.command(aliases=['transferowner', 'ownertransfer'])
    @commands.guild_only()
    @rank('mod')
    async def transfer(self, ctx, *, user):
        """ Make Someone Else the Ticket Owner of a Ticket """
        File_ticket_blacklist = open('/root/Support/Files/blacklist.json').read()
        data_ticket_blacklist = json.loads(File_ticket_blacklist)
        ticket_blacklist = data_ticket_blacklist['ticket']
        ticket_owner = ctx.channel.topic
        ticket_owner = ticket_owner.replace('USERID: ', '')
        tuser = ctx.guild.get_member(int(ticket_owner))
        if tuser is None:
            tuser = await self.bot.fetch_user(int(ticket_owner))
            NotInServer = True
        else:
            NotInServer = False
        ctx_member = ctx.guild.get_member(int(ctx.author.id))
        admin = ctx.guild.get_role(665423523308634113)
        starting_msg = ctx.channel.last_message
        user = user.lower()
        user1 = None
        embed_user = ctx.author
        u = []
        m = []
        failn = []
        faily = []
        def check(m):
            if ctx.author == m.author and ctx.channel == m.channel:
                try:
                    m1 = int(m.content)
                except:
                    faily.append('n')
                    return True
                message_0 = m1 - 1
                if message_0 >= users_len or m1 <= 0:
                    faily.append('n')
                    return True
                else:
                    failn.append('n')
                    return True
            else:
                faily.append('n')
                return False
        guildmem = ctx.guild.members
        for member in guildmem:
            name = f'{member.name}#{member.discriminator}'
            name = name.lower()
            dname = member.display_name
            dname = dname.lower()
            oname = member.name
            oname = oname.lower()
            if dname.__contains__(f'{user}') or name == (f'{user}') or oname.__contains__(f'{user}'):
                u.append(f'{member.mention}')
                m.append(f'{member.id}')
        if len(u) == 1:# If it returns only 1 member
            pop = m.pop(0)
            user1 = ctx.guild.get_member(int(pop))
        elif len(u) == 0:# If it returns 0 members
            if user.startswith('<@') and user.endswith('>'):
                user1 = user.replace('<', '')
                user1 = user1.replace('>', '')
                user1 = user1.replace('!', '')
                user1 = user1.replace('@', '')
                user1 = ctx.guild.get_member(int(user1))
            else:
                try:
                    user1 = ctx.guild.get_member(int(user))
                except:
                    user1 = None
                    pass
            if user1 == None:
                embed = discord.Embed(title='OOPS! An error has occurred >.<', colour=discord.Colour(0xff0000), description='I can not find that user!')
                embed.set_author(name=f'{embed_user}', icon_url=f'{embed_user.avatar_url}')
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/678014140203401246.png?v=1")
                embed.set_footer(text='If you need help please do the -support command.')
                await ctx.send(embed=embed)
                return
        elif len(u) >= 10:
            embed = discord.Embed(title='OOPS! An error has occurred >.<', colour=discord.Colour(0xff0000), description='Too many users found. Please be more specific.')
            embed.set_author(name=f'{embed_user}', icon_url=f'{embed_user.avatar_url}')
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/678014140203401246.png?v=1")
            embed.set_footer(text='If you need help please do the -support command.')
            await ctx.send(embed=embed)
            return
        else:# If it returns more than 1 member
            a = ['1']
            users_list = []
            for item in u:
                num = len(a)
                a.append('f')
                users_list.append(f'{num}. {item}')
            users_len = len(users_list)
            users_list = '\n'.join(users_list)# -- -- -- ADD RESULT TEXT BELOW -- -- --
            embed = discord.Embed(title='Multiple Members Found!', colour=discord.Colour(7506394), description=f'Please type the number that corresponds to the member you want to make the ticket owner.\n{users_list}')
            embed.set_author(name=f'{embed_user}', icon_url=f'{embed_user.avatar_url}')
            msg2 = await ctx.send(embed=embed)
            try:
                msg = await self.bot.wait_for('message', check=check, timeout=60.0)
            except asyncio.TimeoutError:
                return await ctx.send('<:redx:678014058590502912> You took too long to answer the question!')
            if len(failn) >= 1:
                msg1 = int(msg.content)
                popnum = msg1 - 1
                user2 = m.pop(popnum)
                user1 = ctx.guild.get_member(int(user2))
            elif len(faily) >= 1:
                return await ctx.send(f'<:redx:678014058590502912> Invalid Number.')
        # STARTING BLACKLIST CHECK
        blacklisted = False
        for x in ticket_blacklist:
            if x['id'] == user1.id:
                blacklisted = True
        if user1.bot == True:
            return await ctx.send(f'<:redx:678014058590502912> You cannot transfer a Ticket to a Bot!')
        elif user1.id == tuser.id:
            return await ctx.send(f'<:redx:678014058590502912> That Person is already the Ticket Owner!')
        elif blacklisted == True and admin not in ctx_member.roles:
            return await ctx.send(f'<:redx:678014058590502912> You cannot Transfer Ticket Ownership to a Blacklisted User!')
        elif blacklisted == True and admin in ctx_member.roles:
            redx = self.bot.get_emoji(681610313485123602)
            check = self.bot.get_emoji(681610286444314668)
            def check_react(reaction, user_react):
                if ctx.author == user_react:
                    if reaction.emoji == check or reaction.emoji == redx:
                        return True
                    else:
                        return False
                else:
                    return False
            confirm_msg = await ctx.send(f':warning: You are making a Blacklisted User the Ticket Owner.\nAre you sure you want to continue?')
            await confirm_msg.add_reaction(check)
            await confirm_msg.add_reaction(redx)
            try:
                reaction, user_react = await self.bot.wait_for('reaction_add', timeout=120.0, check=check_react)
            except asyncio.TimeoutError:
                return await ctx.author.send('<:redx:678014058590502912> You took too long to react to the message!')
            else:
                if reaction.emoji == check:
                    await confirm_msg.delete()
                elif reaction.emoji == redx:
                    await ctx.send('<:check:678014104111284234> Not adding them to the Ticket.', delete_after=5)
                    await confirm_msg.delete()
                    await starting_msg.delete()
                    try:
                        await msg2.delete()
                        await msg.delete()
                    except:
                        pass
                    return
        await ctx.channel.set_permissions(user1, read_messages=True, send_messages=True, manage_messages=False, reason=f'{ctx.author} ({ctx.author.id}) - Transferring Ticket Ownership')
        if NotInServer == False:
            await ctx.channel.set_permissions(tuser, read_messages=True, send_messages=None, manage_messages=None, reason=f'{ctx.author} ({ctx.author.id}) - Transferring Ticket Ownership')
            if tuser.id != ctx.author.id:
                await tuser.send(f':pencil: Your Ticket ({ctx.channel.mention}) was transferred to **{user1.display_name}**')
        elif user1.id != ctx.author.id:
            await user1.send(f'<:OwnerCrown:507003242249584641> You\'ve are now the owner of {ctx.channel.mention}!')
        await ctx.channel.edit(topic=f'USERID: {user1.id}', name=f'ticket-{user1.display_name}', reason=f'{ctx.author} ({ctx.author.id}) - Transferring Ticket Ownership')
        await ctx.send(f'<:check:678014104111284234> **{ctx_member.display_name}** Transferred Ticket Ownership from {tuser.display_name} to **{user1.display_name}**')
        await starting_msg.delete()
        try:
            await msg2.delete()
            await msg.delete()
        except:
            pass

    @commands.command(aliases=['deletet', 'ticketdelete', 'deleteticket', 'dticket'])
    @commands.guild_only()
    @rank('admin')
    async def tdelete(self, ctx, *, reason=None):
        """ Delete a Ticket """
        ticket_owner = ctx.channel.topic
        ticket_owner = ticket_owner.replace('USERID: ', '')
        archive = ctx.guild.get_channel(729813211704066169)
        tuser = self.bot.get_user(int(ticket_owner))
        member = ctx.guild.get_member(ctx.author.id)
        await ctx.channel.last_message.delete()
        if reason == None:
            def check_msg(m):
                if ctx.author == m.author and ctx.channel == m.channel:
                    return True
                else:
                    return False
            m1 = await ctx.send('What\'s the reason for deleting the ticket?')
            try:
                m2 = await self.bot.wait_for('message', check=check_msg, timeout=60.0)
            except asyncio.TimeoutError:
                return await ctx.send('<:redx:678014058590502912> You took too long to answer the question!')
            reason = m2.content
            await m1.delete()
            await m2.delete()
            if reason.lower() == 'cancel':
                return await ctx.send('<:redx:678014058590502912> Canceled Deleting the Support Ticket.')
        msg = []
        async for message in ctx.channel.history():
            if message.content == '':
                content = 'Content Unavailable (Embed/File)'
            else:
                content = message.content
            msg.append(f"[{message.created_at}] {message.author} - {content}")
        msg.reverse()
        file = discord.File(BytesIO(("\n".join(msg)).encode("utf-8")), filename=f"{ctx.channel.name}.txt")
        try:
            await tuser.send(f'Your ticket ({ctx.channel.name}) has been deleted by **{member.display_name}** with reason **{reason}**\nThe Chat Log is Attached Below.', file=file)
        except:
            await ctx.send(f'{tuser.mention} your ticket has been deleted by {member.display_name} with reason {reason}')
            msg.append(f'{tuser.mention} your ticket has been deleted by {member.display_name} with reason {reason}')
        file = discord.File(BytesIO(("\n".join(msg)).encode("utf-8")), filename=f"{ctx.channel.name}.txt")
        logschat = ctx.guild.get_channel(665427079881555978)
        await logschat.send(f'**{member.display_name}** Just Deleted **{ctx.channel.name}**!\n**Owner:** {tuser.mention} ({tuser.id})\n**Reason:** {reason}', file=file)
        await ctx.channel.delete(reason=f'{member.display_name} - Deleted Ticket with Reason {reason}')

def setup(bot):
    bot.add_cog(Ticket(bot))
