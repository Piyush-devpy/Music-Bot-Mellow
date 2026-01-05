import discord
from discord.ext import commands
import wavelink

class SkipCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def skip(self, ctx: commands.Context):
        player: wavelink.Player = ctx.voice_client

        if not player or not player.playing:
            return await ctx.send(
                embed=discord.Embed(
                    description="➔ Nothing is playing.",
                    color=discord.Color.purple()
                )
            )

        if player.queue.is_empty:
            await player.stop()
            return await ctx.send(
                embed=discord.Embed(
                    description="➔ No more songs in the queue.",
                    color=discord.Color.purple()
                )
            )

        next_track = player.queue.get()
        await player.play(next_track)

        embed = discord.Embed(
            description="➔ Skipped to next song.",
            color=discord.Color.purple()
        )
        embed.set_footer(
            text=f"Requested By: {ctx.author.display_name} | {ctx.author.top_role.name}",
            icon_url=ctx.author.display_avatar.url
        )

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(SkipCommand(bot))
