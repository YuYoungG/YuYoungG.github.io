# 个人主页实现计划

> **面向 AI 代理的工作者：** 必需子技能：使用 superpowers:subagent-driven-development（推荐）或 superpowers:executing-plans 逐任务实现此计划。步骤使用复选框（`- [ ]`）语法来跟踪进度。

**目标：** 构建一个可部署到 GitHub Pages 的纯静态单页个人主页，专业为主并包含少量兴趣生活展示。

**架构：** 网站由 `index.html` 承载页面结构和内容，`styles.css` 负责视觉、布局和响应式适配，`script.js` 只提供轻量增强交互。使用一个 Python 验证脚本检查页面结构、链接安全属性、响应式样式和部署文档，保证纯静态页面在没有后端和构建工具的情况下可验证。

**技术栈：** HTML5、CSS3、少量原生 JavaScript、Python 3 标准库、GitHub Pages。

---

## 文件结构

- 创建：`tests/verify_site.py`
  - 职责：用 Python 标准库验证静态站点结构、必需区块、链接属性、CSS 响应式规则、README 部署说明。
- 创建：`index.html`
  - 职责：承载单页个人主页的语义化结构、导航、首屏、关于我、技能、项目、兴趣生活、联系方式。
- 创建：`styles.css`
  - 职责：定义设计系统变量、布局、卡片、按钮、导航、响应式样式和可访问性焦点样式。
- 创建：`script.js`
  - 职责：实现移动端导航开关、导航点击后关闭菜单、当前年份渲染；核心内容不依赖 JavaScript。
- 创建：`assets/.gitkeep`
  - 职责：保留资源目录，后续可放头像、项目截图和图标。
- 创建：`README.md`
  - 职责：说明本地预览、内容修改、GitHub Pages 部署步骤和可替换内容清单。
- 创建：`.gitignore`
  - 职责：忽略视觉头脑风暴临时文件、系统文件和本地缓存。

## 实施约束

- 保持纯静态，不引入 Node、打包器、第三方 CSS 框架或后端。
- 第一版使用可公开展示的中性中文文案，后续用户可替换为真实姓名、项目和链接。
- 不出现 `TODO`、`待定`、`TBD`、`FIXME` 等未完成标记。
- 外部链接使用 `target="_blank"` 和 `rel="noopener noreferrer"`。
- 核心内容在 JavaScript 失效时仍可阅读。
- 每个任务完成后运行对应验证，并按计划 commit。

---

### 任务 1：建立静态站点验证脚本

**文件：**
- 创建：`tests/verify_site.py`

- [ ] **步骤 1：编写失败的验证脚本**

创建 `tests/verify_site.py`，内容如下：

