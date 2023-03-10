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
    def __init__(self, level: int) -> str:
        """
        初始化一局游戏

        level: 生成等级（遮挡的复杂度，不等于难度）
        """
        # 默认随机字符范围
        self.tofu = self.random_char(
            [
                (0x3400, 0x4DBF),    # 扩A
                (0x9FCD, 0x9FFF),    # 急用汉字
                (0x20000, 0x2A6DF),  # 扩B
                (0x2A700, 0x2B739),  # 扩C
                (0x2B740,0x2B81D),   # 扩D
                (0x2B820, 0x2CEAF),  # 扩E
                (0x2CEB0, 0x2EBEF),  # 扩F
                (0x30000, 0x3134A),  # 扩G
                (0x31350, 0x323AF),  # 扩H
            ]
        )
        # 豆腐块图片（原图）
        self.img = None

        # 被遮挡的豆腐块图片
        self.img_masked = None

        # 等级选择
        if level==0:
            self.tofu = self.random_char(
                [
                    (0x4E00, 0x9FFF),  # 基本
                ]
            )
            self.rule = self.random_mask_rule(
                random.randint(1, 10),
                random.randint(1, 10)
            )
        elif level==1:
            self.rule = self.random_mask_rule(
                random.randint(1, 2),
                random.randint(1, 2)
            )
        elif level==2:
            self.rule = self.random_mask_rule(
                random.randint(3, 4),
                random.randint(3, 4)
            )
        elif level==3:
            self.rule = self.random_mask_rule(
                random.randint(5, 6),
                random.randint(5, 6)
            )
        elif level==4:
            self.rule = self.random_mask_rule(
                random.randint(6, 10),
                random.randint(6, 10)
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
        pass

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
        获取大小为x * y的随机(0/1)二维数组
        """
        rule = [
            [ random.randint(0, 1) for i in range(x) ]
            for j in range(y)
        ]
        rule[0][0] = 0
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
        """
        y = 0
        for r in self.rule:
            x = 0
            for b in r:
                if b == 1:
                    self.rule[y][x] = 0
                    return
                x += 1
            y += 1

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
        mask_block = Image.new("RGB", (mask_block_width, mask_block_height), (0xff, 0x14, 0x93))

        # 使用遮挡块
        y = 0
        for r in self.rule:
            x = 0
            for b in r:
                if b:
                    self.img_masked.paste(mask_block, (x, y))
                x += mask_block_width
            y += mask_block_height
