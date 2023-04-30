# -*- coding: utf-8 -*-

import random
import math
from PIL import Image

class GuessTofu():
    """
    一局猜豆腐游戏

    基本流程：
    1. 初始化游戏
        根据等级(level)，生成随机的字符(tofu)和遮挡块规则(rule)
    2. 生成遮挡后的字符图片
        根据遮挡规则(rule)，调用masker函数生成img_masked
    3. 减少遮挡
        调用后顺序减少(mask_rule_reduce)或随机减少(mask_rule_reduce2)遮挡块
    """
    COMPETE_MAX_LEVEL = 6

    def __init__(self, level: int, char_range=[]) -> str:
        """
        初始化一局游戏

        level: 生成等级（遮挡的复杂度，不等于难度）
        """
        self.level = level
        # 默认随机字符范围
        cjk_a = (0x3400, 0x4DBF)    # 扩A
        cjk_jy = (0x9FCD, 0x9FFF)   # 急用汉字
        cjk_b = (0x20000, 0x2A6DF)  # 扩B
        cjk_c = (0x2A700, 0x2B739)  # 扩C
        cjk_d = (0x2B740, 0x2B81D)  # 扩D
        cjk_e = (0x2B820, 0x2CEAF)  # 扩E
        cjk_f = (0x2CEB0, 0x2EBEF)  # 扩F
        cjk_g = (0x30000, 0x3134A)  # 扩G
        cjk_h = (0x31350, 0x323AF)  # 扩H
        if char_range:
            self.tofu = self.random_char(char_range)
        elif level == 0:
            self.tofu = self.random_char([(0x4E00, 0x9FFF)])
        else:
            self.tofu = self.random_char(
                [cjk_a, cjk_jy, cjk_b, cjk_c, cjk_d, cjk_e, cjk_f, cjk_g, cjk_h]
            )
        # 豆腐块图片（原图）
        self.img = None

        # 被遮挡的豆腐块图片
        self.img_masked = None

        # 总分数
        self.score = 0
        
        # 遮挡数
        self.maskCount = 0
        # 理论最大遮挡
        self.maxCount = 0
        
        # 等级选择
        if level==0:
            self.rule = self.random_mask_rule2(
                random.randint(1, 10),
                random.randint(1, 10)
            )
        elif level==1:
            self.rule = self.random_mask_rule2(
                random.randint(1, 2),
                random.randint(1, 2)
            )
        elif level==2:
            self.rule = self.random_mask_rule2(
                random.randint(3, 4),
                random.randint(3, 4),
                0.6
            )
        elif level==3:
            self.rule = self.random_mask_rule2(
                random.randint(5, 6),
                random.randint(5, 6),
                0.7
            )
        elif level==4:
            self.rule = self.random_mask_rule2(
                random.randint(6, 10),
                random.randint(6, 10),
                0.8
            )
        elif level==5:
            self.rule = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],    # 1
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],    # 2
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],    # 3
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],    # 4
                [0, 1, 1, 1, 1, 0, 1, 1, 1, 0],    # 5
                [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],    # 6
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],    # 7
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],    # 8
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],    # 9
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],    # 10
            ]
            self.maxCount = 100
            sum = 0
            for l in self.rule:
                sum += l.count(1)
            self.maskCount = sum
            self.score = int((self.maskCount / self.maxCount) * ((self.level + 1) * 10)) + 1
        elif level==6:
            self.rule = self.random_mask_rule2(
                100, 100, 0.9
            )
        elif level==7:
            self.rule = self.random_mask_rule2(
                100, 100, 0.99
            )

    def random_char(self, range_list: list[tuple[int]]):
        """
        range_list: 范围列表

        根据传入的范围获取随机字符
        """
        return chr(
            random.choice(
            [ random.randint(a,b) for a,b in range_list ]
            )
        )

    def random_mask_rule(self, x, y)->list[list]:
        """
        获取大小为 x * y 的随机(0/1) 二维数组
        """
        rule = [
            [ random.randint(0, 1) for i in range(x) ]
            for j in range(y)
        ]
        rule[0][0] = 0
        # 计算总分
        sum = 0
        for l in rule:
            sum += l.count(1)
        self.maskCount = sum
        self.maxCount = x*y
        self.score = int((self.maskCount / self.maxCount) * ((self.level + 1) * 10)) + 1
        return rule

    def random_mask_rule2(self, x, y, p=0.5)->list[list]:
        """
        获取大小为 x * y 的随机(0/1) 二维数组,有p的概率为1(p的范围[0,1])
        """
        random.seed()
        rule = [
            [ random.choices([0, 1], weights=[1-p, p])[0] for i in range(x) ]
            for j in range(y)
        ]
        rule[0][0] = 0
        # 计算总分
        sum = 0
        for l in rule:
            sum += l.count(1)
        self.maskCount = sum
        print(self.maskCount)
        self.maxCount = x*y
        self.score = int((self.maskCount / self.maxCount) * ((self.level + 1) * 10)) + 1
        return rule

    def set_img(self, img):
        """
        设置初始img
        """
        self.img = img
        self.img_masked = self.img.copy()

    def mask_rule_reduce(self):
        """
        按顺序去除一个遮挡块

        Returns: True成功 False失败
        """
        y = 0
        for r in self.rule:
            x = 0
            for b in r:
                if b == 1:
                    self.rule[y][x] = 0
                    return True
                x += 1
            y += 1
        return False

    def mask_rule_reduce2(self):
        """
        随机去除一个遮挡块
        """
        rnum = random.randint(0, len(self.rule) - 1)
        bnum = random.randint(0, len(self.rule[0]) - 1)
        while rnum < len(self.rule):
            try:
                # print(f"rnum={rnum}\tbnum={bnum}")
                n = self.rule[rnum].index(1, bnum)
                self.rule[rnum][n] = 0
                return
            except:
                rnum += 1
        self.mask_rule_reduce()
        if self.maskCount > 0:
            self.maskCount -= 1
        self.score = int((self.maskCount / self.maxCount) * ((self.level + 1) * 10)) + 1
        return

    def masker(self):
        """
        按self.rule设置遮挡块到self.img_masked
        """
        # 复制一份
        self.img_masked = self.img.copy()

        # 根据rule 制作遮挡块
        w, h = self.img_masked.size
        row_count = len(self.rule)
        column_count = len(self.rule[0])
        mask_block_width = math.ceil(w/column_count)
        mask_block_height = math.ceil(h/row_count)
        mask_block = Image.new("RGB", (mask_block_width, mask_block_height),
                                (random.randint(0, 0xff), random.randint(0, 0xff),
                                random.randint(0, 0xff)))
                                # (0xff, 0x14, 0x93))

        # 使用遮挡块
        y = 0
        for r in self.rule:
            x = 0
            for b in r:
                if b:
                    self.img_masked.paste(mask_block, (x, y))
                x += mask_block_width
            y += mask_block_height
