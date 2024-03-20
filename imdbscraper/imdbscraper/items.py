
import scrapy


class ImdbscraperItem(scrapy.Item):
    title = scrapy.Field()
    original_title = scrapy.Field()
    directors = scrapy.Field()
    writers = scrapy.Field()
    stars = scrapy.Field()
    popularity = scrapy.Field()
    rating = scrapy.Field()
    year = scrapy.Field()
    duration = scrapy.Field()
    synopsis = scrapy.Field()
    country = scrapy.Field()
    language = scrapy.Field()
    genre = scrapy.Field()