```python
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.tags = []
        self.links = []
        self.buttons = []
        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self.tags.append(tag)
        self.current_tag = tag
        if "id" in attrs_dict:
            self.ids.add(attrs_dict["id"])
        if tag == "a":
            self.links.append(attrs_dict)
        if tag == "button":
            self.buttons.append(attrs_dict)


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def test_html_structure():
    html = read("index.html")
    parser = SiteParser()
    parser.feed(html)

    required_ids = {"home", "about", "skills", "projects", "life", "contact"}
    assert_true(required_ids.issubset(parser.ids), f"Missing section ids: {required_ids - parser.ids}")
    assert_true("main" in parser.tags, "index.html must include a <main> element")
    assert_true("nav" in parser.tags, "index.html must include a <nav> element")
    assert_true("footer" in parser.tags, "index.html must include a <footer> element")
    assert_true('href="styles.css"' in html, "index.html must load styles.css")
    assert_true('src="script.js"' in html, "index.html must load script.js")


def test_content_requirements():
    html = read("index.html")
    required_text = [
        "查看项目",
        "联系我",
        "关于我",
        "技能",
        "项目作品",
        "兴趣生活",
        "联系方式",
        "GitHub",
    ]
    for text in required_text:
        assert_true(text in html, f"Missing required text: {text}")
    forbidden = ["TODO", "TBD", "FIXME", "待定"]
    for text in forbidden:
        assert_true(text not in html, f"Forbidden unfinished marker found: {text}")


def test_links_are_safe_and_useful():
    html = read("index.html")
    parser = SiteParser()
    parser.feed(html)

    hrefs = [link.get("href", "") for link in parser.links]
    for anchor in ["#home", "#about", "#skills", "#projects", "#life", "#contact"]:
        assert_true(anchor in hrefs, f"Missing navigation anchor: {anchor}")
    assert_true(any(href.startswith("mailto:") for href in hrefs), "Missing mailto contact link")

    for link in parser.links:
        href = link.get("href", "")
        if href.startswith("http"):
            assert_true(link.get("target") == "_blank", f"External link must open in new tab: {href}")
            assert_true(link.get("rel") == "noopener noreferrer", f"External link must use safe rel: {href}")


def test_css_responsive_and_accessible():
    css = read("styles.css")
    required_patterns = [
        r":root",
        r"@media\s*\(max-width:\s*768px\)",
        r"\.hero",
        r"\.project-grid",
        r"\.skill-list",
        r":focus-visible",
    ]
    for pattern in required_patterns:
        assert_true(re.search(pattern, css), f"Missing CSS pattern: {pattern}")


def test_javascript_progressive_enhancement():
    js = read("script.js")
    assert_true("nav-toggle" in js, "script.js must wire the mobile navigation toggle")
    assert_true("aria-expanded" in js, "script.js must update aria-expanded")
    assert_true("current-year" in js, "script.js must update the footer year")


def test_readme_documents_deployment():
    readme = read("README.md")
    required_text = [
        "本地预览",
        "GitHub Pages",
        "用户名.github.io",
        "替换内容",
        "python3 -m http.server",
    ]
    for text in required_text:
        assert_true(text in readme, f"README missing: {text}")


def run_all():
    tests = [
        test_html_structure,
        test_content_requirements,
        test_links_are_safe_and_useful,
        test_css_responsive_and_accessible,
        test_javascript_progressive_enhancement,
        test_readme_documents_deployment,
    ]
    failures = []
    for test in tests:
        try:
            test()
            print(f"PASS {test.__name__}")
        except Exception as exc:
            failures.append((test.__name__, exc))
            print(f"FAIL {test.__name__}: {exc}")
    if failures:
        sys.exit(1)


if __name__ == "__main__":
    run_all()
```

- [ ] **步骤 2：运行验证脚本确认失败**

运行：

```bash
python3 tests/verify_site.py
```

预期：命令失败，输出包含 `FAIL test_html_structure`，原因是 `index.html` 还不存在。

- [ ] **步骤 3：Commit 验证脚本**

运行：

```bash
git add tests/verify_site.py
git commit -m "test: add static site verification"
```

---

### 任务 2：实现 HTML 内容结构

**文件：**
- 创建：`index.html`
- 测试：`tests/verify_site.py`

- [ ] **步骤 1：运行验证确认 HTML 相关测试失败**

运行：

```bash
python3 tests/verify_site.py
```

预期：命令失败，至少包含 `FAIL test_html_structure`，因为 `index.html` 尚未创建。

- [ ] **步骤 2：创建 `index.html`**

创建 `index.html`，内容如下：

