import asyncio
import wavelink
import discord
from discord.ext import commands


class LoopSong(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=["repeat"])
    async def loop(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if not vc:
            return await ctx.send(
                embed=discord.Embed(
                    description="➔ You must be connected to a voice channel.",
                    color=discord.Color.purple()
                )
            )

        if not vc.current and vc.queue.is_empty:
            return await ctx.send(
                embed=discord.Embed(
                    description="➔ Queue is empty.",
                    color=discord.Color.purple()
                )
            )

        embed = discord.Embed(
            description=(
                "➔ Choose loop mode:\n"
                "**Current** → Loop current track\n"
                "**Queue** → Loop entire queue\n"
                "**Disable** → Disable the loop"
            ),
            color=discord.Color.purple()
        )
        embed.set_footer(
            text=f"Requested by {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url
        )
        await ctx.send(embed=embed)

        def check(m: discord.Message):
            return (
                m.author == ctx.author
                and m.channel == ctx.channel
                and m.content.lower() in ("current", "queue","disable")
            )

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=15)
        except asyncio.TimeoutError:
            return await ctx.send(
                embed=discord.Embed(
                    description="➔ Session Timeout(15 sec).",
                    color=discord.Color.purple()
                )
            )

        choice = msg.content.lower()

        if choice == "current":
            vc.queue.mode = wavelink.QueueMode.loop
            desc = "➔ Loop enabled for **current track**."

        elif choice == "queue":
            vc.queue.mode = wavelink.QueueMode.loop_all
            desc = "➔ Loop enabled for **entire queue**."
        elif choice == "disable":
            vc.queue.mode == wavelink.QueueMode.normal
            desc = "➔ Loop Disabed"    

        embed = discord.Embed(description=desc, color=discord.Color.purple())
        embed.set_footer(
            text=f"Requested by {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url
        )
        embed.set_footer(
            text=f"Requested by {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url 

        )
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(LoopSong(bot))
