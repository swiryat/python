import pandas as pd
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def extract_product_info(page):
    product_name = page.query_selector('span.tsBody500Medium').text_content()
    current_price = page.query_selector('span.c3118-a1.tsHeadline500Medium').text_content()
    original_price = page.query_selector('span.c3118-a1.tsBodyControl400Small').text_content()
    discount = page.query_selector('span.c3118-a2').text_content()

    return {
        'Название товара': product_name,
        'Текущая цена': current_price,
        'Исходная цена': original_price,
        'Скидка': discount
    }

def main():
    product_data = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('https://www.ozon.ru/category/chemodany-1657')
        page.wait_for_selector('span.tsBody500Medium', timeout=60000)

        product_info = extract_product_info(page)
        product_data.append(product_info)

    df = pd.DataFrame(product_data)
    df.to_csv('product_info.csv', index=False)

if __name__ == "__main__":
    main()



