
import scrapy


class ImdbscraperItem(scrapy.Item):
    title = scrapy.Field()
    directors = scrapy.Field()
    writers = scrapy.Field()
    stars = scrapy.Field()
    popularity = scrapy.Field()
    rating = scrapy.Field()
