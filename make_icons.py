"""Генерирует иконки (icon-180/192/512.png): виниловая пластинка с неоновым градиентом на тёмном фоне."""
from PIL import Image, ImageDraw, ImageFilter
import math, os

HERE = os.path.dirname(os.path.abspath(__file__))
S = 1024
C = S // 2


def lerp(a, b, t):
    return tuple(int(x + (y - x) * t) for x, y in zip(a, b))


# фон: тёмный с фиолетовым свечением
img = Image.new('RGB', (S, S), (11, 9, 18))
glow = Image.new('RGB', (S, S), (0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse((60, 40, 900, 880), fill=(110, 50, 200))
gd.ellipse((420, 360, 1100, 1040), fill=(200, 40, 140))
glow = glow.filter(ImageFilter.GaussianBlur(170))
img = Image.blend(img, glow, 0.55).convert('RGBA')

# неоновое кольцо (градиент розовый → фиолетовый → голубой)
ring = Image.new('RGBA', (S, S), (0, 0, 0, 0))
stops = [(255, 60, 172), (139, 92, 255), (43, 210, 255)]
R0, R1 = 340, 372
px = ring.load()
for y in range(S):
    for x in range(S):
        r = math.hypot(x - C, y - C)
        if R0 - 30 <= r <= R1 + 30:
            t = ((math.atan2(y - C, x - C) + math.pi) / (2 * math.pi) + 0.15) % 1 * 3  # замкнутый круг цветов без стыка
            i = int(t) % 3
            col = lerp(stops[i], stops[(i + 1) % 3], t - int(t))
            if R0 <= r <= R1:
                px[x, y] = col + (255,)
            else:
                d = (R0 - r) if r < R0 else (r - R1)
                px[x, y] = col + (int(150 * (1 - d / 30) ** 2),)
img.alpha_composite(ring.filter(ImageFilter.GaussianBlur(10)))
img.alpha_composite(ring)

# пластинка
d = ImageDraw.Draw(img)
d.ellipse((C - 330, C - 330, C + 330, C + 330), fill=(18, 15, 28))
for rr in range(110, 320, 18):
    d.ellipse((C - rr, C - rr, C + rr, C + rr), outline=(40, 34, 58), width=3)
# блик
hl = Image.new('L', (S, S), 0)
ImageDraw.Draw(hl).pieslice((C - 320, C - 320, C + 320, C + 320), 200, 245, fill=60)
img.paste((255, 255, 255, 255), (0, 0), hl.filter(ImageFilter.GaussianBlur(20)))
d = ImageDraw.Draw(img)
# яблоко пластинки
lab = Image.new('RGBA', (S, S), (0, 0, 0, 0))
lm = Image.new('L', (S, S), 0)
ImageDraw.Draw(lm).ellipse((C - 105, C - 105, C + 105, C + 105), fill=255)
lg = Image.new('RGBA', (S, S))
lp = lg.load()
for y in range(C - 106, C + 106):
    for x in range(C - 106, C + 106):
        t = max(0, min(1, ((x - C) + (y - C) + 210) / 420))
        lp[x, y] = lerp(stops[0], stops[2], t) + (255,)
lab.paste(lg, (0, 0), lm)
img.alpha_composite(lab)
d.ellipse((C - 16, C - 16, C + 16, C + 16), fill=(11, 9, 18))

for size in (180, 192, 512):
    img.convert('RGB').resize((size, size), Image.LANCZOS).save(os.path.join(HERE, f'icon-{size}.png'))
print('ok')
