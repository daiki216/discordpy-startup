# coding=utf-8
# Discord BOT "キメキメくん" ver3.70
# Author : daiki, 2BASA, すなぎも

import sys
import discord  # ディスコード専用関数
import random  # ランダム関数
import gspread  # スプレッドシート関数
# ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials

# 画像処理関連 v3.60から pipでPillowのインストール必須 参考:https://note.nkmk.me/python-pillow-basic/
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

# システム処理関連 主にコンソール画面操作やファイル操作 v3.60から
import os

# おまじないのようなもの
client = discord.Client()

# コース一覧
course_list = [
    "<:01_CrashCove:620475267952934922> タスマニアだいばくそう(Crash Cove)",
    "<:02_MysteryCaves:620479219637682186> カメカメせいてつじょ(Mystery Caves)",
    "<:03_SewerSpeedway:620481967028174858> ハイスピードちかすいどう(Sewer Speedway)",
    "<:04_RoosTubes:620493023167643649> ホネホネかいていトンネル(Roo's Tubes)",
    "<:05_SlideColiseum:620495681064534026> ドリフトスペシャルアリーナ(Slide Coliseum)",
    "<:06_TurboTrack:620498386633621514> ターボスペシャルアリーナ(Turbo Track)",
    "<:07_CocoPark:620516814287274005> ココ・デ・サーキット(Coco Park)",
    "<:08_TigerTemple:620523832121491466> あめふりボワボワいせき(Tiger Temple)",
    "<:09_PapusPyramid:620528688093724682> ひとくいばなテンプル(Papu's Pyramid)",
    "<:10_DingoCanyon:620530704467492864> かっとびアルマジロけいこく(Dingo Canyon)",
    "<:11_PolarPass:620781435300610049> どっきり！カチカチパパぐま(Polar Pass)",
    "<:12_TinyArena:620781459430572045> スーパーどろぬまアリーナ(Tiny Arena)",
    "<:13_DragonMines:620781481035431956> はぐるまトロッコこうざん(Dragon Mines)",
    "<:14_BlizzardBluff:620781505525972992> ゆきやまおおいわサーキット(Blizzard Bluff)",
    "<:15_HotAirSkyway:620788164390289419> つぎはぎスカイウェイ(Hot Air Skyway)",
    "<:16_CortexCastle:620788191758254100> クモクモキャッスル(Cortex Castle)",
    "<:17_NGinLabs:620788210871697427> スーパーかそくトンネル(N.Gin Labs)",
    "<:18_OxideStation:620788253695410197> むじゅうりょくステーション(Oxide Station)",
    "<:19_InfernoIsland:620799723103584256> あつあつインフェルノしま(Inferno Island)",
    "<:20_JungleBoogie:620799747719954482> ジャングル・ブギ(Jungle Boogie)",
    "<:21_ClockworkWumpa:620799766674276353> はぐるまとけいとう(Clockwork Wumpa)",
    "<:22_AndroidAlley:620799785800302592> こちらロボットよこちょう(Android Alley)",
    "<:23_ElectronAvenue:620812240743825418> ハイパージャンプ＆ブースト(Electron Avenue)",
    "<:24_DeepSeaDriving:620812274508234752> ぶっとびしんかいドライブ(Deep Sea Driving)",
    "<:25_ThunderStruck:620812298805575690> あめのスカイサーキット(Thunder Struck)",
    "<:26_TinyTemple:620812318871257089> タイニーのおてら(Tiny Temple)",
    "<:27_MeteorGorge:620835108517314583> ゆきふりメテオきょうこく(Meteor Gorge)",
    "<:28_BarinRuins:620835131556626452> はっくつバリンいせき(Barin Ruins)",
    "<:29_OutOfTime:620835140771512371> いけいけとけいロード(Out of Time)",
    "<:30_AssemblyLane:620835150674133032> モクモクくみたてこうじょう(Assembly Lane)",
    "<:31_HyperSpaceway:620840655924756489> ギャラクシーハイウェイ(Hyper Spaceway)",
    "<:32_TwilightTour:620840669975543820> トワイライトツアー(Twilight Tour)",
    "<:33_PrehistoricPlayground:620840679035371522> こだいのあそびば(Prehistoric Playground)",
    "<:34_SpyroCircuit:620840688698785792> スパイロサーキット(Spyro Circuit)",
    "<:36_NinasNightmare:629138176149028884> ニーナのあくむ(Nina’s Nightmare)",
    "<:38_KoalaCarnival:642620305751277578> コアラカーニバル(Koala Carnival)",
    "<:39_GingerbreadJoyride:654897169240817665> ジングルクッキーロード(Gingerbread Joyride)",
    "<:40_MegamixMania:668788996368760842> メガミックスマニア(Megamix Mania)"
]