```html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="一个偏专业、带个人气息的个人主页，展示个人介绍、技能、项目、兴趣和联系方式。">
  <title>个人主页 | 专业名片</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header class="site-header">
    <a class="brand" href="#home" aria-label="返回首页">个人主页</a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">菜单</button>
    <nav id="site-nav" class="site-nav" aria-label="主导航">
      <a href="#home">首页</a>
      <a href="#about">关于我</a>
      <a href="#skills">技能</a>
      <a href="#projects">项目作品</a>
      <a href="#life">兴趣生活</a>
      <a href="#contact">联系方式</a>
    </nav>
  </header>

  <main>
    <section id="home" class="section hero" aria-labelledby="hero-title">
      <div class="hero-content">
        <p class="eyebrow">Developer / Builder / Lifelong Learner</p>
        <h1 id="hero-title">你好，我是一个正在构建个人作品集的创作者。</h1>
        <p class="hero-summary">我关注实用、清晰、可持续的产品与技术，也喜欢把学习、项目和生活中的观察整理成可分享的内容。</p>
        <div class="hero-actions">
          <a class="button primary" href="#projects">查看项目</a>
          <a class="button secondary" href="#contact">联系我</a>
        </div>
        <div class="social-links" aria-label="社交链接">
          <a href="https://github.com/your-github-username" target="_blank" rel="noopener noreferrer">GitHub</a>
          <a href="https://www.linkedin.com" target="_blank" rel="noopener noreferrer">LinkedIn</a>
        </div>
      </div>
      <div class="hero-card" aria-label="个人摘要卡片">
        <div class="avatar" aria-hidden="true">ME</div>
        <p class="card-label">当前状态</p>
        <p>持续学习、打磨项目、记录成长。</p>
      </div>
    </section>

    <section id="about" class="section" aria-labelledby="about-title">
      <p class="eyebrow">About</p>
      <h2 id="about-title">关于我</h2>
      <p>我希望用这个主页集中展示自己的技能、项目和兴趣。专业上，我重视清晰的问题拆解、可靠的实现和持续迭代；生活中，我喜欢探索新工具、阅读、运动和记录有启发的想法。</p>
    </section>

    <section id="skills" class="section" aria-labelledby="skills-title">
      <p class="eyebrow">Skills</p>
      <h2 id="skills-title">技能</h2>
      <div class="skill-list">
        <span>HTML</span>
        <span>CSS</span>
        <span>JavaScript</span>
        <span>Git</span>
        <span>问题拆解</span>
        <span>文档整理</span>
      </div>
    </section>

    <section id="projects" class="section" aria-labelledby="projects-title">
      <p class="eyebrow">Works</p>
      <h2 id="projects-title">项目作品</h2>
      <div class="project-grid">
        <article class="project-card">
          <h3>个人主页</h3>
          <p>一个部署到 GitHub Pages 的静态个人主页，用来展示个人介绍、技能、项目和联系方式。</p>
          <p class="project-meta">HTML / CSS / JavaScript</p>
          <a href="https://github.com/your-github-username/your-github-username.github.io" target="_blank" rel="noopener noreferrer">查看代码</a>
        </article>
        <article class="project-card">
          <h3>学习记录整理</h3>
          <p>将学习过程中的关键概念、实践经验和工具使用方法整理成结构化笔记。</p>
          <p class="project-meta">Writing / Research / Notes</p>
          <a href="https://github.com/your-github-username" target="_blank" rel="noopener noreferrer">查看更多</a>
        </article>
        <article class="project-card">
          <h3>效率工具实验</h3>
          <p>尝试用简单脚本和工作流减少重复操作，把注意力留给更重要的事情。</p>
          <p class="project-meta">Automation / Workflow</p>
          <a href="https://github.com/your-github-username" target="_blank" rel="noopener noreferrer">项目入口</a>
        </article>
      </div>
    </section>

    <section id="life" class="section" aria-labelledby="life-title">
      <p class="eyebrow">Life</p>
      <h2 id="life-title">兴趣生活</h2>
      <div class="life-grid">
        <article>
          <h3>阅读与记录</h3>
          <p>喜欢把读到的内容转化成自己的理解，沉淀为可复用的笔记。</p>
        </article>
        <article>
          <h3>运动与节奏</h3>
          <p>通过规律运动保持状态，也让工作和生活有更稳定的节奏。</p>
        </article>
        <article>
          <h3>工具探索</h3>
          <p>关注能提升效率和表达质量的工具，并尝试把它们融入日常工作流。</p>
        </article>
      </div>
    </section>

    <section id="contact" class="section contact" aria-labelledby="contact-title">
      <p class="eyebrow">Contact</p>
      <h2 id="contact-title">联系方式</h2>
      <p>如果你想交流项目、合作机会或共同学习的话题，可以通过下面的方式联系我。</p>
      <div class="contact-actions">
        <a class="button primary" href="mailto:hello@example.com">发送邮件</a>
        <a class="button secondary" href="https://github.com/your-github-username" target="_blank" rel="noopener noreferrer">访问 GitHub</a>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <p>© <span id="current-year">2026</span> 个人主页。保持学习，持续构建。</p>
  </footer>

  <script src="script.js" defer></script>
</body>
</html>
```

