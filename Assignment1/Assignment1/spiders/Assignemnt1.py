import scrapy
from ..items import Assignment1Item

class Assignment1(scrapy.Spider):
    name = "books"
    start_urls = [ 
        'https://books.toscrape.com/', 
    ]

    def parse(self,response):
        all_product = response.css('article.product_pod')
        # Tried these approach but while appling preprocessing i checked No other books were added in the CSV except the first one from the HTML
        # These was because only same object was used.
        # items = Assignment1Item()

        for product in all_product:
            # Added these initialization here as the need to be done as we need to re-initialize the object.
            items = Assignment1Item()
            title = product.css('h3 a::attr(title)').extract()
            price = product.css('div.product_price p.price_color::text').extract()
            availability = product.css('div.product_price p.availability::text').getall()
            rating = product.css('p::attr(class)').extract_first()

            rating_list = rating.split(" ")

            items['title'] = title
            items['price'] = price
            items['availability'] = ''.join(availability).strip()
            items['rating'] = rating_list[1]

            yield items
        
        next_page = response.css('li.next a::attr(href)').get()
        
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
