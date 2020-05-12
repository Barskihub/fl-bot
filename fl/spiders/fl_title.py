# -*- coding: utf-8 -*-
import scrapy


class FlTitleSpider(scrapy.Spider):
    name = 'fl-title'
    allowed_domains = ['https://www.fl.ru/']
    start_urls = ['https://www.fl.ru/projects/']

    def parse(self, response):
        # Извлечение данных с помощью селекторов CSS
        product_name = response.css('.b-post__link::text').extract()
        product_link = response.css("a.b-post__link::attr(href)").extract()

        row_data = zip(product_name, product_link)

        # извлечение данных строки
        for item in row_data:
            # создать словарь для хранения извлеченной информации
            scraped_info = {
                'product_name': item[0],
                "url": "https://www.fl.ru" + item[1]
            }

            # генерируем очищенную информацию для скрапа
            yield scraped_info
