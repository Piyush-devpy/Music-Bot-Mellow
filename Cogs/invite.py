import discord
from discord.ext import commands

class Invite(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="invite", aliases=["inv"])
    async def invite(self, ctx: commands.Context):
        permissions = discord.Permissions(
            view_channel=True,
            send_messages=True,
            embed_links=True,
            read_message_history=True,
            connect=True,
            speak=True,
            use_voice_activation=True,
            add_reactions=True,
            attach_files=True,
            use_external_emojis=True,
            manage_messages=True
        )

        invite_url = discord.utils.oauth_url(
            client_id=self.bot.user.id,
            permissions=permissions,
            scopes=("bot", "applications.commands")
        )

        embed = discord.Embed(
            title=" Invite Me",
            description=(
                "Click the link below to invite me to your server!\n"
                f"[➔ Invite Bot]({invite_url})"
            ),
            color=discord.Color.purple()
        )

        embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        embed.set_footer(
            text=f"Requested by {ctx.author}",
            icon_url=ctx.author.display_avatar.url
        )

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Invite(bot))