# コース一覧（コイン多め）
course_coin_list = [
    "<:11_PolarPass:620781435300610049> どっきり！カチカチパパぐま(Polar Pass)",
    "<:12_TinyArena:620781459430572045> スーパーどろぬまアリーナ(Tiny Arena)",
    "<:15_HotAirSkyway:620788164390289419> つぎはぎスカイウェイ(Hot Air Skyway)",
    "<:16_CortexCastle:620788191758254100> クモクモキャッスル(Cortex Castle)",
    "<:17_NGinLabs:620788210871697427> スーパーかそくトンネル(N.Gin Labs)",
    "<:18_OxideStation:620788253695410197> むじゅうりょくステーション(Oxide Station)",
    "<:21_ClockworkWumpa:620799766674276353> はぐるまとけいとう(Clockwork Wumpa)",
    "<:22_AndroidAlley:620799785800302592> こちらロボットよこちょう(Android Alley)",
    "<:23_ElectronAvenue:620812240743825418> ハイパージャンプ＆ブースト(Electron Avenue)",
    "<:25_ThunderStruck:620812298805575690> あめのスカイサーキット(Thunder Struck)",
    "<:29_OutOfTime:620835140771512371> いけいけとけいロード(Out of Time)",
    "<:30_AssemblyLane:620835150674133032> モクモクくみたてこうじょう(Assembly Lane)",
    "<:31_HyperSpaceway:620840655924756489> ギャラクシーハイウェイ(Hyper Spaceway)",
    "<:32_TwilightTour:620840669975543820> トワイライトツアー(Twilight Tour)",
    "<:33_PrehistoricPlayground:620840679035371522> こだいのあそびば(Prehistoric Playground)"
]

# 2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
# 認証情報設定
# ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
credentials = ServiceAccountCredentials.from_json_keyfile_name('discord-bot-eac74959e94c.json', scope)
# OAuth2の資格情報を使用してGoogle APIにログインします。
gc = gspread.authorize(credentials)
# 共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
SPREADSHEET_KEY = '15GGX1iQt5bR8DX_c00gYq6j2z9zGJy42r421Xf3HIK0'
# 共有設定したスプレッドシートを開く
workbook = gc.open_by_key(SPREADSHEET_KEY)
sheet_data = workbook.worksheet("データ")

# チーム戦参加者
entry_dict = {}

# チームメンバー
team1_dict = {}
team2_dict = {}
team1_list = []
team2_list = []

# タッグ戦チームメンバー
tag_team_dict = {}


################################################################
# メイン関数
################################################################


########################
# ログイン時のイベント    #
########################
@client.event
async def on_ready():
    """
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    """

    print('----------------------------------')
    # print("Running File Update Time")
    # print("\t" + str(datetime.datetime.fromtimestamp(os.path.getmtime(__file__))))
    # print("Now Time")
    # print("\t" + str(datetime.datetime.now()))
    # print("")
    print("discord.py Verion")
    print("\t" + discord.__version__)
    print("")
    print('Logged in as')
    print("\tName\t" + str(client.user.name))
    print("\tID\t" + str(client.user.id))
    print('----------------------------------')

    # 「●●をプレイ中」を表示
    activity = discord.Activity(name='Crash Team Racing', type=discord.ActivityType.playing)
    await client.change_presence(activity=activity)