- [ ] **步骤 3：运行验证确认剩余文件缺失**

运行：

```bash
python3 tests/verify_site.py
```

预期：命令失败，HTML 结构和内容相关测试通过，CSS、JavaScript、README 相关测试失败，因为这些文件尚未创建。

- [ ] **步骤 4：Commit HTML 结构**

运行：

```bash
git add index.html
git commit -m "feat: add homepage html structure"
```

---

### 任务 3：实现视觉样式与响应式布局

**文件：**
- 创建：`styles.css`
- 测试：`tests/verify_site.py`

- [ ] **步骤 1：运行验证确认 CSS 测试失败**

运行：

```bash
python3 tests/verify_site.py
```

预期：命令失败，包含 `FAIL test_css_responsive_and_accessible`，因为 `styles.css` 尚未创建。

- [ ] **步骤 2：创建 `styles.css`**

创建 `styles.css`，内容如下：

```css
:root {
  --bg: #f7f8fb;
  --surface: #ffffff;
  --text: #172033;
  --muted: #5d6678;
  --line: #e4e8f0;
  --primary: #3157d5;
  --primary-dark: #2443a8;
  --accent: #e9efff;
  --shadow: 0 20px 45px rgba(23, 32, 51, 0.08);
  --radius: 22px;
  --max-width: 1080px;
}

* {
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  color: var(--text);
  background: radial-gradient(circle at top left, #edf2ff 0, transparent 34rem), var(--bg);
  line-height: 1.7;
}

a {
  color: var(--primary);
  text-decoration: none;
}

a:hover {
  color: var(--primary-dark);
}

a:focus-visible,
button:focus-visible {
  outline: 3px solid rgba(49, 87, 213, 0.35);
  outline-offset: 3px;
}

.site-header {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 1rem 1.25rem;
  background: rgba(247, 248, 251, 0.88);
  backdrop-filter: blur(16px);
}

.brand {
  font-weight: 800;
  color: var(--text);
}

.site-nav {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.95rem;
}

.site-nav a {
  color: var(--muted);
}

.site-nav a:hover {
  color: var(--text);
}

.nav-toggle {
  display: none;
  border: 1px solid var(--line);
  border-radius: 999px;
  padding: 0.55rem 0.9rem;
  color: var(--text);
  background: var(--surface);
}

.section {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 5rem 1.25rem;
}

.hero {
  display: grid;
  grid-template-columns: minmax(0, 1.4fr) minmax(280px, 0.6fr);
  gap: 2rem;
  align-items: center;
  min-height: calc(100vh - 72px);
}

.eyebrow {
  margin: 0 0 0.8rem;
  color: var(--primary);
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

h1,
h2,
h3,
p {
  margin-top: 0;
}

h1 {
  max-width: 760px;
  margin-bottom: 1rem;
  font-size: clamp(2.4rem, 7vw, 4.8rem);
  line-height: 1.05;
  letter-spacing: -0.06em;
}

h2 {
  margin-bottom: 1rem;
  font-size: clamp(2rem, 4vw, 3rem);
  letter-spacing: -0.04em;
}

h3 {
  margin-bottom: 0.6rem;
}

.hero-summary,
.section > p {
  max-width: 760px;
  color: var(--muted);
  font-size: 1.05rem;
}

.hero-actions,
.contact-actions,
.social-links {
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
  align-items: center;
  margin-top: 1.4rem;
}

.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  border-radius: 999px;
  padding: 0.75rem 1.1rem;
  font-weight: 700;
}

.button.primary {
  color: #ffffff;
  background: var(--primary);
  box-shadow: 0 12px 28px rgba(49, 87, 213, 0.22);
}

.button.primary:hover {
  color: #ffffff;
  background: var(--primary-dark);
}

.button.secondary {
  color: var(--text);
  background: var(--surface);
  border: 1px solid var(--line);
}

.hero-card,
.project-card,
.life-grid article {
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: rgba(255, 255, 255, 0.84);
  box-shadow: var(--shadow);
}

.hero-card {
  padding: 1.5rem;
}

.avatar {
  display: grid;
  place-items: center;
  width: 112px;
  height: 112px;
  margin-bottom: 1.2rem;
  border-radius: 32px;
  color: var(--primary);
  background: var(--accent);
  font-size: 2rem;
  font-weight: 900;
}

.card-label,
.project-meta {
  color: var(--primary);
  font-size: 0.85rem;
  font-weight: 800;
}

.skill-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 1.4rem;
}

.skill-list span {
  border: 1px solid var(--line);
  border-radius: 999px;
  padding: 0.65rem 0.95rem;
  color: var(--text);
  background: var(--surface);
  font-weight: 700;
}

.project-grid,
.life-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
  margin-top: 1.5rem;
}

.project-card,
.life-grid article {
  padding: 1.25rem;
}

.project-card p,
.life-grid p,
.hero-card p {
  color: var(--muted);
}

.contact {
  text-align: center;
}

.contact p,
.contact-actions {
  justify-content: center;
  margin-left: auto;
  margin-right: auto;
}

.site-footer {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 2rem 1.25rem 3rem;
  color: var(--muted);
  text-align: center;
}

@media (max-width: 768px) {
  .site-header {
    align-items: flex-start;
  }

  .nav-toggle {
    display: inline-flex;
  }

  .site-nav {
    position: absolute;
    top: 4.2rem;
    left: 1rem;
    right: 1rem;
    display: none;
    flex-direction: column;
    align-items: stretch;
    padding: 1rem;
    border: 1px solid var(--line);
    border-radius: 18px;
    background: var(--surface);
    box-shadow: var(--shadow);
  }

  .site-nav.is-open {
    display: flex;
  }

  .hero {
    grid-template-columns: 1fr;
    min-height: auto;
    padding-top: 3rem;
  }

  .section {
    padding: 3.5rem 1rem;
  }

  .project-grid,
  .life-grid {
    grid-template-columns: 1fr;
  }
}
```

