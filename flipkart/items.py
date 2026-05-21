# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class FlipkartPL(scrapy.Item):
        product_id = scrapy.Field()
        url=scrapy.Field()
class FlipkartItem(scrapy.Item):

        product_id = scrapy.Field()
        catalog_id = scrapy.Field()
        catalog_name = scrapy.Field()
        source = scrapy.Field()
        scraped_date = scrapy.Field()
        product_name = scrapy.Field()
        image_url = scrapy.Field()
        category_hierarchy = scrapy.Field()
        product_price = scrapy.Field()
        arrival_date = scrapy.Field()
        shipping_charges = scrapy.Field()
        is_sold_out = scrapy.Field()
        discount = scrapy.Field()
        mrp = scrapy.Field()
        page_url = scrapy.Field()
        product_url = scrapy.Field()
        number_of_ratings = scrapy.Field()
        avg_rating = scrapy.Field()
        position = scrapy.Field()
        country_code = scrapy.Field()
        others = scrapy.Field()
