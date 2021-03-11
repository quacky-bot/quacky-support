import discord, json, asyncio, datetime, os
from discord.ext import commands, tasks

class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.giveaway_msg.start()
        self.leaderboard.start()

    def cog_unload(self):
        self.giveaway_msg.cancel()
        self.leaderboard.cancel()

    @tasks.loop(minutes=1.0)
    async def giveaway_msg(self):
        if self.bot.giveaway_over is False and datetime.datetime.now().day == 27:
            for x in self.bot.giveaway:# make sure ALL points are counted
                if x['dt'] is not None:
                    time_in_voice = datetime.datetime.strptime(datetime.datetime.now().strftime("%m/%d %H:%M"), "%m/%d %H:%M") - datetime.datetime.strptime(x['dt'], "%m/%d %H:%M")
                    minutes_in_voice = time_in_voice.seconds / 60
                    x['points'] += int(minutes_in_voice)
                    x['dt'] = datetime.datetime.now().strftime("%m/%d %H:%M")

            winner = sorted(self.bot.giveaway, key=lambda k: k['points'], reverse=True)[0]
            server = self.bot.get_guild(665378018310488065)
            channel = server.get_channel(665425563271561217)
            msg = await channel.fetch_message(812050910087348254)
            embed = msg.embeds[0]
            embed.color = discord.Color.red()
            embed.title = "Nitro Contest Ended"
            user = self.bot.get_user(winner['id'])
            embed.description = embed.description.split('\n\n')[0] + f"\n\n**Winner:** {user.mention}"
            await msg.reply(f'{user.mention} has won the contest with **{int(winner["points"])}** minutes <a:MagicTada:565978435357376523>\nDM <@443217277580738571> to claim your prize.', allowed_mentions=discord.AllowedMentions(users=True))
            await msg.edit(embed=embed)
            self.bot.giveaway_over = True

    @tasks.loop(hours=1.0)
    async def leaderboard(self):
        for x in self.bot.giveaway:# make sure ALL points are counted
            if x['dt'] is not None:
                time_in_voice = datetime.datetime.strptime(datetime.datetime.now().strftime("%m/%d %H:%M"), "%m/%d %H:%M") - datetime.datetime.strptime(x['dt'], "%m/%d %H:%M")
                minutes_in_voice = time_in_voice.seconds / 60
                x['points'] += int(minutes_in_voice)
                x['dt'] = datetime.datetime.now().strftime("%m/%d %H:%M")
            top3 = sorted(self.bot.giveaway, key=lambda k: k['points'], reverse=True)[0:3]
            embed_description = []
            emojis = [':first_place:', ':second_place:', ':third_place:']
            for x in top3:
                if emojis[0] == ':first_place:':
                    points = ''
                elif emojis[0] == ':second_place:':
                    points = f"- {top3[0]['points'] - x['points']} Behind"
                elif emojis[0] == ':third_place:':
                    points = f"- {top3[1]['points'] - x['points']} Behind"
                embed_description.append(f"{emojis.pop(0)} <@{x['id']}> {points}")

            server = self.bot.get_guild(665378018310488065)
            channel = server.get_channel(665425563271561217)
            msg = await channel.fetch_message(812395160985272390)
            embed = msg.embeds[0]
            embed.description = "\n".join(embed_description)
            embed.timestamp = datetime.datetime.now()
            await msg.edit(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def giveawayinfo(self, ctx):
        for x in self.bot.giveaway:
            if x['dt'] is not None:
                time_in_voice = datetime.datetime.strptime(datetime.datetime.now().strftime("%m/%d %H:%M"), "%m/%d %H:%M") - datetime.datetime.strptime(x['dt'], "%m/%d %H:%M")
                minutes_in_voice = time_in_voice.seconds / 60
                x['points'] += int(minutes_in_voice)
                x['dt'] = datetime.datetime.now().strftime("%m/%d %H:%M")
        await ctx.send(self.bot.get_user(sorted(self.bot.giveaway, key=lambda k: k['points'], reverse=True)[0]['id']).name)


    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if after.bot is True or before.activities == after.activities:
            return
        has_status = False
        for x in after.activities:
            if type(x) == discord.CustomActivity and x.name is not None and x.name.startswith('quacky.xyz'):
                has_status = True
                break
            elif type(x) == discord.CustomActivity:
                break
        for x in self.bot.giveaway:
            if x['id'] == after.id:
                if has_status is True and x['dt'] is None:
                    x['dt'] = datetime.datetime.now().strftime("%m/%d %H:%M")
                elif has_status is False and x['dt'] is not None:
                    time_in_voice = datetime.datetime.strptime(datetime.datetime.now().strftime("%m/%d %H:%M"), "%m/%d %H:%M") - datetime.datetime.strptime(x['dt'], "%m/%d %H:%M")
                    minutes_in_voice = time_in_voice.seconds / 60
                    x['points'] += int(minutes_in_voice)
                    x['dt'] = None
                break

    @commands.command()
    @commands.guild_only()
    async def signup(self, ctx):
        for x in self.bot.giveaway:
            if x['id'] == ctx.author.id:
                return await ctx.send('<:redx:678014058590502912> You\'ve already entered into the contest!\nIf you would like to opt-out of status logging, email `admin@quacky.xyz`')
        member = ctx.guild.get_member(ctx.author.id)
        dt = None
        for x in member.activities:
            if type(x) == discord.CustomActivity and x.name.startswith('quacky.xyz'):
                dt = datetime.datetime.now().strftime("%m/%d %H:%M")
                break
            elif type(x) == discord.CustomActivity:
                break
        self.bot.giveaway.append({"id": ctx.author.id, "points": 0, "dt": dt})
        await ctx.send('<:check:678014104111284234> I will now track your status for the contest.')

def setup(bot):
    bot.add_cog(Giveaway(bot))
