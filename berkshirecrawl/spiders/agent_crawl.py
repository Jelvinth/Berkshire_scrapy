import scrapy


class berkspiders(scrapy.Spider):
    name = "berksh"
    start_urls = [
        "https://www.bhhsamb.com/agents"
    ]
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
    page_no = 2
    def parse(self, response):
        hrefs = response.css('div.row div.agent-pic a::attr(href)').getall()
        for url in hrefs:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_details)


        next_page = 'https://www.bhhsamb.com/agents?page=' +str(berkspiders.page_no)
        if berkspiders.page_no <= 44:
            berkspiders.page_no += 1
            yield scrapy.Request(url=next_page, callback=self.parse)
    
    def parse_details(self, response):
            yield {
                "name" : response.css('h1.body-title::text').get(),
                "job_title" : response.css('span.big-text ::text').get(),
                "image_url" : response.css('img.agent-photo::attr(src)').get(),
                "address" : response.css('div.text-left span.big-text::text').get(),
                "contact_details" : {
                    'office' : response.css('a[data-type="Office"] ::text').get(),
                    'cell' : response.css('a[data-type="Agent"] ::text').get(),
                    'fax' : response.css('a[data-type="Agent"] ::text').get(),
                },
                "social_accounts" : {
                    'facebook' : response.css('a.fb::attr(href)').get(),
                    'twitter': response.css('a.tw::attr(href)').get(),
                    'linkedin' : response.css('a.li::attr(href)').get(),
                    'youtube' : response.css('a.yt::attr(href)').get(),
                    'pinterest' : response.css('a.pi::attr(href)').get(),
                    'instagram' : response.css('a.ig::attr(href)').get(),

                },
                "offices" : response.css('div#team_offices a::text').getall(),
                "languages" : response.css('ul.first::text').getall(),
                "description" :  ''.join(response.css('div.col-sm-24 >p::text').getall()).replace("\xa0"," "),
            }
        # except:
        #     yield {
        #         "name" : response.css('h1.body-title::text').get(),
        #         "job_title" : response.css('').get(),
        #         "image_url" : response.css('').get(),
        #         "address" : response.css('').get(),
        #         "contact_details" : response.css('').get(),
        #         "social_accounts" : response.css('').get(),
        #         "offices" : response.css('').get(),
        #         "languages" : response.css('').get(),
        #         "description" : response.css('').get(),
        #     }