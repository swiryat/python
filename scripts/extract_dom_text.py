# extract_dom_text.py
from playwright.sync_api import sync_playwright
import pyperclip
import sys

def extract_text_and_math(url: str) -> str:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until='networkidle')

        text = page.evaluate("() => document.body.innerText")

        formulas = page.evaluate(r"""() => {
            const out = [];
            document.querySelectorAll('script[type="math/tex"]').forEach(el => out.push(el.textContent.trim()));
            document.querySelectorAll('annotation[encoding="application/x-tex"]').forEach(el => out.push(el.textContent.trim()));
            return out;
        }""")

        browser.close()

    md = "# Извлечённый текст\n\n" + text + "\n\n"
    if formulas:
        md += "## Формулы (LaTeX)\n\n"
        for fx in formulas:
            md += f"```latex\n{fx}\n```\n\n"
    return md

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python extract_dom_text.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    result = extract_text_and_math(url)
    pyperclip.copy(result)
    print("Извлечено! Скопировано в буфер. Вот начало:\n")
    print(result[:700])
