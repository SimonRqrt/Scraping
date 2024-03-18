import scrapy
from items import ImdbscraperItem
from scrapy.crawler import CrawlerProcess


class ImdbspiderSpider(scrapy.Spider):
    name = "imdbspider"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top"]

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'

    def parse(self, response):
        movies = response.xpath('.//ul[contains(@class, "metadata-list")]/li')
        for movie in movies:
            movie_url = movie.xpath('.//a/@href').get()
            yield response.follow(movie_url,self.parse_movie)

        
    def parse_movie(self, response):
        item = ImdbscraperItem()
        item['title'] = response.xpath('.//h3[contains(@class,"title")]//text()')
        item['directors'] = response.xpath('//div[@class="credit_summary_item"]/h4[contains(., "Director")]/following-sibling::a/text()').getall()
        item['writers'] = response.xpath('//div[@class="credit_summary_item"]/h4[contains(., "Writers")]/following-sibling::a/text()').getall()
        item['stars'] = response.xpath('//div[@class="credit_summary_item"]/h4[contains(., "Stars")]/following-sibling::a/text()').getall()
        item['popularity'] = response.css(".titleReviewBarSubItem span.subText::text")[2].re('([0-9]+)')
        item['rating'] = response.css(".ratingValue span::text").get()
        return item

process = CrawlerProcess()
process.crawl(ImdbspiderSpider)
process.start()

