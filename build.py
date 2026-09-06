#!/usr/bin/env python3
"""从设计稿 Main.dc.html 生成可部署的静态首页 index.html。

设计稿在 Claude Design 画布里改（design/*.dc.html），改完跑一次这个脚本
重新生成 dist/。不要手改 dist/index.html —— 下次构建会覆盖掉。

    python3 build.py
"""
import re
import shutil
import pathlib

ROOT = pathlib.Path(__file__).parent
ACCENT = '#3B7BE8'

# 站点对外地址，用于 canonical 与 og/twitter 卡片。
# bitbuild.cc 接上 Cloudflare Pages 之后，把这里改成 'https://bitbuild.cc/' 即可，
# 全站的绝对地址都跟着走。结尾要带斜杠。
SITE = 'https://neohoy.github.io/homepage/'

SRC  = ROOT / 'design'
DIST = ROOT / 'dist'
DIST.mkdir(exist_ok=True)

src = (SRC / 'Main.dc.html').read_text(encoding='utf-8')
css = src[src.index('<style>') + 7: src.index('</style>')]
body = src[src.index('<div class="page {{themeClass}}"'): src.index('</x-dc>')]

# ── 模板洞 → 静态属性 ──────────────────────────────────────────
body = body.replace('{{themeClass}}', 'ink').replace('{{accent}}', ACCENT)
# 滚动锚点：从设计稿逻辑里解析 key → 元素 id，脚本不写死
logic_src = src[src.index('<script data-dc-script'):]
GO = dict(re.findall(r"(\w+):\s*\(\)\s*=>\s*this\.scrollTo\('([\w-]+)'\)", logic_src))
for k, anchor in GO.items():
    body = body.replace('onClick="{{go.%s}}"' % k, 'data-go="%s"' % anchor)
if '{{go.' in body:
    raise SystemExit('还有没解析的滚动锚点: ' + body[body.index('{{go.'):body.index('{{go.') + 60])
# 分类不写死，直接从设计稿里读出来 —— 以后加分类不用改这里
FILTERS = re.findall(r'class="chip \{\{sel\.(\w+)\}\}"', body)
for k in FILTERS:
    body = body.replace('class="chip {{sel.%s}}" onClick="{{pick.%s}}"' % (k, k),
                        'class="chip" data-filter="%s"' % k)
# 频道不写死，从设计稿里读出来
CHANNELS = re.findall(r'class="tab \{\{ch\.(\w+)\}\}"', body)
for k in CHANNELS:
    body = body.replace('class="tab {{ch.%s}}" onClick="{{tab.%s}}"' % (k, k),
                        'class="tab" data-tab="%s"' % k)
for k in [f for f in FILTERS if f != 'all']:
    body = body.replace('<sc-if value="{{show.%s}}" hint-placeholder-val="{{ true }}">' % k,
                        '<div class="grp" data-work="%s">' % k)
for k in CHANNELS:
    for hint in ('true', 'false'):
        body = body.replace('<sc-if value="{{on.%s}}" hint-placeholder-val="{{ %s }}">' % (k, hint),
                            '<div class="grp" data-panel="%s">' % k)
body = body.replace('</sc-if>', '</div>')
if '{{' in body:
    raise SystemExit('未解析的模板洞: ' + body[body.index('{{'):body.index('{{') + 120])

# ── 挂响应式钩子 ──────────────────────────────────────────────
body = body.replace('<div style="max-width: 1200px; margin: 0 auto;',
                    '<div class="wrap" style="max-width: 1200px; margin: 0 auto;')
GRIDS = [
    ('grid-template-columns: minmax(0, 1fr) minmax(0, 1.06fr); gap: 88px', 'rc'),
    ('grid-template-columns: minmax(0, 0.94fr) minmax(0, 1.06fr);', 'rc'),
    ('grid-template-columns: minmax(0, 1.06fr) minmax(0, 0.94fr);', 'rc'),
    ('grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 56px', 'rc'),
    ('grid-template-columns: minmax(0, 1.12fr) minmax(0, 1fr); gap: 84px', 'rc'),
    ('grid-template-columns: minmax(0, 1fr) 208px; gap: 22px', 'rc'),
    ('grid-template-columns: repeat(4, minmax(0, 1fr));', 'rm'),
    ('grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px', 'rt'),
    ('grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px', 'rt'),
]
for sig, cls in GRIDS:
    body = body.replace('<div style="display: grid; ' + sig,
                        '<div class="%s" style="display: grid; ' % cls + sig)
    body = body.replace('<div class="card" style="display: grid; ' + sig,
                        '<div class="card %s" style="display: grid; ' % cls + sig)

