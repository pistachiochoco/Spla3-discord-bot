import cv2
import io
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


def load_web_image_prev(url):
    '''
    Deprecated.
    Fetches web image by GET request and returns it in opencv-format.
    '''
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


def load_web_image(url):
    '''Fetches web image by GET request and returns it in pillow-format.'''
    response = requests.get(url, stream=True)
    image = Image.open(io.BytesIO(response.content))
    background = Image.new("RGBA", image.size, BACKGROUND_COLOR)
    image = Image.alpha_composite(background, image)

    return image


def horizontal_concat_images_prev(urls):
    '''
    Deprecated.
    Concatenates images horizontally and returns concatenated image.
    '''
    images = []
    for url in urls:
        image = load_web_image(url)
        images.append(image)
    images_concat = cv2.hconcat(images)
    return images_concat


def horizontal_concat_images(urls):
    '''Concatenates images horizontally and returns concatenated image.'''
    images = []
    concat_image_width, concat_image_height = 0, 0
    for url in urls:
        image = load_web_image(url)
        images.append(image)
        concat_image_width += image.width
        concat_image_height = max(concat_image_height ,image.height)
    concat_image = Image.new("RGBA", (concat_image_width, concat_image_height))
    curr_width = 0
    for image in images:
        concat_image.paste(image, (curr_width, 0))
        curr_width += image.width
    return concat_image


def vertical_concat_images_prev(urls):
    '''
    Deprecated.
    Concatenates images vertically and returns concatenated image.
    '''
    images = []
    for url in urls:
        image = load_web_image(url)
        images.append(image)
    images_concat = cv2.vconcat(images)
    return images_concat


def vertical_concat_images(urls):
    '''Concatenates images vertically and returns concatenated image.'''
    images = []
    concat_image_width, concat_image_height = 0, 0
    for url in urls:
        image = load_web_image(url)
        images.append(image)
        concat_image_width = max(concat_image_width ,image.width)
        concat_image_height += image.height
    concat_image = Image.new("RGBA", (concat_image_width, concat_image_height))
    curr_height= 0
    for image in images:
        concat_image.paste(image, (0, curr_height))
        curr_height += image.width
    return concat_image


def vertical_concat_images_coop_prev(img1, img2):
    '''
    Deprecated.
    Concatanates two images vertically with different width.
    '''
    width1 = img1.shape[1]
    width2 = img2.shape[1]
    factor = width2 / width1
    img1 = cv2.resize(img1, dsize=None, fx=factor, fy=factor)
    images_concat = cv2.vconcat([img1, img2])
    return images_concat


def vertical_concat_images_coop(img1, img2):
    '''Concatanates two images vertically with different width.'''
    factor = img2.width / img1.width
    img1 = img1.resize((img2.width, int(img1.height * factor)))
    concat_image = Image.new("RGBA", (img1.width, img1.height + img2.height))
    concat_image.paste(img1, (0, 0))
    concat_image.paste(img2, (0, img1.height))
    return concat_image


def concat_images_coop(weapon_urls, stage_url):
    '''Concatenates weapons' images and stage image for salmon run and returns concatenated image.'''
    weapons_image = horizontal_concat_images(weapon_urls)
    stage_image = load_web_image(stage_url)
    coop_image = vertical_concat_images_coop(weapons_image, stage_image)
    return coop_image


def concat_images_gear_prev(power_urls, gear_url):
    '''Deprecated.'''
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


def concat_images_gear(power_urls, gear_url):
    '''Generate gear image with main power image and gear image.'''
    power_image = horizontal_concat_images(power_urls)
    power_image_size = power_image.height

    # gear power image size is 100x100
    img_black = Image.new("RGBA", (power_image_size * 4, power_image_size), BACKGROUND_COLOR)
    img_black.paste(power_image, (0, 0))

    gear_image = load_web_image(gear_url)
    concat_image = vertical_concat_images_coop(gear_image, img_black)
    return concat_image


def embed_set_images_from_urls(urls, embed):
    '''Sets concatenated image to embed from image urls.'''
    image_concat = horizontal_concat_images(urls)
    embed, file = embed_set_image(image_concat, embed)
    return embed, file


def embed_set_image(image, embed):
    '''Sets concatenated image to embed.'''
    file_name = "image_concat.png"
    # cv2.imwrite(file_name, image)
    image.save(file_name)
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

# for test
if __name__ == '__main__':
    url = "https://api.lp1.av5ja.srv.nintendo.net/resources/prod/skill_img/aaa9b7e95a61bfd869aaa9beb836c74f9b8d4e5d4186768a27d6e443c64f33ce_0.png?Expires=1704844800&Signature=SHgU8h1htngLkcrajryd~JMDuf5mOtXkOhf1FLTXFo9RXBT5LQH0IbVzplW03liu9V1MQTvSrqyt2QTqyPKg3i~BAQLvGvbu6tZV7nl2lwGhUmM8M-qEWwmyYgDtIz33kG8lBagBE35UGky87TX86Z325CnVJvYkifmiKIeUN7M6V3YjwUlgDRnLP0~GWKrIG6HVbGXXUkqYD8tGTDhQ9uV5yfa5pIqOwMWbHEqZtVCwqRoa~yv4k9WADkBAcDATgP-7yhLOZWzyNcp1xJO-yKjh7MG83S-g3p8DW3RZL3hv~7zpy0SS7R6e5N5Hju2RQPL-nSmGW3IhrgsawMrHyA__&Key-Pair-Id=KNBS2THMRC385"
    urls = [url, url]
    img1 = load_web_image(url)
    img2 = horizontal_concat_images(urls)
    img3 = vertical_concat_images(urls)
    img4 = vertical_concat_images_coop(img2, img1)
    gear = "https://api.lp1.av5ja.srv.nintendo.net/resources/prod/gear_img/a7f88319920704c32079b9246bbbd1be236e456f6d780a8e23bef96e49db956f_0.png?Expires=1704844800&Signature=i-EvO6pBDOLq7Or62TnqcBP7UCFeFKocVqPjt7oImdbH2ZrPiUy1fdR6Mh5JjLBkuwbyGEv7v5k3lf6ps2qp8LO6iynUx0hzfZgymMQQ9H5tcEj3UWIFZaT6zpHYHUBdt3Br7nyMyr-IIt6zDDH97Sy5ERV7gYAmu-I62d7oV2dJn8qFML~jjVhEhb7m9BOLs0HVLVcU~veEDddvXpGKmyRYK3PAw4VwN4H9HN8A-i9WtWWpv7iHkRU6Cam3k8sSAY~BQtncXfx7EIKJ9oCGqemNW8tBugvz-748PEM~O8xQhc5me9uUL0QUKlR6xon0wFHoBZMRJfsgQvx5XIKGUg__&Key-Pair-Id=KNBS2THMRC385"
    img5 = concat_images_gear(urls, gear)
    print(img5.size)
    img5.show()

