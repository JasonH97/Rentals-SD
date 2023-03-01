#!/usr/bin/python3

import csv
import json
import requests
import lxml.html
from random import choice
from time import sleep

url = 'https://www.apartments.com/services/search/'
headers = {
    'authority': 'www.apartments.com',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'dnt': '1',
    'origin': 'https://www.apartments.com',
    'referer': 'https://www.apartments.com/carlsbad-ca/',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

payloads = {} # not scalable, but I'm only looking to live in San Diego County lol
payloads["Carlsbad"] = '{"Map":{"Resolution":null,"BoundingBox":{"UpperLeft":{"Latitude":33.19090101518969,"Longitude":-117.34118084167481},"LowerRight":{"Latitude":33.05561737938822,"Longitude":-117.23784069274903}},"CountryCode":"US","Shape":null},"Geography":{"ID":"yfklk9r","PlaceId":null,"Display":"Carlsbad, CA","GeographyType":2,"Address":{"City":"Carlsbad","CountryCode":"USA","County":null,"PostalCode":null,"State":"CA","StreetName":null,"StreetNumber":null,"Title":null,"Abbreviation":null,"BuildingName":null,"CollegeCampusName":null,"MarketName":"San Diego","DMA":"San Diego, CA"},"Location":{"Latitude":33.121,"Longitude":-117.287},"BoundingBox":{"LowerRight":{"Latitude":33.06042,"Longitude":-117.2159},"UpperLeft":{"Latitude":33.18257,"Longitude":-117.35883}},"O":null,"Radius":null,"v":16852},"Listing":{"MinRentAmount":null,"MaxRentAmount":null,"MinBeds":null,"MaxBeds":null,"MinBaths":null,"PetFriendly":null,"Style":null,"Specialties":null,"StudentHousingPricings":null,"StudentHousingAmenities":null,"StudentHousings":null,"Ratings":null,"Amenities":null,"MinSquareFeet":null,"MaxSquareFeet":null,"GreenCertifications":null,"Keywords":null,"MoveInDate":null},"Transportation":null,"StateKey":null,"Paging":{"Page":null,"CurrentPageListingKey":null},"SortOption":null,"Mode":null,"IsExtentLoad":null,"IsBoundedSearch":true,"ResultSeed":664536,"SearchView":null,"MapMode":null,"Options":0,"SavedSearchKey":null,"MonetaryUnitType":null,"CountryAbbreviation":"US","LocalGuideUrl":null}'
payloads["Del Mar"] = '{"Map":{"Shape":null,"BoundingBox":{"UpperLeft":{"Latitude":32.98051,"Longitude":-117.27249},"LowerRight":{"Latitude":32.93741,"Longitude":-117.25549}}},"Geography":{"ID":"2l6v1yc","Display":"Del Mar, CA","GeographyType":2,"Address":{"City":"Del Mar","CountryCode":"USA","State":"CA","MarketName":"San Diego","DMA":"San Diego, CA"},"Location":{"Latitude":32.95896,"Longitude":-117.26399},"BoundingBox":{"LowerRight":{"Latitude":32.93741,"Longitude":-117.25549},"UpperLeft":{"Latitude":32.98051,"Longitude":-117.27249}},"v":26835},"Listing":{},"Paging":{"Page":null},"ResultSeed":696100,"Options":0,"CountryAbbreviation":"US","Transportation":null,"IsBoundedSearch":null}'
payloads["Encinitas"] = '{"Map":{"Shape":null,"BoundingBox":{"UpperLeft":{"Latitude":33.08896,"Longitude":-117.31209},"LowerRight":{"Latitude":32.99967,"Longitude":-117.19568}}},"Geography":{"ID":"0ft1sp0","Display":"Encinitas, CA","GeographyType":2,"Address":{"City":"Encinitas","CountryCode":"USA","State":"CA","MarketName":"San Diego","DMA":"San Diego, CA"},"Location":{"Latitude":33.04431,"Longitude":-117.25389},"BoundingBox":{"LowerRight":{"Latitude":32.99967,"Longitude":-117.19568},"UpperLeft":{"Latitude":33.08896,"Longitude":-117.31209}},"v":16023},"Listing":{},"Paging":{"Page":null},"IsBoundedSearch":null,"ResultSeed":18377,"Options":0,"CountryAbbreviation":"US","Transportation":null}'
payloads["Escondido"] = '{"Map":{"Shape":null,"BoundingBox":{"UpperLeft":{"Latitude":33.21161,"Longitude":-117.1461},"LowerRight":{"Latitude":33.05765,"Longitude":-116.99386}}},"Geography":{"ID":"z1p0wjx","Display":"Escondido, CA","GeographyType":2,"Address":{"City":"Escondido","CountryCode":"USA","State":"CA","MarketName":"San Diego","DMA":"San Diego, CA"},"Location":{"Latitude":33.13463,"Longitude":-117.06998},"BoundingBox":{"LowerRight":{"Latitude":33.05765,"Longitude":-116.99386},"UpperLeft":{"Latitude":33.21161,"Longitude":-117.1461}},"v":36739},"Listing":{"MinRentAmount":null,"MaxRentAmount":null,"MinBeds":null,"MaxBeds":null,"MinBaths":null,"PetFriendly":null,"Style":null,"Specialties":null,"StudentHousingPricings":null,"StudentHousingAmenities":null,"StudentHousings":null,"Ratings":null,"Amenities":null,"MinSquareFeet":null,"MaxSquareFeet":null,"GreenCertifications":null,"Keywords":null,"MoveInDate":null},"Transportation":null,"StateKey":null,"Paging":{"Page":null,"CurrentPageListingKey":null},"SortOption":null,"Mode":null,"IsExtentLoad":null,"IsBoundedSearch":null,"ResultSeed":266933,"SearchView":null,"MapMode":null,"Options":0,"SavedSearchKey":null,"MonetaryUnitType":null,"CountryAbbreviation":"US","LocalGuideUrl":null}'
payloads["La Jolla"] = '{"Map":{"Shape":null,"BoundingBox":{"UpperLeft":{"Latitude":32.931,"Longitude":-117.2823},"LowerRight":{"Latitude":32.80619,"Longitude":-117.21403}}},"Geography":{"ID":"xhbdjsm","Display":"La Jolla, CA","GeographyType":2,"Address":{"City":"La Jolla","CountryCode":"USA","State":"CA","MarketName":"San Diego","DMA":"San Diego, CA"},"Location":{"Latitude":32.86859,"Longitude":-117.24816},"BoundingBox":{"LowerRight":{"Latitude":32.80619,"Longitude":-117.21403},"UpperLeft":{"Latitude":32.931,"Longitude":-117.2823}},"v":5751},"Listing":{},"Paging":{"Page":null},"ResultSeed":341197,"Options":0,"CountryAbbreviation":"US","Transportation":null,"IsBoundedSearch":null}'
payloads["La Mesa"] = '{"Map":{"Shape":null,"BoundingBox":{"UpperLeft":{"Latitude":32.79654,"Longitude":-117.05358},"LowerRight":{"Latitude":32.74315,"Longitude":-116.98184}}},"Geography":{"ID":"y06td1r","Display":"La Mesa, CA","GeographyType":2,"Address":{"City":"La Mesa","CountryCode":"USA","State":"CA","MarketName":"San Diego","DMA":"San Diego, CA"},"Location":{"Latitude":32.76985,"Longitude":-117.01771},"BoundingBox":{"LowerRight":{"Latitude":32.74315,"Longitude":-116.98184},"UpperLeft":{"Latitude":32.79654,"Longitude":-117.05358}},"v":31505},"Listing":{},"Paging":{"Page":null},"ResultSeed":878305,"Options":0,"CountryAbbreviation":"US","Transportation":null,"IsBoundedSearch":null}'
payloads["Oceanside"] = '{"Map":{"Shape":null,"BoundingBox":{"UpperLeft":{"Latitude":33.30006,"Longitude":-117.39978},"LowerRight":{"Latitude":33.15272,"Longitude":-117.23685}}},"Geography":{"ID":"522hl4n","Display":"Oceanside, CA","GeographyType":2,"Address":{"City":"Oceanside","CountryCode":"USA","State":"CA","MarketName":"San Diego","DMA":"San Diego, CA"},"Location":{"Latitude":33.22639,"Longitude":-117.31832},"BoundingBox":{"LowerRight":{"Latitude":33.15272,"Longitude":-117.23685},"UpperLeft":{"Latitude":33.30006,"Longitude":-117.39978}},"v":54554},"Listing":{},"Paging":{"Page":null},"ResultSeed":806618,"Options":0,"CountryAbbreviation":"US","Transportation":null,"IsBoundedSearch":null}'
payloads["Pacific Beach"] = '{"Map":{"Shape":null,"BoundingBox":{"UpperLeft":{"Latitude":32.83826,"Longitude":-117.26622},"LowerRight":{"Latitude":32.75591,"Longitude":-117.20472}}},"Geography":{"ID":"1k3sx57","Display":"Pacific Beach, CA","GeographyType":2,"Address":{"City":"Pacific Beach","CountryCode":"USA","State":"CA","MarketName":"San Diego","DMA":"San Diego, CA"},"Location":{"Latitude":32.79709,"Longitude":-117.23547},"BoundingBox":{"LowerRight":{"Latitude":32.75591,"Longitude":-117.20472},"UpperLeft":{"Latitude":32.83826,"Longitude":-117.26622}},"v":25186},"Listing":{},"Paging":{"Page":null},"ResultSeed":518254,"Options":0,"CountryAbbreviation":"US","Transportation":null,"IsBoundedSearch":null}'
payloads["Poway"] = '{"Map":{"Shape":null,"BoundingBox":{"UpperLeft":{"Latitude":33.06641,"Longitude":-117.0843},"LowerRight":{"Latitude":32.92716,"Longitude":-116.94034}}},"Geography":{"ID":"e3clq2q","Display":"Poway, CA","GeographyType":2,"Address":{"City":"Poway","CountryCode":"USA","State":"CA","MarketName":"San Diego","DMA":"San Diego, CA"},"Location":{"Latitude":32.99678,"Longitude":-117.01232},"BoundingBox":{"LowerRight":{"Latitude":32.92716,"Longitude":-116.94034},"UpperLeft":{"Latitude":33.06641,"Longitude":-117.0843}},"v":31670},"Listing":{},"Paging":{"Page":null},"ResultSeed":51513,"Options":0,"CountryAbbreviation":"US","Transportation":null,"IsBoundedSearch":null}'
payloads["San Marcos"] = '{"Map":{"Shape":null,"BoundingBox":{"UpperLeft":{"Latitude":33.18827,"Longitude":-117.23017},"LowerRight":{"Latitude":33.08056,"Longitude":-117.11045}}},"Geography":{"ID":"jtsnbs6","Display":"San Marcos, CA","GeographyType":2,"Address":{"City":"San Marcos","CountryCode":"USA","State":"CA","MarketName":"San Diego","DMA":"San Diego, CA"},"Location":{"Latitude":33.13442,"Longitude":-117.17031},"BoundingBox":{"LowerRight":{"Latitude":33.08056,"Longitude":-117.11045},"UpperLeft":{"Latitude":33.18827,"Longitude":-117.23017}},"v":46276},"Listing":{},"Paging":{"Page":null},"ResultSeed":932811,"Options":0,"CountryAbbreviation":"US","Transportation":null,"IsBoundedSearch":null}'
payloads["Vista"] = '{"Map":{"Shape":null,"BoundingBox":{"UpperLeft":{"Latitude":33.23854,"Longitude":-117.28825},"LowerRight":{"Latitude":33.13113,"Longitude":-117.19226}}},"Geography":{"ID":"qth448w","Display":"Vista, CA","GeographyType":2,"Address":{"City":"Vista","CountryCode":"USA","State":"CA","MarketName":"San Diego","DMA":"San Diego, CA"},"Location":{"Latitude":33.18484,"Longitude":-117.24025},"BoundingBox":{"LowerRight":{"Latitude":33.13113,"Longitude":-117.19226},"UpperLeft":{"Latitude":33.23854,"Longitude":-117.28825}},"v":17787},"Listing":{},"Paging":{"Page":null},"ResultSeed":782930,"Options":0,"CountryAbbreviation":"US","Transportation":null,"IsBoundedSearch":null}'

def main():
    for city in payloads:
        print(f"Scraping information for {city}...")
        response = requests.post(url,headers=headers,data=payloads[city])
        if response.status_code == 200:
            writeContent(
                city,
                parseHTML(response))
        else:
            print(f"HTTP request failed, response {response.status_code}")
        sleeptime = choice(range(3,13))
        print(f"Waiting {sleeptime} seconds until next connection...")
        sleep(sleeptime)

def parseHTML(response):
    data = json.loads(response.content)["PlacardState"]["HTML"]
    doc = lxml.html.fromstring(data)
    posts = doc.xpath('//li/article')
    lines = []
    for p in posts:
        try: price = p.xpath('./section/div/div/div/div/a/p[@class="property-pricing"]/text()')[0]
        except: continue

        try: beds = p.xpath('./section/div/div/div/div/a/p[@class="property-beds"]/text()')[0]
        except: continue

        try: name = p.xpath('./header/div[@class="property-information"]/a/div[@class="property-title"]/@title')[0]
        except: continue

        try: address = p.xpath('./header/div[@class="property-information"]/a/div[contains(@class,"address")]/@title')[0]
        except: continue

        try: url = p.xpath('./header/div[@class="property-information"]/a/@href')[0]
        except: continue

        lines.append([price,beds,name,address,url])
    return lines

def writeContent(city,lines):
    filename = city+"_apartmentsdotcom.csv"
    print(f"Writing {len(lines)} lines of data to {filename}\n")
    with open(filename,'w') as f:
        csvwriter = csv.writer(f,delimiter=",",quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(["price","beds","name","address","url"])
        for line in lines:
            csvwriter.writerow(line)

main()
