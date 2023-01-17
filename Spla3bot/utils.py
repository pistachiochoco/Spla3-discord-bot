import os, json
self_path = os.path.dirname(__file__)

def load_token():
    config_path = os.path.join(self_path, 'config.txt')
    config_file = open(config_path, "r")
    config_data = json.load(config_file)
    config_file.close()
    token = config_data["token"]

    return token


def stage_embed_format(mode, embed, schedules):
    if mode == 'battle':
        for schedule in schedules:
            embed.add_field(name="日時", value=schedule.start.strftime("%-m月%-d日 %-H:%Mから"), inline=False)
            embed.add_field(name="ルール", value=schedule.rule, inline=True)
            embed.add_field(name="ステージ", value=f"{schedule.stages[0]}　{schedule.stages[1]}", inline=True)
            embed.set_image(url=schedule.stages[0].image)

    if mode == 'coop':
        for schedule in schedules:
            embed.add_field(name="日時", value=schedule.start.strftime("%-m月%-d日 %-H:%Mから"), inline=False)
            embed.add_field(name="ステージ", value=schedule.stage, inline=False)
            embed.add_field(name="ブキ", value=f"{schedule.weapons[0]}　{schedule.weapons[1]}　{schedule.weapons[2]}　{schedule.weapons[3]}", inline=True)
            embed.set_image(url=schedule.stage.image)

    return embed


def gear_embed_format(embed, gear):
    embed.add_field(name="", value=f"あと{gear.left_time}", inline=True)
    embed.add_field(name="ブランド", value=gear.brand, inline=True)
    embed.add_field(name="値段", value=gear.price, inline=True)
    embed.add_field(name="ギアパワー", value=gear.main_power, inline=True)
    embed.add_field(name="スロット数", value=gear.slot, inline=True)
    embed.set_image(url=gear.info.image)
    return embed
