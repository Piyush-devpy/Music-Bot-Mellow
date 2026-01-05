import discord
from discord.ext import commands
from discord import app_commands
import time
import datetime
import psutil
import os

class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()
        self.developer_id = 1408107733621673984  
        self.db_limit_mb = 512.0 

    def get_uptime(self):
        delta = datetime.timedelta(seconds=int(time.time() - self.start_time))
        return str(delta)

    async def get_db_stats(self):
        try:
            # 1. Calculate DB Ping
            start = time.perf_counter()
            await self.bot.db.command('ping')
            end = time.perf_counter()
            db_ping = f"{round((end - start) * 1000)}ms"


            stats = await self.bot.db.command('dbStats')
            used_mb = stats['storageSize'] / (1024 * 1024)
            db_storage = f"{used_mb:.2f}MB / {self.db_limit_mb}MB"
            
            return db_ping, db_storage
        except Exception as e:
            print(f"DB Error: {e}")
            return "N/A", "Unknown"

    async def create_info_embed(self, ctx_or_interaction):
        # API Ping
        api_ping = round(self.bot.latency * 1000)

        #  DB Stats
        db_ping, db_storage = await self.get_db_stats()

        # System Stats (CPU/RAM)
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent

        # Handle Greeting
        user = ctx_or_interaction.user if isinstance(ctx_or_interaction, discord.Interaction) else ctx_or_interaction.author
        greeting = f" Hello, Developer!" 

        if user.id == self.developer_id:
            title=greeting
            description="""
            Espresso Yourself &
            Here Are The Latency's -"""
        else:
            title="Hello there,"
            description="""I am **MELLOW**.\n
              A music bot designed for you and your friends to enjoy premium features for free .
              I provide [**High-Quality**] audio and supports Youtube,Spotify and Soundcloud.
              My default prefix is `.`"""    

        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.purple(),
            timestamp=datetime.datetime.now()
        )

        # Organizational Layout
        embed.add_field(name=" API Latency", value=f"`{api_ping}ms`", inline=True)
        embed.add_field(name=" DB Ping", value=f"`{db_ping}`", inline=True)
        embed.add_field(name=" DB Storage", value=f"`{db_storage}`", inline=True)
        
        embed.add_field(name="CPU Usage", value=f"`{cpu_usage}%`", inline=True)
        embed.add_field(name=" RAM Usage", value=f"`{ram_usage}%`", inline=True)
        embed.add_field(name="Uptime", value=f"`{self.get_uptime()}`", inline=True)
   
        embed.add_field(name="Current Time", value=f"<t:{int(time.time())}:F>", inline=False)
        
        if self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)

        embed.set_footer(text="System Health: Stable")

        return embed

    @commands.hybrid_command(name="info", description="View technical statistics about the bot")
    async def info(self, ctx:commands.Context):
        embed = await self.create_info_embed(ctx)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(BotInfo(bot))    