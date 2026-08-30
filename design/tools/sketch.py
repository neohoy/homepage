import random, math
random.seed(5)

W, H = 560, 420
HZ = 296.0
VPL = (-620.0, HZ)
VPR = (1180.0, HZ)
INK = "#22304A"
BLU = "#2F62C4"

def y_at(P, VP, x):
    px, py = P; vx, vy = VP
    return py + (x - px) * (vy - py) / (vx - px)

P = []

def bow(x1, y1, x2, y2, w=1.5, o=1.0, col=INK, k=None, over=0.0):
    """手绘线：微弯 + 端点抖动 + 可选出头"""
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    x1 -= ux * over; y1 -= uy * over
    x2 += ux * over; y2 += uy * over
    if k is None:
        k = random.uniform(-1.0, 1.0) * min(L * 0.006, 1.6)
    mx, my = (x1 + x2) / 2 - uy * k, (y1 + y2) / 2 + ux * k
    j = 0.7
    return (f'<path d="M{x1+random.uniform(-j,j):.1f} {y1+random.uniform(-j,j):.1f}'
            f'Q{mx:.1f} {my:.1f} {x2+random.uniform(-j,j):.1f} {y2+random.uniform(-j,j):.1f}" '
            f'stroke="{col}" stroke-opacity="{o}" stroke-width="{w}" stroke-linecap="round"/>')

def edge(x1, y1, x2, y2, w=2.0, over=9.0):
    """主轮廓：画两遍，第二遍更轻，端点出头"""
    P.append(bow(x1, y1, x2, y2, w, 0.95, over=over))
    P.append(bow(x1, y1, x2, y2, w * 0.5, 0.30, over=over * 0.5))

def light(x1, y1, x2, y2, w=0.85, o=0.40):
    P.append(bow(x1, y1, x2, y2, w, o))

def face_xs(x0, x1, n, k=0.6):
    return [x0 + (x1 - x0) * (t / (t + (1 - t) * k)) for t in (i / n for i in range(1, n))]

# ═══ 主塔（偏右）═══════════════════════════════════
NX, TOP, BOT = 330.0, 74.0, 318.0
LX, RX = 196.0, 470.0
edge(NX, TOP, NX, BOT, 2.2, 12)
edge(LX, y_at((NX, TOP), VPL, LX), NX, TOP, 1.9)
edge(NX, TOP, RX, y_at((NX, TOP), VPR, RX), 1.9)
edge(LX, y_at((NX, TOP), VPL, LX), LX, y_at((NX, BOT), VPL, LX), 1.8, 7)
edge(RX, y_at((NX, TOP), VPR, RX), RX, y_at((NX, BOT), VPR, RX), 1.8, 7)
edge(LX, y_at((NX, BOT), VPL, LX), NX, BOT, 1.7)
edge(NX, BOT, RX, y_at((NX, BOT), VPR, RX), 1.7)

def part(x0, y0, x1, y1, frac, w, o):
    """从近角往外只画一部分 —— 手绘不会每格都画满"""
    light(x0, y0, x0 + (x1 - x0) * frac, y0 + (y1 - y0) * frac, w, o)

# 顶部退台
SB = 26.0
edge(NX, TOP - SB, NX, TOP, 1.7, 6)
edge(LX + 40, y_at((NX, TOP - SB), VPL, LX + 40), NX, TOP - SB, 1.5)
edge(NX, TOP - SB, RX - 46, y_at((NX, TOP - SB), VPR, RX - 46), 1.5)
edge(LX + 40, y_at((NX, TOP - SB), VPL, LX + 40), LX + 40, y_at((NX, TOP), VPL, LX + 40), 1.4, 4)
edge(RX - 46, y_at((NX, TOP - SB), VPR, RX - 46), RX - 46, y_at((NX, TOP), VPR, RX - 46), 1.4, 4)

for i in range(1, 9):                      # 楼层线
    yy = TOP + (BOT - TOP) * i / 9
    fade = 1.0 - 0.55 * (i / 9)
    if i >= 8:                             # 最底一道画满，楼要落地
        light(NX, yy, LX, y_at((NX, yy), VPL, LX), 0.9, 0.4)
        light(NX, yy, RX, y_at((NX, yy), VPR, RX), 0.9, 0.4)
        continue
    if random.random() > 0.18:
        part(NX, yy, LX, y_at((NX, yy), VPL, LX),
             random.uniform(0.55, 1.0), 0.8, random.uniform(0.24, 0.46) * fade + 0.06)
    if random.random() > 0.18:
        part(NX, yy, RX, y_at((NX, yy), VPR, RX),
             random.uniform(0.6, 1.0), 0.8, random.uniform(0.24, 0.46) * fade + 0.06)

