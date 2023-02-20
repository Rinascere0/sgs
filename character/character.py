MAX = 999
MIN = -999

from card import Card


class Character:
    def __init__(self):
        # core
        self.core = None

        ####
        # base stats

        self.name = None
        self.HP = None
        self.maxHP = None
        self.kill_count = 1
        # 技能名称
        self.base_skills = [None for _ in range(3)]
        # 技能类型
        self.skill_type = [None for _ in range(3)]
        # 标记数量
        self.tag_count = 0

        ####
        # dynamix stats

        # 杀剩余使用次数
        self.kill_remain = None
        # 技能剩余使用次数
        self.skill_remain = [None for _ in range(3)]
        # 可以使用的技能
        self.skills = []
        # 手牌上限
        self.card_limit = None
        # 是否能使用指定其他目标的牌
        self.can_select_target = None
        # 是否造成过伤害
        self.caused_damage = None
        # 本回合使用过的牌名
        self.card_used = []
        # 当前阶段
        self.period = None
        # 是否翻面
        self.fan = False
        self.le = False
        self.duan = False
        self.lian = False

        ####
        # areas
        self.cards = []  # 手牌
        self.judges = [None for _ in range(3)]  # 闪、兵、乐
        self.equips = [None for _ in range(4)]  # 武器、防具、+1、-1

        ####
        # special areas
        self.tag_cards = []  # 标记牌

        ###
        # 临时标记
        self.damage_source = None
        self.damage_card = None
        self.judge_card = None

    def get_color(self, card):
        if '红颜' in self.skills and card.color == 0:
            return 1
        return card.color

    def get_shan(self):
        return self.judges[0]

    def get_duan(self):
        return self.judges[1]

    def get_le(self):
        return self.judges[2]

    def get_hand_num(self):
        return len(self.cards)

    def drop_card(self, card):
        self.lose_card(card)
        self.core.drop_card(card)

    def drop_all(self):
        pass

    def reset_lian(self):
        self.lian = False

    def fanmian(self):
        self.fan = not self.fan

    def reset(self):
        self.lian = False
        self.fan = False

    # round process
    def round_begin(self):
        self.period = 'begin'
        pass

    def prep_period(self):
        self.period = 'prep'

        if '洛神' in self.skills:
            self.luoshen()

        if '观星' in self.skills:
            self.guanxing()

        if '英魂' in self.skills:
            self.yinghun()

        # 觉醒
        if '魂姿' in self.skills:
            self.hunzi()

        if '凿险' in self.skills:
            self.zaoxian()

        if '志继' in self.skills:
            self.zhiji()

        if '自立' in self.skills:
            self.zili()

        if '拜印' in self.skills:
            self.baiyin()

        if '若愚' in self.skills:
            self.ruoyu()

    def judge_period(self):
        self.period = 'judge'

        if '巧变' in self.skills:
            self.qiaobian()

        if '神速' in self.skills:
            self.shensu()

        for i, judge in enumerate(self.judges):
            wuxie = self.core.find_card('wuxie', judge)
            if wuxie:
                continue
            judge_card = self.core.judge(self)
            # 寻找改判
            judge_card = self.core.find_skill('chg_judge', judge_card)
            # 闪电
            judge_color = self.get_color(judge_color)
            if i == 0 and judge_color == 0 and 2 <= judge_card.num <= 9:
                self.damage(val=3, attr='lei', card=judge, source=None)

            if i == 1 and judge_color != 2:
                self.duan = True

            if i == 2 and judge_color != 1:
                self.le = True

    def draw_period(self):
        if self.duan:
            return

        self.period = 'draw'
        draw_count = 2

        if '涉猎' in self.skills:
            self.shelie()
            return

        if '突袭' in self.skills:
            self.tuxi()
            return

        if '好施' in self.skills:
            self.haoshi()
            return

        if '裸衣' in self.skills:
            self.luoyi()

        if '双雄' in self.skills:
            self.shuangxiong()

        if '英姿' in self.skills:
            draw_count += 1

        if '庸肆' in self.skills:
            draw_count += self.core.power_count()

        cards = self.core.draw(self, draw_count)
        self.draw_card(cards)

    def act_period(self):
        if self.le:
            return

        if '巧变' in self.skills:
            self.qiaobian()

        if '放权' in self.skills:
            self.fangquan()

        if '神速' in self.skills:
            self.shensu()

        self.period = 'act'

        while self.check_active:
            action = self.select_action()

    def drop_period(self):

        if '巧变' in self.skills:
            self.qiaobian()

        if '神速' in self.skills:
            self.shensu()

        self.period = 'drop'

        if '庸肆' in self.skills:
            self.yongsi()

        self.drop_count = self.card_limit - self.card_count()

    def round_end(self):
        self.period = 'end'
        pass

    def round(self):
        if self.fan:
            self.fan = True
            return
        self.round_begin()
        self.prep_period()
        self.judge_period()
        self.draw_period()
        self.act_period()
        self.drop_period()
        self.round_end()
        self.period = 'out'

    def judge(self):
        pass

    # 摸牌
    def draw_card(self, num):
        cards = self.core.draw_card(num)
        self.get_card(cards)

    # 获得牌, move为装备到对应区域
    def get_card(self, cards, equip=False):
        pass

    # 失去牌
    def lose_card(self, card):
        pass

    def select_choice(self, name):
        pass

    # 选择目标，name为卡牌或技能
    def select_target(self, name, cancel=False, mask=None):
        pass

    ## 选择牌的返回为字典{'owner','area','pos','item'}

    # 选择目标区域内的牌，判定、装备、手牌
    def select_area_card(self, target, cancel=True, num=1):
        pass

    # 选择目标的牌，装备、手牌
    def select_own_card(self, target, cancel=True, num=1):
        pass

    # 选择目前装备区的牌
    def select_equip(self, target, cancel=True, num=1):
        pass

    # 选择目标的手牌
    def select_hand(self, target, cancel=True, num=1):
        pass

    def use_card(self, card, target):
        pass

    # 界奸雄
    def jianxiong(self):
        self.get_card(self.damage_card)
        self.draw_card(1)

    # 护驾
    def hujia(self):
        self.core.find('护驾')

    # 反馈
    def fankui(self):
        target = self.damage_source
        card = self.select_area_card(target=target)
        if card:
            target.lose_card(card)
            self.get_card(card)

    # 鬼才
    def guicai(self):
        card = self.select_own_card(target=self)
        if card:
            self.lose_card(card)
        return card

    # 刚烈
    def ganglie(self):
        judge = self.core.judge()
        target = self.damage_source
        if self.get_color(judge.color) != 1:
            choice = target.select_choice('刚烈')
            # 弃牌
            if choice == 0:
                target.select_hand(target=target, cancel=True)

    # 突袭
    def tuxi(self, name):
        mask = []
        for _ in range(2):
            target = self.select_target(name, True, mask)
            if target:
                card = self.select_hand(target)
                self.get_card(card)
            else:
                return

    # 界裸衣
    def luoyi(self, name):
        cards = self.core.draw_card(3)
        draw_cards = []
        drop_cards = []
        for card in cards:
            if card.name == '杀' or card.name == '决斗' or card.sub_type == '武器':
                draw_cards.append(card)
            else:
                drop_cards.append(card)
        self.draw_card(draw_cards)
        self.core.drop_card(drop_cards)

    # 天妒
    def tiandu(self, name):
        self.get_card(self.judge_card)

    # 遗计
    def yiji(self, name):
        cards = self.core.draw_card(2)
        self.draw_card(cards)
        for i, card in enumerate(cards):
            target = self.select_target(name, True)
            if target:
                target.get_card(card)
                self.lose_card(-2 + i)

    # 洛神
    def luoshen(self, name):
        cards = []
        while True:
            card = self.core.judge(self)
            if self.get_color(card.color) < 2:
                cards.append(card)
            else:
                break
            if not self.select_choice(name):
                break
        self.get_card(cards)

    # 仁德
    def rende(self, name):
        target = self.select_target(name)
        if not target:
            return
        cards = self.select_hand(self, num=-1)
        if not cards:
            return
        else:
            self.lose_card(cards)
            target.get_card(cards)
            if len(cards) >= self.rende_num:
                self.heal(1, self)
                self.rende_num = MAX
            else:
                self.rende_num -= len(cards)

    def jijiang(self, name):
        return

    def guanxing(self, name):
        pass

    # 界铁骑
    def tieji(self, name):
        target = self.target
        target.tieji = True
        judge = self.core.judge(name)
        choice = self.target.select_choice(name)
        if choice == 0:
            mask = []
            card = target.select_hand(target, mask=mask)
            if card:
                target.drop_card(card)
                return
        target.can_react = False

    # 制衡
    def zhiheng(self, name):
        cards = self.select_hand(self, num=-1)
        if not cards:
            return

    def keji(self, name):
        pass

    def kurou(self, name):
        pass

    def fanjian(self, name):
        pass

    def guose(self, name):
        choice = self.select_choice(name)
        # TODO: 乐mask
        mask = []
        if choice == 0:
            return False
        # 将一张方片牌作为乐贴
        if choice == 1:
            target = self.select_target(mask=mask)
            if not target:
                return False
            card = self.select_own_card(self, color=4)
            if not card:
                return False
            self.use_card(Card('乐不思蜀', card), target)
        # 弃置场上一张乐
        elif choice == 2:
            target = self.select_target(mask=mask)
            if not target:
                return False
            card = target.get_le()
            target.remove(card)

        self.draw_card(1)
        return True

    def liuli(self, name):
        mask = self.get_target_in_dist()
        target = self.select_target(mask=mask)
        return target

    def jieyin(self, name):
        # TODO: 结姻mask
        mask = None
        target = self.select_target(mask=mask)
        choice = self.select_choice(name)
        if choice == 1:
            card = self.select_hand(self)
            if card:
                self.drop_card(card)
            else:
                return False
        elif choice == 2:
            # TODO: 装备牌
            card = self.select_own_card(self)
            if card:
                self.lose_card(card)
                target.get_card(equip=True)
            else:
                return False
        if target.HP < self.HP:
            self.draw_card(1)
            target.heal(1)
        else:
            target.draw_card(1)
            self.heal(1)
        return True

    def xiaoji(self, name):
        self.core.draw_card(2)
        return True

    def qingnang(self, name):
        # TODO: 体力不满
        target = self.select_target()
        if not target:
            return False
        card = self.select_hand(self)
        if card:
            self.drop_card(card)
            target.heal(1)
        return True

    # 界闭月
    def biyue(self, name):
        if self.get_hand_num() == 0:
            self.draw_card(2)
        else:
            self.draw_card(1)

    # 界神速
    def shensu(self, name):
        # TODO: 可杀mask
        target = self.select_target()
        if target:
            if self.period == 'act':
                # TODO:装备牌
                card = self.select_own_card()
                if card:
                    self.drop_card(card)
                else:
                    return False
            if self.period == 'drop':
                self.fanmian()
            self.use_card(Card('杀'), target)
            return True
        else:
            return False

    # 设变
    def shebian(self):
        players = self.core.get_players()
        # 选择移动装备的角色
        mask = []
        for player in players:
            if player.have_equip():
                mask.append(player)
        target1 = self.select_target(mask)
        if not target1:
            return False
        # 选择移动的牌
        card = self.select_equip(target1)
        if not card:
            return False
        # 选择移动目标角色
        mask = []
        for player in players:
            pass
        target2 = self.select_target(mask)
        if not target2:
            return False
        target1.lose_card(card)
        target2.get_card(equip=True)
        return True

    # 据守
    def jushou(self, name):
        self.fanmian()
        self.draw_card(4)
        card = self.select_hand(cancel=False)
        if card.type == 2:
            self.use_card(card, target=self)
        else:
            self.drop_card(card)
        return True

    # 移动场上一张牌
    def move_card(self):
        return

    # 解围
    def jiewei(self, name):
        drop_card = self.select_hand(target=self)
        if not drop_card:
            return False
        if self.move_card():
            self.lose_card(drop_card)
            self.core.drop_card(drop_card)
        else:
            return False
        return True

    # 烈弓
    def liegong(self):
        result = 0
        # %2=1则必中，//2=1则+1伤
        if self.get_hand_num() >= self.target.get_hand_num():
            result += 1
        if self.HP <= self.target.HP:
            result += 2
        return result

    # 界狂骨：
    def kuanggu(self, name):
        choice = self.select_choice(name)
        if choice == 0:
            return False
        elif choice == 1:
            self.heal(1)
        else:
            self.draw_card(1)
        return True

    def lose_hp(self, num):
        self.hp -= num

    # 奇谋
    def qimou(self, name):
        choice = self.select_choice(name)
        if choice == 0:
            return False
        else:
            self.lose_hp(choice)
            self.draw_card(choice)
            self.atk_dist_buff = choice
            self.kill_remain += choice
        return True

    # 界不屈
    def buqu(self, name):
        return

    # TODO: 不屈

    def fenji(self, name):
        target = self.core.get_cur_player()
        if self.select_choice(name):
            target.draw_card(2)
            self.lose_hp(1)
        else:
            return False
        return True

    # 界雷击
    def leiji(self, name):
        # TODO: 除自己以外
        target = self.select_target()
        if not target:
            return False
        judge = target.judge()
        judge_color = target.get_color(judge)
        if judge_color == 1:
            target.damage(2)
        elif judge_color == 2:
            self.heal(1)
            target.damage(1)

    def guidao(self, name, judge):
        # TODO:黑色
        card = self.select_own_card()
        if card:
            self.lose_card(card)
            self.get_card(judge)
        return card

    # 界强袭
    def qiangxi(self, name):
        mask = []
        # TODO: 未指定过的角色
        target = self.select_target(mask)
        choice = self.select_choice(name)
        if choice == 0:
            return False
        elif choice == 1:
            self.damage(1, source=self)
        else:
            # TODO: 武器牌
            card = self.select_own_card()
            if card:
                self.drop_card(card)
            else:
                return False
        target.damage(1, source=self)
        return True

    def shuangxiong(self, name):
        pass

    # 狞恶
    def ninge(self, name, target):
        self.draw_card(1)
        card = self.select_area_card(target=target, cancel=False)
        if not card:
            return
        target.drop_card(card)

    # 驱虎
    def quhu(self, name):
        mask = []
        card = self.select_hand()
        if not card:
            return False
        # TODO: 体力>自己，有手牌
        target1 = self.select_target(mask)
        if not target1:
            return False
        result = self.core.pindian(self, target1)
        if result:
            # TODO: 目标攻击范围内角色
            mask = []
            target2 = self.select_target(mask, cancel=False)
            if target2:
                target2.damage(val=1, source=target1)
        else:
            self.damage(val=1, source=target1)
        return True

    # 节命
    def jieming(self, name):
        # TODO: 手牌不满mask
        mask = []
        target = self.select_target(mask=mask)
        if not target:
            return False
        num = min(5, target.maxHP - target.get_hand_num())
        target.draw_card(num)

    # 涅槃
    def niepan(self, name):
        self.drop_all()
        self.reset()
        self.draw_card(3)
        self.heal(3 - self.HP)

    def tianyi(self, name):
        target = self.select_target()
        if not target:
            return False
        result = self.core.pindian(self, target)
        if result:
            self.status.append('天义')
        else:
            self.kill_remain = MIN
        return True

    def luanji(self, name):
        card1 = self.select_hand(1)
        if not card1:
            return False
        # TODO: 不为card且花色相同
        card2 = self.select_hand(1, card1)
        if card2:
            self.use_card([card1, card2])
        else:
            return False
        return True

    # 界猛进
    def mengjin(self, name, card, target):
        drop_card = self.select_own_card(target)
        if not drop_card:
            return False
        if drop_card.type == 0:
            target.status.append('no_shan')
            self.kill_remain += 1
        else:
            target.get_card(card)
        return True

    def xingshang(self, name, target):
        cards = target.lose_all()
        self.get_card(cards)

    def fangzhu(self, name):
        mask = []
        # TODO: 不是自己
        target = self.select_target(mask=mask)
        if target:
            target.fanmian()
            target.draw_card(self.maxHP - self.HP)
        else:
            return False
        return True

    # 界再起
    def zaiqi(self, name):
        drops = self.core.round_drop()
        num = 0
        for card in drops:
            if card.sub_color == 2:
                num += 1
        mask = []
        # TODO: 选择不同人
        act = False
        for _ in num:
            target = self.select_target(mask=mask)
            if not target:
                break
            choice = target.select_choice(name)
            if choice == 0:
                target.draw_card(1)
            else:
                self.heal(1, target)
        return act

    def qiaobian(self, name):
        card = self.select_hand()
        if not card:
            return False
        else:
            self.drop_card(card)

        if self.period == 'draw':
            self.tuxi(name)
        elif self.period == 'act':
            target1 = self.select_target()
            card = self.select_field_card()
            # TODO: 和第一位不同mask且对应位置无牌mask
            target2 = self.select_target()
            target1.lose_card(card)
            target2.get_card(card, equip=True)
        return True

    # 手牌转化
    def longdan(self, name):
        pass

    def wusheng(self, name):
        pass

    def jijiu(self, name):
        pass

    def qingguo(self, name):
        pass

    def lianhuan(self, name):
        pass

    def duanliang(self, name):
        pass

    def huoji(self, name):
        pass

    def kanpo(self):
        pass

    def use_skill(self, name):
        # 需要确认是否发动
        if self.select_choice(name):
            self.skill_dict[name](name)

    def load_skills(self):
        self.skill_dict = {
            '奸雄', self.jianxiong,
            '护驾', self.hujia,
            '反馈', self.fankui,
            '鬼才', self.guicai,
            '刚烈', self.ganglie,
            '突袭', self.tuxi,
            '裸衣', self.luoyi,
            '天妒', self.tiandu,
            '遗计', self.yiji,
            '倾国', self.qingguo,
            '洛神', self.luoshen,
            '仁德', self.rende,
            '激将', self.jijiang,
            '武圣', self.wusheng,
            '观星', self.guanxing,
            '龙胆', self.longdan,
            '铁骑', self.tieji,
            '集智', self.jizhi,
            '制衡', self.zhiheng,
            '奇袭', self.qixi,
            '克己', self.keji,
            '苦肉', self.kurou,
            '凡间', self.fanjian,
            '国色', self.guose,
            '流离', self.liuli,
            '结姻', self.jieyin,
            '枭姬', self.xiaoji,
            '青囊', self.qingnang,
            '急救', self.jijiu,
            '闭月', self.biyue,
            '妄尊', self.wangzun,
            '神速', self.shensu,
            '设变', self.shebian,
            '据守', self.jushou,
            '解围', self.jiewei,
            '烈弓', self.liegong,
            '狂骨', self.kuanggu,
            '奇谋', self.qimou,
            '红颜', self.hongyan,
            '不屈', self.buqu,
            '奋激', self.fenji,
            '雷击', self.leiji,
            '鬼道', self.guidao,
            '蛊惑', self.guhuo,
            '强袭', self.qiangxi,
            '驱虎', self.quhu,
            '节命', self.jieming,
            '连环', self.lianhuan,
            '涅槃', self.niepan,
            '火计', self.huoji,
            '看破', self.kanpo,
            '天义', self.tianyi,
            '乱击', self.luanji,
            '双雄', self.shuangxiong,
            '猛进', self.mengjin,
            '断粮', self.duanliang,
            '截辎', self.jiezi,
            '行殇', self.xingshang,
            '放逐', self.fangzhu,
            '再起', self.zaiqi,
            '烈刃', self.lieren,
            '英魂', self.yinghun,
            '好施', self.haoshi,
            '缔盟', self.dimeng,
            '酒池', self.jiuchi,
            '乱武', self.luanwu,
            '巧变', self.qiaobian,
            '屯田', self.tuntian,
            '急袭', self.jixi,
            '挑衅', self.tiaoxin,
            '放权', self.fangquan,
            '置谏', self.zhijian,
            '固政', self.guzheng,
            '悲歌', self.beige,
            '涉猎', self.shelie,
            '攻心', self.gongxin,
            '琴音', self.qinyin,
            '业炎', self.yeyan,
            '七星', self.qixing,
            '狂风', self.kuangfeng,
            '大雾', self.dawu,
            '归心', self.guixin,
            '无前', self.wuqian,
            '神愤', self.shenfen,
            '龙魂', self.longhun,
            '极略', self.jilue,
            '落英', self.luoying,
            '酒诗', self.jiushi,
            '伤逝', self.shangshi,
            '举荐', self.jujian,
            '散谣', self.sanyao,
            '制蛮', self.zhiman,
            '眩惑', self.xuanhuo,
            '旋风', self.xuanfeng,
            '破军', self.pojun,
            '甘露', self.ganlu,
            '补益', self.buyi,
            '明策', self.mingce,
            '陷阵', self.xianzhen,
            '清俭', self.qingjian,
            '义绝', self.yijue,
            '替身', self.tishen,
            '涯角', self.yajiao,
            '奋威', self.fenwei,
            '武烈', self.wulie,
            '长标', self.changbiao,
        }

    def damage(self, val=1, attr=0, source=None):
        self.HP -= val

    def heal(self, val, source=None):
        self.HP += val

    def get_weapon(self):
        return self.equips[0]

    def get_armor(self):
        return self.equips[1]

    def get_def_horse(self):
        return self.equips[2]

    def get_atk_horse(self):
        return self.equips[3]

    # 攻击距离
    def get_atk_dist(self, include_weapon=True):
        weapon = self.get_weapon()
        if include_weapon and weapon:
            dist = self.get_weapon().dist
        else:
            dist = 1
        if '马术' in self.skills:
            dist += 1
        if self.get_atk_horse():
            dist += 1
        return dist

    # 防御距离
    def get_def_dist(self):
        dist = 0
        if '飞影' in self.skills:
            dist += 1
        if self.get_def_horse():
            dist += 1
        return dist

    # 获得所有攻击范围内的角色
    def get_target_in_dist(self, include_weapon=True, include_self=False, buff=0):
        players = self.core.get_players()
        atk_dist = self.get_atk_dist(include_weapon)
        targets = []
        for player in players:
            if player.pid == self.pid:
                if include_self:
                    targets.append(player)
                continue
            def_dist = player.get_def_dist()
            if atk_dist > def_dist:
                targets.append(player)
        return targets
