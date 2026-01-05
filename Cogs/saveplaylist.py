import discord
import wavelink
from discord.ext import commands


class PlaylistSaver(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.playlist_col = bot.db.playlists

    @commands.command(aliases=["sp"])
    async def saveplaylist(self, ctx: commands.Context,*, name: str):
        vc: wavelink.Player = ctx.voice_client

        if not vc or vc.queue.is_empty:
            embed = discord.Embed(
                description="➔ The queue is empty.",
                color=discord.Color.purple()
            )
            embed.set_footer(
                text=f"Requested By: {ctx.author.display_name} | {ctx.author.top_role.name}",
                icon_url=ctx.author.display_avatar.url
            )
            return await ctx.send(embed=embed)

        # Collect song URLs
        song_urls = [track.uri for track in vc.queue]

        # Add currently playing song at the start
        if vc.current:
            song_urls.insert(0, vc.current.uri)

        # Save to database
        await self.playlist_col.update_one(
            {
                "user_id": ctx.author.id,
                "playlist_name": name
            },
            {
                "$set": {"songs": song_urls}
            },
            upsert=True
        )

        embed = discord.Embed(
            description=f"➔ Saved **{len(song_urls)}** Songs To Your Playlist: `{name}`",
            color=discord.Color.purple()
        )
        embed.set_footer(
                text=f"Requested By: {ctx.author.display_name} | {ctx.author.top_role.name}",
                icon_url=ctx.author.display_avatar.url
            )
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(PlaylistSaver(bot))
