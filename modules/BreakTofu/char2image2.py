import os
import io
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
# format:
# "Plane" : "font"

# "TH-Times.ttc",
"P0" : "TH-Tshyn-P0.ttf",
"P1" : "TH-Tshyn-P1.ttf",
"P2" : "TH-Tshyn-P2.ttf",
# "TH-Tshyn-P16.ttf"
}

def char2image(
    string: str,
    font_size=60,
    offset=(20, 60, 30),
    background_color=(255, 255, 255),
    char_color=(0, 0, 0)
    ):
    """
    string: 需要渲染的字符（串）
    font_size: 字体大小
    offset: 文本的偏移信息，格式：(x初始位置, y初始位置, 行间距)  单位：像素
    background_color: 背景颜色
    char_color: 字符颜色

    Returns: 图片/img
    """
    fonts_dict = truetype_fonts_creater(fonts, font_size)
    # 借用画布、画笔
    tmp = Image.new("RGB", (0, 0), background_color)
    draw_text = ImageDraw.Draw(tmp)


    # --- TESTING ---
    # 生成画布
    x = offset[0]
    y = offset[1]
    init_x = x
    line_space = offset[2]
    # 进行图片大小的预测计算
    # 输入偏移信息、理想化后的字符串、字体、行间距
    img_size = draw_text.multiline_textbbox((x*2, y*2), idealize_text(string), list(fonts_dict.values())[0], spacing=line_space)
    # 删除借用的画布、画笔
    del tmp, draw_text
    t_w = img_size[2]
    t_h = img_size[3]
    w = t_w
    h = t_h
    img = Image.new("RGB", (w, h), background_color)
    draw_text = ImageDraw.Draw(img)
    # --- END ---


    # 绘制
    for c in string:
        font = font_selector(c, fonts_dict)
        # 换行
        if (x + font.getbbox(c)[2]) > (w - init_x) or c == '\n':
            y += font.getbbox(c)[3] + line_space
            x = init_x
            if c == '\n':
                continue
        draw_text.text((x, y), c, char_color, font)
        x += font.getlength(c)
    
    # DEBUG
    return img

    # io
    result = io.BytesIO()
    img.save(result, format='png', save_all=True)
    return result.getvalue()

def truetype_fonts_creater(fonts: dict, font_size: int):
    """
    fonts: str -> fonts: ImageFont

    fonts: fonts = {"P0": Plane0_font, "P1": Plane1_font, "P2": Plane2_font}
    font_size: font size

    Returns: fonts_dict = {"P0": Plane0_font, "P1": Plane1_font, "P2": Plane2_font}
    """
    # create fonts dict
    fonts_dict = {}
    for p, f in fonts.items():
        fonts_dict[p] = ImageFont.truetype(os.path.join(font_path, f), font_size)
    return fonts_dict

def font_selector(char, fonts_dict):
    """
    Select a font to draw char.

    char: one char
    fonts_dict: fonts dict

    Returns: font
    """
    char = ord(char)
    # H G -> Plane 1
    if (
        0x30000 <= char <= 0x3134a
        or 0x31350 <= char <= 0x323af
    ):
        font = fonts_dict["P1"]
    # B C D E F -> Plane 2
    elif (
        0x20000 <= char <= 0x2A6D6
        or 0x2A700 <= char <= 0x2B734
        or 0x2B740 <= char <= 0x2B81D
        or 0x2B820 <= char <= 0x2CEAF
        or 0x2CEB0 <= char <= 0x2EBEF
    ):
        font = fonts_dict["P2"]
    # default -> Plane 0
    else:
        font = fonts_dict["P0"]
    return font

def idealize_text(text: str) -> str:
    """
    text: origin text

    Returns: idealization text
    """
    sl = text.split('\n')
    sl2 = []
    i = 0
    while i < len(sl):
        if len(sl[i]) > 26:
            sl2.append(sl[i][:26])
            sl.insert(i + 1, sl[i][26:])
        else:
            sl2.append(sl[i])
        i += 1
    return '\n'.join(sl2)
