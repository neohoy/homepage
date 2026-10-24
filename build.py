#!/usr/bin/env python3
"""将 design/Main.dc.html 构建为零依赖的静态主页。

正文与样式在 Main.dc.html 维护；不要直接修改 dist/index.html。
运行：python3 build.py
"""
from collections import Counter
from html.parser import HTMLParser
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / 'design'
DIST = ROOT / 'dist'
ACCENT = '#2855D9'
# Cloudflare Pages 的正式域名；GitHub Pages 保留为备用入口。
SITE = 'https://neo.bitbuild.cc/'
TITLE = '牛叔 neohoy — 建筑科技、AI 与造物'
DESCRIPTION = '牛叔 / neohoy，建筑科技、AI 创作与造物实践。行业观察、持续更新的手册书柜、游戏制作资料、木质玩具，以及正在制作的网站与小程序。'

src = (SRC / 'Main.dc.html').read_text(encoding='utf-8')
css = src[src.index('<style>') + 7:src.index('</style>')]
css = css.replace('    sc-if { display: contents; }\n', '')
css = css.rstrip()
body = src[src.index('<div class="page {{themeClass}}"'):src.index('</x-dc>')]
body = body.replace('{{themeClass}}', 'paper').replace('{{accent}}', ACCENT)
filters = re.findall(r'class="chip \{\{sel\.(\w+)\}\}"', body)
for key in filters:
    body = body.replace(f'class="chip {{{{sel.{key}}}}}" onClick="{{{{pick.{key}}}}}"',
                        f'class="chip" data-filter="{key}"')
for key in (k for k in filters if k != 'all'):
    body = body.replace(f'<sc-if value="{{{{show.{key}}}}}" hint-placeholder-val="{{{{ true }}}}">',
                        f'<div class="project-group" data-work="{key}">')
body = body.replace('</sc-if>', '</div>')
if '{{' in body or '<sc-if' in body:
    raise SystemExit('存在未解析的设计模板属性。')

# 数字只来自页面实际列出的书目，不在首屏与书柜分别手填。
book_ids = re.findall(r'data-book-id="([\w-]+)"', body)
if not book_ids or len(book_ids) != len(set(book_ids)):
    raise SystemExit('书目为空或有重复 data-book-id。')
body = re.sub(r'(<span data-book-count>)\d+(</span>)',
              lambda m: m[1] + str(len(book_ids)) + m[2], body)

class PageCheck(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.anchors = []
        self.images = []
        self.stack = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'a':
            href = a.get('href', '')
            if not href or href == '#' or href.startswith('javascript:'):
                raise ValueError(f'存在无效入口：{href!r}')
            if href.startswith('#'):
                self.anchors.append(href[1:])
            if a.get('target') == '_blank' and 'noopener' not in a.get('rel', '').split():
                raise ValueError(f'外链缺少 noopener：{href}')
        if tag == 'img':
            if not a.get('alt') or not a.get('width') or not a.get('height'):
                raise ValueError('图片缺少替代文字或明确尺寸。')
            self.images.append(a.get('src', ''))
        if tag not in {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}:
            self.stack.append(tag)
    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1] != tag:
            raise ValueError(f'HTML 标签未配对：{tag}，当前 {self.stack[-3:]}')
        self.stack.pop()

check = PageCheck()
check.feed(body)
if check.stack:
    raise SystemExit('HTML 有未闭合标签：' + str(check.stack))
duplicate_ids = [key for key, n in Counter(check.ids).items() if n > 1]
missing_anchors = set(check.anchors) - set(check.ids)
if duplicate_ids or missing_anchors:
    raise SystemExit(f'重复 id：{duplicate_ids}；不存在的锚点：{sorted(missing_anchors)}')
missing_images = [path for path in check.images if not (SRC / path).is_file()]
if missing_images:
    raise SystemExit('缺少图片：' + ', '.join(missing_images))

