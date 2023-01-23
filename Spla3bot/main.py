import os, sys
import discord
from discord.ext import commands
from dotenv import load_dotenv
sys.path.append("../Spla3API")
from query_utils import get_stages, get_gesotown, get_x_ranking, get_x_ranking_borderline, get_stages_by_rule


load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


class Bot(commands.Bot):

    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True

        super().__init__(
            command_prefix='/',
            intents=intents,
            case_insensitive=True,
            help_command=commands.DefaultHelpCommand(no_category="ヘルプコマンド")
        )

    async def on_ready(self):
        print(f'Logged on as {self.user}')
        print('------')

    async def setup_hook(self):
        for file in os.listdir(f"./cogs"):
            extension = file[:-3]
            try:
                await bot.load_extension(f"cogs.{extension}")
                print(f"Loaded extension {extension}")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")


bot = Bot()

bot.run(DISCORD_TOKEN)