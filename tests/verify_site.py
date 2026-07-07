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
    forbidden = ["TO" + "DO", "T" + "BD", "FIX" + "ME", "待" + "定"]
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
