import discord
from discord.ext import commands
import utils
import sys

sys.path.append("../Spla3API")
from query_utils import get_stages, get_gesotown, get_x_ranking

BOT_TOKEN = utils.load_token()


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


@bot.command()
async def add(ctx, left: int, right: int):
    await ctx.send(left + right)


@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)


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


@bot.command()
async def salmon(ctx, num=3):
    schedules = get_stages("coop", num)
    embed = discord.Embed(title="サーモンラン")
    embed = utils.stage_embed_format('coop', embed, schedules)
    await ctx.send(embed=embed)


@bot.command()
async def gear(ctx):
    gears = get_gesotown()
    for gear in gears:
        embed = discord.Embed(title=gear.info)
        embed = utils.gear_embed_format(embed, gear)
        await ctx.send(embed=embed)


@bot.command()
async def xrank(ctx, rule="ALL", num=10):
    rankings = get_x_ranking(rule, num)
    for rule, ranking in rankings.items():
        rule_dict = {"area":"ガチエリア", "tower":"ガチヤグラ", "rainmaker":"ガチホコバトル", "clam":"ガチアサリ"}
        embed = discord.Embed(title=rule_dict[rule])
        embed = utils.xranking_embed_format(embed, ranking)
        await ctx.send(embed=embed)



bot.run(BOT_TOKEN)