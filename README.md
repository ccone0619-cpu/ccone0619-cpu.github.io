# 个人作品集网站

这是一个无构建依赖的静态作品集网站，适合直接部署到 Vercel、Netlify、Cloudflare Pages 或 GitHub Pages。

## 编辑内容

打开 `content.js`，可修改：

- 姓名、职业、位置、邮箱和社交链接
- 首页标题与个人简介
- 首页主视觉图片、替代文本和图片说明
- 个人优势
- 作品名称、分类、年份、描述和角色
- 作品图片地址
- 作品视频地址（将 `type` 改为 `video`）

页面布局与视觉样式在 `index.html`、`styles.css` 和 `app.js` 中维护。

## 本地预览

```bash
python3 -m http.server 4173
```

然后打开 <http://localhost:4173>。