- [ ] **步骤 3：运行验证确认 CSS 通过且脚本/README 失败**

运行：

```bash
python3 tests/verify_site.py
```

预期：命令失败，`test_css_responsive_and_accessible` 通过，`test_javascript_progressive_enhancement` 和 `test_readme_documents_deployment` 失败。

- [ ] **步骤 4：Commit 样式**

运行：

```bash
git add styles.css
git commit -m "feat: add responsive homepage styling"
```

---

### 任务 4：实现轻量 JavaScript 增强

**文件：**
- 创建：`script.js`
- 测试：`tests/verify_site.py`

- [ ] **步骤 1：运行验证确认 JavaScript 测试失败**

运行：

```bash
python3 tests/verify_site.py
```

预期：命令失败，包含 `FAIL test_javascript_progressive_enhancement`，因为 `script.js` 尚未创建。

- [ ] **步骤 2：创建 `script.js`**

创建 `script.js`，内容如下：

```javascript
const navToggle = document.querySelector(".nav-toggle");
const siteNav = document.querySelector("#site-nav");
const currentYear = document.querySelector("#current-year");

if (currentYear) {
  currentYear.textContent = String(new Date().getFullYear());
}

if (navToggle && siteNav) {
  navToggle.addEventListener("click", () => {
    const isOpen = siteNav.classList.toggle("is-open");
    navToggle.setAttribute("aria-expanded", String(isOpen));
  });

  siteNav.addEventListener("click", (event) => {
    const target = event.target;
    if (target instanceof HTMLAnchorElement) {
      siteNav.classList.remove("is-open");
      navToggle.setAttribute("aria-expanded", "false");
    }
  });
}
```

- [ ] **步骤 3：运行验证确认 JavaScript 通过且 README 失败**

运行：

```bash
python3 tests/verify_site.py
```

预期：命令失败，`test_javascript_progressive_enhancement` 通过，`test_readme_documents_deployment` 失败。

- [ ] **步骤 4：Commit 脚本**

运行：

```bash
git add script.js
git commit -m "feat: add progressive navigation script"
```

---

### 任务 5：补充资源目录、忽略规则和部署文档

**文件：**
- 创建：`assets/.gitkeep`
- 创建：`.gitignore`
- 创建：`README.md`
- 测试：`tests/verify_site.py`

