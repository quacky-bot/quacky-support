import discord, json, time, asyncio
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
error_icon = 'https://cdn.discordapp.com/emojis/678014140203401246.png?v=1'

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
        suggest = data['suggest']
        for x in error:
            if x['id'] == ctx.author.id:
                error.remove(x)
        for a in donator:
            if a['id'] == ctx.author.id:
                donator.remove(a)
        if ctx.author.id in special:
            special.remove(ctx.author.id)
        if ctx.author.id in suggest:
            suggest.remove(ctx.author.id)

        with open('/root/Quacky/Files/badges.json', 'w') as f:
            json.dump(data, f, indent=4)
        guild = self.bot.get_guild()
        ctx_member = guild.get_member(ctx.author.id)
        await ctx.send('<:check:678014104111284234> Cleared your Quacky Data!\nIf you would like to sync your roles with your badges do `!rankupdate`')

    @commands.command()
    @commands.cooldown(1, 300.0, BucketType.user)
    async def sapply(self, ctx):
        """ Apple for Support Team (Promotion of Being Helper) """
        redx = self.bot.get_emoji(678014058590502912)
        check = self.bot.get_emoji(678014104111284234)
        guild = self.bot.get_guild(665378018310488065)
        application_channel = guild.get_channel(693938487216308284)
        support_team_role = guild.get_role(729735292734406669)
        member = guild.get_member(ctx.author.id)
        if support_team_role in member.roles:
            return await ctx.send('<:redx:678014058590502912> You\'re already a Support Team Member!')
        File = open('/root/Quacky/Files/misc.json').read()
        data = json.loads(File)
        if ctx.author.id not in data['sapply']:
            return await ctx.send('<:redx:678014058590502912> You\'re not eligible to apply for Support Team.')
        if ctx.guild is not None:
            embed = discord.Embed(title='OOPS! An error has occured >.<', colour=discord.Colour(0xff0000), description=f'This command can not be used in DMs!')
            embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            embed.set_thumbnail(url=f'{error_icon}')
            embed.set_footer(text='If you need help please do the -support command.')
            return await ctx.send(embed=embed)
        def check_msg(m):
            if ctx.author == m.author and ctx.guild is None:
                return True
            else:
                return False
        def check_react(reaction, user_react):
            if ctx.author == user_react:
                if reaction.emoji == check or reaction.emoji == redx:
                    return True
                else:
                    return False
            else:
                return False
        starting_msg = await ctx.author.send('Hello! Thanks for wanting to be a Quacky Bot Support Team Member!\nPlease answer all the questions truthfully and to the best of your ability.\nYou have 5 minutes to answer each quesiton.\nWhen you are ready react with <:check:678014104111284234>')
        await starting_msg.add_reaction(check)
        await starting_msg.add_reaction(redx)
        try:
            reaction, user_react = await self.bot.wait_for('reaction_add', timeout=300.0, check=check_react)
        except asyncio.TimeoutError:
            return await ctx.author.send('<:redx:678014058590502912>  Cancelling your application, because you took too long to react to the message!')
        else:
            if reaction.emoji == check:
                await ctx.author.send('Question 1: **Why do you want to be a support team member?**')
            elif reaction.emoji == redx:
                return await ctx.author.send('<:check:678014104111284234> Canceled Your Application.')
        try:
            msg1 = await self.bot.wait_for('message', check=check_msg, timeout=300.0)
        except asyncio.TimeoutError:
            return await ctx.author.send('<:redx:678014058590502912>  Cancelling your application, you took too long to answer the question!')
        await ctx.author.send(f'Question 2: **Do you have any past expierence in managing support tickets? If so, where?**')
        try:
            msg2 = await self.bot.wait_for('message', check=check_msg, timeout=300.0)
        except asyncio.TimeoutError:
            return await ctx.author.send('<:redx:678014058590502912>  Cancelling your application, you took too long to answer the question!')
        middle_msg = await ctx.author.send('**Section 2: Live Conversation**\nYou will go through a conversation with Quacky being someone that has opened a support ticket.\nThe "Expected Answers" are what the bot is going to respond to, but they are not always correct, redoing this application and replacing them with the "Expected Answers" will cause you to be removed from the staff team.\nA new ticket will occur when a new ticket embed message appears.\nIn all of these situations you are a Support Team Member, but only have the moderation permissions of a Helper.\nWhen you are ready react with <:check:678014104111284234>')
        await middle_msg.add_reaction(check)
        try:
            reaction, user_react = await self.bot.wait_for('reaction_add', timeout=300.0, check=check_react)
        except asyncio.TimeoutError:
            return await ctx.author.send('<:redx:678014058590502912>  Cancelling your application, because you took too long to react to the message!')
        embed = discord.Embed(title='Quacky Support', colour=discord.Colour(7506394), description=f'Hey {ctx.author.mention}! Thanks for making a support ticket.\nA Quacky Staff Member will respond to you as soon as possible.\nTopic: **Question**\nSubject: **how do i apply for staff**')
        await ctx.author.send(embed=embed)
        async with ctx.author.typing():
            await asyncio.sleep(3)
        await ctx.author.send(f'{ctx.author.mention} how do i apply for staff')
        try:
            msg3 = await self.bot.wait_for('message', check=check_msg, timeout=300.0)
        except asyncio.TimeoutError:
            return await ctx.author.send('<:redx:678014058590502912>  Cancelling your application, you took too long to reply to the message!')
        embed = discord.Embed(title='Quacky Support', colour=discord.Colour(7506394), description=f'Hey {ctx.author.mention}! Thanks for making a support ticket.\nA Quacky Staff Member will respond to you as soon as possible.\nTopic: **Report**\nSubject: **DM Advertising**')
        await ctx.author.send(embed=embed, content=f'{ctx.author.mention}')
        async with ctx.author.typing():
            await asyncio.sleep(3)
        await ctx.author.send(f'hi DuckMasterAl was dm advertising me')
        try:
            msg4 = await self.bot.wait_for('message', check=check_msg, timeout=300.0)
        except asyncio.TimeoutError:
            return await ctx.author.send('<:redx:678014058590502912>  Cancelling your application, you took too long to reply to the message!')
        await ctx.author.send(f'**Your Answer:** {msg4.content}\n**Expected Answer:** Ok <@478370481926438932>, could you please send proof of the user dm advertising?')
        async with ctx.author.typing():
            await asyncio.sleep(2)
            await ctx.author.send('Sure, 1 second.')
            await asyncio.sleep(10)
        await ctx.author.send(f'{ctx.author.mention} here you go https://quacky.js.org/files/support_example.png')
        try:
            msg5 = await self.bot.wait_for('message', check=check_msg, timeout=300.0)
        except asyncio.TimeoutError:
            return await ctx.author.send('<:redx:678014058590502912>  Cancelling your application, you took too long to reply to the message!')
        await ctx.author.send(f'**Your Answer:** {msg5.content}\n**Expected Answer:** Ok, I\'m contacting an moderator/admin about this.')
        embed = discord.Embed(title='Quacky Support', colour=discord.Colour(7506394), description=f'Hey {ctx.author.mention}! Thanks for making a support ticket.\nA Quacky Staff Member will respond to you as soon as possible.\nTopic: **Other**\nSubject: **ur bot suc**')
        await ctx.author.send(embed=embed)
        async with ctx.author.typing():
            await asyncio.sleep(3)
        await ctx.author.send('ur bot sux')
        try:
            msg6 = await self.bot.wait_for('message', check=check_msg, timeout=300.0)
        except asyncio.TimeoutError:
            return await ctx.author.send('<:redx:678014058590502912>  Cancelling your application, you took too long to reply to the message!')
        embed = discord.Embed(title='Quacky Support', colour=discord.Colour(7506394), description=f'Hey {ctx.author.mention}! Thanks for making a support ticket.\nA Quacky Staff Member will respond to you as soon as possible.\nTopic: **Question**\nSubject: **How do I setup a mod-log?**')
        await ctx.author.send(embed=embed)
        await ctx.author.send('**System:** You can just reply to this one instantly')
        try:
            msg7 = await self.bot.wait_for('message', check=check_msg, timeout=300.0)
        except asyncio.TimeoutError:
            return await ctx.author.send('<:redx:678014058590502912>  Cancelling your application, you took too long to reply to the message!')
        await ctx.author.send(f'Question 3: **Anything else you\'d like to add?**\n*Type "no" or "none" if you have no additional information you\'d like to add.*')
        try:
            msg8 = await self.bot.wait_for('message', check=check_msg, timeout=300.0)
        except asyncio.TimeoutError:
            return await ctx.author.send('<:redx:678014058590502912>  You took too long to answer the question!')
        else:
            embed_description = f'__**Question - Apply for Staff**__\n**Quacky:** how do i apply for staff\n**You:** {msg3.content}\n__**Report - DM Advertising**__\n**Quacky:** hi DuckMasterAl was dm advertising me\n**You:** {msg4.content}\n**Quacky:** Ok, here you go [Image](https://quacky.js.org/files/support_example.png)\n**You:** {msg5.content}\n__**Other - Your bot sucks**__\n**Quacky:** ur box sux\n**You:** {msg6.content}\n__**Question - How do I setup a mod-log?**__\n**You:** {msg7.content}'
            embed_confirm = discord.Embed(title='Quacky Staff Application', colour=discord.Colour(7506394), description=f'Your questions and answers are below.\n\n{embed_description}')
            embed_confirm.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            embed_confirm.set_footer(text=f'Note: Making False Applications can get you Demoted and/or Blacklisted!')
            embed_confirm.add_field(name=f'Why do you want to be a support team member?', value=f'{msg1.content}')
            embed_confirm.add_field(name=f'Do you have any past expierence in managing support tickets? If so, where?', value=f'{msg2.content}')
            if msg8.content.lower() == 'no' or msg8.content.lower() == 'none':
                embed_confirm.add_field(name=f'Anything else you\'d like to add?', value=f'No Additional Information Provided.\n*This will not show up on your application.*')
                noextrainfo = True
            else:
                embed_confirm.add_field(name=f'Anything else you\'d like to add?', value=f'{msg8.content}', inline=False)
                noextrainfo = False
            confirm_msg = await ctx.author.send(f'Are you sure you want to submit this application?\nBy Submitting this application you agree to the Quacky Application terms of service.\nThe terms of service can be found here: https://quacky-bot.github.io/staff/terms', embed=embed_confirm)
            await confirm_msg.add_reaction(check)
            await confirm_msg.add_reaction(redx)
        try:
            reaction, user_react = await self.bot.wait_for('reaction_add', timeout=600.0, check=check_react)
        except asyncio.TimeoutError:
            await application_channel.send(f'**{ctx.author}** just applied for Support Team but took too long to submit the application')
            return await ctx.author.send('<:redx:678014058590502912>  You took too long to react to the message!')
        else:
            if reaction.emoji == redx:
                await application_channel.send(f'**{ctx.author}** just applied for Support Team but canceled their submittion.')
                return await ctx.author.send('<:check:678014104111284234> Canceled the Application Submittion.')
        embed = discord.Embed(title='Quacky Staff Application', colour=discord.Colour(7506394), timestamp=member.joined_at, description=embed_description)
        embed.set_footer(text='Joined on')
        embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        embed.add_field(name=f'Why do you want to be a support team member?', value=f'{msg1.content}')
        embed.add_field(name=f'Do you have any past expierence in managing support tickets? If so, where?', value=f'{msg2.content}')
        if noextrainfo == False:
            embed.add_field(name=f'Anything else you\'d like to add?', value=f'{msg8.content}', inline=False)
        admin_msg = await application_channel.send(content=f'{ctx.author.name} just applied for Support Team (Promotion)!\n@everyone Vote using the reactions if {ctx.author.mention} should be promoted!', embed=embed)
        await admin_msg.add_reaction(check)
        await admin_msg.add_reaction(redx)
        await ctx.author.send(f'<:check:678014104111284234> Submitted your Application!\nYou will be DM\'d if your application is approved or denied.')
        data['sapply'].remove(ctx.author.id)
        with open('/root/Quacky/Files/misc.json', 'w') as f:
            json.dump(data, f, indent=4)

def setup(bot):
    bot.add_cog(Misc(bot))
