from discord.ext import commands

class CommandsHelper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def clear_commands(
            self,
            ctx: commands.Context
    ):
        ctx.bot.tree.clear_commands(guild=ctx.guild)
        await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send("Cleared all commands of the current guild.")

    @commands.command()
    async def sync_commands(
            self,
            ctx: commands.Context
    ):
        ctx.bot.tree.copy_global_to(guild=ctx.guild)
        synced = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"Synced {len(synced)} commands to the current guild.")


async def setup(bot):
    await bot.add_cog(CommandsHelper(bot))
