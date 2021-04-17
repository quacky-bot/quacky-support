import discord, json, time, asyncio, searching, aiohttp, tokens
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
error_icon = 'https://cdn.discordapp.com/emojis/678014140203401246.png?v=1'

def mod():
    async def predicate(ctx):
        bot = ctx.bot
        guild = bot.get_guild(665378018310488065)
        mod = guild.get_role(665423380207370240)
        admin = guild.get_role(665423523308634113)
        member = guild.get_member(ctx.author.id)
        if mod in member.roles or admin in member.roles:
            return True
        else:
            return False
    return commands.check(predicate)

def admin():
    async def predicate(ctx):
        return ctx.author.id == 345457928972533773 or ctx.author.id == 443217277580738571
    return commands.check(predicate)

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

    @commands.command()
    @commands.cooldown(1, 300.0, BucketType.user)
    async def sapply(self, ctx):
        """ Apply for Support Team (Promotion of Being Helper) """
        redx = self.bot.get_emoji(678014058590502912)
        check = self.bot.get_emoji(678014104111284234)
        guild = self.bot.get_guild(665378018310488065)
        application_channel = guild.get_channel(693938487216308284)
        support_team_role = guild.get_role(729735292734406669)
        member = await guild.fetch_member(ctx.author.id)
        if support_team_role in member.roles:
            return await ctx.send('<:redx:678014058590502912> You\'re already a Support Team Member!')
        File = open('/home/container/Quacky/Files/misc.json').read()
        data = json.loads(File)
        if ctx.author.id not in data['sapply']:
            return await ctx.send('<:redx:678014058590502912> You\'re not eligible to apply for Support Team.\nIf you are looking to apply for staff, use `-apply`')
        if ctx.guild is not None:
            embed = discord.Embed(title='OOPS! An error has occurred >.<', colour=discord.Colour(0xff0000), description=f'This command must be used in DMs!')
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
        await ctx.author.send(f'{ctx.author.mention} here you go https://quacky.elixi.re/i/z5il.png?raw=true')
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
            embed_description = f'__**Question - Apply for Staff**__\n**Quacky:** how do i apply for staff\n**You:** {msg3.content}\n__**Report - DM Advertising**__\n**Quacky:** hi DuckMasterAl was dm advertising me\n**You:** {msg4.content}\n**Quacky:** Ok, here you go [Image](https://quacky.elixi.re/i/z5il.png?raw=true)\n**You:** {msg5.content}\n__**Other - Your bot sucks**__\n**Quacky:** ur box sux\n**You:** {msg6.content}\n__**Question - How do I setup a mod-log?**__\n**You:** {msg7.content}'
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
        admin_msg = await application_channel.send(content=f'{ctx.author.name} just applied for Support Team (Promotion)!\n@everyone Vote using the reactions if {ctx.author.mention} should be promoted!', embed=embed, allowed_mentions=discord.AllowedMentions(everyone=True))
        await admin_msg.add_reaction(check)
        await admin_msg.add_reaction(redx)
        await ctx.author.send(f'<:check:678014104111284234> Submitted your Application!\nYou will be DM\'d if your application is approved or denied.')
        data['sapply'].remove(ctx.author.id)
        with open('/home/container/Quacky/Files/misc.json', 'w') as f:
            json.dump(data, f, indent=4)

    @commands.group(invoke_without_command=True)
    async def partner(self, ctx):
        """ A group of Partner Information Commands... """
        await ctx.send_help(ctx.command)

    @partner.command()
    async def terms(self, ctx):
        """ Parntership Terms """
        msg = """ Please confirm that you agree to following terms.
        By Partnering with Quacky you agree to these terms:
        > https://quacky.xyz/partner/terms """
        embed = discord.Embed(colour=discord.Colour(16750848), description=msg, title='Quacky Partner Terms')
        await ctx.send(embed=embed)

    @partner.command()
    @commands.guild_only()
    @admin()
    async def approve(self, ctx, *, member):
        """ Approve a Partnership Request """
        member = await searching.user(self, ctx, 'approve for bot parntership', member)
        if isinstance(member, discord.Message):
            return
        quacky_guild = self.bot.get_guild(665378018310488065)
        partner_role = quacky_guild.get_role(741701822032379944)
        await member.add_roles(partner_role, reason=f'{ctx.author} ({ctx.author.id}) - Approved Partnership')
        File = open('/home/container/Quacky/Files/badges.json').read()
        data = json.loads(File)
        data['partner'].append(member.id)
        with open('/home/container/Quacky/Files/badges.json', 'w') as f:
            json.dump(data, f, indent=2)
        await ctx.send(f'<:check:678014104111284234> Approved **{member.display_name}** as a Partner <a:atada:794605079616946197>')

    @partner.command()
    async def link(self, ctx):
        """ Show our Partnership Message """
        await ctx.send('You can find our partner message at: <https://quacky.xyz/partner.txt>')

    @partner.command()
    @commands.guild_only()
    @mod()
    async def done(self, ctx):
        """ Mark a Partner as Meeting Requirements """
        await ctx.message.delete()
        await ctx.send(f':notepad_spiral: **{ctx.author.name}** has marked the partnership as __Meeting Requirements__')

    @partner.command(aliases=['new'])
    @commands.guild_only()
    async def apply(self, ctx):
        """ Apply for a Server/Bot Partnership """
        def react_check(reaction, user):
            if ctx.author == user and reaction.emoji in ['\U0001f916', '\U0001f4e2']:
                return True
            return False
        try:
            msg = await ctx.author.send('Are you Partnering a Bot (:robot:) or a Server/Other Product (:loudspeaker:)?')
            await msg.add_reaction('\U0001f916')
            await msg.add_reaction('\U0001f4e2')
            await ctx.send(':mailbox_with_mail: Check your DMs!')
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=react_check)
            except asyncio.TimeoutError:
                return await ctx.author.send('<:redx:678014058590502912> You took too long to react to the message!')
        except:
            return await ctx.send('<:redx:678014058590502912> I cannot DM You!')
        def check_msg(m):
            if ctx.author == m.author and ctx.author.dm_channel == m.channel:
                return True
            else:
                return False
        embed = discord.Embed(title='Quacky Partnership Request', description=f'Thanks for wanting to Partner with Quacky!\nA Moderator will check if you meet the Partner Requirements soon.\nThen, an admin will review your product and approve/deny you.', color=discord.Colour.blurple())
        embed.set_author(name=str(ctx.author), icon_url=str(ctx.author.avatar_url))
        if reaction.emoji == '\U0001f916':
            await ctx.author.send('What is your Bot\'s User ID?')
            try:
                bot = await self.bot.wait_for('message', check=check_msg, timeout=300.0)
            except asyncio.TimeoutError:
                return await ctx.author.send('<:redx:678014058590502912> You took too long to answer the question!')
            try:
                bot = await self.bot.fetch_user(int(bot.content))
            except:
                return await ctx.author.send(f'<:redx:678014058590502912> That\'s not a valid userid!')
            if bot.bot is False:
                return await ctx.author.send(f'<:redx:678014058590502912> That\'s not a bot\'s userid!')
            embed.set_footer(text=str(f'{bot.name} | {bot.id}'), icon_url=str(bot.avatar_url))
        elif reaction.emoji == '\U0001f4e2':
            await ctx.author.send('What is your Server\'s Invite Link?')
            try:
                invite = await self.bot.wait_for('message', check=check_msg, timeout=300.0)
            except asyncio.TimeoutError:
                return await ctx.author.send('<:redx:678014058590502912> You took too long to answer the question!')
            try:
                invite = await self.bot.fetch_invite(invite.content)
            except discord.NotFound:
                return await ctx.author.send(f'<:redx:678014058590502912> That\'s not a valid invite!')
            embed.set_footer(text=str(f'{invite.guild.name} | discord.gg/{invite.code} ({invite.approximate_member_count} members)'), icon_url=str(invite.guild.icon_url))
        member = ctx.guild.get_member(ctx.author.id)
        support_role = ctx.guild.get_role(665423380207370240)
        category = ctx.guild.get_channel(723971770289488013)
        channel = await ctx.guild.create_text_channel(f'partner-{member.display_name}', category=category, reason=f'{ctx.author} ({ctx.author.id}) - Partner Ticket Creation', topic=f'USERID: {ctx.author.id}')
        await channel.set_permissions(ctx.guild.default_role, read_messages=False, reason=f'{ctx.author} ({ctx.author.id}) - Partner Ticket Creation')
        await channel.set_permissions(member, read_messages=True, send_messages=True, manage_messages=False, reason=f'{ctx.author} ({ctx.author.id}) - Partner Ticket Creation')
        await channel.set_permissions(support_role, read_messages=True, send_messages=True, reason=f'{ctx.author} ({ctx.author.id}) - Partner Ticket Creation')
        embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        msg1 = await channel.send(embed=embed)
        await ctx.author.send(f'<:check:678014104111284234> Please send your Invite Link (Bot Invite/Server Invite) in {channel.mention} for a Moderator to Review.')
        await channel.send(ctx.author.mention, delete_after=0.01, allowed_mentions=discord.AllowedMentions(users=True))

    @commands.command()
    async def privacy(self, ctx):
        """ Read Quacky Support's Privacy Policy """
        await ctx.send('You can view Quacky Support\'s Privacy Policy at <https://quacky.xyz/privacy/support>')

    @commands.command()
    async def phook(self, ctx, *, message):
        """ Send a Message in Promoted Services via a Webhook """
        await ctx.trigger_typing()
        guild = self.bot.get_guild(665378018310488065)
        member = guild.get_member(ctx.author.id)
        donator_role = guild.get_role(690234363648016443)
        channel = guild.get_channel(794660260103192596)
        if donator_role not in member.roles:
            return await ctx.send(f'<:redx:678014058590502912> You must be a donator in order to use this command!')
        elif ctx.channel.id != channel.id:
            return await ctx.send(f'<:redx:678014058590502912> This command can only be used in {channel.mention}!')
        data = {"content": message, "username": ctx.author.display_name, "avatar_url": ctx.author.avatar_url}
        async with aiohttp.ClientSession() as session:
            async with session.post(tokens.webhook, data=data) as r:
                if r.status == 204:
                    try:
                        await ctx.message.delete()
                    except:
                        pass

    @commands.command()
    async def crole(self, ctx, *, hexcode):
        """ Get a Custom Color Role (Donator Only) """
        await ctx.trigger_typing()
        guild = self.bot.get_guild(665378018310488065)
        member = guild.get_member(ctx.author.id)
        mega = guild.get_role(690234610462097504)
        community_figure = guild.get_role(801495865352781864)
        booster = guild.get_role(736007066556039170)
        if mega not in member.roles and community_figure not in member.roles and booster not in member.roles:
            return await ctx.send('<:redx:678014058590502912> You must be a MEGA Donator to use this command!\nYou can donate at: <https://quacky.xyz/donate>')
        try:
            hexcode = int(f'0x{hexcode}', 16)
        except ValueError:
            embed = discord.Embed(title='OOPS! An error has occurred >.<', colour=discord.Colour(0xff0000), description='That is not a Valid Hex Code!')
            embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            embed.set_thumbnail(url=f"{error_icon}")
            embed.set_footer(text='If you need help please do the -support command.')
            return await ctx.send(embed=embed)
        File = open('/home/container/Support/Files/misc.json').read()
        data = json.loads(File)
        for x in data['roles']:
            if x['user'] == ctx.author.id:
                role = guild.get_role(x['role'])
                await role.edit(colour=discord.Colour(hexcode), reason=f'{ctx.author} ({ctx.author.id}) - Custom Donator Role')
                return await ctx.send('<:check:678014104111284234> Updated your Donator Role!')
        role = await guild.create_role(name=f'{ctx.author.name} Custom Role', colour=discord.Colour(hexcode), reason=f'{ctx.author} ({ctx.author.id}) - Custom Donator Role')
        await member.add_roles(role, reason=f'{ctx.author} ({ctx.author.id}) - Custom Donator Role')
        boost_role = guild.get_role(736007066556039170)
        await role.edit(position=boost_role.position - 1, reason=f'{ctx.author} ({ctx.author.id}) - Custom Donator Role')
        data['roles'].append({'user': ctx.author.id, 'role': role.id})
        with open('/home/container/Support/Files/misc.json', 'w') as f:
            json.dump(data, f, indent=2)
        await ctx.send('<:check:678014104111284234> Created your Donator Role!')

    @crole.error
    async def crole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send("<:redx:678014058590502912> Please provide a hex code for your role colour")

    @commands.command()
    async def quota(self, ctx):
        """ Check your Suggestion Quota Status (Trial Staff Only) """
        guild = self.bot.get_guild(665378018310488065)
        member = guild.get_member(ctx.author.id)
        trial_staff = guild.get_role(780837048600625162)
        if trial_staff not in member.roles:
            return await ctx.send('<:redx:678014058590502912> You must be a Trial Staff Member to use this command!')

        File = open('/home/container/Quacky/Files/misc.json').read()
        data = json.loads(File)
        for x in data['trial_staff']:
            if x['id'] == ctx.author.id:
                return await ctx.send(f'You have made **{x["suggestions"]}/5** suggestions.\n:notepad_spiral: Some of these suggestions may not be approved yet, so your suggestion count may lower.')
        await ctx.send(':warning: You do not have a Staff Database File. Contact an administrator immediately.')

def setup(bot):
    bot.add_cog(Misc(bot))
