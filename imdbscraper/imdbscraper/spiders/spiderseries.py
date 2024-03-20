import scrapy
from imdbscraper.items import ImdbSerieScraperItem
from scrapy.crawler import CrawlerProcess
from scrapy.utils.reactor import install_reactor

install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")

class SpiderseriesSpider(scrapy.Spider):
    name = "spiderseries"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://www.imdb.com/chart/toptv"]

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'

    def parse(self, response):
        series = response.xpath('.//ul[contains(@class, "metadata-list")]/li')
        for serie in series:
            serie_url = serie.xpath('.//a/@href').get()
            yield response.follow(serie_url,self.parse_serie)

        
    def parse_serie(self, response):
        item = ImdbSerieScraperItem()
        item['title'] = response.xpath('.//span[@class="hero__primary-text"]/text()').get()
        item['original_title'] = response.xpath('.//h1[@data-testid="hero__pageTitle"]/following-sibling::div/text()').get()
        try:
            item['creators'] = response.xpath('.//div[@data-testid="shoveler"]/following-sibling::ul/li/div/ul/li/a/text()')[0].get()
        except:
            item['creators'] = None
        item['stars'] = response.xpath('.//a[@data-testid="title-cast-item__actor"]/text()').getall()
        item['popularity'] = response.xpath('.//div[@data-testid="hero-rating-bar__popularity__score"]/text()').get()
        item['rating'] = response.xpath('.//div[@data-testid="hero-rating-bar__aggregate-rating__score"]/span/text()').get()
        item['year'] = response.xpath('.//h1[@data-testid="hero__pageTitle"]/following-sibling::ul/li/a/text()').get()
        item['duration'] = response.xpath('.//li[@data-testid="title-techspec_runtime"]/div/text()').getall()
        item['synopsis'] = response.xpath('.//span[@data-testid="plot-xl"]/text()').get()
        item['country'] = response.xpath('.//li[@data-testid="title-details-origin"]/div/ul/li/a/text()').get()
        item['language'] = response.xpath('.//li[@data-testid="title-details-languages"]/div/ul/li/a/text()').getall()
        item['genre'] = response.css('span.ipc-chip__text::text').getall()
        try:
            item['seasons'] = response.xpath('.//select[@id="browse-episodes-season"]/option/text()')[0].get()
        except:
            item['seasons'] = response.xpath('.//div[@data-testid="episodes-browse-episodes"]/div/a/span/text()').get()
        item['episodes'] = response.xpath('.//div[@data-testid="episodes-header"]/a/h3[@class="ipc-title__text"]/span[@class="ipc-title__subtext"]/text()').get()
        return item