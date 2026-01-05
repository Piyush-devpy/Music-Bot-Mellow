import discord
import wavelink

class NowPlayingView(discord.ui.View):
    def __init__(self, player: wavelink.Player):
        super().__init__(timeout=None)
        self.player = player

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if (
            not interaction.user.voice
            or interaction.user.voice.channel != self.player.channel
        ):
            embed = discord.Embed(
                description="➔ You must be in my voice channel to use these buttons.",
                color=discord.Color.purple()
            )
            embed.set_footer(
                text=f"Requested By: {interaction.user.display_name} | {interaction.user.top_role.name}",
                icon_url=interaction.user.display_avatar.url
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return False
        return True

    @discord.ui.button(emoji="<:loop:1457374129815814267>", style=discord.ButtonStyle.gray)
    async def loop(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.player.queue.mode == wavelink.QueueMode.loop_all:
            self.player.queue.mode = wavelink.QueueMode.normal
            description = "➔ Loop Disabled."
        else:
            self.player.queue.mode = wavelink.QueueMode.loop_all
            description = "➔ Loop Enabled."

        embed = discord.Embed(
            description=description,
            color=discord.Color.purple()
        )
        embed.set_footer(
            text=f"Requested By: {interaction.user.display_name} | {interaction.user.top_role.name}",
            icon_url=interaction.user.display_avatar.url
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(emoji="<:shuffle:1457374066427301910>", style=discord.ButtonStyle.gray)
    async def shuffle(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.player.queue.shuffle()

        embed = discord.Embed(
            description="➔ Queue Shuffled.",
            color=discord.Color.purple()
        )
        embed.set_footer(
            text=f"Requested By: {interaction.user.display_name} | {interaction.user.top_role.name}",
            icon_url=interaction.user.display_avatar.url
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(emoji="<:videopausebutton:1457381783934074942>", style=discord.ButtonStyle.gray)
    async def pause_resume(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.player.paused:
            await self.player.pause(False)
            button.emoji = "<:videopausebutton:1457381783934074942>"
            description = "➔ Playback Resumed."
        else:
            await self.player.pause(True)
            button.emoji = "<:playbutton:1457382827367731483>"
            description = "➔ Playback Paused."

        embed = discord.Embed(
            description=description,
            color=discord.Color.purple()
        )
        embed.set_footer(
            text=f"Requested By: {interaction.user.display_name} | {interaction.user.top_role.name}",
            icon_url=interaction.user.display_avatar.url
        )

        await interaction.response.edit_message(view=self)
        await interaction.followup.send(embed=embed, ephemeral=True)

    @discord.ui.button(emoji="<:replay:1457373975221895198>", style=discord.ButtonStyle.gray)
    async def replay(self, interaction: discord.Interaction, button: discord.ui.Button):
       if not self.player.current:
        
           embed = discord.Embed(
            description="➔ No track is currently playing.",
            color=discord.Color.purple()
           )
           embed.set_footer(
            text=f"Requested By: {interaction.user.display_name} | {interaction.user.top_role.name}",
            icon_url=interaction.user.display_avatar.url
           )
           return await interaction.response.send_message(embed=embed, ephemeral=True)

       track = self.player.current       
       await self.player.stop()
       await self.player.play(track)

       embed = discord.Embed(
        description="➔ Track replayed from the beginning.",
        color=discord.Color.purple()
       )
       embed.set_footer(
        text=f"Requested By: {interaction.user.display_name} | {interaction.user.top_role.name}",
        icon_url=interaction.user.display_avatar.url
       )

       await interaction.response.send_message(embed=embed, ephemeral=True)

