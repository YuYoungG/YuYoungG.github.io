# 个人主页

这是一个纯静态个人主页，适合部署到 GitHub Pages。页面包含个人介绍、技能、项目作品、兴趣生活和联系方式。

## 本地预览

在项目根目录运行：

```bash
python3 -m http.server 8000
```

然后打开：

```text
http://localhost:8000
```

也可以直接用浏览器打开 `index.html`，但本地服务更接近线上访问方式。

## 替换内容

上线前建议替换以下内容：

- `index.html` 中的姓名、身份标签和首屏介绍
- `index.html` 中的 GitHub 用户名链接
- `index.html` 中的邮箱 `hello@example.com`
- `index.html` 中的项目名称、项目简介和项目链接
- `index.html` 中的技能标签和兴趣生活描述
- `assets/` 中的头像或项目截图，并在 `index.html` 中引用

## GitHub Pages 部署

1. 在 GitHub 创建一个仓库，仓库名使用 `用户名.github.io`。
2. 将本项目文件提交到该仓库的默认分支。
3. 打开仓库 Settings。
4. 进入 Pages 设置。
5. Source 选择默认分支和根目录。
6. 保存后等待 GitHub Pages 发布。
7. 访问 `https://用户名.github.io` 查看主页。

如果仓库名已经是 `用户名.github.io`，GitHub 通常会自动按用户主页发布。

## 验证

运行：

```bash
python3 tests/verify_site.py
```

预期所有检查输出 `PASS`。
