import scrapy
from imdbscraper.items import ImdbMovieScraperItem
from scrapy.crawler import CrawlerProcess
from scrapy.utils.reactor import install_reactor

install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")

class SpiderMoviesSpider(scrapy.Spider):
    name = "spidermovies"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top"]

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'

    def parse(self, response):
        movies = response.xpath('.//ul[contains(@class, "metadata-list")]/li')
        for movie in movies:
            movie_url = movie.xpath('.//a/@href').get()
            yield response.follow(movie_url,self.parse_movie)

        
    def parse_movie(self, response):
        item = ImdbMovieScraperItem()
        item['movie'] = self.name
        item['title'] = response.xpath('.//span[@class="hero__primary-text"]/text()').get()
        item['original_title'] = response.xpath('.//h1[@data-testid="hero__pageTitle"]/following-sibling::div/text()').get()
        item['directors'] = response.xpath('.//div[@data-testid="shoveler"]/following-sibling::ul/li/div/ul/li/a/text()')[0].get()
        item['writers'] = response.xpath('.//div[@data-testid="shoveler"]/following-sibling::ul/li/div/ul/li/a/text()')[1].getall()
        item['stars'] = response.xpath('.//a[@data-testid="title-cast-item__actor"]/text()').getall()
        item['popularity'] = response.xpath('.//div[@data-testid="hero-rating-bar__popularity__score"]/text()').get()
        item['rating'] = response.xpath('.//div[@data-testid="hero-rating-bar__aggregate-rating__score"]/span/text()').get()
        item['year'] = response.xpath('.//h1[@data-testid="hero__pageTitle"]/following-sibling::ul/li/a/text()').get()
        item['duration'] = response.xpath('.//h1[@data-testid="hero__pageTitle"]/following-sibling::ul/li/text()').get()
        item['synopsis'] = response.xpath('.//span[@data-testid="plot-xl"]/text()').get()
        item['country'] = response.xpath('.//li[@data-testid="title-details-origin"]/div/ul/li/a/text()').get()
        item['language'] = response.xpath('.//li[@data-testid="title-details-languages"]/div/ul/li/a/text()').getall()
        item['genre'] = response.css('span.ipc-chip__text::text').getall()
        return item

#process = CrawlerProcess()
#process.crawl(ImdbspiderSpider)
#process.start()

