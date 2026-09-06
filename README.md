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

## 改完怎么验移动端

只查横向溢出**不够**。`.workrow` 那次翻车就是：横向 flex 在窄屏把中间那栏
挤到二十来像素，文字一行一个字，但每个元素的 `right` 都在视口内，
`scrollWidth == clientWidth`，按溢出查是"全绿"的。

两种失效要分开查：

- **溢出** —— `document.documentElement.scrollWidth > clientWidth`。
  注意 `white-space: nowrap` 的文字溢出不撑大盒子，用 `getBoundingClientRect`
  查不出来，只有 `scrollWidth` 会暴露。
- **挤扁** —— 量正文容器的实际宽度和行数。在 390px 下，`.workrow p` 应该
  接近 300px 宽、三五行；如果只有几十像素、几十行，就是被挤了。

```js
const ps = [...document.querySelectorAll('.workrow p')];
ps.map(p => ({
  w: Math.round(p.getBoundingClientRect().width),
  lines: Math.round(p.getBoundingClientRect().height / parseFloat(getComputedStyle(p).lineHeight)),
})).filter(x => x.w < 200)   // 应该是空数组
```

四个宽度都要过：390 / 768 / 1024 / 1400。
