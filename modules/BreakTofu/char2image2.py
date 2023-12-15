import os
import io
from PIL import Image, ImageFont, ImageDraw
from fontTools.ttLib import TTFont


def char2image(
    string: str,
    fonts_dict: list,
    offset=(20, 60, 30),
    background_color=(255, 255, 255),
    char_color=(0, 0, 0),
    #highlight_char_color=(99, 99, 99)  # 目前指定Unicode CJKV ExtI 为“高亮”. 取I（9）为颜色编码（十进制
    highlight_char_color=(0, 0, 0)
    ):
    """
    string: 需要渲染的字符（串）
    font_size: 字体大小
    offset: 文本的偏移信息，格式：(x初始位置, y初始位置, 行间距)  单位：像素
    background_color: 背景颜色
    char_color: 字符颜色
    highlight_char_color: 高亮字符颜色

    Returns: 图片/img
    """
    # 借用临时画布、画笔
    tmp = Image.new("RGB", (0, 0), background_color)
    tmp_draw = ImageDraw.Draw(tmp)


    # --- TESTING ---
    # 生成画布
    x = offset[0]
    y = offset[1]
    init_x = x
    line_space = offset[2]
    # 进行图片大小的预测计算，取(宽，高)最大值
    # 输入偏移信息、理想化后的字符串、字体、行间距
    img_size = ()
    for font in fonts_dict:
        s = tmp_draw.multiline_textbbox((x*2, y*2), idealize_text(string), font[1], spacing=line_space)
        img_size = max(img_size, (s[2], s[3]))
    # 删除借用的画布、画笔
    del tmp, tmp_draw
    t_w = img_size[0]
    t_h = img_size[1]
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
        if 0x2EBF0 <= ord(c) <= 0x2EE5D:
            # 高亮字符
            draw_text.text((x, y), c, highlight_char_color, font)
        else:
            # 正常字符
            draw_text.text((x, y), c, char_color, font)
        x += font.getlength(c)
    
    # return
    return img

def image2bytes(img: Image)->bytes:
    result = io.BytesIO()
    img.save(result, format='png', save_all=True)
    return result.getvalue()

def truetype_fonts_creater(fonts: dict, font_path: str, font_size: int):
    """
    fonts  {Plane: str} -> fonts: {Plane: ImageFont}

    fonts: fonts = {"P0": Plane0_font, "P1": Plane1_font, "P2": Plane2_font}
    font_size: font size

    Returns: fonts_dict = {"P0": Plane0_font, "P1": Plane1_font, "P2": Plane2_font}
    """
    # create fonts dict
    fonts_dict = {}
    for p, f in fonts.items():
        fonts_dict[p] = ImageFont.truetype(os.path.join(font_path, f), font_size)
    return fonts_dict

def fonts_loader(fonts: dict, fonts_path: str, font_size: int)->list:
    """
    create a fonts dict like `[[Cmap, ImageFont], ……]`

    fonts: `{font_info : font_name}`
    font_size: font size
    """
    fonts_dict = []
    for f in fonts.values():
        f = os.path.join(fonts_path, f)
        # get Cmap as key
        if os.path.splitext(f)[-1] == '.ttf':
            ttf = TTFont(f)
            key = tuple(ttf.getBestCmap().keys())
        else:
            continue
        # create ImageFont as value
        value = ImageFont.truetype(f, font_size)
        # push key and value to fonts_dict
        fonts_dict.append([key, value])
    return fonts_dict

def font_selector(char, fonts_dict):
    """
    Select a font to draw char.

    char: one char
    fonts_dict: fonts dict

    Returns: font
    """
    for fd in fonts_dict:
        if ord(char) in fd[0]:
            # If font contains this char, use it.
            return fd[1]
    # Default:
    return fonts_dict[0][1]

def idealize_text(text: str) -> str:
    # 对文本排版
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


if __name__ == '__main__':
    fonts = {
        # 按优先级排序
        "ttc" : "TH-Times.ttc",
        "P0" : "TH-Tshyn-P0.ttf",
        "P1" : "TH-Tshyn-P1.ttf",
        "P2" : "TH-Tshyn-P2.ttf",
        "P16" : "TH-Tshyn-P16.ttf",
        "extend I" : "扩展B-I Regular.ttf"
    }
    fpath = input('fpath=')
    string = input('text:\n')
    fd = fonts_loader(fonts, fpath, 60)
    img = char2image(string, fd, offset=(10, 10, 10))
    img.show()
    
