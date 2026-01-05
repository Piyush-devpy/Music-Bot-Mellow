import discord
from discord.ext import commands
import wavelink

class ResumeCommand(commands.Cog):
    def __init__(self,bot:commands.bot):
        self.bot=bot

    @commands.command()
    async def resume(self,ctx:commands.Context):
        vc: wavelink.Player=ctx.voice_client

        await vc.pause(False)


        embed=discord.Embed(
            description="➔ Player Resumed.",
            color=discord.Color.purple()
        )  
        embed.set_footer(
                text=f"Requested By: {ctx.author.display_name} | {ctx.author.top_role.name}",
                icon_url=ctx.author.display_avatar.url            
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ResumeCommand(bot))       