import os, sys
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
sys.path.append("../../Spla3API")
sys.path.append("../")
from query_utils import get_stages, get_gesotown, get_x_ranking, get_x_ranking_borderline, get_stages_by_rule
import utils
from utils import RULE_DICT, MODE_DICT


class ScheduleByTime(commands.Cog, name="普通のスケジュールスラッシュコマンド"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="バカマオープンのスケジュール")
    @app_commands.describe(
        number="ほしいスケジュールの数",
    )
    async def open(
        self,
        interaction: discord.Interaction,
        number: int
    ):
        await interaction.response.defer()
        await asyncio.sleep(1)
        schedules = get_stages("open", number)
        embeds, files = utils.get_embeds('open', schedules)
        # embeds, files = [], []
        # for i, schedule in enumerate(schedules):
        #     embed, file = utils.battle_stage_embed_format("open", schedule, i)
        #     embeds.append(embed)
        #     files.append(file)
        await interaction.followup.send(files=files, embeds=embeds)
        [os.remove(f"./{file.filename}") for file in files]

    @app_commands.command(description="レギュラーマッチのスケジュール")
    @app_commands.describe(
        number="ほしいスケジュールの数",
    )
    async def regular(
        self,
        interaction: discord.Interaction,
        number: int
    ):
        await interaction.response.defer()
        await asyncio.sleep(1)
        schedules = get_stages("regular", number)
        embeds, files = utils.get_embeds('regular', schedules)
        await interaction.followup.send(files=files, embeds=embeds)
        [os.remove(f"./{file.filename}") for file in files]

    @app_commands.command(description="バカマチャレンジのスケジュール")
    @app_commands.describe(
        number="ほしいスケジュールの数",
    )
    async def challenge(
        self,
        interaction: discord.Interaction,
        number: int
    ):
        await interaction.response.defer()
        await asyncio.sleep(1)
        schedules = get_stages("challenge", number)
        embeds, files = utils.get_embeds('challenge', schedules)
        await interaction.followup.send(files=files, embeds=embeds)
        [os.remove(f"./{file.filename}") for file in files]

    @app_commands.command(description="Xマッチのスケジュール")
    @app_commands.describe(
        number="ほしいスケジュールの数",
    )
    async def xmatch(
        self,
        interaction: discord.Interaction,
        number: int
    ):
        await interaction.response.defer()
        await asyncio.sleep(1)
        schedules = get_stages("xmatch", number)
        embeds, files = utils.get_embeds('xmatch', schedules)
        await interaction.followup.send(files=files, embeds=embeds)
        [os.remove(f"./{file.filename}") for file in files]

    @app_commands.command(description="リーグマッチのスケジュール")
    @app_commands.describe(
        number="ほしいスケジュールの数",
    )
    async def league(
        self,
        interaction: discord.Interaction,
        number: int
    ):
        await interaction.response.defer()
        await asyncio.sleep(1)
        schedules = get_stages("league", number)
        embeds, files = utils.get_embeds('league', schedules)
        await interaction.followup.send(files=files, embeds=embeds)
        [os.remove(f"./{file.filename}") for file in files]


