"""把 AI 底图裁成 3:4 并排上精确中文，生成小红书封面 1080x1440。
改标题/价格只需改下面的文案常量，重跑即可。"""
from PIL import Image, ImageDraw, ImageFont
import os

BASE = "/Users/liqianyu/WorkBuddy/2026-11-13-12-59-28"
SRC = os.path.join(BASE, "generated-images", "A_clean_soft_3D_pastel_illustr_2026-11-13T05-29-20.png")
OUT = os.path.join(BASE, "小红书封面_心动测试_1080x1440.png")
FONT = "/System/Library/Fonts/PingFang.ttc"

W, H = 1080, 1440
LABEL = "趣味测试 · 32 道单选题"
TITLE_1 = "测一测，TA 是不是"
TITLE_2 = "也在偷偷喜欢你"
SUBTITLE = "凭你的心动细节，匹配 TA 的真实心意"
CARD_MAIN = "0.99 尝鲜价 · 拍下自动发货"
CARD_SUB = "32 道题 · 10 种心意结果 · 3 分钟测完"

INK = (59, 43, 51)
PINK = (240, 67, 108)
SOFT = (146, 116, 132)


def font(size):
    return ImageFont.truetype(FONT, size)


img = Image.open(SRC).convert("RGB")
cw, ch = img.size
# 从顶部取 3:4 区域，顺带裁掉原图右下角的 AI 生成水印
crop_h = int(cw * H / W)
img = img.crop((0, 0, cw, min(crop_h, ch)))
img = img.resize((W, H), Image.Resampling.LANCZOS)

draw = ImageDraw.Draw(img, "RGBA")

# 顶部胶囊标签
lf = font(30)
bbox = draw.textbbox((0, 0), LABEL, font=lf)
lw = bbox[2] - bbox[0]
lx, ly = 72, 116
draw.rounded_rectangle((lx, ly, lx + lw + 60, ly + 64), radius=32,
                       fill=(255, 255, 255, 225), outline=(255, 190, 212, 255), width=2)
draw.text((lx + 30, ly + 14), LABEL, font=lf, fill=PINK)

# 主标题（两行，白色描边保证在浅色底图上清晰）
tf = font(82)
draw.text((72, 226), TITLE_1, font=tf, fill=INK, stroke_width=3, stroke_fill=(255, 255, 255, 190))
draw.text((72, 334), TITLE_2, font=tf, fill=PINK, stroke_width=3, stroke_fill=(255, 255, 255, 190))

# 副标题
draw.text((76, 478), SUBTITLE, font=font(36), fill=SOFT)

# 底部信息卡（半透明，保留底图质感）
card = (72, 1150, 1008, 1352)
draw.rounded_rectangle(card, radius=38,
                       fill=(255, 255, 255, 214), outline=(255, 214, 226, 255), width=2)
draw.text((112, 1188), CARD_SUB, font=font(30), fill=SOFT)
draw.text((112, 1240), CARD_MAIN, font=font(46), fill=PINK,
          stroke_width=1, stroke_fill=(255, 255, 255, 160))
# 卡片右侧小爱心（纯图形，避免 emoji 字体缺字）
cx, cy, s = 918, 1258, 20
draw.ellipse((cx - s, cy - s, cx, cy), fill=(255, 150, 180, 235))
draw.ellipse((cx, cy - s, cx + s, cy), fill=(255, 150, 180, 235))
draw.polygon([(cx - s, cy - 3), (cx + s, cy - 3), (cx, cy + s + 8)], fill=(255, 150, 180, 235))

img.save(OUT, "PNG", quality=95)
print("saved:", OUT, img.size)
