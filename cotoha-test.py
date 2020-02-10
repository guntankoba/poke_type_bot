import configparser
import discord
import cotoha as cth
client = discord.Client()

def get_weak_point():
    cotoha = cth.Cotoha()
    poke_types = ["ノーマル", "ほのお", "みず", "でんき", "くさ", "こおり", "かくとう",
        "どく","じめん", "ひこう", "エスパー", "むし", "いわ", "ゴースト", "ドラゴン", "あく", "はがね", "フェアリー"]
    weaks_list_fire = [1,2,0,1,2,2,1,1,0,1,1,2,0,1,1,1,2,2]
    strongs_list_fire = []
    # sent = "火に強いタイプ"
    # parse_text = cotoha.parse(sent)
    # print(parse_text)
    # sent = "火が強いタイプ"
    # parse_text = cotoha.parse(sent)
    # print(parse_text)
    # sent = "火で強いタイプ"
    # parse_text = cotoha.parse(sent)
    # print(parse_text)
    sent = "火にバツグン"
    parse_text = cotoha.parse(sent)
    print(parse_text)

    adjective, dependency_labels = cotoha.get_adjective(parse_text)
    
    if adjective == "strong":
        target = 0
    elif adjective == "weaks":
        target = 2
    else:
        target = 1
        
    
    if dependency_labels["label"] == "nsubj":
        l = strongs_list_fire
    if dependency_labels["label"] == "iobj":
        l = weaks_list_fire

    
    answer = [poke_types[i] for i, x in enumerate(l) if x==target]
    
    response = "火に強いのは" + 'と'.join(answer) + "タイプじゃな！"
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

    if message.content.startswith('火にバツグン'):
        await message.channel.send(get_weak_point())

config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')
TOKEN = config_ini['DISCORD']['Token']
client.run(TOKEN)



