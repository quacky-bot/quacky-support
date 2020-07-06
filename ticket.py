import discord, random, logging, sys, traceback, os, asyncio
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord.ext.commands.cooldowns import BucketType
from time import sleep
from itertools import cycle

def is_owner():
    async def predicate(ctx):
        return ctx.author.id == 443217277580738571 or ctx.author.id == 519482266473332736
    return commands.check(predicate)

def is_in_guild(guild_id):
    async def predicate(ctx):
        return ctx.guild and ctx.guild.id == guild_id or ctx.author.id == 443217277580738571 or ctx.author.id == 519482266473332736
    return commands.check(predicate)

def is_user(user_id):
    async def predicate(ctx):
        return ctx.author.id == 443217277580738571 or ctx.author.id == user_id or ctx.author.id == 519482266473332736
    return commands.check(predicate)

def rank(rank):
    async def predicate(ctx):
        ticket_owner = ctx.channel.topic
        ticket_owner = ticket_owner.replace('USERID: ', '')
        helper = ctx.guild.get_role(690239278277591043)
        mod = ctx.guild.get_role(665423380207370240)
        ctx_member = ctx.guild.get_member(ctx.author.id)
        if rank == 'helper':
            if helper in ctx_member.roles or ticket_owner == str(ctx.author.id):
                return True
            else:
                return False
        elif rank == 'mod':
            if mod in ctx_member.roles or ticket_owner == str(ctx.author.id):
                return True
            else:
                return False
        elif rank == 'blacklist':
            pass
            # @todo Need to make a blacklist file for global and ticket blacklist via Quacky Support
            # if mod in ctx_member.roles or ticket_owner == str(ctx.author.id):
            #     return True
            # else:
            #     return False
        else:
            return False
    return commands.check(predicate)

