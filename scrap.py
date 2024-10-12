import scrapy

class GameSpider(scrapy.Spider):
    name = 'Gamespider'
    start_urls = ['https://store.steampowered.com/']

    def parse(self, response):
        yield {"response": response}


    ## def parse(self, response):
    ##     for title in response.css('.oxy-post-title'):
    ##         yield {'title': title.css('::text').get()}
## 
    ##     for next_page in response.css('a.next'):
    ##         yield response.follow(next_page, self.parse)