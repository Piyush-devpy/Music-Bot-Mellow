import discord
from discord.ext import commands
from Views.nowplayingview import NowPlayingView
import wavelink
import datetime

# Music Cog
class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Track Start Event
    @commands.Cog.listener()
    async def on_wavelink_track_start(
        self, payload: wavelink.TrackStartEventPayload
    ):
        player: wavelink.Player = payload.player
        track: wavelink.Track = payload.track
        seconds = track.length // 1000
        duration = str(datetime.timedelta(seconds=seconds))

        requester_id = getattr(track.extras, "requester_id", None)
        requester_name = "Unknown"
        top_role = "Unknown"
        member = None
        if requester_id:
            member = player.guild.get_member(requester_id)
            if member:
                requester_name = member.display_name
                top_role = member.top_role.name

        embed = discord.Embed(
            title="Now Playing",
            description=f"➔ Currently Playing: **{track.title}**\n",
            color=discord.Color.purple(),
        )
        embed.add_field(name="Duration:", value=f"`{duration}`", inline=True)
        embed.set_footer(
            text=f"Requested By: {requester_name} | {top_role}",
            icon_url=member.display_avatar.url if member else player.guild.me.display_avatar.url
        )
        if track.artwork:
            embed.set_thumbnail(url=track.artwork)

        # Send message in the channel where the play command was used
        channel = getattr(player, 'text_channel', player.guild.text_channels[0])
        try:
            view= NowPlayingView(player)
            message = await channel.send(embed=embed,view=view)
            player.now_playing_msg = message
        except discord.Forbidden:
            # Handle case where bot can't send to the channel
            pass

        if(payload.reason==wavelink.TrackEndReason.FINISHED and player.queue.mode == wavelink.QueueMode.normal and not player.queue.is_empty):
            await player.play(player.queue.get())
            

    # Track End Event
    @commands.Cog.listener()
    async def on_wavelink_track_end(
        self, payload: wavelink.TrackEndEventPayload
    ):
        player: wavelink.Player = payload.player

        if player.queue.mode == wavelink.QueueMode.loop:
            await player.play(payload.track)
        elif player.queue.mode == wavelink.QueueMode.loop_all:
            next_track=player.queue.get()
            await player.play(next_track)
        elif player.queue.mode == wavelink.QueueMode.normal:
            if not player.queue.is_empty:
                next_track =player.queue.get()
                await player.play(next_track)        

        # Remove old Now Playing message
        if hasattr(player, "now_playing_msg"):
            try:
                await player.now_playing_msg.delete()
            except discord.NotFound:
                pass



    # Play Command
    @commands.command(aliases=["p"])
    async def play(self, ctx: commands.Context, *, search: str):
        node = wavelink.Pool.get_node()
        if not node:
            return await ctx.send("No Lavalink nodes are currently available!")
        if not ctx.author.voice:
            embed = discord.Embed(
                description="➔ You must be in the same voice channel as me.",
                color=discord.Color.purple()
            )
            return await ctx.send(embed=embed)

        # Connect or reuse player
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(
                cls=wavelink.Player
            )
        else:
            vc: wavelink.Player = ctx.voice_client

        # Store the channel for later use in events
        vc.channel = ctx.author.voice.channel

        # Search tracks
        tracks = await wavelink.Playable.search(search)
        if not tracks:
            embed = discord.Embed(
                description="➔ No Track Found.",
                color=discord.Color.purple()
            )
            return await ctx.send(embed=embed)

        # Playlist
        if isinstance(tracks, wavelink.Playlist):
            for track in tracks.tracks:
                track.extras.requester_id = ctx.author.id
                await vc.queue.put_wait(track)

            # Use the last track for embed details
            track = tracks.tracks[-1] if tracks.tracks else None
            if track:
                embed = discord.Embed(
                    description=f"➔ Song Name: **{track.title}** playlist added",
                    color=discord.Color.purple()
                )
                embed.set_footer(
                    text=f"Requested By: {ctx.author.display_name} | {ctx.author.top_role.name}",
                    icon_url=ctx.author.display_avatar.url
                )
        else:
            track = tracks[0]
            track.extras.requester_id = ctx.author.id
            await vc.queue.put_wait(track)

            embed = discord.Embed(
                description=f"➔ Song Name: **{track.title}** added to queue",
                color=discord.Color.purple()
            )
            embed.set_footer(
                text=f"Requested By: {ctx.author.display_name} | {ctx.author.top_role.name}",
                icon_url=ctx.author.display_avatar.url
            )

        await ctx.send(embed=embed)

        if not vc.playing:
            await vc.play(vc.queue.get())

async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))