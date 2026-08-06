# 个人作品集网站

公开地址：<https://ccone0619-cpu.github.io/apple-portfolio-site/>

这是一个无构建依赖的静态作品集网站。内容集中放在 `content.js`，图片和视频可以放在 `assets/images` 与 `assets/videos`，简历 PDF 放在 `assets`。

## 方式一：直接在 GitHub 修改

1. 打开仓库：<https://github.com/ccone0619-cpu/apple-portfolio-site>
2. 进入 `assets/images` 或 `assets/videos`，点击 **Add file → Upload files** 上传媒体。
3. 文件名建议只使用英文、数字和短横线，例如 `portrait-01.jpg`、`brand-film.mp4`。
4. 回到仓库根目录，打开 `content.js`，点击铅笔图标编辑内容。
5. 修改完成后点击 **Commit changes**。
6. 等待约 1-2 分钟，公开网站会自动更新。

## 方式二：在电脑本地修改

编辑 [content.js](content.js)，然后运行：

```bash
git add content.js assets
git commit -m "Update portfolio content"
git push
```

## 修改个人信息

在 `content.js` 的 `identity` 中修改：

```js
name: "你的真实姓名",
role: "你的职业 / 身份",
location: "所在城市 · 远程协作",
phone: "你的手机号",
wechat: "你的微信号",
email: "your@email.com",
cvUrl: "assets/your-resume.pdf"
```

社交链接也在 `identity.socials` 中修改。不要继续使用 `#`，换成你的真实主页地址。

## 添加图片作品

先把图片上传到 `assets/images`，再在 `projects` 中新增一个项目：

```js
{
  id: "my-project",
  title: "我的项目",
  category: "品牌",
  year: "2026",
  type: "image",
  image: "assets/images/my-project.jpg",
  summary: "一句话介绍项目。",
  detail: "项目完整介绍。",
  role: "我的职责",
  tags: ["品牌识别", "视觉设计"]
}
```

支持 JPG、PNG、WebP。建议图片宽度至少 1600px，上传前尽量压缩。

## 添加视频作品

视频项目需要一张封面图和一个 MP4 视频地址：

```js
{
  id: "my-film",
  title: "我的视频项目",
  category: "影像",
  year: "2026",
  type: "video",
  image: "assets/images/my-film-poster.jpg",
  video: "assets/videos/my-film.mp4",
  summary: "一句话介绍视频。",
  detail: "视频项目完整介绍。",
  role: "导演 · 剪辑",
  tags: ["品牌短片", "影像"]
}
```

视频建议使用 H.264 编码的 MP4，单个文件尽量控制在 50MB 以内。GitHub 单文件上限是 100MB；更大的视频建议使用 Vimeo、Bilibili 或视频 CDN，再把直链填入 `video`。

## 修改履历区

履历区的标题、个人摘要、技能、项目经历和下载文件都在 `content.js` 的 `resume` 中修改：

```js
resume: {
  title: "你的履历标题",
  intro: "一段个人职业摘要。",
  facts: [],
  skills: [],
  experience: []
}
```

下载按钮使用 `identity.cvUrl`。上传新的 PDF 后，把它改成对应路径，例如 `assets/my-resume.pdf`。

页面还包含轻量滚动显现、顶部阅读进度、主视觉跟随、桌面视频悬停预览和按钮按压反馈；系统开启减少动效时会自动关闭这些效果。

## 简历和其他文件

简历可以上传到 `assets` 目录，然后把 `identity.cvUrl` 改为对应路径，例如 `assets/your-resume.pdf`。

## 本地预览

```bash
python3 -m http.server 4173
```

然后打开 <http://localhost:4173>。
