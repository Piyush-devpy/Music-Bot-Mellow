import discord
from discord.ext import commands
import wavelink

class AllTimeVc(commands.Cog):
    def __init__(self,bot:commands.bot):
        self.bot=bot
    

    @commands.command(aliases=["247"])
    async def alwayson(self,ctx:commands.Context):
        vc: wavelink.Player=ctx.voice_client

        if vc.inactive_timeout is None:
           vc.inactive_timeout=300
           status="Disabled"
        else:
           vc.inactive_timeout =None
           status="Enabled"  

        embed=discord.Embed(
            description=f"24/7 mode is not{status}",
            color= discord.Color.purple()
        )
        embed.set_footer(
                text=f"Requested By: {ctx.author.display_name} | {ctx.author.top_role.name}",
                icon_url=ctx.author.display_avatar.url            
        )   
        await ctx.send(embed=embed
        )

async def setup(bot):
    await bot.add_cog(AllTimeVc(bot))