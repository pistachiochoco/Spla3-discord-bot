import sys, os
import discord
from discord.ext import commands
sys.path.append("../../Spla3API")
sys.path.append("../")
from query_utils import get_stages, get_gesotown, get_x_ranking, get_x_ranking_borderline, get_stages_by_rule
import utils
from utils import RULE_DICT, MODE_DICT


class ScheduleByTime(commands.Cog, name="普通のスケジュール"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def open(
        self, ctx,
        num: int = commands.parameter(description="ほしいスケジュールの数", default=3)
    ):
        """
        バカマオープンのスケジュール（デフォルト：近い3個）
        Query bankara match open schedules. Recent 3 schedules will be returned as default.
        """
        schedules = get_stages("open", num)
        for schedule in schedules:
            embed, file = utils.battle_stage_embed_format("open", schedule)
            await ctx.send(file=file, embed=embed)
        os.remove(f"./{file.filename}")

    @commands.command()
    async def regular(
        self, ctx,
        num: int = commands.parameter(description="ほしいスケジュールの数", default=3)
    ):
        """
        レギュラーマッチのスケジュール（デフォルト：近い3個）
        Query regular match schedules. Recent 3 schedules will be returned as default.
        """
        schedules = get_stages("regular", num)
        for schedule in schedules:
            embed, file = utils.battle_stage_embed_format("regular", schedule)
            await ctx.send(file=file, embed=embed)
        os.remove(f"./{file.filename}")

    @commands.command()
    async def challenge(
        self, ctx,
        num: int = commands.parameter(description="ほしいスケジュールの数", default=3)
    ):
        """
        バカマチャレンジのスケジュール（デフォルト：近い3個）
        Query bankara match challenge schedules. Recent 3 schedules will be returned as default.
        """
        schedules = get_stages("challenge", num)
        for schedule in schedules:
            embed, file = utils.battle_stage_embed_format("challenge", schedule)
            await ctx.send(file=file, embed=embed)
        os.remove(f"./{file.filename}")

    @commands.command()
    async def xmatch(
        self, ctx,
        num: int = commands.parameter(description="ほしいスケジュールの数", default=3)
    ):
        """
        Xマッチのスケジュール（デフォルト：近い3個）
        Query X-match schedules. Recent 3 schedules will be returned as default.
        """
        schedules = get_stages("xmatch", num)
        for schedule in schedules:
            embed, file = utils.battle_stage_embed_format("xmatch", schedule)
            await ctx.send(file=file, embed=embed)
        os.remove(f"./{file.filename}")

    @commands.command()
    async def league(
        self, ctx,
        num: int = commands.parameter(description="ほしいスケジュールの数", default=3)
    ):
        """
        リーグマッチのスケジュール（デフォルト：近い3個）
        Query league match schedules. Recent 3 schedules will be returned as default.
        """
        schedules = get_stages("league", num)
        for schedule in schedules:
            embed, file = utils.battle_stage_embed_format("league", schedule)
            await ctx.send(file=file, embed=embed)
        os.remove(f"./{file.filename}")


class ScheduleByRule(commands.Cog, name="ルール別スケジュール"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def area(
        self, ctx,
        mode: str = commands.parameter(default="xmatch", description="どのルール\n(open/challenge/xmatch/league)")
    ):
        """
        ガチエリアのスケジュール（デフォルト:Xマッチ）
        ほかのルールを検索したいなら：/area challenge
        Query battle schedules of Splat Zones. Schedules of X-match will be returned by default.
        """
        schedules = get_stages_by_rule("Ar", mode)
        for schedule in schedules:
            embed, file = utils.battle_stage_embed_format(mode, schedule)
            await ctx.send(file=file, embed=embed)
        os.remove(f"./{file.filename}")

    @commands.command()
    async def yagura(
        self, ctx,
        mode: str = commands.parameter(default="xmatch", description="どのルール\n(open/challenge/xmatch/league)")
    ):
        """
        ガチヤグラのスケジュール（デフォルト:Xマッチ）
        ほかのルールを検索したいなら：/yagura open
        Query battle schedules of Tower Control. Schedules of X-match will be returned by default.
        """
        schedules = get_stages_by_rule("Lf", mode)
        for schedule in schedules:
            embed, file = utils.battle_stage_embed_format(mode, schedule)
            await ctx.send(file=file, embed=embed)
        os.remove(f"./{file.filename}")

    @commands.command()
    async def hoko(
        self, ctx,
        mode: str = commands.parameter(default="xmatch", description="どのルール\n(open/challenge/xmatch/league)")
    ):
        """
        ガチホコバトルのスケジュール（デフォルト:Xマッチ）
        ほかのルールを検索したいなら：/hoko challenge
        Query battle schedules of Rainmaker. Schedules of X-match will be returned by default.
        """
        schedules = get_stages_by_rule("Gl", mode)
        for schedule in schedules:
            embed, file = utils.battle_stage_embed_format(mode, schedule)
            await ctx.send(file=file, embed=embed)
        os.remove(f"./{file.filename}")

    @commands.command()
    async def asari(
        self, ctx,
        mode: str = commands.parameter(default="xmatch", description="どのルール\n(open/challenge/xmatch/league)")
    ):
        """
        ガチアサリのスケジュール（デフォルト:Xマッチ）
        ほかのルールを検索したいなら：/asari open
        Query battle schedules of Clam Blitz. Schedules of X-match will be returned by default.
        """
        schedules = get_stages_by_rule("Cl", mode)
        for schedule in schedules:
            embed, file = utils.battle_stage_embed_format(mode, schedule)
            await ctx.send(file=file, embed=embed)
        os.remove(f"./{file.filename}")


class SalmonScheduleByTime(commands.Cog, name="サーモンランのスケジュール"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def salmon(
        self, ctx,
        num: int = commands.parameter(description="ほしいシフトの数", default=1)
    ):
        """
        サーモンランのスケジュール（デフォルト：近い1個）
        Query salmon run schedules. Recent 1 schedule will be returned as default.
        """
        schedules = get_stages("coop", num)
        for schedule in schedules:
            embed, file = utils.coop_stage_embed_format("coop", schedule)
            await ctx.send(file=file, embed=embed)
        os.remove(f"./{file.filename}")


class Gear(commands.Cog, name="ゲソタウンのギア"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gear(self, ctx):
        """
        ゲソタウンで売っているギア
        Query sale gears in Gesotown.
        """
        gears = get_gesotown()
        for gear in gears:
            embed = discord.Embed(title=gear.info)
            embed, file = utils.gear_embed_format(embed, gear)
            await ctx.send(file=file, embed=embed)
        os.remove(f"./{file.filename}")


class XRanking(commands.Cog, name="Xランキング関連"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def xrank(
        self, ctx,
        rule: str = commands.parameter(default="ALL", description="知りたいルール(area/tower/rainmaker/clam)"),
        num: int = commands.parameter(default=10, description="何位まで(最大25位まで)")
    ):
        """
        Xランキング
        Query X-ranking.
        """
        rankings = get_x_ranking(rule, num)
        for rule, ranking in rankings.items():
            embed = discord.Embed(title=RULE_DICT[rule])
            embed = utils.xranking_embed_format(embed, ranking)
            await ctx.send(embed=embed)

    @commands.command()
    async def xrankline(self, ctx):
        """各ルール500位に入る必要なXパワー"""
        xpowers = get_x_ranking_borderline()
        embed = discord.Embed(title="500位に入る必要なXパワー")
        for rule, xpower in xpowers.items():
            embed = embed.add_field(name=RULE_DICT[rule], value=xpower, inline=False)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ScheduleByTime(bot))
    await bot.add_cog(ScheduleByRule(bot))
    await bot.add_cog(SalmonScheduleByTime(bot))
    await bot.add_cog(Gear(bot))
    await bot.add_cog(XRanking(bot))