##############################
# メッセージ送信時のイベント     #
##############################
@client.event
async def on_message(message):
    ###
    # BOTの発言だった場合何もしない
    ###
    if message.author.bot:
        return

    ###
    # メッセージの最初が"!test"の処理
    ###
    if message.content.startswith("!test"):
        send_message = "テストメッセージです"
        await message.channel.send(send_message)

    ###
    # メッセージの最初が"!ver"の処理
    ###
    if message.content.startswith("!ver"):
        send_message = "discord.py : " + discord.__version__ + "\n"
        send_message += "gspread : " + gspread.__version__ + "\n"
        await message.channel.send(send_message)

    ###
    # メッセージが"!view"の処理
    # コース一覧を順番通りに出力
    ###
    if message.content == "!view":
        await send_message_from_list(message, course_list)

    ###
    # メッセージの最初が"!select/"の処理
    ###
    if message.content.startswith("!select/"):
        command = message.content.split("/")
        # ■allのとき
        if command[1] == "all":
            await select_all(message)
        # ■数字のとき
        elif command[1].isdecimal():
            await select_num(message, int(command[1]))
        # ■resetのとき
        elif command[1] == "reset":
            await select_reset(message)
        # ■coinのとき
        elif command[1] == "coin":
            await select_coin(message)
        # ■その他のとき
        else:
            await message.channel.send("/ の後には1～" + str(len(course_list)) + "の整数を入力してね")

    ###
    # メッセージが"!member"の処理
    # 現在登録されているメンバーを表示
    ###
    if message.content == "!member":
        await message.channel.send("参加者 - " + str(entry_dict))

    ###
    # メッセージの最初が"!regist/"の処理
    # 参加者登録を行う
    ###
    if message.content.startswith("!regist/"):
        entry_list = message.content.split("/")
        entry_list.remove("!regist")
        print("!regist/前 参加者 - " + str(entry_dict))
        for entry in entry_list:
            entry_category = entry.split(",")
            entry_dict[entry_category[0]] = entry_category[1]
        await message.channel.send("参加者 - " + str(entry_dict))
        print("!regist/後 参加者 - " + str(entry_dict))

    ###
    # メッセージが"!clear"の処理
    # 参加者リストを初期化する
    ###
    if message.content == "!clear":
        entry_dict.clear()
        await message.channel.send("参加者リストを初期化したよ")

    ###
    # メッセージが"!kouhaku"の処理
    # 参加者リストをもとに実力が均等になるようなチーム分けをする
    # 参加者が9名以上の場合待機者が表示される
    ###
    if message.content == "!kouhaku":
        await kouhaku(message)

    ###
    # メッセージが"!tag"の処理
    # 参加者リストをもとに実力が均等になるようなチーム分けをする
    # 参加者が9名以上の場合待機者が表示される
    ###
    if message.content == "!tag":
        await tag(message)

    ###
    # メッセージの最初が"!exit/"の処理
    # mチームからn人を抽選して表示する
    ###
    if message.content.startswith("!exit/"):
        exit_parameter = message.content.split("/")[1].split(",")
        await exit_member(message, exit_parameter[0], exit_parameter[1])

    ###
    # BOT向けのメンションが送られた際の処理
    # 選択肢を表示する
    ###
    if message.content.startswith('<:37_CrashBandicoot:634559192178360370>'):

        reac_emoji = list()
        reac_emoji.append(chr(0x0031) + chr(0x20E3))
        reac_emoji.append(chr(0x0032) + chr(0x20E3))
        reac_emoji.append(chr(0x0033) + chr(0x20E3))
        reac_emoji.append(chr(0x0034) + chr(0x20E3))
        reac_emoji.append(chr(0x0035) + chr(0x20E3))

        msg = await message.channel.send(
            "コマンドを選んでね\n" +
            reac_emoji[0] + " all（全コースランダム表示）\n" +
            reac_emoji[1] + " Nコース（数を指定してランダム表示）\n" +
            reac_emoji[2] + " coin（コイン稼ぎコースランダム表示）\n" +
            reac_emoji[3] + " reset（Nコースの選択状況をリセット）\n" +
            reac_emoji[4] + " team（チーム戦コマンド呼び出し）")

        for add_emoji in reac_emoji:
            await msg.add_reaction(add_emoji)

        reaction, user = await wait_for_reaction_add(message, reac_emoji)

        # 1 (all) のとき
        if str(reaction.emoji) == (reac_emoji[0]):
            await select_all(message)

        # 2 (Nコース) のとき
        elif str(reaction.emoji) == (reac_emoji[1]):
            await message.channel.send("コース数を入力してね(1~" + str(len(course_list)) + ")")

            def num_check(num_msg):
                return (not num_msg.author.bot) and num_msg.author == message.author

            num_msg = await client.wait_for('message', check=num_check)
            if num_msg.content.isdigit():
                await select_num(message, int(num_msg.content))
            elif not num_msg.content.startswith("!"):
                # !から始まるときは数字を入力する前に別のコマンドが打たれたということなので何もしない
                await message.channel.send("数字以外が入力されているよ")

        # 3 (coin) のとき
        elif str(reaction.emoji) == (reac_emoji[2]):
            await select_coin(message)

        # 4 (reset) のとき
        elif str(reaction.emoji) == (reac_emoji[3]):
            await select_reset(message)

        # 5 (team) のとき
        elif str(reaction.emoji) == (reac_emoji[4]):

            reac_emoji_team = list()
            reac_emoji_team.append(chr(0x0031) + chr(0x20E3))
            reac_emoji_team.append(chr(0x0032) + chr(0x20E3))
            reac_emoji_team.append(chr(0x0033) + chr(0x20E3))

            msg = await message.channel.send(
                "チーム戦コマンドを選んでね\n" +
                reac_emoji_team[0] + " 参加登録・チーム分け\n" +
                reac_emoji_team[1] + " 離脱者選択\n" +
                reac_emoji_team[2] + " クラス登録・変更\n")

            for add_emoji in reac_emoji_team:
                await msg.add_reaction(add_emoji)

            reaction, user = await wait_for_reaction_add(message, reac_emoji_team)

            # 1 (参加登録・チーム分け) のとき
            if str(reaction.emoji) == reac_emoji_team[0]:
                entry_dict.clear()

                reac_emoji_member = list()
                reac_emoji_member.append(chr(0x270B))
                reac_emoji_member.append(chr(0x0031) + chr(0x20E3))
                reac_emoji_member.append(chr(0x0032) + chr(0x20E3))

                msg = await message.channel.send(
                    "参加者うけつけちゅ～\n" +
                    reac_emoji_member[0] + " 参加\n" +
                    reac_emoji_member[1] + " 紅白戦チーム分け開始\n" +
                    reac_emoji_member[2] + " タッグ戦チーム分け開始")

                for add_emoji in reac_emoji_member:
                    await msg.add_reaction(add_emoji)

                msg_entry = await message.channel.send("参加者 - ")
                while True:

                    reaction, user = await wait_for_reaction_add(message, reac_emoji_member, False)

                    # "参加"のとき
                    if str(reaction.emoji) == reac_emoji_member[0]:
                        try:
                            cell = sheet_data.find(str(user.id))
                        except gspread.exceptions.APIError as e:
                            print(e)
                            gc.login()
                            cell = sheet_data.find(str(user.id))
                        name = sheet_data.cell(cell.row, cell.col + 1).value
                        rank = sheet_data.cell(cell.row, cell.col + 2).value
                        if name == "" or rank == "":
                            await message.channel.send("スプレッドシートに登録されていないよ")
                        else:
                            entry_dict[name] = rank

                            send_message = "参加者 - " + str(len(entry_dict)) + "人\n"

                            for mystr in entry_dict:
                                send_message += "　" + mystr + "(" + entry_dict[mystr] + ")" + "\n"

                            await msg_entry.edit(content=send_message)

                    # "紅白戦チーム分け開始"のとき
                    elif str(reaction.emoji) == reac_emoji_member[1]:
                        await kouhaku(message)
                        break

                    # "紅白戦チーム分け開始"のとき
                    elif str(reaction.emoji) == reac_emoji_member[2]:
                        await tag(message)
                        break

            # 2 (離脱者選択) のとき
            elif str(reaction.emoji) == reac_emoji_team[1]:
                reac_emoji_team_choice = list()
                reac_emoji_team_choice.append(chr(0x0031) + chr(0x20E3))
                reac_emoji_team_choice.append(chr(0x0032) + chr(0x20E3))

                msg = await message.channel.send("どっちのチーム？")

                for add_emoji in reac_emoji_team_choice:
                    await msg.add_reaction(add_emoji)

                reaction, user = await wait_for_reaction_add(message, reac_emoji_team_choice)

                exit_team = "0"
                # 1のとき
                if str(reaction.emoji) == (reac_emoji_team_choice[0]):
                    exit_team = "1"
                # 2のとき
                elif str(reaction.emoji) == (reac_emoji_team_choice[1]):
                    exit_team = "2"

                reac_emoji_secede = list()
                reac_emoji_secede.append(chr(0x0031) + chr(0x20E3))
                reac_emoji_secede.append(chr(0x0032) + chr(0x20E3))
                reac_emoji_secede.append(chr(0x0033) + chr(0x20E3))

                msg = await message.channel.send("離脱する人数は？")

                for add_emoji in reac_emoji_secede:
                    await msg.add_reaction(add_emoji)

                reaction, user = await wait_for_reaction_add(message, reac_emoji_secede)

                exit_num = "0"
                # 1のとき
                if str(reaction.emoji) == (reac_emoji_secede[0]):
                    exit_num = "1"
                # 2のとき
                elif str(reaction.emoji) == (reac_emoji_secede[1]):
                    exit_num = "2"
                # 3のとき
                elif str(reaction.emoji) == (reac_emoji_secede[2]):
                    exit_num = "3"
                await exit_member(message, exit_team, exit_num)

            # 3 (クラス登録・変更) のとき
            elif str(reaction.emoji) == (reac_emoji_team[2]):
                try:
                    cell = sheet_data.find(str(user.id))
                except gspread.exceptions.APIError as e:
                    print(e)
                    gc.login()
                    cell = sheet_data.find(str(user.id))
                except gspread.exceptions.CellNotFound as e:
                    # IDが未登録
                    # ID欄が空欄の行番号を取得してA列にIDを入力
                    id_list = sheet_data.col_values(1)
                    if '' in id_list:
                        blank_row = id_list.index('') + 1
                    else:
                        blank_row = len(id_list) + 1
                    sheet_data.update_cell(blank_row, 1, str(user.id))
                    # IDが登録されたので再検索
                    cell = sheet_data.find(str(user.id))

                name = sheet_data.cell(cell.row, cell.col + 1).value
                rank = sheet_data.cell(cell.row, cell.col + 2).value
                if name == "":
                    # IDだけ登録されていて名前が未登録
                    await message.channel.send("チーム戦で使う名前を入力してね")

                    def name_check(name_msg):
                        return (not name_msg.author.bot) and name_msg.author == message.author

                    name_msg = await client.wait_for('message', check=name_check)
                    if name_msg.content.startswith("<:") or name_msg.content.startswith("!"):
                        # 別のbotコマンドが入力されるとそれが名前として登録されてしまうので処理を終了
                        return
                    name = name_msg.content
                    sheet_data.update_cell(cell.row, cell.col + 1, name_msg.content)

                if rank == "":
                    # 名前は登録されているがクラスが未登録
                    await message.channel.send("登録したいクラス(D/D+/C/C+/B/B+/A/A+/S/S+/SS)を入力してね\n" +
                                               "・Dクラス\n" +
                                               "\tCTR:NF初心者\n" +
                                               "\tドリフトターボ、ジャンプターボに慣れつつある実力\n" +
                                               "・Cクラス\n" +
                                               "\tエヌ・トロピーへの挑戦権を獲得できる実力を持つ\n" +
                                               "・Bクラス\n" +
                                               "\tほぼ全てのエヌ・トロピーに勝つ実力を持つ\n" +
                                               "・Aクラス\n" +
                                               "\tほぼ全てのひたトラオキサイドを倒し、普通に上手い実力者\n" +
                                               "\t超加速維持、インコース攻めが出来始めたら立派な猛者\n" +
                                               "・Sクラス\n" +
                                               "\tガチガチの猛者\n" +
                                               "\tほぼ全てのコースで加速維持経験がある。\n" +
                                               "\tひたトラリーダーボードにてSwitchでは2桁、PS4では300位以内を取る実力を備えている\n" +
                                               "・SSクラス\n" +
                                               "\t世界ランカー　ろむさん並み\n" +
                                               "\tオンラインレースで妨害が無ければWR+5～10秒程度を安定して出せる実力を持つ\n")
                else:
                    # クラスがすでに登録されている
                    await message.channel.send("変更先のクラスを選択してね（現在" + rank + "クラスだよ）")

                # クラスの登録・変更
                def rank_check(rank_msg):
                    return (not rank_msg.author.bot) and rank_msg.author == message.author

                rank_msg = await client.wait_for('message', check=rank_check)
                if rank_msg.content in ["D", "D+", "C", "C+", "B", "B+", "A", "A+", "S", "S+", "SS"]:
                    # スプレッドシートにクラスを登録
                    sheet_data.update_cell(cell.row, cell.col + 2, rank_msg.content)
                    await message.channel.send(name + "さんを" + rank_msg.content + "クラスで登録したよ")
                else:
                    await message.channel.send("D/D+/C/C+/B/B+/A/A+/S/S+/SSのいずれかを入力してね")

    ###
    # tipsのコラ画像を作成する
    ###
    if message.content.startswith("!tips/"):
        arg = message.content.split("/")[1]
        split_arg = arg.split(',')

        p = create_tips_image(split_arg[0], split_arg[1])
        p.save("tips.png", quality=100)

        await message.channel.send(file=discord.File("tips.png"))
        os.remove("tips.png")

    ###
    # メッセージの最初が"!logout"の処理
    # BOTをオフラインにする
    ###
    if message.content.startswith('!logout'):
        await client.logout()
        await sys.exit()


