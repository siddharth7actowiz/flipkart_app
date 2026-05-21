from itertools import product

import scrapy
import json,re,os,gzip
from flipkart.items import FlipkartPL

from scrapy.cmdline import execute
#---PagesaveDir--
pagesave=r"D:\apps\flipkart\flipkart\pagesave\product_listing"
class Flipkart_PL(scrapy.Spider):
    name = "pl"

    def start_requests(self):
        payload = {
            "pageUri": "/search?q=t+shirts&sid=search.flipkart.com&as-show=on&marketplace=FLIPKART&inputType=TEXT&predictiveHint=watches&widgetUniqueId=6",
            "pageContext": {
                "pageHashKey": None,
                "slotContextMap": None,
                "paginationContextMap": {
                    "federator": {
                        "SHOP_PRODUCT_CARD": 0,
                        "store.path": "search.flipkart.com",
                        "ccsi": "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",
                        "SHOP_CARD": 0,
                        "layout": "grid"
                    }
                },
                "stateInfoMap": None,
                "slotIdInfoMap": None,
                "gamificationBUInfoMap": None,
                "paginatedFetch": True,
                "pageNumber": 2,
                "fetchAllPages": False,
                "networkSpeed": 26,
                "trackingContext": {
                    "context": {
                        "eVar51": "Search",
                        "eVar61": "Search"
                    }
                },
                "fetchSeoData": False,
                "ltcContext": None
            },
            "partnerContext": None,
            "locationContext": None,
            "requestContext": {
                "type": "BROWSE_PAGE",
                "ssid": "76b96b4d-aaad-419c-a09f-7d46294cb615",
                "sqid": "cf795ad5-d656-4142-bdf4-905224e3c53b",
                "disableSearchInfo": None,
                "imageContext": None,
                "flippiContext": None
            }
        }
        headers = {
            'Accept-Encoding': 'gzip',
            'at': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImQ2Yjk5NDViLWZmYTEtNGQ5ZC1iZDQyLTFkN2RmZTU4ZGNmYSJ9.eyJleHAiOjE3ODEwNjI1MjgsImlhdCI6MTc3OTMzNDUyOCwiaXNzIjoia2V2bGFyIiwianRpIjoiNGEwOTIzYWEtMzY0OS00NTdkLTk4OWItYWFiZjU0MTg2NjIxIiwidHlwZSI6IkFUIiwiZElkIjoiZDBmODhlNjU1ZTk3NzdlNzdkOThjNTcxOTVjNDkyNzYiLCJrZXZJZCI6IlZJOUM2MzdFODExQTE0NDcwMTlERTAxNzM3MkZFMzVBRDAiLCJ0SWQiOiJtYXBpIiwidnMiOiJMTyIsInoiOiJDSCIsIm0iOnRydWUsImdlbiI6MX0.XZ6KkOs15BNNe7OhcuhPpFqSljY7AKi7mAolhIK0ofs',
            'Connection': 'Keep-Alive',
            'Content-Type': 'application/json; charset=UTF-8',
            'Cookie': 'vd=VI9C637E811A1447019DE017372FE35AD0-1779334528108-5.1779350361.1779350361.151238385; Max-Age=15552000; Domain=flipkart.net; Path=/; Secure; HttpOnly; ud=6.vlZgohnaUd0_DVPJq-kjaj6Cy-DScTH6yvnOmMT-9CfuSBJ7zl_viltudP8-4tbHDcoUH3DUmr2qLfM9KPGGAk5MfiKNlq0zcGaiI6ZNaAi5XrzEvdhOd_uBB-VakDSdKLoSBvKQf3TX0_T6IV9jYLxQT0bhWbAU0nm6oEcRemes7icV9TAaRg5Ztvm7XX7j8u79tLc76WTtYLP-CPuSuKk67RbiPR6JNAU0eZ_zp_DrD3-6sdGZ_p6628-pohKZlGRBFQ2mlUmuwPN5TaXhlywgpi-271hBpGUAWruJej-tJTOVDZkJ1dvhzPCMGmUP332FfOofOyEzi...; vd=VI9C637E811A1447019DE017372FE35AD0-1779334528108-6.1779352754.1779352754.151398154',
            'Host': '1.rome.api.flipkart.net',
            'Network-Type': 'wifi',
            'secureCookie': 'd1t15P3E/Pz8/P1I/Pz8/OXE/ReRvs87rHk2LIz/VMymIlzXDgXvOjP50eZzSgbh+O11cWp9bl9mOF5msfml9mFyzQA==',
            'secureToken': 'AL0Xw2RxlzLDYc+CaN0TSMbIvFCHE44Ejodm1E272OcjD8EKeJ3t33Sk1ZylKLglOmfak0ic9+h2uTTBYthW5Q==',
            'sn': 'VI9C637E811A1447019DE017372FE35AD0.TOK2519ACDA7F3F454693245316F6854EFC.1779350402011.LO',
            'User-Agent': 'okhttp/4.9.2',
            'X-AppSession-ID': 'bbbd5abe-023f-4428-b8b1-f2719c133d9a_1779344621780',
            'X-AR-AVAILABILITY': 'PRESENT',
            'x-atlas-versions': '30010000/3130100',
            'X-DLS': 'true',
            'X-INPUT-TYPE': 'TEXT',
            'X-Layout-Version': '{"appVersion":"910000","frameworkVersion":"1.0"}',
            'X-Location-Info': '{"cl":true}',
            'X-MULTIWIDGET-VERSION': '8.8.8',
            'X-NewRelic-ID': 'VwEHUVRUARABUVlaAAQGXlED',
            'x-request-metaInfo': '{"pageUri":"%2Fsearch%3Fq%3Dt%2Bshirts%26sid%3Dsearch.flipkart.com%26as-show%3Don%26marketplace%3DFLIPKART%26inputType%3DTEXT%26predictiveHint%3Dwatches%26widgetUniqueId%3D6"}',
            'x-unified-atlas-version': '3130100.-1.-1.8008008.3000010.1003003',
            'X-User-Agent': 'Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI) FKUA/Retail/3130100/Android/Mobile (Asus/ASUS_I003DD/d0f88e655e9777e77d98c57195c49276)',
            'X-Visit-Id': 'd0f88e655e9777e77d98c57195c49276-1779344621878'
        }

        url = "https://1.rome.api.flipkart.net/4/page/fetch"
        for i in range(1,25):
            page_no=i
            payload["pageContext"]["pageNumber"]=page_no

            yield scrapy.Request( url=url,method="POST", headers=headers, body=json.dumps(payload),callback=self.parse,meta={"page_no":page_no})

    def parse(self,response):
        page_no=response.meta.get("page_no")
        print(response.status)
        data=json.loads(response.text)
        item=FlipkartPL()
        #response save

        filepath=os.path.join(pagesave,f"{page_no}_pl.json.gz")
        with gzip.open(filepath,"wt",encoding="utf-8")as f:
            json.dump(data,f,indent=4,ensure_ascii=False)
            print("Response of pl Saved to",filepath)
        #RESPONSE.slots[0].widget.data.products[0].action.url
        slots=data.get("RESPONSE",{}).get("slots",[])
        for  slot in slots:
            products=slot.get("widget",{}).get("data").get("products",{})

            for p in products:
                url=p.get("action").get("url")
                pid = re.search(r"pid=([A-Z0-9]+)", url).group(1)
                print(f"{pid}:{url}")
                item={
                    "product_id":pid,
                    "url":url
                }
                yield item
                # print("https://www.flipkart.com/"+url)
if __name__=="__main__":
    execute("scrapy crawl pl".split())

