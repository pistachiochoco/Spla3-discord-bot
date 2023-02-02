import os, sys
import discord
from discord import app_commands
from discord.ext import commands
sys.path.append("../../Spla3API")
sys.path.append("../")
from query_utils import get_stages, get_gesotown, get_x_ranking, get_x_ranking_borderline, get_stages_by_rule
import utils
from utils import RULE_DICT, MODE_DICT

import asyncio


class ScheduleByTime(commands.Cog, name="普通のスケジュールスラッシュコマンド"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.describe(
        number="ほしいスケジュールの数",
    )
    async def open(
        self,
        interaction: discord.Interaction,
        number: int
    ):
        """
        バカマオープンのスケジュール
        """
        await interaction.response.defer()
        await asyncio.sleep(1)
        schedules = get_stages("open", number)
        embeds, files = [], []
        for i, schedule in enumerate(schedules):
            embed, file = utils.battle_stage_embed_format("open", schedule, i)
            embeds.append(embed)
            files.append(file)
        await interaction.followup.send(files=files, embeds=embeds)
        [os.remove(f"./{file.filename}") for file in files]

    @app_commands.command()
    @app_commands.describe(
        number="ほしいスケジュールの数",
    )
    async def regular(
        self,
        interaction: discord.Interaction,
        number: int
    ):
        """
        レギュラーマッチのスケジュール
        """
        await interaction.response.defer()
        await asyncio.sleep(1)
        schedules = get_stages("regular", number)
        embeds, files = [], []
        for i, schedule in enumerate(schedules):
            embed, file = utils.battle_stage_embed_format("regular", schedule, i)
            embeds.append(embed)
            files.append(file)
        await interaction.followup.send(files=files, embeds=embeds)
        [os.remove(f"./{file.filename}") for file in files]

    @app_commands.command()
    @app_commands.describe(
        number="ほしいスケジュールの数",
    )
    async def challenge(
        self,
        interaction: discord.Interaction,
        number: int
    ):
        """
        バカマチャレンジのスケジュール
        """
        await interaction.response.defer()
        await asyncio.sleep(1)
        schedules = get_stages("challenge", number)
        embeds, files = [], []
        for i, schedule in enumerate(schedules):
            embed, file = utils.battle_stage_embed_format("challenge", schedule, i)
            embeds.append(embed)
            files.append(file)
        await interaction.followup.send(files=files, embeds=embeds)
        [os.remove(f"./{file.filename}") for file in files]

    @app_commands.command()
    @app_commands.describe(
        number="ほしいスケジュールの数",
    )
    async def xmatch(
        self,
        interaction: discord.Interaction,
        number: int
    ):
        """
        Xマッチのスケジュール
        """
        await interaction.response.defer()
        await asyncio.sleep(1)
        schedules = get_stages("xmatch", number)
        embeds, files = [], []
        for i, schedule in enumerate(schedules):
            embed, file = utils.battle_stage_embed_format("xmatch", schedule, i)
            embeds.append(embed)
            files.append(file)
        await interaction.followup.send(files=files, embeds=embeds)
        [os.remove(f"./{file.filename}") for file in files]

    @app_commands.command()
    @app_commands.describe(
        number="ほしいスケジュールの数",
    )
    async def league(
        self,
        interaction: discord.Interaction,
        number: int
    ):
        """
        リーグマッチのスケジュール
        """
        await interaction.response.defer()
        await asyncio.sleep(1)
        schedules = get_stages("league", number)
        embeds, files = [], []
        for i, schedule in enumerate(schedules):
            embed, file = utils.battle_stage_embed_format("league", schedule, i)
            embeds.append(embed)
            files.append(file)
        await interaction.followup.send(files=files, embeds=embeds)
        [os.remove(f"./{file.filename}") for file in files]


async def setup(bot):
    await bot.add_cog(ScheduleByTime(bot))
    # await bot.add_cog(ScheduleByRule(bot))
    # await bot.add_cog(SalmonScheduleByTime(bot))
    # await bot.add_cog(Gear(bot))
    # await bot.add_cog(XRanking(bot))