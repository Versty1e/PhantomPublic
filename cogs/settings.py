import discord
from discord.ext import commands
from discord.utils import get
from discord import utils
import sys

import pymongo
from pymongo import MongoClient

class SettingsCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['prefix'])
    @commands.has_permissions(administrator = True)
    async def setprefix(self, ctx, prefix, guild: discord.Guild = None):
        guild = ctx.guild if not guild else guild
        emb = discord.Embed(colour = 0x55ffee)
        await ctx.channel.purge(limit=1)
        mongo_url = "Your mongodb code"
        cluster = MongoClient(mongo_url)
        db = cluster["servers"]
        collection = db["prefixes"]
        guild_id = ctx.guild.id
        guild_prefix = prefix
        author = ctx.author

        gld_id = {"_id": guild_id}
        gld_prefix = {"Prefix": guild_prefix}

        if collection.count_documents({}) == 0:
            prefix_info = {"_id": guild_id, "Prefix": guild_prefix}
            collection.insert_one(prefix_info)

        if collection.count_documents(gld_id) == 0:
            prefix_info = {"_id": guild_id, "Prefix": guild_prefix}
            collection.insert_one(prefix_info)

        pfx = collection.find(gld_id)
        for prefix in pfx:
            cur_prefix = prefix["Prefix"]
            new_prefix = guild_prefix

        if cur_prefix is not None:
            collection.update({"_id": guild_id}, {"$set": {"Prefix": new_prefix}})
            emb.set_author(name ='Պրեֆիքս ի փոփոխում', icon_url = guild.icon_url)
            emb.add_field(name = "**Նոր Պրեֆիքս**", value = f"**{new_prefix}**")
            emb.set_footer(text=f"{author.name}", icon_url=author.avatar_url)
        elif cur_prefix == guild_prefix:
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Խնդիր**", value = f"**Ձեր սերվերի նախածանցն արդեն կա: ``{cur_prefix}``**")
            emb.set_footer(text=f"Հայցվել է փոխել {author.name}", icon_url=author.avatar_url)
        else:
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Խնդիր**", value = f"**Սխալ առաջացավ: Նորից փորձեք.**")
            emb.set_footer(text=f"Հայցվել է փոխել {author.name}", icon_url=author.avatar_url)

        collection = db["command-channels"]

        cmdch = collection.find(gld_id)
        for cmdchannel in cmdch:
            cur_channel = cmdchannel["Command_channel"]

        if collection.count_documents(gld_id) == 0:
            await ctx.send(embed = emb)
        else:
            channel = self.bot.get_channel( cur_channel )
            await channel.send( embed = emb)



    @setprefix.error
    async def setprefix_error( self, ctx, error ):
        if isinstance( error, commands.MissingRequiredArgument ):
            embed=discord.Embed(color=0xa80b0b)
            embed.set_author(name=f"{ ctx.author.name } Նոր Պրեֆիքս դնելու համար !prefix Ձեր Պրեֆիքսը։")
            await ctx.send(embed=embed)
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(color=0xa80b0b)
            embed.set_author(name=f"{ ctx.author.name } Դուք Չունեք Բավարար իրավունք հետեվյալ Հրամանը օգտագործելու համար")
            await ctx.send(embed=embed)
        if isinstance( error, commands.errors.BadArgument ):
            embed=discord.Embed(color=0xa80b0b)
            embed.set_author(name="սխալ եք գրել, փորձեք կրկին !prefix Ձեր Պրեֆիքսը")
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(SettingsCommands(bot))