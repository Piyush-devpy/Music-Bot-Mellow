import discord
from discord.ext import commands
import wavelink
import math


class QueueMenu(discord.ui.View):
    def __init__(self, queue, ctx: commands.Context):
        super().__init__(timeout=60)
        self.queue = list(queue)
        self.ctx = ctx
        self.current_page = 0
        self.items_per_page = 10
        self.max_pages = max(1, math.ceil(len(self.queue) / self.items_per_page))

    def create_embed(self) -> discord.Embed:
        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        page_items = self.queue[start:end]

        description = ""
        for i, track in enumerate(page_items, start=start + 1):
            mm = track.length // 60000
            ss = (track.length // 1000) % 60
            description += f"**{i}.** {track.title} `{mm:02d}:{ss:02d}`\n"

        embed = discord.Embed(
            title=" Current Queue",
            description=description or "➔ The queue is empty.",
            color=discord.Color.purple()
        )

        embed.set_footer(
            text=f"Page {self.current_page + 1}/{self.max_pages} • Requested by {self.ctx.author.display_name}",
            icon_url=self.ctx.author.display_avatar.url
        )
        return embed

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(
                "➔ Only the command author can use these buttons.",
                ephemeral=True
            )
            return False
        return True

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True

    @discord.ui.button(label=" Previous", style=discord.ButtonStyle.gray)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            await interaction.response.edit_message(embed=self.create_embed(), view=self)
        else:
            await interaction.response.send_message(
                "➔ You are already on the first page.",
                ephemeral=True
            )

    @discord.ui.button(label="Next ", style=discord.ButtonStyle.gray)
    async def next_page(self, interaction: discord.Interation, button: discord.ui.Button):
        if self.current_page < self.max_pages - 1:
            self.current_page += 1
            await interaction.response.edit_message(embed=self.create_embed(), view=self)
        else:
            await interaction.response.send_message(
                "➔ You are already on the last page.",
                ephemeral=True
            )


class QueueCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=["sq"])
    async def showqueue(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if not vc or not vc.queue:
            return await ctx.send("➔ The queue is empty.")

        view = QueueMenu(vc.queue, ctx)
        embed = view.create_embed()

        if vc.current:
            embed.insert_field_at(
                index=0,
                name=" Now Playing",
                value=vc.current.title,
                inline=False
            )

        await ctx.send(embed=embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(QueueCog(bot))
