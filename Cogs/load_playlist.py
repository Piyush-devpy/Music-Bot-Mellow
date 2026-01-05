import wavelink
import discord
import datetime
from discord.ext import commands

class playlistload(commands.Cog):
    def __init__(self,bot:commands.bot):
        self.bot = bot
        self.playlist_col = bot.db.playlists

    @commands.command(aliases=["lp"])
    async def loadplaylist(self, ctx: commands.Context, *,name: str):
        vc: wavelink.Player =ctx.voice_client

        if not vc:
            if ctx.author.voice:
                vc= await ctx.author.voice.channel.connect(cls=wavelink.Player)
                vc.channel=ctx.channel
            else:
                embed= discord.Embed(
                    description = "➔ Please Join A Voice Channel First.",
                    color = discord.Color.purple()
                )
                embed.set_footer(
                text=f"Requested By: {ctx.author.display_name} | {ctx.author.top_role.name}",
                icon_url=ctx.author.display_avatar.url
                )
                return await ctx.send(embed=embed)     

        playlist_data = await self.playlist_col.find_one({
            "user_id":ctx.author.id,
            "playlist_name": name
        })                   

        if not playlist_data:
            embed= discord.Embed(
                description = f"➔ Now Playlist Found With Name:{name}",
                color = discord.Color.purple()
            )
            embed.set_footer(
                text=f"Requested By: {ctx.author.display_name} | {ctx.author.top_role.name}",
                icon_url=ctx.author.display_avatar.url
            )
            return await ctx.send(embed=embed)
        
        songs= playlist_data.get("songs",[])
        if not songs:
            embed= discord.Embed(
                description = "➔ That Playlist Is Empty.",
                color= discord.Color.purple()
            )
            embed.set_footer(
                text=f"Requested By: {ctx.author.display_name} | {ctx.author.top_role.name}",
                icon_url=ctx.author.display_avatar.url
            )
            return await ctx.send(embed=embed)
        

        added_count = 0 
        for url in songs:
            try:
                search = await wavelink.Playable.search(url)
                if search:
                    track = search[0]
                    track.extras = {"requester_id": ctx.author.id}
                    await vc.queue.put_wait(track)
                    added_count += 1
            except Exception as e:
                print(f"➔ Error Loading Track: {e}")

        if not vc.playing:
            await vc.play(vc.queue.get())
            embed = discord.Embed(
                description = f"➔ Successfully Added **{added_count}** Tracks To The Queue",
                color= discord.Color.purple()
            )
            embed.set_footer(
                text=f"Requested By: {ctx.author.display_name} | {ctx.author.top_role.name}",
                icon_url=ctx.author.display_avatar.url
            )  
            return await ctx.send(embed=embed)      

async def setup(bot):
    await bot.add_cog(playlistload(bot))            