from bot_init import BOT
#SYS = "Windows"
import io
import os
import math
from PIL.ImageFont import FreeTypeFont
from PIL import Image, ImageFont, ImageDraw, ImageShow

#读取配置
config = BOT.get_modules_config('break_tofu')
#说明： 字体文件来自 天珩全字库(TH-Tshyn)(http://cheonhyeong.com/Simplified/download.html)
#全字库路径
if BOT.sys == 'Windows':
    th_font_path = config['font_path_windows']
elif BOT.sys == 'Linux':
    th_font_path = config['font_path_linux']
#字体文件中未收录的字符
undecode_char = "\U0010ffff"
#自动换行——单行字数
line_max = 26

def char2image(string: str, font_size=60, background_color=(255, 255, 255), char_color=(0, 0, 0)):
    # 字体列表
    fontt = ImageFont.truetype(os.path.join(th_font_path, "TH-Times.ttc"), font_size)
    font0 = ImageFont.truetype(os.path.join(th_font_path, "TH-Tshyn-P0.ttf"), font_size)
    font1 = ImageFont.truetype(os.path.join(th_font_path, "TH-Tshyn-P1.ttf"), font_size)
    font2 = ImageFont.truetype(os.path.join(th_font_path, "TH-Tshyn-P2.ttf"), font_size)
    font16 = ImageFont.truetype(os.path.join(th_font_path, "TH-Tshyn-P16.ttf"), font_size)
    font_l = [fontt, font0, font1, font2, font16]
    # 画布大小计算，文字预处理
    str_len = len(string)
    if str_len <= line_max:
        width = font_l[0].getsize(string)[0] + 30
        height = font_l[0].getsize(string)[1] + 20
    else:
        # 画布
        line_num = math.ceil(str_len/line_max)
        w = font_l[0].getsize('　')[0]
        h = font_l[0].getsize('　')[1]
        width = w * line_max + 30
        height = h * line_num + 20
        # 文字
        string_list = []
        g = sub_string_generator(string, line_max)
        try:
            while True:
                string_list.append(next(g))
        except StopIteration:
            print("文字切分完毕")
            pass
        string = string_list
    img = Image.new("RGB", (width, height), background_color)

    # 渲染单行 函数
    def draw_line(img, string, x=0, y=10):
        # 渲染 单行
        for s in string:
            #print(s)
            for f in font_l:
                #print(f.getname())
                f = f
                img1 = add_string2img(img, f, (x, y), s, char_color)
                img2 = add_string2img(img, f, (x, y), undecode_char, char_color)
                img1_b = img2bytes(img1)
                img2_b = img2bytes(img2)
                if img1_b != img2_b:
                    img = img1
                    break
            img = img1
            x += f.getsize(s)[0]
            #print(f"下一个渲染开始点{starting}")
        return img

    # 渲染
    if type(string) == list:
        x , y = 0, 0
        for s in string:
            img = draw_line(img, s, x, y)
            y += font_l[0].getsize('　')[1]
        return img2bytes(img)
    else:
        img = draw_line(img, string)
        return img2bytes(img)

def add_string2img(img: Image, f: FreeTypeFont, starting_xy: tuple, s: str, char_color: tuple):
    img_cp = Image.Image.copy(img)  #复制img到img_cp
    darw_text = ImageDraw.Draw(img_cp)
    darw_text.text(starting_xy, s, char_color, font=f)
    return img_cp

def img2bytes(img: Image):
    img_b = io.BytesIO()
    img.save(img_b, format='png', save_all=True)
    img_b = img_b.getvalue()
    return img_b

def sub_string_generator(string:str, n:int):
    """
    子字符串生成器
    string：父字符串
    n：每次取出的长度
    next()返回每次取出的字符串
    """
    start, end = 0, n
    count = math.ceil(len(string)/n)
    while count > 0:
        s = string[start:end]
        yield s
        end += n
        start += n
        count -= 1
    return

#豆腐块测试：
if __name__ == '__main__':
    s1 = "ﺢÿ𓐒ᐲ𒍁𱍁"
    s2 = "次次都着样𛆅策⼠"
    s3 = "𬳰𬳱𬳲𬳳𬳴𬳵𬳶𬳷"
    s4 = "𣥄𨛜𰒥𠄏𢨋𧹂𮗙㫈㪳㔔𤕈𠪳𦹗𢀓𡆢𠄷𠕲𠙴𡦹𠇇𠄓𠃉𡧑𦱼𠆭𠄔𦮙𠍋𠐲𠁼𪛗𪛘𪛙𪛚𪛛𪛜𪛝𫬯"
    u13 = "𰻞𫜵"
    u132 = "𰻝"
    cjkh = "𱍐"
    longtext = """这是一段长文字这是一段长文字这是一段长文字这是一段长文字这是一段长文字这是一段长文字这是一段长文字这是一段长文字"""
    img = char2image(longtext)
    ImageShow.show(img)
    exit()