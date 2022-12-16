import scrapy
import pandas as pd
from datetime import datetime

from quotes_js_scraper.items import QuoteItem

from scrapy_splash import SplashRequest 

lua_script ="""
function main(splash, args)
  assert(splash:go(args.url))
  assert(splash:wait(5))
  return {
    html = splash:html(),
    png = splash:png(),
    har = splash:har(),
  }
end

"""
class QuotesSpider(scrapy.Spider):
    name = 'naverFlight'

    def start_requests(self):
        url = 'https://flight.naver.com/flights/international/ICN-CDG-20221218?2&isDirect=true&fareType=N'
        yield SplashRequest(
            url, 
            callback=self.parse, 
            endpoint='execute', 
            args={'wait': 0.5, 'lua_source': lua_script,  url :'https://flight.naver.com/flights/international/ICN-CDG-20221218?2&isDirect=true&fareType=N'}
            )

    def parse(self, response):
        # print("response")

        departTime = []
        arrivalTime = []

        # print(response.text)

        # print("area")
        product = response.css('div.indivisual_results__3bdgf') # 아시아나 항공부터 에어프랑스까지 표현되어 있는 하나의 블록
        # print(product)

        # 하나의 블록에는 여러가지가 있으니까 그중에서 하나를 선언한다.

        # airlineList = product.css('b.name::text')

        # for i in range(0,airlineList):
        #     print(airlineList[i].get())

        airlineList = product.css('b.name::text').getall() # 한 블럭에 있는 내용중 b 태크의 class명 name의 text 속성들을 getall()하면 리턴값이 리스트이다.
        print(airlineList)

        print(type(airlineList))

        length = len(airlineList)

        print("총 길이: " + str(length))

        # print(type(airlineList))

        for i in range(0, length):
            airlineBasicInfo = product.css('div.route_Route__2UInh')[i]

            time = airlineBasicInfo.css('b.route_time__-2Z1T::text').getall()

            # print("departTime" + time[0])
            # print("arrivalTime" + time[1])

            departTime.append(time[0])
            arrivalTime.append(time[1])

        # print(departTime)
        # print(arrivalTime)

        airlineInfo = pd.DataFrame(zip(airlineList, departTime, arrivalTime), columns=['airline', 'departTime', 'arrivalTime'])

        print(airlineInfo)
        
        now = datetime.now() 
        fileName = now.strftime("%Y-%m-%d %H:%M:%S")

        # location = f'./data/{fileName}.csv'
        location = f'quotes_js_scraper/data/{fileName}.csv'

# import quotes_js_scraper.data


        airlineInfo.to_csv(location, header=True)



        # airlineBasicInfo = product.css('div.route_Route__2UInh')[0] # 출발 시간, 출발 장소, 도착 시간, 직항, 시간

        # time = airlineBasicInfo.css('b.route_time__-2Z1T::text').getall()
        # print(time)

        # print(airlineTime)

        



        # airlineDepartTime = product.css('span.route_airport__3VT7M::text').getall()
        # print(airlineDepartTime)



        # print("총 갯수: " + len(airlineList))

        # name = product.css('b.name::text')[0].get()
        # print(name)

        # oneBlock = product[0].css('div.indivisual_IndivisualItem__3co62 result')
        # print(oneBlock)

        # airline = product.css('div.indivisual_IndivisualItem__3co62 result') # 한개 한개중 하나 로우 하나
        # one = airline[0]
        # print(one)

        # airlineName = one.css('b.name::text')
        # print(airlineName)

        # print("airline")
        # airline = product[0].css('b.name::text')
        # print(airline)

        # quote_item = QuoteItem()
        # for quote in response.css('div.quote'):
        #     quote_item['text'] = quote.css('span.text::text').get()
        #     quote_item['author'] = quote.css('small.author::text').get()
        #     quote_item['tags'] = quote.css('div.tags a.tag::text').getall()
        #     yield quote_item