import asyncio
import discord
from discord.ext import commands


def get_color_role(member):
    for role in member.roles:
        if role.color == member.color:
            return role

GUILD_ID = 215424443005009920

class Selfmanage:
    """A cog for managing yourself"""

    all_roles = [
        353019520983629824, 347689132908085248, 371251751564869632, 371251837946560533, 323409208584306700,
        373135777955315712, 373135762230607882
    ]
    legal = "Welcome to Waifu Worshipping, the home of all your lewd socialising needs! " \
            "Please make sure to read over #information and #rules to learn the essentials.\n" \
            "Also understand that due to the content of the server, all users are required to be over the age of 18.\n"\
            "By continuing with these questions, you confirm that you are of legal age.\n\n" \
            "**When you're ready to receive your roles, please reply with the following: **`begin`"
    questions = [
        ('Are you happy to receive messages from other users in the server?', 353019520983629824),
        ('Are you interested in being informed about all future server-wide events? (Movie nights, gaming events, and other fun activities)', 347689132908085248),
        ('Are you interested in seeing vanilla 18+ content? (Includes #hentai, #ecchi, #porn, #rule-34, #doujins #hentai-gifs)', 371251751564869632),
        ('Are you interetsed in seeing kink-related 18+ content? (Includes #anal, #feet, #femdom, #bondage, #petplay, #yuri, #yaoi, #trap, #futa, #tentacles, #furry)', 371251837946560533),
        ('Are you interested in seeing extreme 18+ content? (Includes #extreme, #ahegao, #forced)', 323409208584306700),
    ]

    def __init__(self, bot):
        self.bot = bot

    async def on_member_join(self, member):
        if member.guild.id == GUILD_ID:
            await self.questionare(member.guild, member)

    @commands.command()
    async def intro(self, ctx):
        guild = self.bot.get_guild(GUILD_ID) or ctx.guild
        if not guild:
            return
        if ctx.guild:
            await ctx.send(f'{ctx.author.mention} I sent you a DM!')
        await self.questionare(guild, guild.get_member(ctx.author.id))

    async def questionare(self, guild, member):
        roles_to_add = []
        await member.send(self.legal)
        try:
            await self.bot.wait_for('message',
                                    check=lambda m: m.content.lower() == 'begin' and m.author == member, timeout=300)
            for question, role in self.questions:
                if await self.ask_question(member, question):
                    roles_to_add.append(discord.utils.get(guild.roles, id=role))
            if await self.ask_question(member, "Are you currently in a relationship?"):
                if await self.ask_question(member, "Would you like to display you're taken?"):
                    roles_to_add.append(discord.utils.get(guild.roles, id=373135777955315712))
            else:
                if await self.ask_question(member, "Would you like to display you're single?"):
                    roles_to_add.append(discord.utils.get(guild.roles, id=373135762230607882))
        except asyncio.TimeoutError:
            await member.send('Sorry, you took too long to answer. Use `~intro` if you want to start over.')
        else:
            roles_to_add.append(discord.utils.get(guild.roles, id=373122164544765953))
            await member.remove_roles(*[discord.utils.get(guild.roles, id=x) for x in self.all_roles])
            await member.add_roles(*roles_to_add)
            await member.send('Thank you for answering, the appropriate roles have been assigned to you! If there are any issues, please contact a staff member and they will happily assist you.')

    async def ask_question(self, user, question):
        def check(m):
            return isinstance(m.channel, discord.DMChannel) and m.author == user and is_answer(m.content)

        def is_answer(c):
            return 'y' in c.lower() or 'n' in c.lower()

        await user.send(question+' `yes / no`')

        m = await self.bot.wait_for('message', check=check, timeout=120)
        if 'y' in m.content.lower():
            await m.add_reaction('✅')
            return True
        else:
            return False


def setup(bot):
    bot.add_cog(Selfmanage(bot))