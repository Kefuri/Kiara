import aiohttp
from discord.ext import commands

import discord
import random

class Rng:
    """Random helpful commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['r'])
    async def random(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid subcommand passed')

    @random.command()
    async def cat(self, ctx):
        async with ctx.typing():
            await ctx.message.delete()
            async with aiohttp.ClientSession() as session:
                async with session.get('http://random.cat/meow') as r:
                    if r.status == 200:
                        js = await r.json()
                        await ctx.send(js['file'])

    @random.command()
    async def rps(self, ctx):
        await ctx.send(random.choice(['✊','✋','✌']))

    @commands.command()
    async def rps(self, ctx, user: discord.Member):
        m = await ctx.author.send('Pick one')
        for re in ['✊', '✋', '✌']:
            await m.add_reaction(re)
        reaction1, user1 = await self.bot.wait_for('reaction_add', check=lambda r, u: u.id == ctx.author.id and any(
            r.emoji == re for re in ['✊', '✋', '✌']))
        print(reaction1.emoji)
        m = await ctx.send(f'`{ctx.author.name}` 🤜 🤛 `{user.name}`')
        for re in ['✊', '✋', '✌']:
            await m.add_reaction(re)
        reaction2, user2 = await self.bot.wait_for('reaction_add', check=lambda r, u: u.id == user.id and any(
            r.emoji == re for re in ['✊', '✋', '✌']))
        await m.edit(content=f'`{user1.name}` {reaction1.emoji} {reaction2.emoji} `{user2.name}`')

    @commands.command(aliases=['8', '8b'])
    async def ball(self, ctx, *, question):
        chance = ["It is certain","It is decidedly so","Without a doubt","Yes definitely","You may rely on it",
                  "As I see it, yes","Most likely","Outlook good","Yes","Signs point to yes","Reply hazy try again",
                  "Ask again later","Better not tell you now","Cannot predict now","Concentrate and ask again",
                  "Don't count on it","My reply is no","My sources say no","Outlook not so good","Very doubtful"]
        await ctx.send(random.choice(chance))

def setup(bot):
    bot.add_cog(Rng(bot))
