import configparser
import discord
import cotoha as cth
from discord.ext import commands

bot = commands.Bot(command_prefix='$')
client = discord.Client()

def get_weak_point(sentence):
    cotoha = cth.Cotoha()
    TYPES = ["ノーマル", "ほのお", "みず", "でんき", "くさ", "こおり", "かくとう",
        "どく","じめん", "ひこう", "エスパー", "むし", "いわ", "ゴースト", "ドラゴン", "あく", "はがね", "フェアリー"]
    
    TPYE_TABLE = [
        [1,1,1,1,1,1,1,1,1,1,1,1,2,3,1,1,2,1], # ノーマル
        [1,2,2,1,0,0,1,1,1,1,1,0,2,1,2,1,0,1], # ほのお
        [1,0,2,1,2,1,1,1,0,1,1,1,0,1,2,1,1,1], # みず
        [1,1,0,2,2,1,1,1,3,0,1,1,1,1,2,1,1,1], # でんき
        [1,2,0,1,2,1,1,2,0,2,1,2,0,1,2,1,2,1], # くさ
        [1,2,2,1,0,2,1,1,0,0,1,1,1,1,0,1,2,1], # こおり
        [0,1,1,1,1,0,1,2,1,2,2,2,0,3,1,0,0,2], # かくとう
        [1,1,1,1,0,1,1,2,2,1,1,1,2,2,1,1,3,0], # どく
        [1,0,1,0,2,1,1,0,1,3,1,2,0,1,1,1,0,1], # じめん
        [1,1,1,2,0,1,0,1,1,1,1,0,2,1,1,1,2,1], # ひこう
        [1,1,1,1,1,1,0,0,1,1,2,1,1,1,1,3,2,1], # エスパー
        [1,2,1,1,0,1,2,2,1,2,0,1,1,2,1,0,2,2], # むし
        [1,0,1,1,1,0,2,1,2,0,1,0,1,1,1,1,2,1], # いわ
        [3,1,1,1,1,1,1,1,1,1,0,1,1,0,1,2,1,1], # ゴースト
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,2,3], # ドラゴン
        [1,1,1,1,1,1,2,1,1,1,0,1,1,0,1,2,1,2], # あく
        [1,2,2,2,1,0,1,1,1,1,1,1,0,1,1,1,2,0], # はがね
        [1,2,1,1,1,1,0,2,1,1,1,1,1,1,0,0,2,1]  # フェアリー
    ]
    parse_text = cotoha.parse(sentence)
    print(parse_text)

    adjective, dependency_labels = cotoha.get_adjective(parse_text)
    if (dependency_labels == {}):
        return "わしにはわからん"

    type_id = cotoha.get_poke_type(parse_text, dependency_labels['token_id'], TYPES)
    if (type_id == None):
        return "そんなタイプは知らんぞ。。。デジモンか？"
    print("対象タイプ："+str(type_id))
    
    
    # 強弱判定
    if adjective == "strong":
        target = 0
        strong_text = "強い"
    elif adjective == "weak":
        target = 2
        strong_text = "弱い"
    else:
        target = 1
        strong_text = "普通な"
    
    # 係り受け判定
    if dependency_labels["label"] == "nsubj":
        #table_axis = "horizontal"
        depend_text = "が"
        answers = [TYPES[i] for i, x in enumerate(TPYE_TABLE[type_id]) if x==target]
        pass
    elif dependency_labels["label"] == "iobj" or "dobj":
        #table_axis = "vertical"
        depend_text = "に"
        answers = [TYPES[i] for i, x in enumerate(TPYE_TABLE) if x[type_id]==target]

    
    response = TYPES[type_id] + "タイプ" + depend_text + strong_text + "のは" + 'と'.join(answers) + "タイプじゃな！"

    return response


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    #if message.content.startswith('$type'):
    #    await message.channel.send(get_weak_point())

@bot.command()
async def test(ctx, arg):
    await ctx.send(get_weak_point(arg))

config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')
TOKEN = config_ini['DISCORD']['Token']
bot.run(TOKEN)



