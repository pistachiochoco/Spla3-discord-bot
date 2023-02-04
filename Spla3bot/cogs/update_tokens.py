import sys
import logging
import datetime
from discord.ext import commands, tasks
sys.path.append("../../Spla3API")
sys.path.append("../")
from login_utils import validate_tokens, generate_tokens

WEB_SERVICE_TOKEN = ''
BULLET_TOKEN = ''

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

utc = datetime.timezone.utc
times = [datetime.time(hour=i, tzinfo=utc) for i in range(0, 24, 2)]


class UpdateTokens(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update.start()

    def cog_unload(self):
        self.update.cancel()

    @tasks.loop(time=times)
    async def update(self):
        global WEB_SERVICE_TOKEN, BULLET_TOKEN
        WEB_SERVICE_TOKEN, BULLET_TOKEN = generate_tokens()
        if validate_tokens() is False:
            logger.error("Tokens are invalid.")

    @update.before_loop
    async def generate(self):
        global WEB_SERVICE_TOKEN, BULLET_TOKEN
        WEB_SERVICE_TOKEN, BULLET_TOKEN = generate_tokens()
        logger.info("Tokens are generated.")

    # @printer.after_loop
    # async def after_slow_count(self):
    #     print('done!')

async def setup(bot):
    await bot.add_cog(UpdateTokens(bot))
