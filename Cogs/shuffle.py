import discord
from discord.ext import commands
import wavelink

class ShuffleCog(commands.Cog):
    def __init__(self,bot:commands.bot):
        self.bot=bot

    @commands.command()
    async def shuffle(self,ctx:commands.Context):
        vc:wavelink.Player=ctx.voice_client

        if len(vc.queue) < 2:
            embed =discord.Embed(
                description = "➔ Length Of Queue To Small To Shuffle.",
                color =discord.Color.purpe()
            )    
            embed.set_footer(
                text=f"Requested By: {ctx.author.display_name} | {ctx.author.top_role.name}",
                icon_url=ctx.author.display_avatar.url

            )
            return await ctx.send(embed=embed)
        

        vc.queue.shuffle()

        embed= discord.Embed(
            description="➔ The Queue Is Shuffled Successfully.",
            color=discord.Color.purple()
        )
        embed.set_footer(
                text=f"Requested By: {ctx.author.display_name} | {ctx.author.top_role.name}",
                icon_url=ctx.author.display_avatar.url
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ShuffleCog(bot))        