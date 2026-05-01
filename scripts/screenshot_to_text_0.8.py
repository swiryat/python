# screenshot_to_text_dom.py

from playwright.sync_api import sync_playwright  # Шаг 1: headless‑браузер
import argparse                                  # Шаг 2: парсинг аргументов
import pyperclip                                 # Шаг 3: буфер обмена

def extract_page(url: str, auth_token: str = None) -> str:
    """Загружает страницу в headless‑Chromium, вытаскивает текст и формулы."""
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context()

        # Шаг 4: если нужна авторизация, ставим cookie
        if auth_token:
            ctx.add_cookies([{
                'name': 'auth',
                'value': auth_token,
                'domain': url.split('/')[2],
                'path': '/'
            }])

        page = ctx.new_page()
        page.goto(url, wait_until='networkidle')

        # Шаг 5: получаем весь текст страницы
        text: str = page.evaluate("() => document.body.innerText")

        # Шаг 6: собираем TeX‑формулы MathJax/KaTeX
        formulas = page.evaluate(r"""() => {
            const out = [];
            // MathJax в <script type="math/tex">
            document.querySelectorAll('script[type="math/tex"]').forEach(el => {
                out.push(el.textContent.trim());
            });
            // KaTeX в <annotation encoding="application/x-tex">
            document.querySelectorAll('annotation[encoding="application/x-tex"]').forEach(el => {
                out.push(el.textContent.trim());
            });
            return out;
        }""")

        browser.close()

    # Шаг 7: формируем Markdown
    md = "# Извлечённый текст\n\n" + text + "\n\n"
    if formulas:
        md += "## Формулы (TeX)\n\n"
        for fx in formulas:
            md += f"```latex\n{fx}\n```\n\n"
    return md

if __name__ == '__main__':
    p = argparse.ArgumentParser(description="Извлечение текста и формул из веб‑страницы")
    p.add_argument('url', help="URL страницы для анализа")
    p.add_argument('--auth', help="JWT или cookie для авторизации", default=None)
    args = p.parse_args()

    result_md = extract_page(args.url, args.auth)
    pyperclip.copy(result_md)  # Шаг 8: сразу в буфер обмена
    print("Результат сохранён в буфер. Вот первые 500 символов:\n")
    print(result_md[:500])
