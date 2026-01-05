import discord
from discord.ext import commands
import psutil
import time
import wavelink

BOT_VERSION = "v2.0"

class Stats(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.start_time = time.time()

    @commands.command()
    async def stats(self, ctx: commands.Context):
        process = psutil.Process()
        used_memory = process.memory_info().rss / 1024 / 1024
        total_memory = psutil.virtual_memory().total / 1024 / 1024

        guilds = len(self.bot.guilds)
        users = sum(g.member_count or 0 for g in self.bot.guilds)

        players = sum(
            1 for vc in self.bot.voice_clients
            if isinstance(vc,wavelink.Player)
        )

        shard_id = ctx.guild.shard_id if ctx.guild else 0
        shard_count = self.bot.shard_count or 1

        embed = discord.Embed(color=discord.Color.purple())

        embed.add_field(
            name=" <:tool:1457402931006537819> Bot Stats:",
            value=(
                f"``` Version :: {BOT_VERSION}\n Guilds :: {guilds}\n Users :: {users}\n Players :: {players}\n Memory :: {used_memory:.0f}MB/{total_memory:.0f}MB```"
            ),
            inline=False
        )

        embed.add_field(
            name=" <:wifi:1457402861989400761> System:",
            value=(
                f"``` Shard :: {shard_id + 1}/{shard_count}\n Latency :: {round(self.bot.latency * 1000)}ms```\n"
            ),
            inline=False
        )

        embed.set_footer(
            text=f"Requested by {ctx.author}",
            icon_url=ctx.author.display_avatar.url
        )

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Stats(bot))
