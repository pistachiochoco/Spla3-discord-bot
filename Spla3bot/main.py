import discord
from discord.ext import commands
import utils
import sys

sys.path.append("../Spla3API")
from query_utils import get_stages, get_gesotown, get_x_ranking, get_x_ranking_borderline, get_stages_by_rule

BOT_TOKEN = utils.load_token()
RULE_DICT = {
    "area": "ガチエリア", "Ar": "ガチエリア",
    "tower": "ガチヤグラ", "Lf": "ガチヤグラ",
    "rainmaker": "ガチホコバトル", "Gl": "ガチホコバトル",
    "clam": "ガチアサリ", "Cl": "ガチアサリ"
}

MODE_DICT = {
    "xmatch": "Xマッチ",
    "open": "バンカラマッチ オープン",
    "challenge": "バンカラマッチ チャレンジ",
    "league": "リーグマッチ"
}

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(
    command_prefix='/',
    intents=intents,
    case_insensitive=True,
)


@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}')
    print('------')


''' for test '''
@bot.command()
async def add(ctx, left: int, right: int):
    await ctx.send(left + right)


@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)


''' Query battle schedule, default returns recent 3 schedules '''
@bot.command()
async def open(ctx, num=3):
    schedules = get_stages("open", num)
    embed = discord.Embed(title="バンカラマッチ オープン")
    embed = utils.stage_embed_format('battle', embed, schedules)
    await ctx.send(embed=embed)

@bot.command()
async def regular(ctx, num=3):
    schedules = get_stages("regular", num)
    embed = discord.Embed(title="レギュラーマッチ")
    embed = utils.stage_embed_format('battle', embed, schedules)
    await ctx.send(embed=embed)

@bot.command()
async def challenge(ctx, num=3):
    schedules = get_stages("challenge", num)
    embed = discord.Embed(title="バンカラマッチ チャレンジ")
    embed = utils.stage_embed_format('battle', embed, schedules)
    await ctx.send(embed=embed)

@bot.command()
async def xmatch(ctx, num=3):
    schedules = get_stages("xmatch", num)
    embed = discord.Embed(title="Xマッチ")
    embed = utils.stage_embed_format('battle', embed, schedules)
    await ctx.send(embed=embed)

@bot.command()
async def league(ctx, num=3):
    schedules = get_stages("league", num)
    embed = discord.Embed(title="リーグマッチ")
    embed = utils.stage_embed_format('battle', embed, schedules)
    await ctx.send(embed=embed)


''' Query salmon run schedule '''
@bot.command()
async def salmon(ctx, num=3):
    schedules = get_stages("coop", num)
    embed = discord.Embed(title="サーモンラン")
    embed = utils.stage_embed_format('coop', embed, schedules)
    await ctx.send(embed=embed)


''' Query sale gear in Gesotown '''
@bot.command()
async def gear(ctx):
    gears = get_gesotown()
    for gear in gears:
        embed = discord.Embed(title=gear.info)
        embed = utils.gear_embed_format(embed, gear)
        await ctx.send(embed=embed)


''' Query X-ranking (default is top10) '''
@bot.command()
async def xrank(ctx, rule="ALL", num=10):
    rankings = get_x_ranking(rule, num)
    for rule, ranking in rankings.items():
        embed = discord.Embed(title=RULE_DICT[rule])
        embed = utils.xranking_embed_format(embed, ranking)
        await ctx.send(embed=embed)


@bot.command()
async def xrankline(ctx):
    xpowers = get_x_ranking_borderline()
    embed = discord.Embed(title="500位に入る必要なXパワー")
    for rule, xpower in xpowers.items():
        embed = embed.add_field(name=RULE_DICT[rule], value=xpower, inline=False)
    await ctx.send(embed=embed)


''' Query battle schedule by gachi-Rule '''
@bot.command()
async def area(ctx, mode='xmatch'):
    schedules = get_stages_by_rule("Ar", mode)
    embed = discord.Embed(title=f"{MODE_DICT[mode]}　ガチエリア")
    embed = utils.stage_embed_format('battle', embed, schedules)
    await ctx.send(embed=embed)

@bot.command()
async def yagura(ctx, mode='xmatch'):
    schedules = get_stages_by_rule("Lf", mode)
    embed = discord.Embed(title=f"{MODE_DICT[mode]}　ガチヤグラ")
    embed = utils.stage_embed_format('battle', embed, schedules)
    await ctx.send(embed=embed)

@bot.command()
async def hoko(ctx, mode='xmatch'):
    schedules = get_stages_by_rule("Gl", mode)
    embed = discord.Embed(title=f"{MODE_DICT[mode]}　ガチホコバトル")
    embed = utils.stage_embed_format('battle', embed, schedules)
    await ctx.send(embed=embed)

@bot.command()
async def asari(ctx, mode='xmatch'):
    schedules = get_stages_by_rule("Cl", mode)
    embed = discord.Embed(title=f"{MODE_DICT[mode]}　ガチアサリ")
    embed = utils.stage_embed_format('battle', embed, schedules)
    await ctx.send(embed=embed)


bot.run(BOT_TOKEN)