import discord
from discord.ext import commands
import wavelink

class MusicJoin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=["j", "connect"])
    async def join(self, ctx: commands.Context):
        
        if not ctx.author.voice:
            embed=discord.Embed(
                    description="➔ You must be in a voice channel for me to join!",
                    color=discord.Color.purple()
                )
            embed.set_footer(
                     text=f"Requested By: {ctx.author.display_name} | {ctx.author.top_role.name}",
                     icon_url=ctx.author.display_avatar.url    

                )
            await ctx.send (embed=embed)    
            


        if ctx.voice_client:
            if ctx.voice_client.channel == ctx.author.voice.channel:
                return await ctx.send("➔ I am already in your voice channel!")
            else:

                embed=discord.Embed(
                        description=f"➔ I am already busy in {ctx.voice_client.channel.mention}.",
                        color=discord.Color.orange()
                    )
                embed.set_footer(
                     text=f"Requested By: {ctx.author.display_name} | {ctx.author.top_role.name}",
                     icon_url=ctx.author.display_avatar.url                        
                    )
                return await ctx.send(embed=embed)    
                


        try:

            await ctx.author.voice.channel.connect(cls=wavelink.Player)
            
            embed = discord.Embed(
                description=f"➔ Joined **{ctx.author.voice.channel.name}**",
                color=discord.Color.purple()
            )
            embed.set_footer(
                text=f"Requested By: {ctx.author.display_name} | {ctx.author.top_role.name}",
                icon_url=ctx.author.display_avatar.url

            )
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"An error occurred while joining:` {e}`")

async def setup(bot: commands.Bot):
    await bot.add_cog(MusicJoin(bot))