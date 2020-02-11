
import configparser
import cotoha as cth

class Orchid():
    def __init__(self):
        self.TPYE_TABLE = [
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
        self.TYPES = [
            "ノーマル", "ほのお", "みず", "でんき",
            "くさ", "こおり", "かくとう","どく",
            "じめん", "ひこう", "エスパー", "むし", "いわ", 
            "ゴースト", "ドラゴン", "あく", "はがね", "フェアリー"
        ]
        self.EXEPT_TYPES = [
            "タイプ", "たいぷ", "技", "わざ", "ワザ"
        ]
        self.cotoha = cth.Cotoha()

    def get_poke_type(self, tokens, token_id):
        poke_type = None
        target_token = tokens[token_id]
        try:
            if target_token["form"] in self.EXEPT_TYPES:
                # タイプ、ワザの前にかかっている想定
                target_token = tokens[token_id - 1]
            

            poke_type = self.TYPES.index(target_token["form"])
            
        except Exception as e:
            print(e)
            poke_type = None
        
        return poke_type

    def get_weak_point(self, sentence):
        parse_text = self.cotoha.parse(sentence)
        tokens = self.cotoha.get_tokens(parse_text)
        print(tokens)
        adjective, dependency_labels = self.cotoha.get_adjective(tokens)
        if (dependency_labels == {}):
            return "お前、サトシではないな？"
        print("get adjective")
        type_id = self.get_poke_type(tokens, dependency_labels['token_id'])
        if (type_id == None):
            return "そんなタイプは知らんぞ。。。デジモンか？"
        print("対象タイプ："+str(type_id))
        print("依存関係ラベル："+ dependency_labels["label"])
        print("adjective："+adjective)
        
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

            #table_axis = "horizontal"
            answers = [self.TYPES[i] for i, x in enumerate(self.TPYE_TABLE[type_id]) if x==target]
            response = self.TYPES[type_id] + "タイプ技が" + strong_text + "ポケモンは、" + 'と'.join(answers) + "タイプじゃな！"

        elif (dependency_labels["label"] == "iobj") or (dependency_labels["label"] == "dobj"):

            #table_axis = "vertical"
            answers = [self.TYPES[i] for i, x in enumerate(self.TPYE_TABLE) if x[type_id]==target]
            response = self.TYPES[type_id] + "タイプポケモンに" + strong_text + "わざは、" + '、'.join(answers) + "タイプじゃな！"
        
        else:
            response = "トラブルじゃ。マサラタウンに帰れ！！"
        
        return response