for j, x in enumerate(face_xs(NX, LX, 4)): # 竖挺，只画上半段
    if random.random() > 0.15:
        yt = y_at((NX, TOP), VPL, x); yb = y_at((NX, BOT), VPL, x)
        light(x, yt, yt + (yb - yt) * random.uniform(0.5, 0.92), 0, 0)
        P[-1] = bow(x, yt, x, yt + (yb - yt) * random.uniform(0.5, 0.92), 0.75, random.uniform(0.2, 0.34))
for j, x in enumerate(face_xs(NX, RX, 5)):
    if random.random() > 0.15:
        yt = y_at((NX, TOP), VPR, x); yb = y_at((NX, BOT), VPR, x)
        P.append(bow(x, yt, x, yt + (yb - yt) * random.uniform(0.5, 0.92), 0.75, random.uniform(0.2, 0.34)))

# 左立面阴影：短促斜排线，只压在下半段
for i in range(30):
    t = random.uniform(0.02, 0.98)
    x = LX + (NX - LX) * t
    yt = y_at((NX, TOP), VPL, x); yb = y_at((NX, BOT), VPL, x)
    y0 = yt + (yb - yt) * random.uniform(0.42, 0.86)
    P.append(f'<path d="M{x:.1f} {y0:.1f}l-5.5 9" stroke="{BLU}" stroke-opacity="0.16" stroke-width="1"/>')

# ═══ 基座（让塔楼落到地上）════════════════════════
PLB = 336.0
edge(LX - 8, y_at((NX, PLB), VPL, LX - 8), NX, PLB, 1.5)
edge(NX, PLB, RX + 8, y_at((NX, PLB), VPR, RX + 8), 1.5)
light(LX, y_at((NX, BOT), VPL, LX), LX, y_at((NX, PLB), VPL, LX), 1.2, 0.55)
light(RX, y_at((NX, BOT), VPR, RX), RX, y_at((NX, PLB), VPR, RX), 1.2, 0.55)
# 入口
light(NX - 30, y_at((NX, BOT), VPL, NX - 30), NX - 30, y_at((NX, PLB), VPL, NX - 30), 0.9, 0.4)
light(NX + 34, y_at((NX, BOT), VPR, NX + 34), NX + 34, y_at((NX, PLB), VPR, NX + 34), 0.9, 0.4)

# ═══ 远景轮廓（淡）════════════════════════════════
for (bx, bw, bh) in ((30, 34, 62), (68, 26, 40), (500, 30, 52)):
    P.append(bow(bx, 292, bx, 292 - bh, 1.1, 0.16))
    P.append(bow(bx, 292 - bh, bx + bw, 292 - bh, 1.1, 0.16))
    P.append(bow(bx + bw, 292 - bh, bx + bw, 292, 1.1, 0.16))

# ═══ 塔吊 ═════════════════════════════════════════
CX, CBASE, CTOP = 104.0, 346.0, 96.0
edge(CX, CBASE, CX, CTOP, 1.4, 4)
P.append(bow(CX - 9, CBASE, CX + 9, CBASE, 1.2, 0.7))
edge(CX - 40, CTOP + 11, CX + 86, CTOP - 3, 1.4, 4)
P.append(bow(CX, CTOP - 22, CX + 62, CTOP - 1, 1.0, 0.55))
P.append(bow(CX, CTOP - 22, CX - 34, CTOP + 8, 1.0, 0.55))
P.append(bow(CX, CTOP, CX, CTOP - 22, 1.1, 0.6))
P.append(bow(CX + 58, CTOP + 2, CX + 58, CTOP + 30, 0.9, 0.5))
P.append(bow(CX + 52, CTOP + 30, CX + 64, CTOP + 30, 1.1, 0.6))
for i in range(6):                          # 塔身格构
    yy = CTOP + 16 + (CBASE - CTOP - 16) * i / 6
    P.append(bow(CX - 5, yy, CX + 5, yy + 22, 0.7, 0.34))
    P.append(bow(CX + 5, yy, CX - 5, yy + 22, 0.7, 0.34))
P.append(bow(CX - 5, CTOP + 10, CX - 5, CBASE, 0.8, 0.4))
P.append(bow(CX + 5, CTOP + 10, CX + 5, CBASE, 0.8, 0.4))

# ═══ 地面 ═════════════════════════════════════════
P.append(bow(4, 370, 556, 362, 1.7, 0.85))
for i in range(11):
    x = 16 + i * 52 + random.uniform(-8, 8)
    P.append(bow(x, 376 + random.uniform(-3, 3), x + random.uniform(18, 34), 375 + random.uniform(-3, 3), 0.9, 0.2))