HOOKS = [
    ('<div style="padding-left: 206px; margin-top: 26px;">',
     '<div class="heroName" style="padding-left: 206px; margin-top: 26px;">'),
    ('<div style="position: absolute; left: 28px; bottom: -58px; width: 148px; height: 148px;',
     '<div class="heroAvatar" style="position: absolute; left: 28px; bottom: -58px; width: 148px; height: 148px;'),
    ('<div style="display: flex; align-items: center; gap: 34px;">',
     '<div class="navLinks" style="display: flex; align-items: center; gap: 34px;">'),
    ('<div style="display: flex; border-bottom: 1px solid var(--line);">',
     '<div class="tabRow" style="display: flex; border-bottom: 1px solid var(--line);">'),
    ('<div style="display: flex; gap: 9px; flex-shrink: 0; padding-bottom: 6px;">',
     '<div class="chipRow" style="display: flex; gap: 9px; flex-shrink: 0; padding-bottom: 6px;">'),
    ('<div style="display: flex; align-items: center; gap: 14px; margin-bottom: 30px;">',
     '<div class="kicker" style="display: flex; align-items: center; gap: 14px; margin-bottom: 30px;">'),
    ('<p class="serif" style="margin: 0 auto; max-width: 28em;',
     '<p class="serif epigraph" style="margin: 0 auto; max-width: 28em;'),
]
for a, b in HOOKS:
    body = body.replace(a, b)
body = re.sub(r'<div style="display: flex; align-items: flex-end; justify-content: space-between; gap: 60px;',
              '<div class="secHead" style="display: flex; align-items: flex-end; justify-content: space-between; gap: 60px;',
              body)
css = css.replace('    sc-if { display: contents; }\n', '')

EXTRA = '''
    /* ── 筛选 / 页签分组容器 ── */
    .grp { display: contents; }
    .grp[hidden] { display: none; }

    /* ── 响应式 ── */
    @media (max-width: 1000px) {
      .wrap { padding-left: 28px !important; padding-right: 28px !important; }
      .rc { grid-template-columns: 1fr !important; gap: 0 !important; }
      .rc > * { min-width: 0; }
      .card.rc > div:first-child { border-right: none !important; border-left: none !important; border-bottom: 1px solid var(--line) !important; }
      .rm { grid-template-columns: repeat(2, minmax(0, 1fr)) !important; }
      .rm > div { padding: 26px 22px !important; border-right: 1px solid var(--line) !important; border-bottom: 1px solid var(--line) !important; }
      .rm > div:nth-child(2n) { border-right: none !important; }
      .rm > div:nth-child(n+3) { border-bottom: none !important; }
      .secHead { flex-wrap: wrap !important; gap: 26px !important; }
      .chipRow { flex-wrap: wrap; flex-shrink: 1 !important; width: 100%; padding-bottom: 0 !important; }
      .epigraph { white-space: normal !important; text-wrap: pretty !important; max-width: 100% !important; font-size: 24px !important; }
      .heroClose > p.serif { font-size: 44px !important; }
      .navLinks { gap: 20px !important; }
      .navLinks .navlink { font-size: 12.5px !important; }
      .tabRow { flex-wrap: wrap; }
      .tabRow > .tab { flex: 1 1 50%; border-right: 1px solid var(--line) !important; border-bottom: 1px solid var(--line); }
    }
    @media (max-width: 720px) {
      .wrap { padding-left: 20px !important; padding-right: 20px !important; }
      .navLinks { display: none !important; }
      .heroAvatar { left: 16px !important; bottom: -34px !important; width: 92px !important; height: 92px !important; border-width: 3px !important; }
      .heroName { padding-left: 122px !important; margin-top: 16px !important; }
      .heroName h1 { font-size: 44px !important; }
      .heroName span.serif { font-size: 30px !important; }
      .rt { grid-template-columns: repeat(2, minmax(0, 1fr)) !important; }
      h1 { letter-spacing: 0 !important; }
      h2 { font-size: 32px !important; }
      h3 { font-size: 22px !important; }
      .card > div { padding: 26px 22px !important; }
      .card.rc > div:first-child { padding: 22px 22px 0 !important; }
      .chip { min-height: 44px; display: inline-flex; align-items: center; }
      .epigraph { font-size: 20px !important; line-height: 1.8 !important; }
      .heroClose > p.serif { font-size: 32px !important; white-space: normal !important; line-height: 1.36 !important; }
      .kicker { gap: 9px !important; margin-bottom: 22px !important; }
      .kicker .mono { font-size: 8.5px !important; letter-spacing: .12em !important; white-space: nowrap; }
      .btn { height: 48px; }
    }
    @media (max-width: 560px) {
      .heroName { padding-left: 0 !important; margin-top: 46px !important; }
      .heroName h1 { font-size: 40px !important; }
      .heroClose > p.serif { font-size: 27px !important; }
      .rt { grid-template-columns: 1fr !important; }
    }
'''