JS = r'''
(function () {
  var activeFilter = 'all';
  var buttons = Array.from(document.querySelectorAll('[data-filter]'));
  var groups = Array.from(document.querySelectorAll('[data-work]'));
  var status = document.getElementById('filter-status');
  var menu = document.querySelector('.mobile-nav');
  var media = window.matchMedia('(prefers-reduced-motion: reduce)');

  function paintProjects() {
    buttons.forEach(function (button) {
      var selected = button.dataset.filter === activeFilter;
      button.classList.toggle('on', selected);
      button.setAttribute('aria-pressed', String(selected));
    });
    var visibleCount = 0;
    groups.forEach(function (group) {
      var visible = activeFilter === 'all' || group.dataset.work === activeFilter;
      group.hidden = !visible;
      if (visible) visibleCount += group.querySelectorAll('.brand-block').length;
    });
    if (status) status.textContent = activeFilter === 'all'
      ? '按品牌整理 · ' + visibleCount + ' 个项目方向'
      : '当前显示 ' + visibleCount + ' 个项目方向';
  }

  document.addEventListener('click', function (event) {
    var copy = event.target.closest('[data-copy-group]');
    if (copy) {
      var message = copy.parentElement.querySelector('.copy-status');
      if (!navigator.clipboard || !navigator.clipboard.writeText) {
        message.textContent = '请手动复制左侧群号';
        return;
      }
      navigator.clipboard.writeText(copy.dataset.copyGroup).then(function () {
        message.textContent = '群号已复制';
      }).catch(function () {
        message.textContent = '请手动复制左侧群号';
      });
      return;
    }
    var filter = event.target.closest('[data-filter]');
    if (filter) {
      activeFilter = filter.dataset.filter;
      paintProjects();
      return;
    }
    var anchor = event.target.closest('a[href^="#"]');
    if (!anchor) return;
    var id = anchor.getAttribute('href').slice(1);
    var target = document.getElementById(id);
    if (!target) return;
    // 从首屏或书柜进入某个品牌时，先恢复被筛选隐藏的项目。
    if (target.closest('[data-work][hidden]')) {
      activeFilter = 'all';
      paintProjects();
    }
    if (menu) menu.open = false;
    event.preventDefault();
    if (location.hash !== '#' + id) history.pushState(null, '', '#' + id);
    target.scrollIntoView({ behavior: media.matches ? 'instant' : 'smooth', block: 'start' });
    if (!target.hasAttribute('tabindex') && !target.matches('a, button, input, summary')) target.setAttribute('tabindex', '-1');
    target.focus({ preventScroll: true });
  });
  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape' && menu && menu.open) {
      menu.open = false;
      menu.querySelector('summary').focus();
    }
  });
  document.addEventListener('click', function (event) {
    if (menu && menu.open && !menu.contains(event.target)) menu.open = false;
  });
  window.addEventListener('popstate', function () {
    var target = document.getElementById(location.hash.slice(1));
    if (target && target.closest('[data-work][hidden]')) {
      activeFilter = 'all';
      paintProjects();
    }
  });
  paintProjects();
})();
'''

favicon = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
           "%3Crect width='32' height='32' rx='4' fill='%230C1118'/%3E"
           "%3Cpath d='M9 23V9l14 14V9' fill='none' stroke='%2391B5FF' stroke-width='2'/%3E%3C/svg%3E")
html = f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<title>{TITLE}</title>
<meta name="description" content="{DESCRIPTION}">
<meta name="author" content="牛叔 neohoy">
<link rel="canonical" href="{SITE}">
<meta property="og:type" content="website">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESCRIPTION}">
<meta property="og:image" content="{SITE}banner.jpg">
<meta property="og:image:alt" content="观察变化，参与其中。牛叔的建筑科技、AI 与造物工作台。">
<meta property="og:url" content="{SITE}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@neohoy77">
<meta name="twitter:title" content="{TITLE}">
<meta name="twitter:description" content="{DESCRIPTION}">
<meta name="twitter:image" content="{SITE}banner.jpg">
<link rel="icon" href="{favicon}">
<style>
html {{ scroll-behavior: smooth; }}
{css}
.project-group {{ display: contents; }}
.project-group[hidden] {{ display: none; }}
</style>
</head>
<body>
{body}
<script>{JS}</script>
</body>
</html>
'''
DIST.mkdir(exist_ok=True)
image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.avif', '.svg'}
assets = sorted(p for p in SRC.iterdir() if p.suffix.lower() in image_extensions)
for asset in assets:
    shutil.copyfile(asset, DIST / asset.name)
(DIST / 'index.html').write_text(html, encoding='utf-8')
print(f'dist/index.html 已生成 · {len(html):,} 字符 · {len(book_ids)} 本手册 · {len(assets)} 张图片')
