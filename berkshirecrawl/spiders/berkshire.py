from gc import callbacks
from wsgiref import headers
import scrapy


class berkspider(scrapy.Spider):
    name = "berk"
    start_urls = [
        "https://www.bhhsamb.com/agents"
    ]
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
    page_no = 2
    def parse(self, response):
        for profiles in response.css('div.agent-info'):
            yield {
                "name": profiles.css('span.agent-name a::text').get(),  
            }

        #next_page = response.css('a.page-link').attrib['href']
        #last_page = response.css('span.page-link')
        #if next_page is not last_page:
         #   yield response.follow(next_page, callback=self.parse)

        next_page = 'https://www.bhhsamb.com/agents?page=' +str(berkspider.page_no)
        if berkspider.page_no <= 44:
            berkspider.page_no += 1
            yield scrapy.Request(url=next_page, callback=self.parse)
