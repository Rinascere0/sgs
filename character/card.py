class Card:
    def __init__(self, name, item):
        # 花色：无、黑、梅、红、方
        self.color = None
        # 颜色：无色、黑色、红色
        self.sub_color = None
        # 点数：A~K
        self.num = None
        # 名称：
        self.name = None
        # 属性:
        self.attr = None
        # 类型：基本、锦囊、装备
        self.type = None
        # 具体类型：武器牌、防具牌、坐骑牌、伤害牌
        self.sub_type = None
        # 内含牌：转化牌所包含的原始牌
        self.item = None

        # 距离（武器，锦囊）
        self.dist = None
