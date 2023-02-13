import os
import math
from PIL import Image, ImageFont, ImageDraw, ImageShow

from bot_init import BOT

# config
config = BOT.get_modules_config('break_tofu')
#说明： 字体文件来自 天珩全字库(TH-Tshyn)(http://cheonhyeong.com/Simplified/download.html)
#全字库路径
if BOT.sys == 'Windows':
    font_path = config['font_path_windows']
elif BOT.sys == 'Linux':
    font_path = config['font_path_linux']


# font config
fonts = {

#"TH-Times.ttc",
0 : "TH-Tshyn-P0.ttf",
1 : "TH-Tshyn-P1.ttf",
2 : "TH-Tshyn-P2.ttf",
# "TH-Tshyn-P16.ttf"
}

def char2image(string: str, font_size=60, background_color=(255, 255, 255), char_color=(0, 0, 0)):
    fonts_list = truetype_list_creater(fonts, font_size)
    # 画布
    bbox = fonts_list[0].getbbox(string)
    w = bbox[2] + 20
    h = bbox[3] + 20
    img = Image.new("RGB", (w, h), background_color)
    # 画笔
    draw_text = ImageDraw.Draw(img)


    # --- TESTING ---
    # 长度限制换行处理
    sl = string.split('\n')
    sl2 = []
    i = 0
    while i < len(sl):
        if len(sl[i]) > 26:
            sl2.append(sl[i][:26])
            sl.insert(i + 1, sl[i][26:])
        else:
            sl2.append(sl[i])
        i += 1
    print(sl2)
    string = '\n'.join(sl2)

    # 多行文本画布大小计算
    m = draw_text.multiline_textbbox((0, 0), string, fonts_list[0], spacing=font_size)
    print(m)
    t_w = m[2] + 20
    t_h = m[3] + 20
    w = t_w
    h = t_h
    img = Image.new("RGB", (w, h), background_color)
    draw_text = ImageDraw.Draw(img)
    # --- END ---

    x = 10
    y = 10
    # 绘制
    for c in string:
        font = font_selector(c, fonts_list)
        # 换行
        if (x + font.getbbox(c)[2]) > w or c == '\n':
            y += font.getbbox(c)[3] + 10
            x = 10
            if c == '\n':
                continue
        draw_text.text((x, y), c, char_color, font)
        x += font.getlength(c)
    return img

def truetype_list_creater(fonts: dict, font_size=60):
    # create fonts list
    fonts_list = []
    for f in fonts.values():
        fonts_list.append(ImageFont.truetype(os.path.join(font_path, f), font_size))
    return fonts_list

def font_selector(char, fonts_list):
    char = ord(char)
    # H G
    if (
        0x30000 <= char <= 0x3134a
        or 0x31350 <= char <= 0x323af
    ):
        font = fonts_list[1]
    # B C D E F
    elif (
        0x20000 <= char <= 0x2A6D6
        or 0x2A700 <= char <= 0x2B734
        or 0x2B740 <= char <= 0x2B81D
        or 0x2B820 <= char <= 0x2CEAF
        or 0x2CEB0 <= char <= 0x2EBEF
    ):
        font = fonts_list[2]
    # default
    else:
        font = fonts_list[0]
    return font


if __name__ == '__main__':
    i = input('INPUT TEXT:\n')
    img = char2image(i)
    img.show()