import discord, json, asyncio, datetime
from discord.ext import commands, tasks
error_icon = 'https://cdn.discordapp.com/emojis/678014140203401246.png?v=1'

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # (activity=discord.Game(name="a game"))
        # (activity=discord.Streaming(name="My Stream", url=my_twitch_url))
        # (activity=discord.Activity(type=discord.ActivityType.listening, name="a song"))
        # (activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"))
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Support Questions | !new'), status=discord.Status.online)
        print(f'"{self.bot.user.name}" is ready to use.')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        if guild.id == 665378018310488065:
            # Doing Rank Check
            File = open('/root/Quacky/Files/badges.json').read()
            data = json.loads(File)
            rank = 0
            for a in data['donator']:
                if a['id'] == member.id:
                    rank = a['rank']
            PFile = open('/root/Quacky/Files/partner.json').read()
            pdata = json.loads(PFile)
            for x in pdata['server']:
                if x['owner'] == user1.id:
                    partner = guild.get_role(741701822032379944)
                    await member.add_roles(partner, reason='Has Partner Badge')
            for x in pdata['bot']:
                if x['owner'] == user1.id:
                    partner = guild.get_role(741701822032379944)
                    await member.add_roles(partner, reason='Has Partner Badge')
            if member.id in data['early_supporter']:
                early_supporter = guild.get_role(764569252111187988)
                await member.add_roles(early_supporter, reason='Has Early Supporter Badge')
            if member.id in data['bug_hunter']:
                bug_hunter = guild.get_role(761340790869065729)
                await member.add_roles(bug_hunter, reason='Has Bug Hunter Badge')
            if member.id in data['special']:
                special = guild.get_role(689520201259417682)
                await member.add_roles(special, reason='Has Special Badge')
            donator = guild.get_role(690234363648016443)
            if rank == 3:
                mega = guild.get_role(690234610462097504)
                await member.add_roles(mega, donator, reason='Has MEGA Badge')
            elif rank == 2:
                mvp = guild.get_role(690234421294530657)
                await member.add_roles(mvp, donator, reason='Has MVP Badge')
            elif rank == 1:
                vip = guild.get_role(665423079454801930)
                await member.add_roles(vip, donator, reason='Has VIP Badge')
            # Sending Join Message
            if member.bot == True or member.id == 475117152106446849:
                return
            File = open('/root/Quacky/Files/misc.json').read()
            data = json.loads(File)
            channel = guild.get_channel(665378018809741324)
            msg = await channel.send(f'<@&750436218755350568>, Welcome **{member.name}** to the Quacky Support Server <:Quacky:665378357021638656>', allowed_mentions=discord.AllowedMentions(roles=True))
            data['member'] = msg.id
            with open('/root/Quacky/Files/misc.json', 'w') as f:
                json.dump(data, f, indent=4)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        if guild.id == 665378018310488065:
            File = open('/root/Quacky/Files/partner.json').read()
            data = json.loads(File)
            adminchat = guild.get_channel(665427384899600395)
            for x in data['bot']:
                if x['owner'] == member.id:
                    await adminchat.send(f'<a:siren:493542252891734016> {member} ({member.id}) just left while under Bot Partnership.')
            if member.bot == True or member.id == 475117152106446849:
                return
            channel = guild.get_channel(665378018809741324)
            File = open('/root/Quacky/Files/misc.json', 'r').read()
            data = json.loads(File)
            File = data['member']
            msg = await channel.fetch_message(int(File))
            content = msg.content
            content = content.replace('<@&750436218755350568>, Welcome **', '')
            content = content.replace('** to the Quacky Support Server <:Quacky:665378357021638656>', '')
            if member.name == content:
                await msg.edit(content=f'~~{msg.content}~~ They left <a:RIPBlob:478001829397921824>')

    """@commands.Cog.listener()
    async def on_member_update(self, before, after):
        if after.guild.id != 665378018310488065 or before.roles == after.roles:
            return
        guild = self.bot.get_guild(665378018310488065)
        roles = after.roles
        booster = guild.get_role(736007066556039170)
        donators = guild.get_role(690234363648016443)
        mega = guild.get_role(690234610462097504)
        mvp = guild.get_role(690234421294530657)
        vip = guild.get_role(665423079454801930)
        donatorchat = guild.get_channel(665426877841670166)
        File = open('/root/Quacky/Files/badges.json').read()
        data = json.loads(File)
        if booster in roles:
            y = {"id": after.id, "rank": 2}
            data['donator'].append(y)
            with open('/root/Quacky/Files/badges.json', 'w') as f:
                json.dump(data, f, indent=4)
            await after.add_roles(mvp, reason='Boosted the Quacky Support Server')
            await donatorchat.send(f'<:join:659881573012865084> {after.mention} is now a Booster!')
        elif booster in before.roles and booster not in after.roles:
            for x in data['donator']:
                if x.id == after.id:
                    data['donator'].remove(x)
            with open('/root/Quacky/Files/badges.json', 'w') as f:
                json.dump(data, f, indent=4)
            await after.remove_roles(mvp, reason='No longer Boosting the Quacky Support Server')
            await donatorchat.send(f'<a:RIPBlob:478001829397921824> {after.mention} is no longer a Booster!')
        if vip in roles or mvp in roles or mega in roles:
            await after.add_roles(donators, reason='Given a Donator Role')
            await donatorchat.send(f'<:join:659881573012865084> {after.mention} is now a Donator!')"""

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.MissingRequiredArgument):
            command = self.bot.get_command(f'{ctx.command.name}')
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
            embed = discord.Embed(title='OOPS! An error has occurred >.<', colour=discord.Colour(0xff0000), description=f'{error}\n**Command Usage:** `{ctx.prefix}{ctx.command.name} {arguments}`')
            embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/678014140203401246.png?v=1")
            embed.set_footer(text='If you need help please do the -support command.')
            await ctx.send(embed=embed)
        elif isinstance(error, commands.ExtensionNotLoaded) or isinstance(error, commands.ExtensionAlreadyLoaded) or isinstance(error, commands.ExtensionFailed) or isinstance(error, commands.ExtensionNotFound) or isinstance(error, commands.BadArgument):
            embed = discord.Embed(title='OOPS! An error has occurred >.<', colour=discord.Colour(0xff0000), description=f'{error}')
            embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            embed.set_thumbnail(url=f'{error_icon}')
            embed.set_footer(text='If you need help please do the -support command.')
            try:
                await ctx.send(embed=embed)
            except:
                try:
                    await ctx.send(f':bangbang: An error has occurred!\n{error}\n*Please give me the `Embed Links` Permission for more Information*')
                except:
                    pass
        elif isinstance(error, commands.CommandOnCooldown):
            if ctx.author.id == 443217277580738571 or ctx.author.id == 344509223360659457:
                ctx.command.reset_cooldown(ctx)
                return await ctx.reinvoke()
            embed = discord.Embed(title='Slow Down!', colour=discord.Colour(0xff0000), description=f'{error}')
            embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            embed.set_thumbnail(url=f'{error_icon}')
            embed.set_footer(text='If you need help please do the -support command.')
            after_cd = discord.Embed(title='Slow Down!', colour=discord.Colour(4886754), description=f'You can now run `{ctx.prefix}{ctx.command}`, {ctx.author.mention}!')#.retry_after
            after_cd.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            after_cd.set_footer(text='If you need help please do the -support command.')
            try:
                msg = await ctx.send(embed=embed)
                await asyncio.sleep(error.retry_after)
                await msg.edit(content=f'{ctx.author.mention}', embed=after_cd)
            except:
                try:
                    await ctx.send(f':bangbang: Slow Down!\n{error}\n*Please give me the `Embed Links` Permission for more Information*')
                except:
                    pass
        elif isinstance(error, commands.NoPrivateMessage):
            embed = discord.Embed(title='OOPS! An error has occurred >.<', colour=discord.Colour(0xff0000), description=f'This command can not be used in DMs!')
            embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            embed.set_thumbnail(url=f'{error_icon}')
            embed.set_footer(text='If you need help please do the -support command.')
            try:
                await ctx.send(embed=embed)
            except:
                try:
                    await ctx.send(f':bangbang: An error has occurred!\nThis command can not be used in DMs!\n*Please give me the `Embed Links` Permission for more Information*')
                except:
                    pass
        elif isinstance(error, commands.PrivateMessageOnly):
            embed = discord.Embed(title='OOPS! An error has occurred >.<', colour=discord.Colour(0xff0000), description=f'This command must be used in DMs!')
            embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            embed.set_thumbnail(url=f'{error_icon}')
            embed.set_footer(text='If you need help please do the -support command.')
            try:
                await ctx.send(embed=embed)
            except:
                try:
                    await ctx.send(f':bangbang: An error has occurred!\nThis command must be used in DMs!\n*Please give me the `Embed Links` Permission for more Information*')
                except:
                    pass
        elif isinstance(error, commands.MissingPermissions) or isinstance(error, commands.BotMissingPermissions):
            missing_perms = error.missing_perms
            if len(missing_perms) == 1:
                missing_perms = missing_perms.pop(0)
                s = ':'
                missing_perms = missing_perms.split('_')
                a = missing_perms.pop(0)
                b = missing_perms.pop(0)
                a = a.capitalize()
                b = b.capitalize()
                missing_perms = f'{a} {b}'
            elif len(missing_perms) == 2:
                a = missing_perms.pop(0)
                b = missing_perms.pop(0)
                a = a.split('_')
                a1 = a.pop(0)
                b1 = a.pop(0)
                a1 = a1.capitalize()
                b1 = b1.capitalize()
                a = f'{a1} {b1}'
                b = b.split('_')
                a2 = b.pop(0)
                b2 = b.pop(0)
                a2 = a2.capitalize()
                b2 = b2.capitalize()
                b = f'{a2} {b2}'
                missing_perms = f'{a} and {b}'
                s = 's:'
            elif len(missing_perms) == 3:
                a = missing_perms.pop(0)
                b = missing_perms.pop(0)
                c = missing_perms.pop(0)
                a = a.split('_')
                a1 = a.pop(0)
                b1 = a.pop(0)
                a1 = a1.capitalize()
                b1 = b1.capitalize()
                a = f'{a1} {b1}'
                b = b.split('_')
                a2 = b.pop(0)
                b2 = b.pop(0)
                a2 = a2.capitalize()
                b2 = b2.capitalize()
                b = f'{a2} {b2}'
                c = c.split('_')
                a3 = c.pop(0)
                b3 = c.pop(0)
                a3 = a3.capitalize()
                b3 = b3.capitalize()
                c = f'{a3} {b3}'
                missing_perms = f'{a}, {b}, and {c}'
                s = 's:'
            if isinstance(error, commands.BotMissingPermissions):
                who_error = 'I'
            elif isinstance(error, commands.MissingPermissions):
                who_error = 'You'
            embed = discord.Embed(title='OOPS! An error has occurred >.<', colour=discord.Colour(0xff0000), description=f'{who_error} do not have permission to do this command!\nMissing Permission{s} `{missing_perms}`')
            embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            embed.set_thumbnail(url=f'{error_icon}')
            embed.set_footer(text='If you need help please do the -support command.')
            try:
                await ctx.send(embed=embed)
            except:
                try:
                    await ctx.send(f':bangbang: An error has occurred!\n{who_error} do not have permission to do this command!\nMissing Permission{s} `{missing_perms}`\n*Please give me the `Embed Links` Permission for more Information*')
                except:
                    pass
        elif isinstance(error, commands.DisabledCommand):
            await ctx.send(f'<:redx:678014058590502912> This command is currently disabled!')
        elif isinstance(error, commands.CheckFailure):
            return await ctx.send(f'<:redx:678014058590502912>  {ctx.author.mention}, you don\'t have permission to use this command!')
        else:
            if ctx.author.id == 443217277580738571 or ctx.author.id == 475117152106446849: # Owner (including alt)
                embed = discord.Embed(title='OOPS! An error has occurred >.<', colour=discord.Colour(0xff0000), description=f'{error}')
                embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
                embed.set_thumbnail(url=f'{error_icon}')
                embed.set_footer(text='You are getting this message because you\'re a developer...', icon_url='https://cdn.discordapp.com/avatars/693075783220199514/bc15748197f8c6c3fbdd0d1779f11914.png')
                try:
                    await ctx.send(embed=embed)
                except:
                    try:
                        await ctx.author.send(embed=embed)
                        await ctx.send(f':bangbang: Check DMs!')
                    except:
                        pass
            else:
                quacky_guild = self.bot.get_guild(665378018310488065)
                error_channel = quacky_guild.get_channel(693497754621706290)
                if ctx.guild == None:
                    embed = discord.Embed(title=f'An Error Has Occurred!', description=f'Command: {ctx.prefix}{ctx.command}\nError Message: **{error}**\nUser: {ctx.author} ({ctx.author.id})\nGuild: DMs', color=16727552, timestamp=datetime.datetime.now())
                else:
                    embed = discord.Embed(title=f'An Error Has Occurred!', description=f'Command: {ctx.prefix}{ctx.command}\nError Message: **{error}**\nUser: {ctx.author} ({ctx.author.id})\nGuild: {ctx.guild} ({ctx.guild.id})\nChannel: {ctx.channel} ({ctx.channel.id})\n[Jump to Message]({ctx.message.jump_url})', color=16727552, timestamp=datetime.datetime.now())
                embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
                embed.set_footer(text=f'This bug was found')
                embed_bug = discord.Embed(title='You just found an Bug!', colour=discord.Colour(0xff0000), description=f'Hey {ctx.author.name}, you just found a Bug with Quacky!\nThis bug has been reported to the developers and you may get a reward for finding the bug!')
                embed_bug.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
                embed_bug.set_thumbnail(url=f'{error_icon}')
                embed_bug.set_footer(text='For more information please do the -support command.')
                try:
                    msg = await ctx.send(embed=embed_bug)
                    a = 1
                except discord.Forbidden:
                    try:
                        await ctx.send(f':bangbang: You just found a Quacky Bot Error!\nIt has been reported to a developer.\n*Please give me the `Embed Links` Permission for more Information*')
                        a = 0
                    except discord.Forbidden:
                        return
                await error_channel.send(f'<@443217277580738571> a bug with the `{ctx.command}` command has been found :bug:', embed=embed, allowed_mentions=discord.AllowedMentions(users=True))

def setup(bot):
    bot.add_cog(Events(bot))
