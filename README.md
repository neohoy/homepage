# 牛叔 · 个人主页

零依赖静态个人主页。当前版本采用暖白纸感、叠放作品册、独立品牌铭牌与书柜展台，以牛叔 / neohoy 的个人身份承接建筑科技、AI 与造物实践。

## 维护与构建

- `design/Main.dc.html`：当前正文、样式和设计画布逻辑。
- `build.py`：解析设计模板，补上筛选交互、站点元数据，生成静态站。
- `dist/`：部署目录。不要直接编辑，构建会覆盖。
- `design/Mobile.dc.html`、`design/System.dc.html`：旧版视觉参考，不参与当前构建；当前移动端由 Main 的响应式样式实现。
- `niushu-ip-homepage.html`：旧设计工具导出文件，不参与构建。

修改 Main 后运行：

```bash
python3 build.py
python3 -m http.server 8947 --bind 127.0.0.1 --directory dist
```

本地预览：<http://127.0.0.1:8947/>。

构建会检查标签配对、重复 id、站内锚点、图片、空链接和外链属性。页面不依赖远程字体或前端框架，直接打开 `dist/index.html` 也可查看。

## 品牌与内容关系

| 英文标识 | 中文品牌 | 内容 |
| --- | --- | --- |
| Bit Build | 建造观察局 | 建筑科技与 AI 的行业观察、公众号、行业网站 |
| NEO Creative | 造物集 | AI 内容、创作实践、手册书柜、创作 Skill、数字项目 |
| Game Makers | 游戏学社 | RPG Maker 中文资料与游戏制作社群 |
| Mu Shop | 明木趣玩 | 木质轨道、玩具选品与销售 |
| Strait Connect | 海峡助手 | 两岸信息、公众号、小程序 |

- Leaf Notes 一叶茶记与安心爸妈家先归到 NEO Creative，标明制作中。
- 创作 Skill 归到 NEO Creative。NEO 手绘动画（MV Skill）已公开，入口为 `https://github.com/neohoy/neo-handdrawn-motion`；写书（书柜配套）、视频制作、宣传片、创意图片、IP 设计技能目前内部使用，计划陆续公开。尚无技能集合网站，不展示为已上线站点。
- 明木造物作为文创与定制木玩方向展示，标明筹备中。英文名称暂未确定，不自行填入 Mu Studio。
- 协会使用中文正式名称，列为海峡助手的关联机构，不自行确认英文名称或 CCSA 缩写。
- 抖音、小红书、B 站、X 是个人综合内容渠道。
- 不把网站展示名称变更视作外部账号、商店或域名已经改名。

## 关注与社群数字

按用户 2026-10-24 提供的信息显示：建造观察局公众号 5000+，NEO造物集公众号 1000+，游戏群 2000+，B 站 1500+。数字分别放在对应品牌、社群和渠道，不汇总成站点访问人数。

行业网站、Yanfly 中文文档、商店独立站采用整张可点击的资源入口卡片，保留原有真实地址。

## 游戏学社

展示 Yanfly 官方授权的插件文档中文翻译与整理，不再展示 MV 帮助入口。社群保留实际群名 Game Maker Monster School，QQ群号 744013203，提供复制按钮；人数按 2026-10-24 用户提供的信息显示为 2000+ 人。更完整的 RPG Maker 插件站标为制作中。

## 书柜

书柜是 NEO Creative 的核心作品，在创作 Skill 之前以独立卡片展示，并链接到下方完整书柜展区。

本次核对书柜数据源：`/Users/mac/06项目/NEO造物/产品/手册/在线站点/bookshelf/src/books.js`。

当前六本：大模型、Claude Code、Codex、豆包、WorkBuddy、OpenDesign。主入口指向现有立体书柜，首页每张手册卡片分别提供阅读正文与导航站两个入口。五本整书直达书柜的 `/books/<id>.html`，大模型手册从入门篇第一篇正文开始，导航站仍使用各站首页。

在 Main 的 `.book-grid` 中增减带 `data-book-id` 的条目；构建时根据这些条目统一生成各处册数。书柜本身仍由原工程维护，首页截图也需要在书柜明显变化时更新。

## 图片

`design/` 顶层图片会同步到 `dist/`。当前使用 `avatar.jpg`、`banner.jpg`、`bookshelf.png`，以及 `wechat-bitbuild.jpg`、`wechat-neo.jpg`、`wechat-strait.jpg` 三张公众号二维码原图。旧 `wechat-qr.jpg` 保留为历史资产，不再由当前页面引用。原始大图放在 `design/_source/`，子目录不参与构建。

`bookshelf.png` 来源于本次已访问的真实书柜截图。三张公众号二维码使用用户提供的原始 JPEG，完整复制，不裁切或重绘；展开公众号入口后可查看，点击图片可打开原图。海峡助手下标明扫码关注的是协会公众号。

## 待补入口

抖音、小红书、B 站、抖店、虾皮、海峡助手小程序尚未拿到明确的公开链接，页面只展示名称或项目说明，不设置空按钮。X 与邮箱沿用旧主页已有地址；发布前宜由本人确认。

## 验证

内容调整记录在 `research/2026-10-23-个人定位与作品盘点/主页调整/`；当前白色视觉版本的检查脚本、截图与调整前备份在 `research/2026-10-24-白色纸感/`。

检查四种宽度：390 / 768 / 1024 / 1400。横向溢出与段落挤扁分别检查，并验证项目筛选、品牌锚点、公众号展开、手机菜单和书柜册数。

## 部署

现有两条流水线保留，推送 `main` 会触发 GitHub Pages 部署。发布前运行 `python3 build.py` 并同步提交源文件、图片和 `dist/`，部署成功后回查线上页面。Cloudflare 流水线仅在仓库变量 `CLOUDFLARE_ENABLED=true` 且已配置所需凭据时运行。

| 平台 | 地址 | 配置 |
| --- | --- | --- |
| Cloudflare Pages（预留配置） | bitbuild.cc | 输出目录 `dist`，需启用仓库变量与凭据，不能据配置认定域名已上线 |
| GitHub Pages | neohoy.github.io/homepage | `.github/workflows/deploy.yml` |

canonical 和分享卡片地址由 `build.py` 的 `SITE` 配置，当前保留原有 GitHub Pages 地址。正式域名切换需要另行核实后修改。
