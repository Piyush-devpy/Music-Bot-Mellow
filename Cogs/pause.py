import discord
from discord.ext import commands
import wavelink

class PauseCommand(commands.Cog):
    def __init__(self,bot:commands.bot):
        self.bot=bot

    @commands.command()
    async def pause(self,ctx:commands.Context):
        vc: wavelink.Player=ctx.voice_client

        await vc.pause(True)


        embed=discord.Embed(
            description="➔ Player Paused.",
            color=discord.Color.purple()
        )  
        embed.set_footer(
                text=f"Requested By: {ctx.author.display_name} | {ctx.author.top_role.name}",
                icon_url=ctx.author.display_avatar.url            
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(PauseCommand(bot))       