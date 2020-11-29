import discord, json, asyncio, searching
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

async def remove_reaction(payload):
    channel = payload.member.guild.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    await message.remove_reaction(payload.emoji, payload.member)

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_raw_reaction_add')
    async def reaction_ticket(self, payload):
        if payload.message_id != 776290458640580629:
            return
        File = open('/root/Support/Files/blacklist.json').read()# Blacklist Check
        data = json.loads(File)
        for x in data['ticket']:
            if x['id'] == payload.member.id:
                return await remove_reaction(payload)

        await remove_reaction(payload)
        dm = False
        try:
            msg1 = await payload.member.send('What is the Subject of your Support Ticket?')
        except:
            subject = 'Unknown'
        else:
            def check_msg(m):
                if payload.member.id == m.author.id and payload.member.dm_channel == m.channel:
                    return True
                else:
                    return False
            try:
                msg = await self.bot.wait_for('message', check=check_msg, timeout=300.0)
            except asyncio.TimeoutError:
                subject = 'Unknown'
                await msg1.edit(content=f'~~{msg1.content}~~\n:notepad_spiral: You took too long to respond to the Question!')
            else:
                dm = True
                subject = msg.content

        support_role = payload.member.guild.get_role(729735292734406669)
        category = payload.member.guild.get_channel(723971770289488013)
        channel = await payload.member.guild.create_text_channel(f'ticket-{payload.member.display_name}', category=category, reason=f'{payload.member} ({payload.member.id}) - Ticket Creation', topic=f'USERID: {payload.member.id}')
        await channel.set_permissions(payload.member.guild.default_role, read_messages=False, reason=f'{payload.member} ({payload.member.id}) - Ticket Creation')
        await channel.set_permissions(payload.member, read_messages=True, send_messages=True, manage_messages=False, reason=f'{payload.member} ({payload.member.id}) - Ticket Creation')
        await channel.set_permissions(support_role, read_messages=True, send_messages=True, reason=f'{payload.member} ({payload.member.id}) - Ticket Creation')
        embed = discord.Embed(title='Quacky Support', colour=discord.Colour.blurple(), description=f'Hey {payload.member.mention}! Thanks for making a support ticket.\nA Quacky Staff Member will respond to you as soon as possible.\nTopic: **Reaction Ticket**\nSubject: **{subject}**')
        embed.set_author(name=f'{payload.member}', icon_url=f'{payload.member.avatar_url}')
        await channel.send(embed=embed)
        if dm is True:
            await payload.member.send(f'<:check:678014104111284234> Created your Support Ticket --> {channel.mention}')
        await channel.send(payload.member.mention, delete_after=0.01, allowed_mentions=discord.AllowedMentions(users=True))

    @commands.command()
    @rank('blacklist')
    async def new(self, ctx, *, subject=None):
        """ Create a Ticket!
        Ticket Categories are Report, Question, and Other.
        To prevent spam, you can only make a ticket once every 5 minutes. """
        guild = self.bot.get_guild(665378018310488065)
        await ctx.message.delete()
        mod = guild.get_role(665423380207370240)
        support_role = guild.get_role(729735292734406669)
        admin = guild.get_role(665423523308634113)
        staff_role = guild.get_role(665423057430511626)
        member1 = guild.fetch_member(ctx.author.id)
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
            embed = discord.Embed(title='Quacky Support', colour=discord.Colour.blurple(), description=f'Hey {ctx.author.mention}! Thanks for making a support ticket.\nA Quacky Staff Member will respond to you as soon as possible.\nTopic: **{topic}**\nSubject: **{subject}**')
        elif staff_request == True:
            embed = discord.Embed(title='Quacky Staff Request', colour=discord.Colour.blurple(), description=f'Hey {ctx.author.mention}! Thanks for making a staff request ticket.\nA Quacky Admin will respond to you as soon as possible.\nTopic: **{topic}**\nSubject: **{subject}**')
        embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        await channel.send(embed=embed)
        delcontent = await channel.send(f'{content}', delete_after=0.01, allowed_mentions=discord.AllowedMentions(users=True))
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
        tuser = await self.bot.fetch_user(int(ticket_owner))
        member = ctx.guild.get_member(ctx.author.id)
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages = False
        overwrite.read_messages = True
        await ctx.message.delete()
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
        # I stole this from Moksej he's pretty cool --> https://github.com/TheMoksej
        msg_history = []
        async for message in ctx.channel.history():
            if message.content == '':
                content = 'Content Unavailable (Embed/File)'
            else:
                content = message.content
            msg_history.append(f"[{message.created_at}] {message.author} - {content}")
        msg_history.reverse()
        file = discord.File(BytesIO(("\n".join(msg_history)).encode("utf-8")), filename=f"{ctx.channel.name}.txt")
        msg = await ctx.send(f'<a:Loading:540153374763384852> Sending the Message and Updating Permissions...', file=file)
        try:
            await tuser.send(f'Your ticket has been closed by **{member.display_name}** with reason **{reason}**\nYou can read the chat history here: {msg.jump_url}')
        except discord.errors.HTTPException:
            await ctx.send(f'{tuser.mention} your ticket has been closed by {member.display_name} with reason {reason}', delete_after=5, allowed_mentions=discord.AllowedMentions(users=True))
        if ctx.channel.name.startswith(('staff-', 'break-')):
            await ctx.channel.edit(category=archive, reason=f'{ctx.author} ({ctx.author.id}) - Ticket Close Command', sync_permissions=False, position=0)
        else:
            await ctx.channel.edit(category=archive, reason=f'{ctx.author} ({ctx.author.id}) - Ticket Close Command', sync_permissions=True, position=0)
        await ctx.channel.set_permissions(tuser, overwrite=overwrite)
        await msg.edit(content=f':lock: Ticket Closed by **{member.display_name}**\nReason: **{reason}**')

    @commands.command(usage='<user>')
    @commands.guild_only()
    @rank('mod')
    async def add(self, ctx, *, member):
        """ Add Someone to a Ticket """
        if ctx.channel.category_id != 723971770289488013:
            return await ctx.send(f'<:redx:678014058590502912> You can only do this command in a Support Ticket.')
        user = await searching.user(self, ctx, 'add to the ticket', member)
        if isinstance(user, discord.Message):
            return
        ctx_member = ctx.guild.get_member(ctx.author.id)
        if discord.PermissionOverwrite.is_empty(ctx.channel.overwrites_for(user)) == False:
            return await ctx.send('<:redx:678014058590502912> You can\'t add someone to the ticket if they\'ve already been added!')
        await ctx.channel.set_permissions(user, read_messages=True)
        try:
            await user.send(f'<:join:659881573012865084> You\'ve been added to **{ctx.channel.mention}** by **{ctx_member.display_name}.**')
        except:
            pass
        await ctx.message.delete()
        await ctx.send(f'<:check:678014104111284234> **{ctx_member.display_name}** added **{user.display_name}** to the channel.')

    @commands.command(usage='<user>')
    @commands.guild_only()
    @rank('mod')
    async def remove(self, ctx, *, member):
        """ Remove Someone from a Ticket """
        if ctx.channel.category_id != 723971770289488013:
            return await ctx.send(f'<:redx:678014058590502912> You can only do this command in a Support Ticket.')
        user = await searching.user(self, ctx, 'remove from the ticket', member)
        if isinstance(user, discord.Message):
            return
        ticket_owner = ctx.channel.topic
        ticket_owner = ticket_owner.replace('USERID: ', '')
        tuser = await self.bot.fetch_user(int(ticket_owner))
        tmember = ctx.guild.get_member(int(ticket_owner))
        support = ctx.guild.get_role(729735292734406669)
        quacky_bot_role = ctx.guild.get_role(665409797885263882)
        ctx_member = ctx.guild.get_member(ctx.author.id)
        if user == tmember:
            return await ctx.send(f'<:redx:678014058590502912> You can\'t remove the Ticket Owner from the ticket!')
        elif support in user.roles:
            return await ctx.send(f'<:redx:678014058590502912> You cannot remove another Support Team Member from the Ticket!')
        elif quacky_bot_role in user.roles or user.id == 235148962103951360:
            return await ctx.send(f'<:redx:678014058590502912> You cannot remove this bot. It has permission to see every channel.')
        elif discord.PermissionOverwrite.is_empty(ctx.channel.overwrites_for(user)):
            return await ctx.send(f'<:redx:678014058590502912> {user.display_name} hasn\'t been added to the Ticket!')
        await ctx.channel.set_permissions(user, overwrite=None)
        await ctx.message.delete()
        await ctx.send(f'<:check:678014104111284234> **{ctx_member.display_name}** removed **{user.display_name}** from the channel.')

    @commands.command()
    @commands.guild_only()
    @rank('helper')
    async def rename(self, ctx, *, prefix):
        """ Rename a Ticket's Prefix """
        if ctx.channel.category_id != 723971770289488013:
            return await ctx.send(f'<:redx:678014058590502912> You can only do this command in a Support Ticket.')
        ticket_owner = ctx.channel.topic
        ticket_owner = ticket_owner.replace('USERID: ', '')
        tuser = await self.bot.fetch_user(int(ticket_owner))
        tmember = ctx.guild.get_member(int(ticket_owner))
        ctx_member = ctx.guild.get_member(ctx.author.id)
        await ctx.channel.edit(name=f'{prefix}-{tmember.display_name}')
        await ctx.send(f'<:check:678014104111284234> **{ctx_member.display_name}** renamed the channel to **{ctx.channel.name}**')
        await ctx.message.delete()

    @commands.command(aliases=['transferowner', 'ownertransfer'], usage='<user>')
    @commands.guild_only()
    @rank('mod')
    async def transfer(self, ctx, *, member):
        """ Make Someone Else the Ticket Owner of a Ticket """
        if ctx.channel.category_id != 723971770289488013:
            return await ctx.send(f'<:redx:678014058590502912> You can only do this command in a Support Ticket.')
        user = await searching.user(self, ctx, 'transfer the ticket to', member)
        if isinstance(user, discord.Message):
            return
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
        # STARTING BLACKLIST CHECK
        blacklisted = False
        for x in ticket_blacklist:
            if x['id'] == user.id:
                blacklisted = True
        if user.bot == True:
            return await ctx.send(f'<:redx:678014058590502912> You cannot transfer a Ticket to a Bot!')
        elif user.id == tuser.id:
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
                    return await ctx.message.delete()
        await ctx.channel.set_permissions(user, read_messages=True, send_messages=True, manage_messages=False, reason=f'{ctx.author} ({ctx.author.id}) - Transferring Ticket Ownership')
        if NotInServer == False:
            await ctx.channel.set_permissions(tuser, read_messages=True, send_messages=None, manage_messages=None, reason=f'{ctx.author} ({ctx.author.id}) - Transferring Ticket Ownership')
            if tuser.id != ctx.author.id:
                try:
                    await tuser.send(f':pencil: Your Ticket ({ctx.channel.mention}) was transferred to **{user.display_name}**')
                except discord.errors.HTTPException:
                    await ctx.send(f'{tuser.mention}, you no longer own {ctx.channel.name}. It was transfered to {user.display_name}.', delete_after=5)
        elif user.id != ctx.author.id:
            try:
                await user.send(f'<:OwnerCrown:507003242249584641> You\'ve are now the owner of {ctx.channel.mention}!')
            except discord.errors.HTTPException:
                await ctx.send(f'{user.mention}, you now own {ctx.channel.name}!', delete_after=5)
        await ctx.channel.edit(topic=f'USERID: {user.id}', name=f'ticket-{user.display_name}', reason=f'{ctx.author} ({ctx.author.id}) - Transferring Ticket Ownership')
        await ctx.send(f'<:check:678014104111284234> **{ctx_member.display_name}** Transferred Ticket Ownership from {tuser.display_name} to **{user.display_name}**')
        await ctx.message.delete()

    @commands.command(aliases=['deletet', 'ticketdelete', 'deleteticket', 'dticket'])
    @commands.guild_only()
    @rank('admin')
    async def tdelete(self, ctx, *, reason=None):
        """ Delete a Ticket """
        if ctx.channel.category_id != 723971770289488013:
            return await ctx.send(f'<:redx:678014058590502912> You can only do this command in a Support Ticket.')
        ticket_owner = ctx.channel.topic
        ticket_owner = ticket_owner.replace('USERID: ', '')
        archive = ctx.guild.get_channel(729813211704066169)
        tuser = await self.bot.fetch_user(int(ticket_owner))
        member = ctx.guild.get_member(ctx.author.id)
        await ctx.message.delete()
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
        # I stole this from Moksej he's pretty cool --> https://github.com/TheMoksej
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
        except discord.errors.HTTPException:
            await ctx.send(f'{tuser.mention} your ticket has been deleted by {member.display_name} with reason {reason}')
            msg.append(f'{tuser.mention} your ticket has been deleted by {member.display_name} with reason {reason}')
        file = discord.File(BytesIO(("\n".join(msg)).encode("utf-8")), filename=f"{ctx.channel.name}.txt")
        logschat = ctx.guild.get_channel(665427079881555978)
        await logschat.send(f'**{member.display_name}** Just Deleted **{ctx.channel.name}**!\n**Owner:** {tuser.mention} ({tuser.id})\n**Reason:** {reason}', file=file)
        await ctx.channel.delete(reason=f'{member.display_name} - Deleted Ticket with Reason {reason}')

    @commands.command()
    @commands.guild_only()
    @rank('admin')
    async def reopen(self, ctx):
        """ Reopen a Ticket """
        if ctx.channel.category_id != 729813211704066169:
            return await ctx.send(f'<:redx:678014058590502912> You can only do this command in a Closed Support Ticket.')
        ticket_owner = ctx.channel.topic
        ticket_owner = ticket_owner.replace('USERID: ', '')
        category = ctx.guild.get_channel(723971770289488013)
        tuser = self.bot.get_user(int(ticket_owner))
        member = ctx.guild.get_member(ctx.author.id)
        await channel.set_permissions(tuser, read_messages=True, send_messages=True, manage_messages=False, reason=f'{ctx.author} ({ctx.author.id}) - Reopen Ticket Command')
        await ctx.channel.edit(category=category, reason=f'{ctx.author} ({ctx.author.id}) - Reopen Ticket Command')
        await ctx.send(f':unlock: Ticket Reopened by **{member.display_name}**')
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(Ticket(bot))
