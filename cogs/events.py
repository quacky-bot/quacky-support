import discord, json, asyncio, datetime, searching
from discord.ext import commands, tasks
error_icon = 'https://cdn.discordapp.com/emojis/678014140203401246.png?v=1'

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.activity_test.start()

    def cog_unload(self):
        self.activity_test.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        # (activity=discord.Game(name="a game"))
        # (activity=discord.Streaming(name="My Stream", url=my_twitch_url))
        # (activity=discord.Activity(type=discord.ActivityType.listening, name="a song"))
        # (activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"))
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Support Questions | !new'), status=discord.Status.online)
        print(f'"{self.bot.user.name}" is ready to use.')

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """ Runs Commands on Edit """
        if after.author.bot is True:
            return
        prefixes = commands.when_mentioned_or('!')(self.bot, after)
        if after.content.startswith(tuple(prefixes)):
            ctx = await self.bot.get_context(after)
            msg = await self.bot.invoke(ctx)

    @tasks.loop(minutes=30.0)
    async def activity_test(self):
        """ Sends the Results of Activity Tests """
        await self.bot.wait_until_ready()
        File = open('/home/container/Support/Files/misc.json').read()
        data = json.loads(File)
        if data['activity'] != []:
            if datetime.datetime.strptime(data['activity'][1], "%m/%d %H:%M") <= datetime.datetime.strptime(datetime.datetime.now().strftime("%m/%d %H:%M"), "%m/%d %H:%M"):
                guild = self.bot.get_guild(665378018310488065)
                channel = guild.get_channel(665426967692181514)
                msg = await channel.fetch_message(data['activity'][0])
                reaction = msg.reactions.pop(0)
                users = await reaction.users().flatten()
                role = guild.get_role(665423057430511626)
                role1 = guild.get_role(746145667029663785)
                failed = []
                for x in role.members:
                    if x.id == 443217277580738571 or x in role1.members:
                        pass
                    elif x not in users:
                        failed.append(f"{x.mention} ({x.id})")
                if failed == []:
                    embed = discord.Embed(title='Activity Test Results', description="Everyone Passed the [Activity Test]({msg.jump_url})", color=discord.Colour.blue())
                    embed.set_thumbnail(url="https://bongo-duck.elixi.re/i/ey3x.png?raw=1")
                else:
                    failed = '\n> '.join(failed)
                    embed = discord.Embed(title='Activity Test Results', description=f"The Following Staff Members Failed the [Activity Test:]({msg.jump_url})\n> {failed}", color=discord.Colour.red())
                msg1 = await channel.send(embed=embed)

                oembed = discord.Embed(title='Old Activity Test', description=f'This activity test has ended. [Results Message]({msg1.jump_url})', color=discord.Colour.dark_orange())
                oembed.set_thumbnail(url="https://quacky.elixi.re/i/fhvc.png?raw=1")
                await msg.edit(embed=oembed)
                await msg.unpin()
                await msg.clear_reactions()
                data['activity'] = []
                with open('/home/container/Support/Files/misc.json', 'w') as f:
                    json.dump(data, f, indent=2)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        if guild.id == 665378018310488065:
            # Doing Rank Check
            File = open('/home/container/Quacky/Files/badges.json').read()
            data = json.loads(File)
            rank = 0
            for a in data['donator']:
                if a['id'] == member.id:
                    rank = a['rank']
            PFile = open('/home/container/Quacky/Files/partner.json').read()
            pdata = json.loads(PFile)
            for x in pdata['server']:
                if x['owner'] == member.id:
                    partner = guild.get_role(741701822032379944)
                    await member.add_roles(partner, reason='Has Partner Badge')
            for x in pdata['bot']:
                if x['owner'] == member.id:
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
            File = open('/home/container/Quacky/Files/misc.json').read()
            data = json.loads(File)
            channel = guild.get_channel(665378018809741324)
            msg = await channel.send(f'<@&750436218755350568>, Welcome **{member.name}** to the Quacky Support Server <:Quacky:665378357021638656>', allowed_mentions=discord.AllowedMentions(roles=True))
            data['member'] = msg.id
            with open('/home/container/Quacky/Files/misc.json', 'w') as f:
                json.dump(data, f, indent=4)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        if guild.id == 665378018310488065:
            File = open('/home/container/Quacky/Files/partner.json').read()# PARTNER ALERTS
            data = json.loads(File)
            adminchat = guild.get_channel(665427384899600395)
            for x in data['bot']:
                if x['owner'] == member.id:
                    await adminchat.send(f'<a:siren:493542252891734016> {member} ({member.id}) just left while under Bot Partnership.')

            File = open('/home/container/Support/Files/misc.json').read()# DELETE CUSTOM ROLE
            data = json.loads(File)
            for x in data['roles']:
                if x['user'] == member.id:
                    role = guild.get_role(x['role'])
                    await role.delete()
                    data['roles'].remove(x)
                    with open('/home/container/Support/Files/misc.json', 'w') as f:
                        json.dump(data, f, indent=2)

            if member.bot == True or member.id == 475117152106446849:# LEFT SERVER ALERTS
                return
            channel = guild.get_channel(665378018809741324)
            File = open('/home/container/Quacky/Files/misc.json', 'r').read()
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
        File = open('/home/container/Quacky/Files/badges.json').read()
        data = json.loads(File)
        if booster in roles:
            y = {"id": after.id, "rank": 2}
            data['donator'].append(y)
            with open('/home/container/Quacky/Files/badges.json', 'w') as f:
                json.dump(data, f, indent=4)
            await after.add_roles(mvp, reason='Boosted the Quacky Support Server')
            await donatorchat.send(f'<:join:659881573012865084> {after.mention} is now a Booster!')
        elif booster in before.roles and booster not in after.roles:
            for x in data['donator']:
                if x.id == after.id:
                    data['donator'].remove(x)
            with open('/home/container/Quacky/Files/badges.json', 'w') as f:
                json.dump(data, f, indent=4)
            await after.remove_roles(mvp, reason='No longer Boosting the Quacky Support Server')
            await donatorchat.send(f'<a:RIPBlob:478001829397921824> {after.mention} is no longer a Booster!')
        if vip in roles or mvp in roles or mega in roles:
            await after.add_roles(donators, reason='Given a Donator Role')
            await donatorchat.send(f'<:join:659881573012865084> {after.mention} is now a Donator!')"""

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await searching.error_event(self, ctx, error)

def setup(bot):
    bot.add_cog(Events(bot))
