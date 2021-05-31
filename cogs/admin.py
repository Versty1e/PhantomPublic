import discord
from discord.ext import commands
from discord.utils import get
from discord import utils
import pymongo
from pymongo import MongoClient
import sys

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases = ['cl'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int, guild: discord.Guild = None):
        guild = ctx.guild if not guild else guild

        emb = discord.Embed(title='**Clear**', colour = 0x55ffee)
        await ctx.channel.purge(limit=amount + 1)

        emb.set_author(name=guild, icon_url=guild.icon_url)
        emb.set_thumbnail(url=self.bot.user.avatar_url)
        emb.set_footer(text='Ջնջվում են նամակները{}'.format(
            ctx.author.name), icon_url=ctx.author.avatar_url)

        mongo_url = "Your mongodb code"
        cluster = MongoClient(mongo_url)
        db = cluster["servers"]
        collection = db["command-channels"]
        guild_id = ctx.guild.id
        author = ctx.author
        gld_id = {"_id": guild_id}

        cmdch = collection.find(gld_id)
        for cmdchannel in cmdch:
            cur_channel = cmdchannel["Command_channel"]

        if collection.count_documents(gld_id) == 0:
            await ctx.send(embed = emb)
        else:
            channel = self.bot.get_channel( cur_channel )
            await channel.send( embed = emb)


    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(color=0xa20606)
            embed.set_author(name="Խնդրում ենք նշել քանակը (Օրինակ !clear 100)")
            await ctx.send(embed=embed)
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(color=0xa20606)
            embed.set_author(name="Դուք չունեք բավարար իրավունք այս հրամանը օգտագործոլու համար")
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Admin(bot))