
import scrapy


class ImdbMovieScraperItem(scrapy.Item):
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


class ImdbSerieScraperItem(scrapy.Item):
    title = scrapy.Field()
    original_title = scrapy.Field()
    creators = scrapy.Field()
    stars = scrapy.Field()
    popularity = scrapy.Field()
    rating = scrapy.Field()
    year = scrapy.Field()
    duration = scrapy.Field()
    synopsis = scrapy.Field()
    country = scrapy.Field()
    language = scrapy.Field()
    genre = scrapy.Field()
    seasons = scrapy.Field()
    episodes = scrapy.Field()