- [ ] **步骤 1：运行验证确认 README 测试失败**

运行：

```bash
python3 tests/verify_site.py
```

预期：命令失败，包含 `FAIL test_readme_documents_deployment`，因为 `README.md` 尚未创建。

- [ ] **步骤 2：创建 `assets/.gitkeep`**

运行：

```bash
mkdir -p assets
touch assets/.gitkeep
```

- [ ] **步骤 3：创建 `.gitignore`**

创建 `.gitignore`，内容如下：

```gitignore
.DS_Store
Thumbs.db
.pytest_cache/
__pycache__/
.superpowers/
```

- [ ] **步骤 4：创建 `README.md`**

创建 `README.md`，内容如下：

```markdown
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
```

- [ ] **步骤 5：运行验证确认全部通过**

运行：

```bash
python3 tests/verify_site.py
```

预期：命令成功，输出包含以下 6 行：

```text
PASS test_html_structure
PASS test_content_requirements
PASS test_links_are_safe_and_useful
PASS test_css_responsive_and_accessible
PASS test_javascript_progressive_enhancement
PASS test_readme_documents_deployment
```

- [ ] **步骤 6：Commit 文档和项目辅助文件**

运行：

```bash
git add README.md .gitignore assets/.gitkeep
git commit -m "docs: add homepage usage and deployment guide"
```

---

### 任务 6：本地预览与最终验证

**文件：**
- 修改：无
- 测试：`tests/verify_site.py`

- [ ] **步骤 1：运行自动验证**

运行：

```bash
python3 tests/verify_site.py
```

预期：命令成功，输出 6 个 `PASS`。

- [ ] **步骤 2：启动本地静态服务**

运行：

```bash
python3 -m http.server 8000
```

预期：终端输出类似：

```text
Serving HTTP on 0.0.0.0 port 8000
```

如果端口被占用，改用：

```bash
python3 -m http.server 8080
```

- [ ] **步骤 3：手动浏览器验证桌面布局**

打开 `http://localhost:8000` 或对应端口地址，检查：

```text
首屏能看到标题、简介、查看项目按钮、联系我按钮和个人摘要卡片。
顶部导航点击后能跳转到对应区块。
项目作品以卡片形式展示。
联系方式区域有邮件和 GitHub 入口。
```

- [ ] **步骤 4：手动浏览器验证移动布局**

把浏览器宽度缩小到手机宽度，检查：

```text
顶部显示菜单按钮。
点击菜单按钮后导航展开。
点击任意导航链接后菜单关闭。
项目卡片和兴趣生活卡片变为单列。
按钮不溢出屏幕。
```

- [ ] **步骤 5：检查未完成标记**

运行：

```bash
rg -n "TODO|TBD|FIXME|待定" index.html styles.css script.js README.md tests/verify_site.py
```

预期：无输出。如果 `rg` 不存在，运行：

```bash
grep -RInE "TODO|TBD|FIXME|待定" index.html styles.css script.js README.md tests/verify_site.py
```

预期：无输出。

- [ ] **步骤 6：Commit 最终验证记录**

如果前面步骤发现问题，先修复并提交对应变更。若没有文件变化，不创建空 commit。运行：

```bash
git status --short
```

预期：没有与实现相关的未提交变更。

---

## 规格覆盖自检

- 首屏介绍：任务 2 创建 `#home`，任务 3 实现首屏布局。
- 关于我：任务 2 创建 `#about`。
- 技能展示：任务 2 创建 `#skills`，任务 3 实现标签样式。
- 项目作品：任务 2 创建 `#projects`，任务 3 实现项目卡片布局。
- 兴趣生活：任务 2 创建 `#life`，任务 3 实现卡片布局。
- 联系方式和社交链接：任务 2 创建 `#contact`、`mailto:` 和外部链接，任务 1 验证安全链接属性。
- 响应式布局：任务 3 添加 `@media (max-width: 768px)`，任务 6 手动验证移动布局。
- GitHub Pages 部署说明：任务 5 创建 README 部署步骤。
- 无后端、无构建工具：所有任务仅使用静态文件、Python 标准库和浏览器。
