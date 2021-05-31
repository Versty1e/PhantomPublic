import discord
from discord import client
from discord.ext import commands
from discord.utils import get
from discord import utils
import pymongo
from pymongo import MongoClient
import os
import io

def get_prefix(bot, message):
    mongo_url = "Your mongodb code"
    cluster = MongoClient(mongo_url)
    db = cluster["servers"]
    collection = db["prefixes"]
    guild_id = message.guild.id

    gld_id = {"_id": guild_id}

    if collection.count_documents(gld_id) == 0:
        prefix_info = {"_id": guild_id, "Prefix": '!'}
        collection.insert_one(prefix_info)
    else:
        pfx = collection.find(gld_id)
        for prefix in pfx:
            cus_prefix = prefix["Prefix"]

        return cus_prefix

bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True)
bot.remove_command('help')

# Bot's status
@bot.event
async def on_ready():
    print(f'{bot.user} is connected')

    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=3, name=f'!help'))
    
    @bot.command(aliases=['botinfo'])
    async def about(ctx):
        embed=discord.Embed(color=0x00e66f)
        embed.set_author(name="Բոտի մասին տեղեկություն։", icon_url="https://cdn.discordapp.com/icons/816583329440596000/818fc05fcfc78f1709757fc95a2ac158.webp?size=1024")
        embed.add_field(name="Բոտի Անվանում։", value=f"{bot.user}", inline=True)
        embed.add_field(name="Բոտի Հեղինակ։", value="^ •IM Verstyle• ^#7858", inline=True)
        embed.add_field(name="Ծրագրավորման լեզու։", value="Python", inline=True)
        embed.add_field(name="Գրադարան։", value="Discord.py", inline=True)
        embed.add_field(name="Ստեղծվել  է:.", value=" 3 մարտի 2021 թ", inline=True)
        embed.add_field(name="Discord Խումբ:", value="[Մուտք](https://discord.gg/ZTDHRZaVbj)", inline=True)
        embed.add_field(name="Բոտի Հիմնական Պրեֆիքս:", value="!", inline=True)
        embed.set_footer(text = 'Made with 💖 with discord.py', icon_url = "https://www.python.org/static/opengraph-icon-200x200.png")
        await ctx.send(embed=embed)

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run('Your token')