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

自定义域名只能指向一个，给了 Cloudflare。GitHub Pages 那个当备用镜像。

## 待补

- 联系区的微信二维码（现在是制图占位框）
- NEO 造物集的成品实拍图
- 核心指标里公众号读者数与 GitHub Stars 需要定期更新
