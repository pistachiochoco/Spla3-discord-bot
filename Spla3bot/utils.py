import cv2
import numpy as np
import requests
import discord
from PIL import Image

RULE_DICT = {
    "area": "ガチエリア", "Ar": "ガチエリア",
    "tower": "ガチヤグラ", "Lf": "ガチヤグラ",
    "rainmaker": "ガチホコバトル", "Gl": "ガチホコバトル",
    "clam": "ガチアサリ", "Cl": "ガチアサリ"
}

MODE_DICT = {
    "regular": "レギュラーマッチ",
    "xmatch": "Xマッチ",
    "open": "バンカラマッチ オープン",
    "challenge": "バンカラマッチ チャレンジ",
    "league": "リーグマッチ",
    "coop": "サーモンラン"
}

# TODO: Add color codes of different battle modes
COLOR_DICT = {
    "regular": "",
    "xmatch": "",
    "open": "",
    "challenge": "",
    "league": "",
    "coop": "",
}

BACKGROUND_COLOR = (0, 0, 0, 255)


def load_web_image(url):
    '''Fetches web image by GET request and returns it in opencv-format.'''
    response = requests.get(url, stream=True).raw
    image = np.asarray(bytearray(response.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)

    # opencv -> PIL
    image_pil = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
    image_pil = Image.fromarray(image_pil)

    # add background color
    background = Image.new("RGBA", image_pil.size, BACKGROUND_COLOR)
    image_bg = Image.alpha_composite(background, image_pil)

    # PIL -> opencv
    image_cv = np.array(image_bg, dtype=np.uint8)
    image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGBA2BGRA)

    return image_cv


def horizontal_concat_images(urls):
    '''Concatenates images horizontally and returns concatenated image.'''
    images = []
    for url in urls:
        image = load_web_image(url)
        images.append(image)
    images_concat = cv2.hconcat(images)
    return images_concat


def vertical_concat_images(urls):
    '''Concatenates images vertically and returns concatenated image.'''
    images = []
    for url in urls:
        image = load_web_image(url)
        images.append(image)
    images_concat = cv2.vconcat(images)
    return images_concat


def vertical_concat_images_coop(img1, img2):
    '''Concatanates two images vertically with different width.'''
    width1 = img1.shape[1]
    width2 = img2.shape[1]
    factor = width2 / width1
    img1 = cv2.resize(img1, dsize=None, fx=factor, fy=factor)
    images_concat = cv2.vconcat([img1, img2])
    return images_concat


def concat_images_coop(weapon_urls, stage_url):
    '''Concatenates weapons' images and stage image for salmon run and returns concatenated image.'''
    weapons_image = horizontal_concat_images(weapon_urls)
    stage_image = load_web_image(stage_url)
    coop_image = vertical_concat_images_coop(weapons_image, stage_image)
    return coop_image


def concat_images_gear(power_urls, gear_url):
    power_image = horizontal_concat_images(power_urls)

    # gear power image size is 100x100
    img_black = Image.new("RGBA", (100, 100), BACKGROUND_COLOR)
    img_black = np.array(img_black, dtype=np.uint8)
    img_black = cv2.cvtColor(img_black, cv2.COLOR_RGBA2BGRA)

    for _ in range(4 - len(power_urls)):
        power_image = cv2.hconcat([power_image, img_black])
    gear_image = load_web_image(gear_url)
    concat_image = vertical_concat_images_coop(power_image, gear_image)
    return concat_image


def embed_set_images_from_urls(urls, embed):
    '''Sets concatenated image to embed from image urls.'''
    image_concat = horizontal_concat_images(urls)
    embed, file = embed_set_image(image_concat, embed)
    return embed, file


def embed_set_image(image, embed):
    '''Sets concatenated image to embed.'''
    file_name = "image_concat.png"
    cv2.imwrite(file_name, image)
    file = discord.File(file_name, filename=file_name)
    embed.set_image(url=f"attachment://{file_name}")
    return embed, file


