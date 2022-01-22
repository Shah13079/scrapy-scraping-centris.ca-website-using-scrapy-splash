from ast import Add, Yield
from cgitb import html
from tkinter import Y
from numpy import product
import scrapy
from json import dumps, load, loads
from .Back_code import Splash_lua_script, User_Agnets
from scrapy_splash import SplashRequest

class CentrisSpiderSpider(scrapy.Spider):
    name = 'file'
    allowed_domains = ['www.centris.ca']

    start_position = {"startPosition": 0}

    def start_requests(self):

        quert_to_server = {
            "query": {
                "UseGeographyShapes": 0,
                "Filters": [
                    {
                        "MatchType": "GeographicArea",
                        "Text": "Nord-du-Québec",
                        "Id": "RARA10"
                    }
                ],
                "FieldsValues": [
                    {
                        "fieldId": "GeographicArea",
                        "value": "RARA10",
                        "fieldConditionId": "",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "Category",
                        "value": "Residential",
                        "fieldConditionId": "",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "SellingType",
                        "value": "Sale",
                        "fieldConditionId": "",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "LandArea",
                        "value": "SquareFeet",
                        "fieldConditionId": "IsLandArea",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "SalePrice",
                        "value": 0,
                        "fieldConditionId": "ForSale",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "SalePrice",
                        "value": 999999999999,
                        "fieldConditionId": "ForSale",
                        "valueConditionId": ""
                    }
                ]
            },
            "isHomePage": True

        }

        yield scrapy.Request(url="https://www.centris.ca/property/UpdateQuery",
                             method='POST',
                             headers={"content-type": "application/json"},
                             body=dumps(quert_to_server),
                             callback=self.Query_submitted)


    def Query_submitted(self, response):

        yield scrapy.Request(url="https://www.centris.ca/Property/GetInscriptions",
                             method="POST",
                             headers={"content-type": "application/json",'accept-language':' en-US'},
                             body=dumps(self.start_position),
                             callback=self.Parse_results
                             )



    def Parse_results(self, response):
        parse_as_dict = loads(response.body)

        Get_html_as_str = parse_as_dict.get("d").get("Result").get('html')
        html_markup = scrapy.Selector(text=Get_html_as_str)

        each_item = html_markup.xpath("//div[@class='shell']")
        for each in each_item:
            Price = each.xpath(".//meta[@itemprop='price']/@content").get()
            Currency = each.xpath(
                ".//meta[@itemprop='priceCurrency']/@content").get()
            Category=each.xpath("normalize-space(.//span[@class='category']/div/text())").get()
            Address=each.xpath(".//span[@class='address']/div/text()").getall()
            Address=','.join(Address)
            Bed_rooms=each.xpath(".//div[@class='cac']/text()").get()
            Washroom=each.xpath(".//div[@class='sdb']/text()").get()
            SKU=each.xpath(".//meta[@itemprop='sku']/@content").get()
            Image=each.xpath(".//a/img[@itemprop='image']/@src").get()
            product_url=each.xpath(".//a[@class='property-thumbnail-summary-link']/@href").get()

            product_url=response.urljoin(product_url)


            yield SplashRequest(

                url=product_url,

                callback=self.parse_product_details,

                endpoint='execute',

                args={
                    "lua_source":Splash_lua_script,
                    },

                meta={
                    "Price":Price,
                    "Currency":Currency,
                    "Category":Category,
                    "Address":Address,
                    "Bed_Rooms":Bed_rooms,
                    "Washroom":Washroom,
                    "Product_SKU":SKU,
                    "Image":Image,
                    "Product_url":product_url

                }
            )


           
        

        total_count=parse_as_dict.get("d").get("Result").get('count')
        Increament_per_page=parse_as_dict.get("d").get("Result").get('inscNumberPerPage')

        #Sending Request for another page startposition is not equal to total counts
        if self.start_position['startPosition'] <= int(total_count):
            self.start_position['startPosition']+=Increament_per_page

            yield scrapy.Request(url="https://www.centris.ca/Property/GetInscriptions",
                             method="POST",
                             headers={"content-type": "application/json"},
                             body=dumps(self.start_position),
                             callback=self.Parse_results
                             )

    
    def parse_product_details(self,response):
        description=response.xpath('normalize-space(//div[@itemprop="description"]/text())').get()
        price=response.request.meta['Price']
        Currency=response.request.meta['Currency']
        Category=response.request.meta['Category']
        Address=response.request.meta['Address']
        Bed_Rooms=response.request.meta['Bed_Rooms']
        Washroom=response.request.meta['Washroom']
        SKU=response.request.meta['Product_SKU']
        Image=response.request.meta['Image']
        Product_url=response.request.meta['Product_url']
      

       

        yield{
            'desc':description,
            "Price":price,
            'Currency':Currency,
            'Category':Category,
            'Address':Address,
            'Bed_Rooms':Bed_Rooms,
            'Washroom':Washroom,
            'SKU':SKU,
            'Image':Image,
            'Product_url':Product_url,
                                        }
                    
            



        