# ═══ 树 ═══════════════════════════════════════════
def tree(cx, base, h, r, o=0.55):
    P.append(bow(cx, base, cx, base - h, 1.35, 0.78))
    P.append(bow(cx, base - h * 0.58, cx - r * 0.42, base - h * 0.8, 1.0, 0.5))
    P.append(bow(cx, base - h * 0.66, cx + r * 0.44, base - h * 0.86, 1.0, 0.5))
    cy = base - h - r * 0.34
    for pass_i in range(3):                       # 三圈涂鸦，团出树冠
        pts, n = [], 15
        rr0 = r * (1.0 - pass_i * 0.2)
        for k in range(n + 1):
            a = 2 * math.pi * k / n
            rr = rr0 * random.uniform(0.74, 1.1)
            pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr * 0.7))
        d = f'M{pts[0][0]:.1f} {pts[0][1]:.1f}' + ''.join(
            f'Q{(pts[i][0]+pts[i+1][0])/2 + random.uniform(-3,3):.1f} '
            f'{(pts[i][1]+pts[i+1][1])/2 + random.uniform(-3,3):.1f} '
            f'{pts[i+1][0]:.1f} {pts[i+1][1]:.1f}' for i in range(n))
        P.append(f'<path d="{d}" fill="none" stroke="{INK}" '
                 f'stroke-opacity="{o * (0.85 - pass_i * 0.22):.2f}" stroke-width="1.05" stroke-linecap="round"/>')

tree(58, 368, 44, 26)
tree(526, 362, 30, 18, 0.44)

# ═══ 人 ═══════════════════════════════════════════
def person(x, base, s=1.0):
    P.append(f'<g stroke="{INK}" stroke-opacity="0.66" stroke-width="1.2" stroke-linecap="round" fill="none" '
             f'transform="translate({x} {base}) scale({s})">'
             f'<circle cx="0" cy="-19" r="3.1"/>'
             f'<path d="M0 -16v10M0 -6l-4.5 6M0 -6l4.5 6M0 -13l-5 4M0 -13l5 4"/></g>')
person(268, 366)
person(288, 364, 0.9)

body = '\n      '.join(P)

svg = f'''<svg viewBox="0 0 {W} {H}" style="display: block; width: 100%; height: auto;" role="img" aria-label="建筑草图">
  <defs>
    <pattern id="skg" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M28 0H0V28" fill="none" stroke="rgba(40,80,150,0.085)" stroke-width="1"/>
    </pattern>
  </defs>
  <rect width="{W}" height="{H}" fill="#FBF9F4"/>
  <rect width="{W}" height="{H}" fill="url(#skg)"/>
  <g fill="rgba(60,110,200,0.12)">
    <path d="M150 372q64-20 186-20t188 16q-84 16-192 16t-182-12z"/>
    <path d="M34 374q22-8 52-7t46 7q-24 7-52 6t-46-6z"/>
    <path d="M498 368q16-6 38-5t32 5q-18 5-38 4t-32-4z"/>
  </g>
  <g fill="none">
      {body}
  </g>
  <g font-family="monospace" font-size="9" letter-spacing="1.8" fill="rgba(40,80,150,0.5)">
    <text x="26" y="34">SKETCH · 001</text>
    <text x="534" y="34" text-anchor="end">2B · A3</text>
  </g>
</svg>'''

open('art.svg', 'w').write(svg)
open('preview.html', 'w').write(
    '<!doctype html><meta charset="utf-8"><body style="margin:0;background:#0B1017;display:flex;'
    'align-items:center;justify-content:center;min-height:100vh">'
    '<div style="width:600px;border:1px solid rgba(146,168,200,.28);border-radius:3px;overflow:hidden">'
    + svg + '</div></body>')
print('v2:', len(svg), '字符 /', len(P), '条笔画')

# ── 说明 ───────────────────────────────────────────────
# 首屏那张建筑草图的生成脚本。透视按两个灭点实算（VPL / VPR），
# 手绘感来自 bow()：每条线是微弯的二次贝塞尔 + 端点抖动 + 主轮廓画两遍。
# 立面刻意不画满 —— 楼层线随机漏画、只画一部分、越往下越淡。
#
#     python3 design/tools/sketch.py     # 产出 art.svg 与 preview.html
#
# 改完把 art.svg 里的 <svg> 整块换进 design/Main.dc.html，再同步 Mobile。
# 换 random.seed() 可以摇出另一张笔触不同的稿。
