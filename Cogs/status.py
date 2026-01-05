import discord
from discord.ext import commands, tasks
import itertools

class StatusCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # Define your rotating statuses here (type, text)
        # Available types: playing, listening, watching, streaming, competing
        self.status_list = [
            ("playing", "Music "),
            ("listening", "Chill Beats "),
            ("watching", "Movies "),
            ("competing", "In a Music Contest "),
        ]

        # Create an infinite iterator to cycle statuses
        self.status_cycle = itertools.cycle(self.status_list)

        # Start the task
        self.change_status.start()

    @tasks.loop(seconds=3600)  # Change status every 60 seconds
    async def change_status(self):
        status_type, text = next(self.status_cycle)

        activity_type = {
            "playing": discord.ActivityType.playing,
            "listening": discord.ActivityType.listening,
            "watching": discord.ActivityType.watching,
            "streaming": discord.ActivityType.streaming,
            "competing": discord.ActivityType.competing
        }.get(status_type, discord.ActivityType.playing)

        activity = discord.Activity(type=activity_type, name=text)
        await self.bot.change_presence(activity=activity, status=discord.Status.online)

    @change_status.before_loop
    async def before_change_status(self):
        await self.bot.wait_until_ready()  # Wait until bot is ready

    # Optional: Command to manually set status
    @commands.command()
    @commands.is_owner()  # Only bot owner
    async def setstatus(self, ctx, type: str, *, text: str):
        type = type.lower()
        activity_type = {
            "playing": discord.ActivityType.playing,
            "listening": discord.ActivityType.listening,
            "watching": discord.ActivityType.watching,
            "streaming": discord.ActivityType.streaming,
            "competing": discord.ActivityType.competing
        }.get(type)

        if not activity_type:
            return await ctx.send(" Invalid type! Use playing, listening, watching, streaming, competing.")

        activity = discord.Activity(type=activity_type, name=text)
        await self.bot.change_presence(activity=activity, status=discord.Status.online)
        await ctx.send(f"Status changed to **{type} {text}** manually.")

async def setup(bot: commands.Bot):
    await bot.add_cog(StatusCog(bot))
