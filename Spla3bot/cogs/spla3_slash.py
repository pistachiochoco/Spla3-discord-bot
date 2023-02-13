import datetime
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
        # embeds, files = utils.get_embeds('open', schedules)
        # embeds, files = [], []
        for i, schedule in enumerate(schedules):
            embed, file = utils.battle_stage_embed_format("open", schedule, i)
            await interaction.followup.send(file=file, embed=embed)
        os.remove(f"./{file.filename}")
        #     embeds.append(embed)
        #     files.append(file)
        # await interaction.followup.send(files=files, embeds=embeds)
        # [os.remove(f"./{file.filename}") for file in files]

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
        for i, schedule in enumerate(schedules):
            embed, file = utils.battle_stage_embed_format("regular", schedule, i)
            await interaction.followup.send(file=file, embed=embed)
        os.remove(f"./{file.filename}")

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
        for i, schedule in enumerate(schedules):
            embed, file = utils.battle_stage_embed_format("challenge", schedule, i)
            await interaction.followup.send(file=file, embed=embed)
        os.remove(f"./{file.filename}")

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
        for i, schedule in enumerate(schedules):
            embed, file = utils.battle_stage_embed_format("xmatch", schedule, i)
            await interaction.followup.send(file=file, embed=embed)
        os.remove(f"./{file.filename}")

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
        for i, schedule in enumerate(schedules):
            embed, file = utils.battle_stage_embed_format("league", schedule, i)
            await interaction.followup.send(file=file, embed=embed)
        os.remove(f"./{file.filename}")

    @app_commands.command(description="フェスマッチのスケジュール")
    @app_commands.describe(
        number="ほしいスケジュールの数",
    )
    async def fes(
        self,
        interaction: discord.Interaction,
        number: int
    ):
        await interaction.response.defer()
        await asyncio.sleep(1)
        schedules, fest = get_stages("fest", number)
        if not fest:
            await interaction.followup.send("フェスの情報はありません！！")
        else:
            embed, file = utils.fest_info_embed_format("fest", fest)
            if len(schedules) == 0:
                embed.add_field(name="フェスまだ始まってない！！", value="", inline=False)
                await interaction.followup.send(file=file, embed=embed)
                os.remove(f"./{file.filename}")
            else:
                await interaction.followup.send(file=file, embed=embed)
                for i, schedule in enumerate(schedules):
                    embed, file = utils.battle_stage_embed_format("fest", schedule, i)
                    await interaction.followup.send(file=file, embed=embed)
                os.remove(f"./{file.filename}")



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
        for i, schedule in enumerate(schedules):
            embed, file = utils.battle_stage_embed_format(mode, schedule, i)
            await interaction.followup.send(file=file, embed=embed)
        os.remove(f"./{file.filename}")

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
        for i, schedule in enumerate(schedules):
            embed, file = utils.battle_stage_embed_format(mode, schedule, i)
            await interaction.followup.send(file=file, embed=embed)
        os.remove(f"./{file.filename}")

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
        for i, schedule in enumerate(schedules):
            embed, file = utils.battle_stage_embed_format(mode, schedule, i)
            await interaction.followup.send(file=file, embed=embed)
        os.remove(f"./{file.filename}")

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
        for i, schedule in enumerate(schedules):
            embed, file = utils.battle_stage_embed_format(mode, schedule, i)
            await interaction.followup.send(file=file, embed=embed)
        os.remove(f"./{file.filename}")

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
        for i, schedule in enumerate(schedules):
            embed, file = utils.coop_stage_embed_format("coop", schedule, i)
            await interaction.followup.send(file=file, embed=embed)
        os.remove(f"./{file.filename}")


class Gear(commands.Cog, name="ゲソタウンのギアスラッシュコマンド"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="ゲソタウンで売っているギア")
    async def gear(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await asyncio.sleep(1)
        gears = get_gesotown()
        for i, gear in enumerate(gears):
            embed = discord.Embed(title=gear.info)
            embed, file = utils.gear_embed_format(embed, gear, i)
            await interaction.followup.send(file=file, embed=embed)
        os.remove(f"./{file.filename}")


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