def battle_stage_embed_format(mode, schedule):
    '''Generates one embed message for one battle schedule.'''
    time_str = schedule.start.strftime("%-m月%-d日 %-H:%Mから")
    embed = discord.Embed(title=f"{MODE_DICT[mode]} {time_str}")
    embed.add_field(name="ルール", value=schedule.rule, inline=True)
    embed.add_field(name="ステージ", value=f"{schedule.stages[0]}　　{schedule.stages[1]}", inline=False)
    image_urls = [schedule.stages[i].image for i in range(2)]
    embed, file = embed_set_images_from_urls(image_urls, embed)
    return embed, file


def stage_embed_format_prev(mode, embed, schedules):
    '''Deprecated'''
    if mode == 'battle':
        for schedule in schedules:
            embed.add_field(name="日時", value=schedule.start.strftime("%-m月%-d日 %-H:%Mから"), inline=False)
            embed.add_field(name="ルール", value=schedule.rule, inline=True)
            embed.add_field(name="ステージ", value=f"{schedule.stages[0]}\n{schedule.stages[1]}", inline=True)
            images_urls = [schedule.stages[i].image for i in range(2)]
            embed, file = embed_set_images_from_urls(images_urls, embed)
            # embed.set_image(url=schedule.stages[0].image)
    return embed, file


def coop_stage_embed_format(mode, schedule):
    '''Generates one embed message for one salmon run schedule.'''
    embed = discord.Embed(title=f"{MODE_DICT[mode]}")
    time_str = schedule.start.strftime("%-m月%-d日 %-H:%Mから") + " " + schedule.end.strftime("%-m月%-d日 %-H:%Mまで")
    embed.add_field(name="日時", value=time_str, inline=False)
    embed.add_field(name="ステージ", value=schedule.stage, inline=False)
    embed.add_field(name="ブキ", value=f"{schedule.weapons[0]}\n{schedule.weapons[1]}\n{schedule.weapons[2]}\n{schedule.weapons[3]}", inline=False)
    weapon_image_urls = [schedule.weapons[i].image for i in range(4)]
    stage_image_url = schedule.stage.image
    coop_image = concat_images_coop(weapon_image_urls, stage_image_url)
    embed, file = embed_set_image(coop_image, embed)
    return embed, file


def coop_stage_embed_format_prev(mode, embed, schedules):
    '''Deprecated'''
    if mode == 'coop':
        for schedule in schedules:
            time_str = schedule.start.strftime("%-m月%-d日 %-H:%Mから") + schedule.end.strftime("%-m月%-d日 %-H:%Mまで")
            embed.add_field(name="日時", value=time_str, inline=False)
            embed.add_field(name="ステージ", value=schedule.stage, inline=False)
            embed.add_field(name="ブキ", value=f"{schedule.weapons[0]}\n{schedule.weapons[1]}\n{schedule.weapons[2]}\n{schedule.weapons[3]}", inline=True)
            embed.set_image(url=schedule.stage.image)

    return embed


def gear_embed_format(embed, gear):
    '''Generate one embed message for one gear.'''
    embed.add_field(name="残り時間", value=f"あと{gear.left_time}", inline=True)
    embed.add_field(name="ブランド", value=gear.brand, inline=True)
    embed.add_field(name="値段", value=gear.price, inline=True)
    embed.add_field(name="ギアパワー", value=gear.main_power, inline=True)
    embed.add_field(name="スロット数", value=gear.slot, inline=True)
    gear_power_image_urls = [gear.main_power.image] + [gear.sub_power.image for _ in range(gear.slot)]
    gear_image_url = gear.info.image
    gear_image = concat_images_gear(gear_power_image_urls, gear_image_url)
    embed, file = embed_set_image(gear_image, embed)
    return embed, file


def xranking_embed_format(embed, ranking):
    for player in ranking:
        embed.add_field(name="", value=player, inline=False)
    return embed