################################################################
# 関数定義
################################################################


###
# コースリストをもとにメッセージを送信
###
async def send_message_from_list(message, from_list, first_num=1):
    send_message = ""

    i = first_num
    for course in from_list:

        send_message += num2emoji2(i, 2) + " " + course
        send_message += "\n"

        if i % 10 == 0:
            await message.channel.send(send_message)
            send_message = ""

        i += 1

    if send_message != "":
        await message.channel.send(send_message)


###
# 参加者のクラスを数値に置換したものを返す
###
def class2num(dict_class):
    class_def = {"D": 1, "D+": 1.5, "C": 2, "C+": 2.5, "B": 3, "B+": 3.5, "A": 4, "A+": 4.5, "S": 5, "S+": 5.5, "SS": 6}
    dict_num = {}
    for member in dict_class.items():
        dict_num[member[0]] = class_def[member[1]]
    return dict_num


###
# dict型の中身をシャッフルして返す
###
def shuffle_dict(d):
    keys = list(d.keys())
    random.shuffle(keys)
    keys = [(key, d[key]) for key in keys]
    return dict(keys)


# 数値の絵文字リスト
num_char = [
    ":zero:",
    ":one:",
    ":two:",
    ":three:",
    ":four:",
    ":five:",
    ":six:",
    ":seven:",
    ":eight:",
    ":nine:"
]


