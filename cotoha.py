import requests
import json
import configparser


class Cotoha():
    def __init__(self):
        config_ini = configparser.ConfigParser()
        config_ini.read('config.ini', encoding='utf-8')

        self._CLIENT_ID = config_ini['COTOHA']['Id']
        self._CLIENT_SECRET = config_ini['COTOHA']['Secret']
        self.BASE_URL = config_ini['COTOHA']['BaseUrl']#"https://api.ce-cotoha.com/api/dev/nlp/"
        self.TOKEN_URL = config_ini['COTOHA']['TokenUrl']#"https://api.ce-cotoha.com/v1/oauth/accesstokens"
        self.access_token = self.get_access_token(self._CLIENT_ID, self._CLIENT_SECRET)

    def get_access_token(self, client_id, client_secret):
        
        headers = {
            "Content-Type": "application/json",
            "charset": "UTF-8"
        }
        data = {
            "grantType": "client_credentials",
            "clientId": client_id,
            "clientSecret": client_secret
        }
        r = requests.post(self.TOKEN_URL,
                        headers=headers,
                        data=json.dumps(data))
        return r.json()["access_token"]

    def parse(self, sentence: str):
        headers = {
            "Content-Type": "application/json",
            "charset": "UTF-8",
            "Authorization": "Bearer {}".format(self.access_token)
        }
        data = {
            "sentence": sentence,
            "type": "default"
        }
        try:
            r = requests.post(
                self.BASE_URL + "v1/parse",
                headers=headers,
                data=json.dumps(data)
            )
        except:
            if r.status_code == 401:
                self.access_token = self.get_access_token(self._CLIENT_ID, self._CLIENT_SECRET)
                headers["Authorization"] = "Bearer " + self.access_token
                r = requests.post(
                    self.BASE_URL + "v1/parse",
                    headers=headers,
                    data=json.dumps(data)
                )

        return r.json()["result"]

    def get_tokens(self, chunks):
        tokens = []
        for c in chunks:
            for token in c["tokens"]:
                tokens.append(token)
        print(len(tokens))

        return tokens

    def get_type(self):
        """
        タイプワイルドって感じだ
        """
        pass

    def get_pos(self, json_response):
        pos_list = []
        for chunk in json_response:
            for token in chunk["tokens"]:
                if token["pos"] == "名詞":
                    pos_list.append(token["lemma"])
        return pos_list

    def get_adjective(self, tokens):
        strongs = {"強い", "有利", "優勢", "抜群"}
        weaks = {"弱い", "不利", "劣勢", "今一つ"}
        invalid = {"無効", "効かない", "当たらない"}

        type_adjective = "normal"
        dependency_labels = []
        for token in tokens:          
            if token["lemma"] in strongs:
                type_adjective = "strong"
                dependency_labels = token["dependency_labels"]
            elif token["lemma"] in weaks:
                type_adjective = "weak"
                dependency_labels = token["dependency_labels"]
            elif token["lemma"] in invalid:
                type_adjective = "invalid"
                dependency_labels = token["dependency_labels"]
        print("debug")
        if not len(dependency_labels) == 0:
            return type_adjective, dependency_labels[0]
        else:
            return type_adjective, {}
    

        

"""
火に強い→水
火が強い→草
火で強い→草
火が弱い→

依存関係について
iobj: に
nsubj:が、で

属性表：
強い：0
普通：1
弱い：2
無効：3
"""

if(__name__=="__main__"):
    cotoha = Cotoha()
    poke_types = [
        "ノーマル", "ほのお", "みず", "でんき", "くさ", "こおり", 
        "かくとう","どく","じめん", "ひこう", "エスパー", "むし", 
        "いわ", "ゴースト", "ドラゴン", "あく", "はがね", "フェアリー"
    ]

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

    sent = "かくとうが無効"
    parse_text = cotoha.parse(sent)
    print(parse_text)

    adjective, dependency_labels = cotoha.get_adjective(parse_text)
    if (dependency_labels == {}):
        exit()
    
    type_id = cotoha.get_poke_type(parse_text, dependency_labels['token_id'], poke_types)
    print("対象タイプ：" + str(type_id))
    print("依存関係ラベル："+ dependency_labels["label"])
    # 強弱判定
    if adjective == "strong":
        target = 0
        strong_text = "バツグンな"
    elif adjective == "weak":
        target = 2
        strong_text = "いまひとつな"
    elif adjective == "invalid":
        target = 3
        strong_text = "効果なしの"
    else:
        target = 1
        strong_text = "普通な"
    
    # 係り受け判定
    if (dependency_labels["label"] == "nsubj") or (dependency_labels["label"] == "nmod"):
        print('ggg')
        #table_axis = "horizontal"
        answers = [poke_types[i] for i, x in enumerate(TPYE_TABLE[type_id]) if x==target]
        response = poke_types[type_id] + "タイプ技が" + strong_text + "ポケモンは、" + 'と'.join(answers) + "タイプじゃな！"

    elif (dependency_labels["label"] == "iobj") or (dependency_labels["label"] == "dobj"):
        print('nnn')
        #table_axis = "vertical"
        answers = [poke_types[i] for i, x in enumerate(TPYE_TABLE) if x[type_id]==target]
        response = poke_types[type_id] + "タイプポケモンに" + strong_text + "わざは、" + '、'.join(answers) + "タイプじゃな！"
    
    else:
        response = "eee"
    # response = poke_types[type_id] + "タイプ" + depend_text + strong_text + "のは" + 'と'.join(answers) + "タイプじゃな！"
    print(response)

    