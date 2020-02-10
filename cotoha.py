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
        r = requests.post(
            self.BASE_URL + "v1/parse",
            headers=headers,
            data=json.dumps(data)
        )
        return r.json()["result"]

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

    def get_adjective(self, json_response):
        strongs = {"強い", "有利", "優勢", "抜群"}
        weaks = {"弱い", "不利", "劣勢", "今一つ"}
        type_adjective = "normal"
        dependency_labels = []
        for chunk in json_response:
            for token in chunk["tokens"]:
                print(token["lemma"])
                if token["lemma"] in strongs:
                    print("強い")
                    type_adjective = "strong"
                    dependency_labels = token["dependency_labels"]
                elif token["lemma"] in weaks:
                    print("弱い")
                    type_adjective = "weak"
                    dependency_labels = token["dependency_labels"]
                
                    
        return type_adjective, dependency_labels[0]
    
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
    print(response)

    