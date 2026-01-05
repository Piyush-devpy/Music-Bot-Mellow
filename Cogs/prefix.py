import discord
from discord.ext import commands

class CustomPrefix(commands.Cog):
    def __init__(self,bot):
        self.bot = bot 

    @commands.command()
    @commands.has_permissions(administrator= True)
    async def setprefix(self,ctx,new_prefix: str):
        result =await self.bot.prefixes.update_one(
            {"guild_id":int(ctx.guild.id)},
            {"$set":{"prefix":new_prefix}},
            upsert=True
        )
        embed= discord.Embed(
            description = f'➔ Your Server Prefix Is Set To "{new_prefix}."',
            color=discord.Colour.purple()
        )
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        if isinstance(error, commands.MissingPermissions):
            embed= discord.Embed(
                description="You Are Missing The Required Permissions.",
                color=discord.Color.purple()
            )
            embed.set_footer(
                text=f"Requested By: {ctx.author.display_name} | {ctx.author.top_role.name}",
                icon_url=ctx.author.display_avatar.url
            )
            await ctx.send(embed=embed)   
        else:
              await ctx.send(f'An Error Occured:\n```{error}```')    

async def setup(bot):
    await bot.add_cog(CustomPrefix(bot))