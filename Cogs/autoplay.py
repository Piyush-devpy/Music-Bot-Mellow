import discord
from discord.ext import commands
import wavelink

class AutoPlayCommand(commands.Cog):
    def __init__(self,bot:commands.bot):
        self.bot=bot

    @commands.command(aliases=["ap"])
    async def autoplay(self,ctx:commands.Context):
        vc:wavelink.Player = ctx.voice_client    

        if vc.autoplay == wavelink.Autoplay.enabled:
            vc.autoplay = wavelink.AutoPlayMode.disabled
            status = "**➔ Disabled**"
        else:
            vc.autoplay = wavelink.AutoPlayMode.enabled
            status = "➔ Enabled"

        embed=discord.Embed(
            description=f"➔ Autoplay is {status}",
            color =discord.Color.purple()
        )    
        embed.set_footer(
                text=f"Requested By: {ctx.author.display_name} | {ctx.author.top_role.name}",
                icon_url=ctx.author.display_avatar.url
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AutoPlayCommand(bot))        