###
# 数値を絵文字で返す（桁合わせ無し）
###
def num2emoji(num):
    ans = ""
    tmp = int(num)
    while tmp > 0:
        ans = num_char[(int(tmp) % 10)] + ans
        tmp = int(tmp / 10)
    return ans


###
# 数値を絵文字で返す（桁合わせ有り）
###
def num2emoji2(num, keta):
    ans = ""
    tmp = int(num)
    i = 0
    while i < keta:
        ans = num_char[(int(tmp) % 10)] + ans
        tmp = int(tmp / 10)
        i += 1
    return ans


###
# 以下、被りなしのコース抽出部分
###
list_random = list()
list_num = 0


def random_list_return_list(list_count):
    # return用変数
    ans = list()

    for _ in range(list_count):
        global list_num

        # コースリスト周回の初回にリストをランダムにする
        if list_num <= 0:
            random_list_reset()

        ans.append(list_random[list_num])
        list_num += 1

        # 一周完了したら0に戻す
        if list_num >= len(list_random):
            list_num = 0
    return ans


def random_list_reset():
    global list_random
    global list_num
    list_random = random.sample(course_list, len(course_list))
    list_num = 0
    # print("ランダムコース抽出 全コースが抽出対象になります")


###
# 各種selectコマンドを関数化
###
async def select_all(message):
    # コースリストランダム化
    course_list_random = random.sample(course_list, len(course_list))
    # リストを元にメッセージ送信
    await send_message_from_list(message, course_list_random)


async def select_num(message, num):
    if num == 0:
        await message.channel.send("1～" + str(len(course_list)) + "の整数を入力してね")
        return
    if num > len(course_list):
        await message.channel.send("コース数の上限を超えてるよ")
        return
    # コースリストランダム化
    course_list_random = random_list_return_list(num)
    # リストを元にメッセージ送信
    await send_message_from_list(message, course_list_random)


async def select_coin(message):
    course_list_random = random.sample(course_coin_list, len(course_coin_list))
    await send_message_from_list(message, course_list_random)


async def select_reset(message):
    random_list_reset()
    await message.channel.send("全コースがまた選ばれるよ")


