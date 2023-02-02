import os, sys
import discord
from discord.ext import commands
from dotenv import load_dotenv
sys.path.append("../Spla3API")

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


class Bot(commands.Bot):

    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True

        super().__init__(
            command_prefix='?',
            intents=intents,
            case_insensitive=True,
            help_command=commands.DefaultHelpCommand(no_category="ヘルプコマンド")
        )

    async def on_ready(self):
        print(f'Logged on as {self.user}')
        print('------')

    async def setup_hook(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                extension = filename[:-3]
                try:
                    await bot.load_extension(f"cogs.{extension}")
                    print(f"Loaded extension {extension}")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    print(f"Failed to load extension {extension}\n{exception}")


bot = Bot()

bot.run(DISCORD_TOKEN)