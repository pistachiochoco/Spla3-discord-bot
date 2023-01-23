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

def stage_embed_format(mode, embed, schedules):
    if mode == 'battle':
        for schedule in schedules:
            embed.add_field(name="日時", value=schedule.start.strftime("%-m月%-d日 %-H:%Mから"), inline=False)
            embed.add_field(name="ルール", value=schedule.rule, inline=True)
            embed.add_field(name="ステージ", value=f"{schedule.stages[0]}\n{schedule.stages[1]}", inline=True)
            embed.set_image(url=schedule.stages[0].image)

    if mode == 'coop':
        for schedule in schedules:
            time_str = schedule.start.strftime("%-m月%-d日 %-H:%Mから") + schedule.end.strftime("%-m月%-d日 %-H:%Mまで")
            embed.add_field(name="日時", value=time_str, inline=False)
            embed.add_field(name="ステージ", value=schedule.stage, inline=False)
            embed.add_field(name="ブキ", value=f"{schedule.weapons[0]}\n{schedule.weapons[1]}\n{schedule.weapons[2]}\n{schedule.weapons[3]}", inline=True)
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


def xranking_embed_format(embed, ranking):
    for player in ranking:
        embed.add_field(name="", value=player, inline=False)
    return embed