class ScheduleByRule(commands.Cog, name="ルール別スケジュールスラッシュコマンド"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="ガチエリアのスケジュール")
    @app_commands.describe(
        mode="バトルモードを指定",
    )
    async def area(
        self,
        interaction: discord.Interaction,
        mode: str
    ):
        await interaction.response.defer()
        await asyncio.sleep(1)
        schedules = get_stages_by_rule('Ar', mode)
        embeds, files = utils.get_embeds(mode, schedules)
        await interaction.followup.send(files=files, embeds=embeds)
        [os.remove(f"./{file.filename}") for file in files]

    @app_commands.command(name="yagura", description="ガチヤグラのスケジュール")
    @app_commands.describe(
        mode="バトルモードを指定",
    )
    async def tower_control(
        self,
        interaction: discord.Interaction,
        mode: str
    ):
        await interaction.response.defer()
        await asyncio.sleep(1)
        schedules = get_stages_by_rule('Lf', mode)
        embeds, files = utils.get_embeds(mode, schedules)
        await interaction.followup.send(files=files, embeds=embeds)
        [os.remove(f"./{file.filename}") for file in files]

    @app_commands.command(name="hoko", description="ガチホコバトルのスケジュール")
    @app_commands.describe(
        mode="バトルモードを指定",
    )
    async def rainmaker(
        self,
        interaction: discord.Interaction,
        mode: str
    ):
        await interaction.response.defer()
        await asyncio.sleep(1)
        schedules = get_stages_by_rule('Gl', mode)
        embeds, files = utils.get_embeds(mode, schedules)
        await interaction.followup.send(files=files, embeds=embeds)
        [os.remove(f"./{file.filename}") for file in files]

    @app_commands.command(name="asari", description="ガチアサリのスケジュール")
    @app_commands.describe(
        mode="バトルモードを指定",
    )
    async def clam(
        self,
        interaction: discord.Interaction,
        mode: str
    ):
        await interaction.response.defer()
        await asyncio.sleep(1)
        schedules = get_stages_by_rule('Cl', mode)
        embeds, files = utils.get_embeds(mode, schedules)
        await interaction.followup.send(files=files, embeds=embeds)
        [os.remove(f"./{file.filename}") for file in files]

    @area.autocomplete("mode")
    @tower_control.autocomplete("mode")
    @rainmaker.autocomplete("mode")
    @clam.autocomplete("mode")
    async def mode_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ):
        modes = ['open', 'challenge', 'xmatch', 'league']
        return [
            app_commands.Choice(name=mode, value=mode)
            for mode in modes if current.lower() in mode.lower()
        ]


class SalmonScheduleByTime(commands.Cog, name="サーモンランのスケジュールスラッシュコマンド"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="サーモンランのスケジュール")
    @app_commands.describe(
        number="ほしいスケジュールの数",
    )
    async def salmon(
        self,
        interaction: discord.Interaction,
        number: int
    ):
        await interaction.response.defer()
        await asyncio.sleep(1)
        schedules = get_stages("coop", number)
        embeds, files = utils.get_embeds("coop", schedules)
        await interaction.followup.send(files=files, embeds=embeds)
        [os.remove(f"./{file.filename}") for file in files]


class Gear(commands.Cog, name="ゲソタウンのギアスラッシュコマンド"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="ゲソタウンで売っているギア")
    async def gear(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await asyncio.sleep(1)
        gears = get_gesotown()
        embeds, files = utils.get_embeds_gears(gears)
        await interaction.followup.send(files=files, embeds=embeds)
        [os.remove(f"./{file.filename}") for file in files]


class XRanking(commands.Cog, name="Xランキング関連スラッシュコマンド"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Xランキング")
    @app_commands.describe(
        rule="どのガチルール",
        number="何位まで(最大25位まで)",
    )
    async def xrank(
        self,
        interaction: discord.Interaction,
        rule: str,
        number: int
    ):
        await interaction.response.defer()
        await asyncio.sleep(1)
        rankings = get_x_ranking(rule, number)
        embeds = utils.get_embeds_xranking(rankings)
        await interaction.followup.send(embeds=embeds)

    @xrank.autocomplete("rule")
    async def mode_autocomplete(
            self,
            interaction: discord.Interaction,
            current: str,
    ):
        rules = ['area', 'tower', 'rainmaker', 'clam']
        return [
            app_commands.Choice(name=mode, value=mode)
            for mode in rules if current.lower() in mode.lower()
        ]

    @app_commands.command(description="各ルール500位に入る必要なXパワー")
    async def xrankline(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await asyncio.sleep(1)
        xpowers = get_x_ranking_borderline()
        embed = discord.Embed(title="500位に入る必要なXパワー")
        for rule, xpower in xpowers.items():
            embed = embed.add_field(name=RULE_DICT[rule], value=xpower, inline=False)
        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ScheduleByTime(bot))
    await bot.add_cog(ScheduleByRule(bot))
    await bot.add_cog(SalmonScheduleByTime(bot))
    await bot.add_cog(Gear(bot))
    await bot.add_cog(XRanking(bot))
