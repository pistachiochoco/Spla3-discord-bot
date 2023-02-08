import sys
import logging
import datetime
from discord.ext import commands, tasks
sys.path.append("../../Spla3API")
sys.path.append("../")
from login_utils import validate_tokens, generate_tokens
from query_utils import save_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

utc = datetime.timezone.utc
times = [datetime.time(hour=i, tzinfo=utc) for i in range(0, 24, 2)]
times_gear = [datetime.time(hour=i, minute=1, tzinfo=utc) for i in range(0, 24, 4)]

class UpdateTokens(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update.start()
        # self.save_gesotown.start()

    def cog_unload(self):
        self.update.cancel()
        # self.save_gesotown.cancel()

    @tasks.loop(time=times)
    async def update(self):
        generate_tokens()
        if validate_tokens() is False:
            logger.error("Tokens are invalid.")
        save_data("schedules.json")
        save_data("gesotown.json")
        # print("data updated")

    # @tasks.loop(time=times_gear)
    # async def save_gesotown(self):
    #     save_data("gesotown.json")

    @update.before_loop
    async def generate(self):
        generate_tokens()
        logger.info("Tokens are generated.")
        save_data("schedules.json")
        save_data("gesotown.json")


async def setup(bot):
    await bot.add_cog(UpdateTokens(bot))
