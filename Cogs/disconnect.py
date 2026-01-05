import discord
from discord.ext import commands
import wavelink

class BotDisconnect(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=["dc", "leave"])
    async def disconnect(self, ctx: commands.Context):
        vc: wavelink.Player | None = ctx.voice_client

        if not vc:

            embed=discord.Embed(
                    description="➔ I Am Not Connected To A Voice Channel.",
                    color=discord.Color.purple()
                )
            embed.set_footer(
                text=f"Requested By: {ctx.author.display_name} | {ctx.author.top_role.name}",
                icon_url=ctx.author.display_avatar.url

            )
            return await ctx.send(embed=embed)
                 
        vc.queue.clear()
        await vc.disconnect()  


        embed=discord.Embed(
                    description="➔ Bot Left The Voice Channel.",
                    color=discord.Color.purple()
            )
        embed.set_footer(
                text=f"Requested By: {ctx.author.display_name} | {ctx.author.top_role.name}",
                icon_url=ctx.author.display_avatar.url
        )
        return await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(BotDisconnect(bot))
