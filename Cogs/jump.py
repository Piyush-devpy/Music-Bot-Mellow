import discord
from discord.ext import commands
import wavelink


class Jump(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="jump")
    async def jump(self, ctx: commands.Context, position: int):
        player: wavelink.Player = ctx.voice_client
        queue = player.queue


        if queue.is_empty:
            embed = discord.Embed(
                description=" The queue is empty.",
                color=discord.Color.purple()
            )
            embed.set_footer(
                text=f"Requested By: {ctx.author.display_name} | {ctx.author.top_role.name}",
                icon_url=ctx.author.display_avatar.url
            )
            return await ctx.send(embed=embed)


        if position < 1 or position > len(queue):
            embed = discord.Embed(
                description=f" Invalid position. Choose between **1** and **{len(queue)}**.",
                color=discord.Color.purple()
            )
            embed.set_footer(
                text=f"Requested By: {ctx.author.display_name} | {ctx.author.top_role.name}",
                icon_url=ctx.author.display_avatar.url
            )
            return await ctx.send(embed=embed)


        index = position - 1

        for _ in range(index):
            queue.get()

        await player.stop()  


        embed = discord.Embed(
            description=f" Jumped to song **#{position}** in the queue.",
            color=discord.Color.purple()
        )
        embed.set_footer(
            text=f"Requested By: {ctx.author.display_name} | {ctx.author.top_role.name}",
            icon_url=ctx.author.display_avatar.url
        )

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Jump(bot))