class Ticket(commands.Cog):# @todo NEed to update all the commands with the check above, proper emojis, and proper roles/categories
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @rank('blacklist')
    async def new(self, ctx, *, subject=None):
        """ Create a Ticket!
        Ticket Categories are Report, Question, and Other. """
        ticket_blacklist = open('/root/Duckville/Files/ticket_blacklist.txt', 'r').read()
        ticket_blacklist = ticket_blacklist.split('\n')
        if str(ctx.author.id) in ticket_blacklist:
            await ctx.send(f'<:fancyx:681610313485123602> You are Blacklisted from Making Tickets!')
            return
        guild = self.bot.get_guild(581696157529407519)
        await ctx.channel.last_message.delete()
        duckville_helper = guild.get_role(671159224176345089)
        member1 = guild.get_member(ctx.author.id)
        category = self.bot.get_channel(702166396255338496)
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
                await ctx.send('<:fancyx:681610313485123602> You took too long to answer the question!')
                return
            subject = msg.content
            await m1.delete()
            await msg.delete()
            if subject.lower() == 'cancel':
                await ctx.send('<:fancyx:681610313485123602> Canceled Creating the Support Ticket.')
                return
        react_msg = await ctx.send(f'**Identify Your Ticket\'s Topic:**\n:bangbang: - Report\n:grey_question: - Server Question\n:newspaper: - Other\n<:fancyx:681610313485123602> - Cancel Your Ticket Creation')
        bangbang = '\U0000203c'
        news = '\U0001f4f0'
        question = '\U00002754'
        bug = '\U0001f41b'
        cancel_emoji = self.bot.get_emoji(681610313485123602)
        await react_msg.add_reaction(bangbang)
        await react_msg.add_reaction(question)
        await react_msg.add_reaction(news)
        await react_msg.add_reaction(cancel_emoji)
        def check_react(reaction, user_react):
            if ctx.author == user_react:
                if reaction.emoji == bangbang or reaction.emoji == question or reaction.emoji == news or reaction.emoji == cancel_emoji:
                    return True
                else:
                    return False
            else:
                return False
        try:
            reaction, user_react = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_react)
        except asyncio.TimeoutError:
            await ctx.send('<:fancyx:681610313485123602> You took too long to react to the message!')
            return
        else:
            if reaction.emoji == bangbang:
                m = []
                online = discord.Status.online
                for member in duckville_helper.members:
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
            elif reaction.emoji == cancel_emoji:
                await ctx.send(f'<:fancycheck:681610286444314668> Canceled the Ticket Making Process.', delete_after=10)
                await react_msg.delete()
                return
            await react_msg.delete()
        channel = await guild.create_text_channel(f'{ticket_prefix}-{member1.display_name}', category=category, reason=f'{ctx.author} - Ticket Creation', topic=f'USERID: {ctx.author.id}')
        await channel.set_permissions(guild.default_role, read_messages=False, reason=f'{ctx.author} - Ticket Creation')
        await channel.set_permissions(ctx.author, read_messages=True, send_messages=True, manage_messages=False, reason=f'{ctx.author} - Ticket Creation')
        await channel.set_permissions(duckville_helper, read_messages=True, send_messages=True, reason=f'{ctx.author} - Ticket Creation')#, manage_channel=True)
        embed = discord.Embed(title='Duckville Support', colour=discord.Colour(7506394), description=f'Hey {ctx.author.mention}! Thanks for making a support ticket.\nA duckville helper will respond to you as soon as possible.\nTopic: **{topic}**\nSubject: **{subject}**')
        embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        await channel.send(embed=embed)
        delcontent = await channel.send(f'{content}', delete_after=0.01)
        await ctx.send(f'<:fancycheck:681610286444314668> Created your Support Ticket --> {channel.mention}', delete_after=10)

    @commands.command()
    @commands.guild_only()
    async def close(self, ctx, *, reason=None):
        """ Close a Ticket """
        if ctx.channel.category_id != 702166396255338496:
            await ctx.send(f'<:fancyx:681610313485123602> You can only do this command in a Support Ticket.')
            return
        ticket_owner = ctx.channel.topic
        ticket_owner = ticket_owner.replace('USERID: ', '')
        archive = ctx.guild.get_channel(711227298157953035)
        tuser = self.bot.get_user(int(ticket_owner))
        dvhelper = ctx.guild.get_role(671159224176345089)
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
                await ctx.send('<:fancyx:681610313485123602> You took too long to answer the question!')
                return
            reason = m2.content
            await m1.delete()
            await m2.delete()
            if reason.lower() == 'cancel':
                await ctx.send('<:fancyx:681610313485123602> Canceled Closing the Support Ticket.')
                return
        if dvhelper in member.roles or ticket_owner == str(ctx.author.id):
            msg = await ctx.send(f'<a:Loading:540153374763384852> Sending the Message and Updating Permissions...')
            try:
                await tuser.send(f'Your ticket has been closed by **{member.display_name}** with reason **{reason}**\nYou can read the chat history here: {msg.jump_url}')
            except:
                await ctx.send(f'{tuser.mention} your ticket has been closed by {member.display_name} with reason {reason}', delete_after=5)
            await ctx.channel.edit(category=archive, reason=f'{ctx.author} - Ticket Close Command', sync_permissions=True, position=0)
            await ctx.channel.set_permissions(tuser, overwrite=overwrite)
            await msg.edit(content=f':lock: Ticket Closed by **{member.display_name}**\nReason: **{reason}**')
        else:
            await ctx.send('<:fancyx:681610313485123602> You don\'t have permission to do this command.')

    @commands.command()
    @commands.guild_only()
    async def add(self, ctx, *, user):
        """ Add Someone to a Ticket """
        if ctx.channel.category_id != 702166396255338496:
            await ctx.send(f'<:fancyx:681610313485123602> You can only do this command in a Support Ticket.')
            return
        ticket_owner = ctx.channel.topic
        ticket_owner = ticket_owner.replace('USERID: ', '')
        tuser = self.bot.get_user(int(ticket_owner))
        dvhelper = ctx.guild.get_role(671159224176345089)
        ctx_member = ctx.guild.get_member(ctx.author.id)
        starting_msg = ctx.channel.last_message
        if dvhelper in ctx_member.roles or ticket_owner == str(ctx.author.id):
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
                    embed = discord.Embed(title='OOPS! An error has occured >.<', colour=discord.Colour(0xff0000), description='I can not find that user!')
                    embed.set_author(name=f'{embed_user}', icon_url=f'{embed_user.avatar_url}')
                    embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/678014140203401246.png?v=1")
                    embed.set_footer(text='If you need help please do the -support command.')
                    await ctx.send(embed=embed)
                    return
            elif len(u) >= 10:
                embed = discord.Embed(title='OOPS! An error has occured >.<', colour=discord.Colour(0xff0000), description='Too many users found. Please be more specific.')
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
                    await ctx.send('<:fancyx:681610313485123602> You took too long to answer the question!')
                    return
                if len(failn) >= 1:
                    msg1 = int(msg.content)
                    popnum = msg1 - 1
                    user2 = m.pop(popnum)
                    user1 = ctx.guild.get_member(int(user2))
                elif len(faily) >= 1:
                    await ctx.send(f'<:fancyx:681610313485123602> Invalid Number.')
                    return
            if discord.PermissionOverwrite.is_empty(ctx.channel.overwrites_for(user1)) == False:
                await ctx.send('<:fancyx:681610313485123602> You can\'t add someone to the ticket if they\'ve already been added!')
                return
            try:
                await user1.send(f'<:join:659881573012865084> You\'ve been added to **{ctx.channel.mention}** by **{ctx.author.display_name}.**')
            except:
                pass
            await ctx.channel.set_permissions(user1, read_messages=True)
            await starting_msg.delete()
            try:
                await msg2.delete()
                await msg.delete()
            except:
                pass
            await ctx.send(f'<:fancycheck:681610286444314668> **{ctx_member.display_name}** added **{user1.display_name}** to the channel.')
        else:
            await ctx.send('<:fancyx:681610313485123602> You don\'t have permission to do this command.')

    @commands.command()
    @commands.guild_only()
    async def remove(self, ctx, *, user):
        """ Remove Someone from a Ticket """
        if ctx.channel.category_id != 702166396255338496:
            await ctx.send(f'<:fancyx:681610313485123602> You can only do this command in a Support Ticket.')
            return
        ticket_owner = ctx.channel.topic
        ticket_owner = ticket_owner.replace('USERID: ', '')
        tuser = self.bot.get_user(int(ticket_owner))
        tmember = ctx.guild.get_member(int(ticket_owner))
        dvhelper = ctx.guild.get_role(671159224176345089)
        ctx_member = ctx.guild.get_member(ctx.author.id)
        starting_msg = ctx.channel.last_message
        if dvhelper in ctx_member.roles or ticket_owner == str(ctx.author.id):
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
                    embed = discord.Embed(title='OOPS! An error has occured >.<', colour=discord.Colour(0xff0000), description='I can not find that user!')
                    embed.set_author(name=f'{embed_user}', icon_url=f'{embed_user.avatar_url}')
                    embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/678014140203401246.png?v=1")
                    embed.set_footer(text='If you need help please do the -support command.')
                    await ctx.send(embed=embed)
                    return
            elif len(u) >= 10:
                embed = discord.Embed(title='OOPS! An error has occured >.<', colour=discord.Colour(0xff0000), description='Too many users found. Please be more specific.')
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
                    await ctx.send('<:fancyx:681610313485123602> You took too long to answer the question!')
                    return
                if len(failn) >= 1:
                    msg1 = int(msg.content)
                    popnum = msg1 - 1
                    user2 = m.pop(popnum)
                    user1 = ctx.guild.get_member(int(user2))
                elif len(faily) >= 1:
                    await ctx.send(f'<:fancyx:681610313485123602> Invalid Number.')
                    return
            if user1 == tmember:
                return await ctx.send(f'<:fancyx:681610313485123602> You can\'t remove the Ticket Owner from the ticket!')
            elif dvhelper in user1.roles:
                return await ctx.send(f'<:fancyx:681610313485123602> You cannot remove a Duckville Helper from the Ticket!')
            elif user1.id == 235148962103951360 or user1.id == 681598966399369341 or user1.id == 534589798267224065 or user1.id == 356950275044671499:
                return await ctx.send(f'<:fancyx:681610313485123602> You cannot remove this bot. It has permission to see every channel.')
            elif discord.PermissionOverwrite.is_empty(ctx.channel.overwrites_for(user1)):
                return await ctx.send(f'<:fancyx:681610313485123602> {user1.display_name} hasn\'t been added to the Ticket!')
            await ctx.channel.set_permissions(user1, overwrite=None)
            await starting_msg.delete()
            try:
                await msg2.delete()
                await msg.delete()
            except:
                pass
            await ctx.send(f'<:fancycheck:681610286444314668> **{ctx_member.display_name}** removed **{user1.display_name}** from the channel.')
        else:
            await ctx.send('<:fancyx:681610313485123602> You don\'t have permission to do this command.')

    @commands.command()
    @commands.guild_only()
    async def rename(self, ctx, *, prefix):
        """ Rename a Ticket's Prefix """
        if ctx.channel.category_id != 702166396255338496:
            await ctx.send(f'<:fancyx:681610313485123602> You can only do this command in a Support Ticket.')
            return
        ticket_owner = ctx.channel.topic
        ticket_owner = ticket_owner.replace('USERID: ', '')
        tuser = self.bot.get_user(int(ticket_owner))
        tmember = ctx.guild.get_member(int(ticket_owner))
        dvhelper = ctx.guild.get_role(671159224176345089)
        ctx_member = ctx.guild.get_member(ctx.author.id)
        starting_msg = ctx.channel.last_message
        if dvhelper in ctx_member.roles:
            await ctx.channel.edit(name=f'{prefix}-{tmember.display_name}')
            await ctx.send(f'<:fancycheck:681610286444314668> **{ctx_member.display_name}** renamed the channel to **{ctx.channel.name}**')
            await starting_msg.delete()
        else:
            await ctx.send('<:fancyx:681610313485123602> You don\'t have permission to do this command.')

    @commands.command(aliases=['transferowner', 'ownertransfer'])
    @commands.guild_only()
    async def transfer(self, ctx, *, user):
        """ Make Someone Else the Ticket Owner of a Ticket """
        ticket_owner = ctx.channel.topic
        ticket_owner = ticket_owner.replace('USERID: ', '')
        tuser = self.bot.get_user(int(ticket_owner))
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
                embed = discord.Embed(title='OOPS! An error has occured >.<', colour=discord.Colour(0xff0000), description='I can not find that user!')
                embed.set_author(name=f'{embed_user}', icon_url=f'{embed_user.avatar_url}')
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/678014140203401246.png?v=1")
                embed.set_footer(text='If you need help please do the -support command.')
                await ctx.send(embed=embed)
                return
        elif len(u) >= 10:
            embed = discord.Embed(title='OOPS! An error has occured >.<', colour=discord.Colour(0xff0000), description='Too many users found. Please be more specific.')
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
                await ctx.send('<:fancyx:681610313485123602> You took too long to answer the question!')
                return
            if len(failn) >= 1:
                msg1 = int(msg.content)
                popnum = msg1 - 1
                user2 = m.pop(popnum)
                user1 = ctx.guild.get_member(int(user2))
            elif len(faily) >= 1:
                await ctx.send(f'<:fancyx:681610313485123602> Invalid Number.')
                return
        if user1.bot == True:
            return await ctx.send(f'<:fancyx:681610313485123602> You cannot transfer a Ticket to a Bot!')
        elif user1.id == tuser.id:
            return await ctx.send(f'<:fancyx:681610313485123602> That Person is already the Ticket Owner!')
        elif str(user1.id) in ticket_blacklist and dvhelper not in ctx_member.roles:
            return await ctx.send(f'<:fancyx:681610313485123602> You cannot Transfer Ticket Ownership to a Blacklisted User!')
        elif str(user1.id) in ticket_blacklist and dvhelper in ctx_member.roles:
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
                await ctx.author.send('<:fancyx:681610313485123602> You took too long to react to the message!')
                return
            else:
                if reaction.emoji == check:
                    await confirm_msg.delete()
                elif reaction.emoji == redx:
                    await ctx.send('<:fancycheck:681610286444314668> Not adding them to the Ticket.', delete_after=5)
                    await confirm_msg.delete()
                    await starting_msg.delete()
                    try:
                        await msg2.delete()
                        await msg.delete()
                    except:
                        pass
                    return
        await ctx.channel.set_permissions(user1, read_messages=True, send_messages=True, manage_messages=False, reason=f'{ctx.author} - Transferring Ticket Ownership')
        await ctx.channel.set_permissions(tmember, read_messages=True, send_messages=None, manage_messages=None, reason=f'{ctx.author} - Transferring Ticket Ownership')
        if tuser.id != ctx.author.id:
            await tuser.send(f'<a:NeonReachBlob:480163662263353376> Your Ticket ({ctx.channel.mention}) was transferred to **{user1.display_name}**')
        elif user1.id != ctx.author.id:
            await user1.send(f'<a:WiggleBlob:500388529881219092> You\'ve are now the owner of {ctx.channel.mention}.')
        await ctx.channel.edit(topic=f'USERID: {user1.id}', name=f'ticket-{user1.display_name}', reason=f'{ctx.author} - Transferring Ticket Ownership')
        await ctx.send(f'<:fancycheck:681610286444314668> **{ctx_member.display_name}** Transferred Ticket Ownership from {tmember.display_name} to **{user1.display_name}**')
        await starting_msg.delete()
        try:
            await msg2.delete()
            await msg.delete()
        except:
            pass

def setup(bot):
    bot.add_cog(Ticket(bot))
