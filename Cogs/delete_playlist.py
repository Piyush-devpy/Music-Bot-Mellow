import discord
from discord.ext import commands

class playlistremover(commands.Cog):
    def __init__(self,bot:commands.bot):
        self.bot=bot
        self.playlist_col = bot.db.playlists

    @commands.command(aliases=["rp"])
    async def removeplaylist(self,ctx: commands.Context,*, name: str):
        result = await self.playlist_col.delete_one({
            "user_id":ctx.author.id,
            "playlist_name":name
        })

        if result.deleted_count > 0:
            embed= discord.Embed(
                description= f"➔ Playlisted Has Been Deleted Successfully:`{name}`",
                color=discord.Color.purple(),
            )
            embed.set_footer(
                text=f"Requested By: {ctx.author.display_name} | {ctx.author.top_role.name}",
                icon_url=ctx.author.display_avatar.url
            )
            await ctx.send(embed=embed) 
        else:
            embed= discord.Embed(
                description= f"➔ Playlist Not Found With Name:`{name}`",
                color=discord.Color.purple(),
            )
            embed.set_footer(
                text=f"Requested By: {ctx.author.display_name} | {ctx.author.top_role.name}",
                icon_url=ctx.author.display_avatar.url
            )   
            await ctx.send(embed=embed)      

async def setup(bot):
    await bot.add_cog(playlistremover(bot))               