import discord
from discord.ext import commands
from discord.utils import get
from discord import utils
import pymongo
from pymongo import MongoClient
import sys

class Other(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['server'])
    async def serverinfo(self,ctx):
        mongo_url = "Your mongodb code"
        cluster = MongoClient(mongo_url)
        db = cluster["servers"]
        collection = db["prefixes"]
        guild_id = ctx.guild.id
        guild_name = ctx.guild.name
        author = ctx.author
        gld_id = {"_id": guild_id}
        gld_name= {"_name": guild_name}

        pfx = collection.find(gld_id)
        for prefix in pfx:
            cus_prefix = prefix["Prefix"]
        embed = discord.Embed(title=f"{ctx.guild.name} Սերվերի մասին", color=discord.Color.green())
        embed.add_field(name="Ստեղծման ամսաթիվը", value=f"{ctx.guild.created_at}", inline=False)
        embed.add_field(name="Սերվերի Շրջան", value=f"{ctx.guild.region}", inline=False)
        embed.add_field(name="Սերվերի այդի", value=f"{ctx.guild.id}", inline=False)
        embed.add_field(name="Անդամների քանակ", value=f"{ctx.guild.member_count}")
        embed.add_field(name="Սերվերի Պրեֆիքս:", value=f"{cus_prefix}", inline=True)
        embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
        await ctx.send(embed=embed)

    @commands.command(aliases=["user", "usinfo"])
    @commands.guild_only()
    async def userinfo(self, ctx, *, user: discord.Member = None):
        user = user or ctx.author
        embed=discord.Embed()
        embed.set_author(name="Անդամի մասին որոշակի տեղեկություն։", icon_url=f"{user.avatar_url_as(size=1024)}")
        embed.set_thumbnail(url=f"{user.avatar_url_as(size=1024)}")
        embed.add_field(name="Անուն։", value=f"{user.name}", inline=False)
        embed.add_field(name="Այդի։", value=f"{user.id}", inline=False)
        embed.add_field(name="Ստեղծման ամսաթիվ։", value=f"{user.created_at}", inline=False)
        embed.add_field(name="Մուտք գործման ամսաթիվ։", value=f"{user.joined_at}", inline=False)
        await ctx.send(embed=embed)


    @userinfo.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send(f'{ ctx.author.name } Նշեք անդամին')

def setup(bot):
    bot.add_cog(Other(bot))