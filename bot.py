import discord
from discord.ext import commands
import os
import asyncio
import logging

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)

discord.utils.setup_logging()

discord.utils.setup_logging(level=logging.INFO, root=False)


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    await load()
    await bot.start('MTAzNDA4MTMxNTk5MTA4MDk5MA.GdAyfJ.qKXeRnK7gUjIgscb_t2L3Th1PDB5GxPBke_fGo')

asyncio.run(main())
