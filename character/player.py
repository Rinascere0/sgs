# player interface, also character base class

from lib.characters import characters


class Player:
    def __init__(self):
        pass

    def load_character(self, name):
        self.character = characters[name]()

    # interface
    def gen_action(self):
        pass

    # 需要打出牌响应
    def react_card(self):
        pass

    # 使用牌
    def use_card(self):
        pass

    # 需要做出选择
    def select_choice(self, choiceName):
        pass



    # check status functions
    def possess_card(self, cardName):
        pass
