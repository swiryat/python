import scrapy
from scrapy.crawler import CrawlerProcess

class TomskKnigiSpider(scrapy.Spider):
    name = 'tomsk_knigi'
    start_urls = ['https://knigi.tomsk.ru/catalog/literatura_dlya_detey_i_roditeley/detskaya_razvivayushchaya_literatura/52320/']

    def parse(self, response):
        # Извлекаем название книги
        book_title = response.css('h1.product-info-title::text').get()

        # Извлекаем цену книги
        book_price = response.css('span.price-value::text').get()

        # Извлекаем описание книги
        book_description = response.css('div.product-description-text::text').get()

        # Выводим полученные данные
        print(f"Название книги: {book_title}")
        print(f"Цена книги: {book_price}")
        print(f"Описание книги: {book_description}")

# Создаем процесс для запуска Spider
process = CrawlerProcess()

# Запускаем Spider
process.crawl(TomskKnigiSpider)
process.start()
