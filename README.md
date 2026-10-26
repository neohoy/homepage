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
| Strait Connect | 海峡助手 | 台胞政策网站、两岸信息、公众号、小程序 |

- Leaf Notes 一叶茶记与安心爸妈家先归到 NEO Creative，标明制作中。
- 创作 Skill 归到 NEO Creative。NEO 手绘动画（MV Skill）已公开，入口为 `https://github.com/neohoy/neo-handdrawn-motion`；写书（书柜配套）、视频制作、宣传片、创意图片、IP 设计技能目前内部使用，计划陆续公开。尚无技能集合网站，不展示为已上线站点。
- 明木造物作为文创与定制木玩方向展示，标明筹备中。英文名称暂未确定，不自行填入 Mu Studio。
- 协会使用中文正式名称，列为海峡助手的关联机构，不自行确认英文名称或 CCSA 缩写。
- 海峡助手网站入口为 <https://strait.bitbuild.cc/>，目前展示台胞政策与办事资讯；旅游资讯、交流活动等仍在筹备，不作为已上线功能宣传。
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

`design/` 顶层图片会同步到 `dist/`。当前使用 `avatar.jpg`、`banner.jpg`、`bookshelf.png`，以及 `wechat-bitbuild.jpg`、`wechat-neo.jpg`、`wechat-strait.jpg` 三张公众号二维码原图。个人微信使用 `wechat-personal-qr.png`，放在页面最后的联系区，可点击放大。旧 `wechat-qr.jpg` 为建造观察局公众号历史资产，不作为个人微信使用。原始大图放在 `design/_source/`，子目录不参与构建。

个人微信图按用户要求从原图裁出二维码和四周白边：裁剪区域 x=96、y=264、宽高 696 像素，不含上方头像、名字、地区或下方说明。输出 PNG 未缩放或重绘，已核对裁剪范围内的像素与原图一致；原图保存在 `design/_source/wechat-personal-original.jpg`。

`bookshelf.png` 来源于本次已访问的真实书柜截图。三张公众号二维码使用用户提供的原始 JPEG，完整复制，不裁切或重绘；展开公众号入口后可查看，点击图片可打开原图。海峡助手下标明扫码关注的是协会公众号。

产品小插画使用 8 张 `product-*-v1.webp`：行业网站、书柜、创作 Skill、一叶茶记、安心爸妈家、游戏资料、木质玩具、海峡服务。由内置图片生成工具独立生成，各图 640 × 427，保留透明背景并延迟加载，总计约 659 KiB。原始 PNG 保存在本地 `design/_source/product-illustrations-v1/`，提示词、文件清单与视觉检查在本地 `research/2026-10-24-产品小插画/`。这些是项目主题插画，不是产品实拍或网站截图。

当前作品册卡片直接沿用首屏的结构：外层错位底板与橙色索引签，内层暖白渐变纸张、双纸边与分层投影，保留全页 3.5% 轻噪点。卡片保持紧凑，行业网站用稍大的标题与蓝色圆章突出；书柜仍在 NEO Creative 的 Skill 前。`paper-cotton-v1.webp` 为本地历史材质试样，当前页面不再引用、不随本次发布。方案与截图见本地 `research/2026-10-24-产品小插画/作品册卡片设计.md`。

## 待补入口

抖音、小红书、B 站、抖店、虾皮、海峡助手小程序尚未拿到明确的公开链接，页面只展示名称或项目说明，不设置空按钮。X 与邮箱沿用旧主页已有地址；发布前宜由本人确认。

## 验证

内容调整记录在 `research/2026-10-23-个人定位与作品盘点/主页调整/`；当前白色视觉版本的检查脚本、截图与调整前备份在 `research/2026-10-24-白色纸感/`。

检查四种宽度：390 / 768 / 1024 / 1400。横向溢出与段落挤扁分别检查，并验证项目筛选、品牌锚点、公众号展开、手机菜单和书柜册数。

## 部署

正式站已于 2026-10-24 通过 Wrangler 发布到 Cloudflare Pages，项目为 `homepage`，生产分支为 `main`。`neo.bitbuild.cc` 在 Spaceship DNS 中通过 CNAME 指向 `homepage-7cr.pages.dev`，不需要迁移整个域名的名称服务器。

| 平台 | 地址 | 配置 |
| --- | --- | --- |
| Cloudflare Pages 正式域名 | <https://neo.bitbuild.cc/> | 项目 `homepage`，生产分支 `main` |
| Cloudflare Pages 默认域名 | <https://homepage-7cr.pages.dev/> | 与正式域名提供同一生产版本 |
| GitHub Pages 备用入口 | <https://neohoy.github.io/homepage/> | `.github/workflows/deploy.yml`，推送 `main` 后自动发布 |

修改后先运行 `python3 build.py`，将源文件、图片和 `dist/` 一起提交，再发布 Cloudflare：

```bash
python3 scripts/deploy-cloudflare.py --check
python3 scripts/deploy-cloudflare.py
```

脚本使用本机 Wrangler 的既有登录。需要重新登录时运行 `npx --yes wrangler@4 login`，不将登录凭据提交到仓库。脚本会重新构建，核对构建文件与当前提交一致，只将已提交的 `dist/` 文件放入临时上传目录；本地研究资料、二维码原图和未入库的纹理试样不会上传。

Cloudflare 的 GitHub Actions 流水线仍未启用，因此推送 GitHub 不会自动更新 Cloudflare。未来配置 `CLOUDFLARE_API_TOKEN`、`CLOUDFLARE_ACCOUNT_ID` 和仓库变量 `CLOUDFLARE_ENABLED=true` 后才会自动发布。

canonical 和分享卡片地址由 `build.py` 的 `SITE` 配置，当前为 `https://neo.bitbuild.cc/`。发布后回查正式域名的 HTTPS、页面与图片，并核对线上 HTML 与本地 `dist/index.html` 的 SHA-256；本次验收记录在本地 `research/2026-10-24-Cloudflare发布/`。
