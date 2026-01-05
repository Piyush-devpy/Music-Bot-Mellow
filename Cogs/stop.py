import discord
from discord.ext import commands
import wavelink

class StopCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def stop(self, ctx: commands.Context):
        player: wavelink.Player = ctx.voice_client

        if not player:
            return await ctx.send(
                embed=discord.Embed(
                    description="➔ I'm not connected to a voice channel.",
                    color=discord.Color.purple()
                )
            )

        if not player.playing:
            return await ctx.send(
                embed=discord.Embed(
                    description="➔ Nothing is playing.",
                    color=discord.Color.purple()
                )
            )

        # 🔴 ACTUALLY STOP THE PLAYER
        player.queue.clear()
        player.autoplay = wavelink.AutoPlayMode.disabled
        await player.stop()

        embed = discord.Embed(
            description="➔ Player stopped.",
            color=discord.Color.purple()
        )
        embed.set_footer(
            text=f"Requested By: {ctx.author.display_name} | {ctx.author.top_role.name}",
            icon_url=ctx.author.display_avatar.url
        )

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(StopCommand(bot))
