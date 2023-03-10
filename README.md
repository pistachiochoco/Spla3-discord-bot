# Spla3 Discord Bot
This discord bot is designed to fetch information from Splatoon3 API inside Nintendo Switch Online App which only 
available on mobile. It can provide real-time battle schedules, salmon run schedules, sale gears and x-ranking.

## Setup
- In /Spla3bot, create a file with filename `".env"` and paste your discord bot token in this form:
  - `DISCORD_TOKEN = "your discord bot token"`
- In /Spla3API, paste your session token after `"session_token":`. 
([How to generate a session token?](https://github.com/pistachiochoco/NSO-API-for-Spla3#2-get-a-session-token))


## Usage 
### Slash commands (prefix `/`)
#### Fetch battle schedules by time (時間順)
- Regular Match(レギュラーマッチ): `/regular <number>`
- Bankara Match(バンカラマッチ):
  - Challenge(チャレンジ): `/challenge <number>`
  - Open(オープン): `/open <number>`
- X Match(Xマッチ): `/xmatch <number>`
- League Match(リーグマッチ): `/league <number>`
  - Not implemented in game now
- Fes Match(フェスマッチ): `/fes <number>`
  - will also return tricolor stage(トリカラのステージ)

`<number>` is a required argument which means the number of schedules it will return. The maximum of this value is `12`.
<br><br>

#### Fetch battle schedules by rule (ルール別)
- Splat Zones(ガチエリア): `/area <mode>`
- Tower Control(ガチヤグラ): `/yagura <mode>`
- Rainmaker(ガチホコバトル): `/hoko <mode>`
- Clam Blitz(ガチアサリ): `/asari <mode>`

`<mode>`: The mode values supported are `xmatch`, `open`, `challenge`, `league`.<br><br>

#### Fetch salmon-run schedules by time (時間順)
- Salmon Run(サーモンラン): `/salmon <number>`

`<number>`: The maximum of this value is `5`.
<br><br>

#### Fetch sale gear(ゲソタウン)
- All sale gears: `/gear`
<br><br>

#### Fetch X-ranking (only top 25 available for now)
- X-ranking: `/xrank <rule>, <number>`

`<rule>`: The rule values supported are `area`(エリア), `tower`(ヤグラ), `rainmaker`(ホコ), `clam`(アサリ).<br>
`<number>`: The maximum of this value is `25`.
<br><br>

### Commands with prefix `?`
#### Fetch battle schedules by time (時間順)
- Regular Match(レギュラーマッチ): `?regular <number(optional, default=3)>`
- Bankara Match(バンカラマッチ):
  - Challenge(チャレンジ): `?challenge <number(optional, default=3)>`
  - Open(オープン): `?open <number(optional, default=3)>`
- X Match(Xマッチ): `?xmatch <number(optional, default=3)>`
- League Match(リーグマッチ): `?league <number(optional, default=3)>`
  - Not implemented in game now

`<number>` is an optional argument, the default value is 3 which means if you send `?open`, it will return recent 3 
schedules by time.<br> If you send  `?open 5`, it will return recent 5 schedules by time.<br>

#### Fetch battle schedules by rule (ルール別)
- Splat Zones(ガチエリア): `?area <mode(optional, default=xmatch)>`
- Tower Control(ガチヤグラ): `?yagura <mode(optional, default=xmatch)>`
- Rainmaker(ガチホコバトル): `?hoko <mode(optional, default=xmatch)>`
- Clam Blitz(ガチアサリ): `?asari <mode(optional, default=xmatch)>`

`<mode>` is an optional argument, the default value is `xmatch` which means it will return X Match schedules of the 
input rule. If you send `?area`, it will return all available Splat Zones schedules of X Match by time. If you want to
know Splat Zones of Bankara Match Challenge, you can send command `?area challenge`. <br>
The mode values supported are `xmatch`, `open`, `challenge`, `league`.<br>

#### Fetch salmon-run schedules by time (時間順)
- Salmon Run(サーモンラン): `?salmon <number(optional, default=1)>`

#### Fetch sale gear(ゲソタウン)
- All sale gears: `?gear`

#### Fetch X-ranking (only top 25 available for now)
- X-ranking: `?xrank <rule(optional, default=ALL)>, <number(optional, default=10)>`

`<rule>` is an optional argument, the default value is `ALL` which means it will return X-ranking of all rules. <br>
The rule values supported are `area`(エリア), `tower`(ヤグラ), `rainmaker`(ホコ), `clam`(アサリ).<br>
`<number>` is an optional argument, the default value is 10 which means if you send `?xrank`, it will return top 10 
players of each rule.






## Demo
### Slash command (save data locally)
[demo video3.mp4](https://user-images.githubusercontent.com/85484153/216977236-2ea39b93-8e23-4151-8cb3-725274d78424.mp4)

### Slash command
[demo video2.mp4](https://user-images.githubusercontent.com/85484153/216753490-572b4239-5e8e-4463-8741-0cc63be143b5.mp4)

### Previous
[demo video.mp4](https://user-images.githubusercontent.com/85484153/214571258-cee6e87e-a4c0-4b99-ba22-f289a5119315.mp4)

<br>

## TODOs
1. Make query utils applicable ~~for Fest(2.11~2.13) and~~ Big Run(???)
2. Find a way to make this bot always online
3. ~~The validity period of tokens of spla3 API is 2 hours so generating tokens every 2 hours rather than generating 
tokens when send commands may make bot response faster(?)~~ `tasks.look()`
~~or saving schedules every 2 hours and reading data locally may be faster(?)~~
4. ~~find which process is slow~~(?)
