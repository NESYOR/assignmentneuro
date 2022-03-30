import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import json
d=[]

class ProductsCrawlSpider(CrawlSpider):
    name = 'products_crawl'
    allowed_domains = ['www.midsouthshooterssupply.com']
    start_urls = ['https://www.midsouthshooterssupply.com/dept/reloading/primers?itemsperpage=90']

    rules = (
        Rule(LinkExtractor(allow=r'item/'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        full_description=response.xpath('//section[@class="page-content"]/div[@id="description"]/b/text()').extract()
        manufacturer=full_description[1].lower().split("by")[1]
        status=response.xpath('//div[@class="product-info"]/span[@class="status"]/span/text()').extract()
        stock=True
        if status[0]=='Out of Stock':
            stock=False


        d.append({
            'Title':response.xpath('/html/body/form/main/div/section/div[1]/div[1]/h1/text()').extract(),
            'Price':response.xpath('//div[@class="product-info"]/div[@class="offer"]/span[@class="price"]/span/text()').extract(),
            'full_Desc':full_description,
            'Description':response.xpath('/html/body/form/main/div/section/div[2]/text()').extract(),
            'status':stock,
            'DeliveryInfo':response.xpath('//div[@id="delivery-info"]/ul/li/text()').extract(),
            'manufacturer':manufacturer,
            'review':response.xpath('/html/body/form/main/div/section/div[1]/div[3]/div[4]/div/section/div/div[1]/div/div[1]/div/div[2]').extract()

        })
        jdf=json.dumps(d)

        with open('scrapy.json','w') as file:
            file.write(jdf)
           
#'Price':response.xpath('/html/body/form/main/div/section/div[1]/div[3]/div[1]/span/span/text()').extract_first(),

#         Price in dollars
# Description
# Review
# Delivery Info
# Title
# Stock status i.e. in-stock or out-stock. If in-stock then the value would true and for out-stock value should be false.
# Manufacturer i.e. Remington, Winchester, etc.