###
# 紅白戦チーム分け関数
###
async def kouhaku(message):
    print("len(entry_dict) = " + str(len(entry_dict)))
    wait_list = list()
    if len(entry_dict) > 8:
        entry_dict_shuffle = shuffle_dict(entry_dict)
        for _ in range(len(entry_dict_shuffle) - 8):
            wait_member = entry_dict_shuffle.popitem()
            wait_list.append(wait_member[0])
    elif len(entry_dict) < 4:
        await message.channel.send("参加者数が3人以下だよ")
        return
    elif len(entry_dict) % 2 == 1:
        await message.channel.send("参加者数が奇数だよ")
        return
    else:
        entry_dict_shuffle = shuffle_dict(entry_dict)

    team1_dict.clear()
    team2_dict.clear()
    team1_list.clear()
    team2_list.clear()

    print("entry_dict_shuffle = " + str(entry_dict_shuffle))
    entry_dict_num = class2num(entry_dict_shuffle)
    print("entry_dict_num = " + str(entry_dict_num))
    threshold = 0
    for _ in range(4):
        threshold += 0.5
        print("threshold = " + str(threshold))
        for _ in range(30):
            entry_dict_num = shuffle_dict(entry_dict_num)
            team1_sum = 0
            team2_sum = 0
            k = 0
            for member in entry_dict_num.items():
                if k < len(entry_dict_num) / 2:
                    team1_sum += float(member[1])
                else:
                    team2_sum += float(member[1])
                k += 1
            print("entry_dict_num = " + str(entry_dict_num))
            print("team1_sum = " + str(team1_sum))
            print("team2_sum = " + str(team2_sum))
            if abs(team1_sum - team2_sum) <= threshold:
                k = 0
                for member in entry_dict_num.items():
                    if k < len(entry_dict_num) / 2:
                        team1_dict[member[0]] = member[1]
                        team1_list.append(member[0])
                    else:
                        team2_dict[member[0]] = member[1]
                        team2_list.append(member[0])
                    k += 1
                k = 0
                send_message = ""
                send_message += "チーム１ - ["
                for member in team1_dict.items():
                    # send_message += num2emoji(join_order_team1[k])
                    send_message += member[0] + "(" + entry_dict[member[0]] + ")"
                    if k < len(team1_dict) - 1:
                        send_message += ", "
                    k += 1
                send_message += "]"
                send_message += "\n"
                k = 0
                send_message += "チーム２ - ["
                for member in team2_dict.items():
                    # send_message += num2emoji(join_order_team2[k])
                    send_message += member[0] + "(" + entry_dict[member[0]] + ")"
                    if k < len(team2_dict) - 1:
                        send_message += ", "
                    k += 1
                send_message += "]"
                await message.channel.send(send_message)
                if len(entry_dict) > 8:
                    await message.channel.send("待機者 - " + str(wait_list))
                return
    await message.channel.send("均等なバランスでチーム分け出来なかったよ")


###
# タッグ戦チーム分け関数
###
async def tag(message):
    print("len(entry_dict) = " + str(len(entry_dict)))
    wait_list = list()
    if len(entry_dict) > 8:
        entry_dict_shuffle = shuffle_dict(entry_dict)
        for _ in range(len(entry_dict_shuffle) - 8):
            wait_member = entry_dict_shuffle.popitem()
            wait_list.append(wait_member[0])
    elif len(entry_dict) < 4:
        await message.channel.send("参加者数が3人以下だよ")
        return
    elif len(entry_dict) % 2 == 1:
        await message.channel.send("参加者数が奇数だよ")
        return
    else:
        entry_dict_shuffle = shuffle_dict(entry_dict)

    tag_team_dict.clear()
    tag_team_num = len(entry_dict_shuffle) // 2

    print("entry_dict_shuffle = " + str(entry_dict_shuffle))
    entry_dict_num = class2num(entry_dict_shuffle)
    print("entry_dict_num = " + str(entry_dict_num))
    threshold = 0
    for _ in range(4):
        threshold += 0.5
        print("threshold = " + str(threshold))
        for _ in range(30):
            entry_dict_num = shuffle_dict(entry_dict_num)
            tag_sum = []
            tag_in_sum = 0
            k = 0
            for member in entry_dict_num.items():
                tag_in_sum += float(member[1])
                if k % 2 == 1:
                    tag_sum.append(tag_in_sum)
                    tag_in_sum = 0
                k += 1
            print("entry_dict_num = " + str(entry_dict_num))
            print("tag_sum = " + str(tag_sum))
            max_delta = 0
            for i in range(tag_team_num):
                for j in range(tag_team_num):
                    if max_delta < abs(tag_sum[i] - tag_sum[j]):
                        max_delta = abs(tag_sum[i] - tag_sum[j])
            print("max_delta = " + str(max_delta))
            if max_delta <= threshold:
                k = 0
                for member in entry_dict_num.items():
                    i = k // 2
                    if i not in tag_team_dict:
                        tag_team_dict[i] = {}
                    tag_team_dict[i][member[0]] = member[1]
                    k += 1
                print("tag_team_dict = " + str(tag_team_dict))
                send_message = ""
                for i in range(tag_team_num):
                    k = 0
                    send_message += "チーム" + str(i + 1) + " - ["
                    for member in tag_team_dict[i].items():
                        send_message += member[0] + "(" + entry_dict[member[0]] + ")"
                        if k % 2 == 0:
                            send_message += ", "
                        else:
                            send_message += "]"
                            send_message += "\n"
                        k += 1
                await message.channel.send(send_message)
                if len(entry_dict) > 8:
                    await message.channel.send("待機者 - " + str(wait_list))
                return
    await message.channel.send("均等なバランスでチーム分け出来なかったよ")


