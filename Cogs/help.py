import discord
from discord.ext import commands

class Help(commands.Cog):
    """Custom Help Command"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx: commands.Context, *, category: str = None):
        embed = discord.Embed(
            title="<:openbook:1457432770354872371> Help Menu",
            color=discord.Color.purple()
        )

        # ---------- NO CATEGORY ----------
        if category is None:
            embed.description = (
                "Use `.help <category>` to see commands.\n\n"
                "**Available Categories:**"
            )

            embed.add_field(
                name="<:music:1457411800789156043> Music",
                value="""
                `play`, `pause`, `resume`, `stop`, `loop`, `shuffle`, `queue`
                `skip`,`jump`,`saveplaylist`,loadplaylist`,`removeplaylist`,`autoplay`
                """,
                inline=False
            )

            embed.add_field(
                name="<:workbelt:1457411749950128261> Utility",
                value="`stats`",
                inline=False
            )

            embed.add_field(
                name="<:extra:1457411847450792051> Extra",
                value="`help`, `info`, `invite`",
                inline=False
            )

            embed.set_footer(
                text=f"Requested by {ctx.author}",
                icon_url=ctx.author.display_avatar.url
            )

            return await ctx.send(embed=embed)

        # ---------- MUSIC ----------
        if category.lower() == "music":
            embed.title = "<:music:1457411800789156043> Music Commands"
            embed.description = (
                "`play[p]` - Play a song or playlist.\n"
                "`pause` - Pause playback.\n"
                "`resume` - Resume playback.\n"
                "`stop` - Stop music.\n"
                "`loop` - Loop current song.\n"
                "`shuffle` - Shuffle queue.\n"
                "`showqueue[sq]` - Show queue.\n"
                "`skip`- Skip to next track.\n"
                "`jump` - Jump to specific song in queue.\n"
                "`removeplayelist[rp]`- Remove your playlist.\n"
                "`loadplaylist[lp]` - Load your saved playlist.\n"
                "`saveplaylist[sp]` - Save your spotify playlist inside bot.\n"
                "`autoplay`- Plays songs automatically depending on last track you  played."
            )

        # ---------- UTILITY ----------
        elif category.lower() == "utility":
            embed.title = "<:workbelt:1457411749950128261> Utility Commands"
            embed.description = (
                "`stats` - Show bot stats"
            )

        # ---------- EXTRA ----------
        elif category.lower() == "extra":
            embed.title = "<:extra:1457411847450792051> Extra Commands"
            embed.description = (
                "`help` - Show this menu\n"
                "`info` - Info about the bot\n"
                "`invite` - Bot invite link"
            )

        else:
            embed.description = "➔ Invalid category.\nUse `.help`"

        embed.set_footer(
            text=f"Requested by {ctx.author}",
            icon_url=ctx.author.display_avatar.url
        )

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
