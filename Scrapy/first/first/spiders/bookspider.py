import scrapy

class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    start_urls = ['https://www.labirint.ru/books/1012134/']

    def parse(self, response):
        # Извлекаем заголовок книги
        title = response.css('div#product-title h1::text').get()

        # Извлекаем статус доступности книги
        availability = response.css('div.prodtitle-availibility span::text').get()

        # Извлекаем цену книги
        price = response.css('span.buying-pricenew-val-number::text').get()

        # Извлекаем валюту цены книги
        currency = response.css('span.buying-pricenew-val-currency::text').get()

        # Создаем словарь с извлеченными данными
        item = {
            'title': title.strip() if title else None,
            'availability': availability.strip() if availability else None,
            'price': price.strip() if price else None,
            'currency': currency.strip() if currency else None
        }

        yield item


            
            
  
        