###
# mチームからn人を抽選して表示する
###
async def exit_member(message, team, num):
    if not num.isdecimal():
        await message.channel.send(", のあとには整数を入力してね")
        return
    elif int(num) > len(team1_list):
        await message.channel.send("チームの人数を超えてるよ")
        return
    if str(team) == "1":
        random.shuffle(team1_list)
        exit_list = team1_list[0:int(num)]
    elif str(team) == "2":
        random.shuffle(team2_list)
        exit_list = team2_list[0:int(num)]
    else:
        await message.channel.send("コマンド入力にミスがあるよ")
        return
    send_message = ""
    send_message += "離脱者 - ["
    for member in exit_list:
        send_message += member
        if member != exit_list[len(exit_list) - 1]:
            send_message += ","
    send_message += "]"
    await message.channel.send(send_message)


# リアクションのチェック
async def wait_for_reaction_add(message, reaction_emoji_list, is_author_only=True):
    while True:
        reaction, user = await client.wait_for('reaction_add')

        # is_author_only が Trueのとき、リアクションが発言者以外だったら再待機
        if is_author_only and (not (user == message.author)):
            continue

        # BOTが発言したチャンネル以外は再待機
        if not (message.channel.id == reaction.message.channel.id):
            continue

        # BOT自身によるリアクションは再待機
        if user.bot:
            continue

        # リアクションが対象の絵文字であればwhileを抜ける
        for my_str in reaction_emoji_list:
            if str(reaction.emoji) == my_str:
                return reaction, user


# tipsコラ画像を作成して返す
def create_tips_image(titleStr, mainStr):
    my_dir = "."

    # 背景。最終的にこれを返す
    img_bg = Image.new('RGBA', (1280, 720))

    img_back = Image.open(my_dir + "/tips/" + 'back.png').resize((1280, 720), Image.LANCZOS)
    img_bg.paste(img_back, (0, 0))

    ###
    # タイトル文字
    ###

    titlefontsize = 52

    img_str = Image.new('RGBA', (img_back.width, int(titlefontsize * 2)), (0, 0, 0))
    draw = ImageDraw.Draw(img_str)

    fnt = ImageFont.truetype(my_dir + "/tips/" + "msgothic.ttc", titlefontsize)

    # 描画した時の横幅縦幅を取得 参考 : https://watlab-blog.com/2019/08/27/add-text-pixel/
    str_w, str_h = draw.textsize(titleStr, fnt)

    # 線が細いので複数描画で太くする
    for ii in range(2):
        for jj in range(2):
            draw.text((int(0 + ii), int((img_str.height - str_h) / 2) + jj), titleStr, fill=(255, 255, 255), font=fnt)

    # 境界をぼかす場合
    # img_str = img_str.filter(ImageFilter.GaussianBlur(1))
    # 色反転するときはこちら
    # img_str = ImageOps.invert(img_str)

    # モノクロ画像化する。透過するときの素材となる
    img_str = img_str.convert('L')

    # 背景画像。テクスチャ
    img_tx = Image.open(my_dir + "/tips/" + 'fontcolor.png').resize((img_str.size), Image.LANCZOS)

    # 文字imageをもとに背景色画像をくり抜く
    img_txstr = img_tx.copy()
    img_txstr.putalpha(img_str)

    # 影を作るよ
    img_str_shadow = Image.new('RGBA', (img_str.size), (0, 0, 0))
    draw_shadow = ImageDraw.Draw(img_str_shadow)

    # 背景が黒、文字部分が白の画像を作成する。透明部分はまだ無し
    for ii in range(2):
        for jj in range(2):
            draw_shadow.text((int(0 + ii), int((img_str.height - str_h) / 2) + jj), titleStr, fill=(255, 255, 255),
                             font=fnt)

    # 真っ黒の画像を作成
    img_black = Image.new('RGBA', (img_str_shadow.size), (0, 0, 0))

    # 真っ黒の画像に対し、背景黒,文字白の画像でくり抜く。背景透明,文字黒の画像ができる
    img_black.putalpha(img_str_shadow.convert('L'))

    # 縁の太さ
    bw = 3

    # 位置
    Loc_Left = int((1280) / 2 - (str_w / 2))
    Loc_Top = int(img_bg.height * 0.395)

    # 透過で合成 参考 : https://symfoware.blog.fc2.com/blog-entry-1532.html
    c = Image.new('RGBA', img_bg.size, (255, 255, 255, 0))

    # 線が細いので複数描画で太くする
    for ii in range(bw):
        for jj in range(bw):
            c.paste(img_black, (Loc_Left - jj, Loc_Top - ii), img_black)
            c.paste(img_black, (Loc_Left - jj, Loc_Top + ii), img_black)
            c.paste(img_black, (Loc_Left + jj, Loc_Top - ii), img_black)
            c.paste(img_black, (Loc_Left + jj, Loc_Top + ii), img_black)

            # 左下部分はちょっと長めにとる
            c.paste(img_black, (Loc_Left - jj * 3, Loc_Top + ii * 3), img_black)

    img_bg = Image.alpha_composite(img_bg, c)

    c = Image.new('RGBA', img_bg.size, (255, 255, 255, 0))

    c.paste(img_txstr, (Loc_Left, Loc_Top), img_txstr)

    # return用のimageオブジェクトに反映
    img_bg = Image.alpha_composite(img_bg, c)

    ###
    # 本文
    ###

    # はみ出ないようにいい感じに分けるリスト。これから格納する
    spl_mainStr = list()

    # 空白で全分けしたリスト
    tmp_mainStr = mainStr.split()

    mainfontsize = 24
    fnt = ImageFont.truetype(my_dir + "/tips/" + "msgothic.ttc", mainfontsize)

    nowstr = ""
    beforeStr = ""
    ii = 0
    while (True):
        nowstr = nowstr + " " + tmp_mainStr[ii]

        # 描画した時の横幅縦幅を取得 参考 : https://watlab-blog.com/2019/08/27/add-text-pixel/
        str_w, str_h = draw.textsize(nowstr, fnt)

        if (str_w > (1280 * 0.625)):
            spl_mainStr.append(beforeStr)
            nowstr = tmp_mainStr[ii]

        beforeStr = nowstr

        ii += 1

        if (ii >= len(tmp_mainStr)):
            spl_mainStr.append(beforeStr)
            break

    draw = ImageDraw.Draw(img_bg)
    Loc_Top = int(img_bg.height * 0.532)
    ii = 0
    for mystr in spl_mainStr:
        str_w, str_h = draw.textsize(mystr, fnt)

        Loc_Left = int((1280) / 2 - (str_w / 2))

        draw.text((int(Loc_Left + 0), Loc_Top + (ii * mainfontsize)), mystr, fill=(240, 240, 240), font=fnt)
        draw.text((int(Loc_Left + 1), Loc_Top + (ii * mainfontsize)), mystr, fill=(240, 240, 240), font=fnt)

        ii += 1

    return img_bg