JS = '''
  (function () {
    var state = { filter: 'all', panel: '__FIRST_CHANNEL__' };

    function paintWorks() {
      document.querySelectorAll('[data-filter]').forEach(function (c) {
        c.classList.toggle('on', c.dataset.filter === state.filter);
      });
      document.querySelectorAll('[data-work]').forEach(function (g) {
        g.hidden = !(state.filter === 'all' || state.filter === g.dataset.work);
      });
    }
    function paintPanels() {
      document.querySelectorAll('[data-tab]').forEach(function (t) {
        t.classList.toggle('on', t.dataset.tab === state.panel);
      });
      document.querySelectorAll('[data-panel]').forEach(function (p) {
        p.hidden = p.dataset.panel !== state.panel;
      });
    }

    document.addEventListener('click', function (e) {
      var go = e.target.closest('[data-go]');
      if (go) {
        var el = document.getElementById(go.dataset.go);
        if (el) { e.preventDefault(); el.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
        return;
      }
      var f = e.target.closest('[data-filter]');
      if (f) { state.filter = f.dataset.filter; paintWorks(); return; }
      var t = e.target.closest('[data-tab]');
      if (t) { state.panel = t.dataset.tab; paintPanels(); }
    });

    paintWorks();
    paintPanels();
  })();
'''

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' "
           "stroke='%233B7BE8' stroke-width='1.6' stroke-linecap='square'%3E%3Cpath d='M3 21h18'/%3E"
           "%3Cpath d='M6 21V9l6-4.5L18 9v12'/%3E%3Cpath d='M10 21v-6h4v6'/%3E%3Cpath d='M12 4.5V2'/%3E%3C/svg%3E")

JS = JS.replace('__FIRST_CHANNEL__', CHANNELS[0] if CHANNELS else '')

html = f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>牛叔 neohoy — AI × 建筑科技 × 造物</title>
<meta name="description" content="牛叔 / neohoy。AI × 建筑科技 × 造物，独立开发者、作者。BitBuild 建造观察局看行业，NEO 造物集做东西。Claude Code 中文教程与豆包工作手册作者。">
<meta name="author" content="牛叔 neohoy">
<link rel="canonical" href="{SITE}">
<meta property="og:type" content="website">
<meta property="og:title" content="牛叔 neohoy — AI × 建筑科技 × 造物">
<meta property="og:description" content="观察世界，也创造世界。BitBuild 建造观察局看行业，NEO 造物集做东西。">
<meta property="og:image" content="{SITE}banner.jpg">
<meta property="og:url" content="{SITE}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@neohoy77">
<meta name="twitter:image" content="{SITE}banner.jpg">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&family=Noto+Serif+SC:wght@600;900&family=JetBrains+Mono:wght@400;600&display=swap">
<style>
*, *::before, *::after {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
img {{ max-width: 100%; }}
{css}{EXTRA}
</style>
</head>
<body>
{body}
<script>{JS}</script>
</body>
</html>
'''

# design/ 下的图片全部同步到 dist/，加新图不用改脚本
IMG_EXT = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.avif', '.svg'}
assets = sorted(p for p in SRC.iterdir() if p.suffix.lower() in IMG_EXT)
for a in assets:
    shutil.copyfile(a, DIST / a.name)

# 页面里引用到的图必须真的存在，否则线上就是碎图
referenced = set(re.findall(r'src="([^"/:]+\.(?:jpg|jpeg|png|gif|webp|avif|svg))"', body))
missing = sorted(referenced - {a.name for a in assets})
if missing:
    raise SystemExit('design/ 缺少页面引用的图片: ' + ', '.join(missing))

out = DIST / 'index.html'
out.write_text(html, encoding='utf-8')
opens, closes = html.count('<div'), html.count('</div>')
if opens != closes:
    raise SystemExit(f'div 不平衡: {opens} 开 / {closes} 闭')
print(f'dist/index.html 已生成 · {len(html):,} 字符 · div {opens} 对 · 图片 {len(assets)} 张')
