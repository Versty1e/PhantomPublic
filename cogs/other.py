import discord
from discord.ext import commands
from discord.utils import get
from discord import utils
import pymongo
from pymongo import MongoClient
import sys

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["ava", "psp"])
    @commands.guild_only()
    async def avatar(self, ctx, *, user: discord.Member = None):
        user = user or ctx.author
        embed=discord.Embed(title=f"{user.name}", description=f"[png]({user.avatar_url_as(size=1024, format='png')}) | [webp]({user.avatar_url_as(size=1024, format='webp')}) | [jpg]({user.avatar_url_as(size=1024, format='jpg')}) ")
        embed.set_image(url=f"{user.avatar_url_as(size=1024)}")
        await ctx.send(embed=embed)

    @commands.command(aliases=['commands'])
    async def help(self,ctx):
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
        embed=discord.Embed(color=0x49b800)
        embed.set_author(name="Հրամանների ցանկը", icon_url="https://images-ext-1.discordapp.net/external/6EA5GIAW189-8W-f6-zB2TinTdIXvjePfLAMBdXhcj0/%3Fsize%3D1024/https/cdn.discordapp.com/icons/816583329440596000/818fc05fcfc78f1709757fc95a2ac158.webp")
        embed.add_field(name=f"{cus_prefix}userinfo", value="Անդամի Մասին Որոշակի տեղեկություն", inline=False)
        embed.add_field(name=f"{cus_prefix}serverinfo", value="Սերվերի մասին որոշակի տեղեկություն", inline=False)
        embed.add_field(name=f"{cus_prefix}servericon", value="Սերվերի նկարը", inline=False)
        embed.add_field(name=f"{cus_prefix}avatar", value="Անդամի նկարը", inline=False)
        embed.add_field(name=f"{cus_prefix}about", value="Բոտի մասին տեղեկություն", inline=False)
        embed.add_field(name=f"{cus_prefix}prefix", value="Բոտի Պրեֆիքսը փոխելու համար", inline=False)
        embed.add_field(name=f"{cus_prefix}clear", value="Մաքրություն", inline=False)
        embed.set_footer(text="Help command", icon_url="https://images-ext-2.discordapp.net/external/6TYOvVFfy7POWp-ZrZxYw_E_l7odtNPhX8KDGFUaDpk/https/images-ext-1.discordapp.net/external/6EA5GIAW189-8W-f6-zB2TinTdIXvjePfLAMBdXhcj0/%253Fsize%253D1024/https/cdn.discordapp.com/icons/816583329440596000/818fc05fcfc78f1709757fc95a2ac158.webp")
        await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(Commands(bot))