"""
###
# コースリストをもとにメッセージを送信します
# 2BASA - 画像化送信　版
###
async def send_message_from_list(message, from_list, first_num=1):
    send_message = ""

    i = first_num
    for course in from_list:

        send_message += Return_NumStr2(i, 2) + " " + course
        send_message += "\n"

        if i % 10 == 0:
            # await message.channel.send(send_message)
            send_message = ""

        i += 1

    if send_message != "":
        # await message.channel.send(send_message)
        hogehoge = "" # if文の中がコメントアウトのみだとエラー吐くので緊急でこの行があります

    ####
    # 以下追加部分
    ####


    # os.path.dirname(__file__)でカレントディレクトリを取りたかったがうまく取れず…

    # Pic_dir = os.path.dirname(__file__) + "/data"
    pic_dir = "data"

    # アイコンサイズ。アイコンは正方形で扱う前提
    icon_size = 32

    bg_width = icon_size * 20 # 20は適度な数値。横幅短過ぎず長すぎずで

    #一番の親キャンバス。最終的にこれに張り付けてある部分が画像として保存・送信されます
    img_bg = Image.new('RGBA', (bg_width, icon_size * len(from_list)))

    ii = 0
    for _ in range(len(from_list)):
        loc_left = 0

        # 1行分のキャンバス
        img_row = Image.new('RGBA', (bg_width, icon_size))

        # コース数2桁までを前提にしています。3桁になるときっと止まる…
        # 十の位
        img = Image.open(pic_dir + "/num_" + str(int((ii + 1) / 10)) + ".png")
        img = img.resize((icon_size, icon_size), Image.LANCZOS)
        img_row.paste(img, (loc_left, 0))
        loc_left += icon_size

        # 一の位
        img = Image.open(pic_dir + "/num_" + str(int((ii + 1) % 10)) + ".png")
        img = img.resize((icon_size, icon_size), Image.LANCZOS)
        img_row.paste(img, (loc_left, 0))
        loc_left += icon_size

        # コース名
        text = from_list[ii].split(">")[1] # 絵文字部分の文字列を除く
        fnt = ImageFont.truetype(pic_dir + "/Splatfont 2.ttf", 20) # 今回準備していたフォントがSplatfont2でした
        draw = ImageDraw.Draw(img_row)
        color = (240, 240, 240)
        draw.text((loc_left, -4),text,fill=color,font=fnt) # 「-4」はSplatfont2のフォントのクセで、若干下寄りなので調整値です


        # 親キャンバスに貼り付け
        img_bg.paste(img_row, (0,icon_size * ii))

        ii += 1


    # img_FilePath = os.path.dirname(__file__) + "/course.png"
    img_FilePath = "course.png"

    img_bg.save(img_FilePath, quality=100)

    await message.channel.send(file=discord.File(img_FilePath))

    os.remove(img_FilePath)
"""

# BOTのトークン
client.run("NjE4NDQ1Mjg3MjkxMzU1MTQw.XW5yLQ.PUHv-EOWr4K6-Hu0ofELKrf6oWE")
