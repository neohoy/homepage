# 牛叔 · 个人主页

[bitbuild.cc](https://bitbuild.cc) 的源码。零依赖静态站，一个 `index.html` 加两张图，整站 272KB。

## 目录

```
design/     设计稿（Claude Design 画布的 .dc.html 源文件）
dist/       构建产物，部署的就是这个目录
build.py    design/Main.dc.html → dist/index.html
```

## 改内容

正文、作品卡、联系方式这些都在 `design/Main.dc.html` 里。改完跑：

```bash
python3 build.py
```

会重新生成 `dist/index.html` 并同步图片。**不要直接改 `dist/index.html`**，下次构建会覆盖。

`design/Mobile.dc.html` 和 `design/System.dc.html` 只是设计参考（手机版视觉稿、设计系统），不参与构建——线上站是响应式的，一套代码适配。

## 部署

两条流水线并存，推 `main` 都会自动触发：

| 平台 | 地址 | 配置 |
| --- | --- | --- |
| Cloudflare Pages | bitbuild.cc | 构建命令留空，输出目录 `dist` |
| GitHub Pages | neohoy.github.io/homepage | `.github/workflows/deploy.yml` |

自定义域名只能指向一个，打算给 Cloudflare。GitHub Pages 那个当备用镜像。

站点对外地址（canonical、og 卡片用）在 `build.py` 顶部的 `SITE` 常量里。
bitbuild.cc 接上 Cloudflare 之后把它改成 `https://bitbuild.cc/`，重新构建即可。
现在指向 GitHub Pages —— bitbuild.cc 还没解析到站上，canonical 不能指死链。

## 待补

- 联系区的微信二维码（现在是制图占位框）
- NEO 造物集的成品实拍图
- 核心指标里公众号读者数与 GitHub Stars 需要定期更新

## 图片

`design/` 顶层的图片会被 `build.py` 全量同步到 `dist/`，加新图直接放进去即可，
不用改脚本；页面引用了但 `design/` 里没有的图会让构建直接失败，避免线上碎图。

原始大图放 `design/_source/`（子目录不参与打包），例如横幅的 webp 原件。
