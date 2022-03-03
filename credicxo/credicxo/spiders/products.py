import scrapy
import pandas as pd


class ProductsSpider(scrapy.Spider):
    '''
    spider to scrape amazon products, info of which is in the csv file list.csv
    '''
    name = 'products'

    def start_requests(self):
        df = pd.read_csv('list.csv',index_col=0)

        for x in range(len(df)):
            country = df['country'][x]
            asin = df['Asin'][x]
            if asin[-1] != 'X':
                asin = '000'+asin
            url = f"https://www.amazon.{country}/dp/{asin}"

            yield scrapy.FormRequest(
            url,
            callback=self.parse,
            meta = {'URL':url}
            )  

        

    def parse(self, response):
        url = response.meta.get('URL')
        title = response.xpath('//span[@id="productTitle"]/text()').extract_first()
        if title:
            title = title.strip()
        image_url = response.xpath('//div[@id="imgTagWrapperId" or @id="img-canvas"]/img/@src').extract_first()
        price = response.xpath('//span[@class="a-size-base a-color-price a-color-price"]/text()').extract_first()
        
        # To deal with different forms of html page we have to use the if else statment to get the prices
        if price:
            price = price.strip().replace(u'\xa0',u' ')
        else:
            price = response.xpath('//span[@class="a-color-base"]/text()').extract_first()
            if price:
                pass
            else:
                price = response.xpath('//span[@class="a-offscreen"]/text()').extract_first()

        yield{
            'Url':url,
            'Title':title,
            'Image_URL': image_url,
            'Price': price
        }




# Rough work

# title
# response.xpath('//span[@id="productTitle"]/text()').extract_first().strip()

# image url
# response.xpath('//img[@id="imgBlkFront"]/@src').extract_first()

# price
# response.xpath('//span[@id="price"]/text()').extract_first().replace(u'\xa0',u' ')

# details