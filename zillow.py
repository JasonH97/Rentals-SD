#!/usr/bin/python3

import csv
import json
import lxml.html
import re
import requests
from time import sleep

#searchTerm = "Post%20Falls%2C%20ID" # format as appears in URL
#west = "-116.95183861726733"
#east = "-116.93432915681811"
#south = "47.700640437167365"
#north = "47.71323155942821"

#zoom = "500"
# configurable, currently not working
#'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22'+searchTerm+'%22%2C%22mapBounds%22%3A%7B%22west%22%3A'+west+'%2C%22east%22%3A'+east+'%2C%22south%22%3A'+south+'%2C%22north%22%3A'+north+'%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A40420%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%2C%22sortSelection%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A'+zoom+'%7D&wants={%22cat1%22:[%22listResults%22,%22mapResults%22],%22cat2%22:[%22total%22]}&requestId=2'

urls = [ # rentals
# San Diego
'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22San%20Diego%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-117.669281234375%2C%22east%22%3A-116.548675765625%2C%22south%22%3A32.32011066666613%2C%22north%22%3A33.326410248566326%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A54296%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%2C%22isForRent%22%3A%7B%22value%22%3Atrue%7D%2C%22isForSaleByAgent%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleByOwner%22%3A%7B%22value%22%3Afalse%7D%2C%22isNewConstruction%22%3A%7B%22value%22%3Afalse%7D%2C%22isComingSoon%22%3A%7B%22value%22%3Afalse%7D%2C%22isAuction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleForeclosure%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D&wants={%22cat1%22:[%22listResults%22,%22mapResults%22]}&requestId=2',

# La Mesa
'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22La%20Mesa%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-117.06402084179688%2C%22east%22%3A-116.92394515820313%2C%22south%22%3A32.70493249090968%2C%22north%22%3A32.8308012406622%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A46089%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22isForSaleByAgent%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleByOwner%22%3A%7B%22value%22%3Afalse%7D%2C%22isNewConstruction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleForeclosure%22%3A%7B%22value%22%3Afalse%7D%2C%22isComingSoon%22%3A%7B%22value%22%3Afalse%7D%2C%22isAuction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForRent%22%3A%7B%22value%22%3Atrue%7D%2C%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A13%7D&wants={%22cat1%22:[%22mapResults%22]}&requestId=2',

# Tierrasanta
'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Tierrasanta%2C%20San%20Diego%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-117.13281484179689%2C%22east%22%3A-116.99273915820314%2C%22south%22%3A32.771995124120664%2C%22north%22%3A32.89776902735328%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A118541%2C%22regionType%22%3A8%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22isForSaleByAgent%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleByOwner%22%3A%7B%22value%22%3Afalse%7D%2C%22isNewConstruction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleForeclosure%22%3A%7B%22value%22%3Afalse%7D%2C%22isComingSoon%22%3A%7B%22value%22%3Afalse%7D%2C%22isAuction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForRent%22%3A%7B%22value%22%3Atrue%7D%2C%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A13%7D&wants={%22cat1%22:[%22mapResults%22]}&requestId=2',

# Grantville
'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Grantville%2C%20San%20Diego%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-117.13211242089844%2C%22east%22%3A-117.06207457910156%2C%22south%22%3A32.76557391029629%2C%22north%22%3A32.828487675276804%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A115372%2C%22regionType%22%3A8%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22isForSaleByAgent%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleByOwner%22%3A%7B%22value%22%3Afalse%7D%2C%22isNewConstruction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleForeclosure%22%3A%7B%22value%22%3Afalse%7D%2C%22isComingSoon%22%3A%7B%22value%22%3Afalse%7D%2C%22isAuction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForRent%22%3A%7B%22value%22%3Atrue%7D%2C%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A14%7D&wants={%22cat1%22:[%22mapResults%22]}&requestId=2',

# Lake Murray
'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Lake%20Murray%2C%20San%20Diego%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-117.06587642089843%2C%22east%22%3A-116.99583857910156%2C%22south%22%3A32.78705436053624%2C%22north%22%3A32.84995292763973%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A268247%2C%22regionType%22%3A8%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22isForSaleByAgent%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleByOwner%22%3A%7B%22value%22%3Afalse%7D%2C%22isNewConstruction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleForeclosure%22%3A%7B%22value%22%3Afalse%7D%2C%22isComingSoon%22%3A%7B%22value%22%3Afalse%7D%2C%22isAuction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForRent%22%3A%7B%22value%22%3Atrue%7D%2C%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A14%7D&wants={%22cat1%22:[%22mapResults%22]}&requestId=2',

# Kearny Mesa
'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Kearny%20Mesa%2C%20San%20Diego%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-117.18136092089844%2C%22east%22%3A-117.11132307910157%2C%22south%22%3A32.79647416717914%2C%22north%22%3A32.85936606678271%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A274164%2C%22regionType%22%3A8%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22isForSaleByAgent%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleByOwner%22%3A%7B%22value%22%3Afalse%7D%2C%22isNewConstruction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleForeclosure%22%3A%7B%22value%22%3Afalse%7D%2C%22isComingSoon%22%3A%7B%22value%22%3Afalse%7D%2C%22isAuction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForRent%22%3A%7B%22value%22%3Atrue%7D%2C%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A14%7D&wants={%22cat1%22:[%22mapResults%22]}&requestId=2',

# North Clairemont
'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22North%20Clairemont%2C%20San%20Diego%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-117.22819642089843%2C%22east%22%3A-117.15815857910155%2C%22south%22%3A32.802483664831755%2C%22north%22%3A32.86537130992305%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A116921%2C%22regionType%22%3A8%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22isForSaleByAgent%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleByOwner%22%3A%7B%22value%22%3Afalse%7D%2C%22isNewConstruction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleForeclosure%22%3A%7B%22value%22%3Afalse%7D%2C%22isComingSoon%22%3A%7B%22value%22%3Afalse%7D%2C%22isAuction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForRent%22%3A%7B%22value%22%3Atrue%7D%2C%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A14%7D&wants={%22cat1%22:[%22mapResults%22]}&requestId=2',

# Pacific Beach
'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Pacific%20Beach%2C%20San%20Diego%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-117.27306742089843%2C%22east%22%3A-117.20302957910155%2C%22south%22%3A32.76788411233663%2C%22north%22%3A32.830796243223766%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A117156%2C%22regionType%22%3A8%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22isForSaleByAgent%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleByOwner%22%3A%7B%22value%22%3Afalse%7D%2C%22isNewConstruction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleForeclosure%22%3A%7B%22value%22%3Afalse%7D%2C%22isComingSoon%22%3A%7B%22value%22%3Afalse%7D%2C%22isAuction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForRent%22%3A%7B%22value%22%3Atrue%7D%2C%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A14%7D&wants={%22cat1%22:[%22mapResults%22]}&requestId=2',

# Ocean Beach
'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Ocean%20Beach%2C%20San%20Diego%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-117.26318346044923%2C%22east%22%3A-117.22816453955079%2C%22south%22%3A32.72991434480988%2C%22north%22%3A32.76138939380873%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A117021%2C%22regionType%22%3A8%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22isForSaleByAgent%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleByOwner%22%3A%7B%22value%22%3Afalse%7D%2C%22isNewConstruction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleForeclosure%22%3A%7B%22value%22%3Afalse%7D%2C%22isComingSoon%22%3A%7B%22value%22%3Afalse%7D%2C%22isAuction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForRent%22%3A%7B%22value%22%3Atrue%7D%2C%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A15%7D&wants={%22cat1%22:[%22mapResults%22]}&requestId=2',

# La Jolla
'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22La%20Jolla%2C%20San%20Diego%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-117.32483884179688%2C%22east%22%3A-117.18476315820313%2C%22south%22%3A32.78499624444908%2C%22north%22%3A32.91075174032662%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A46087%2C%22regionType%22%3A8%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22isForSaleByAgent%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleByOwner%22%3A%7B%22value%22%3Afalse%7D%2C%22isNewConstruction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleForeclosure%22%3A%7B%22value%22%3Afalse%7D%2C%22isComingSoon%22%3A%7B%22value%22%3Afalse%7D%2C%22isAuction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForRent%22%3A%7B%22value%22%3Atrue%7D%2C%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A13%7D&wants={%22cat1%22:[%22mapResults%22]}&requestId=2',

# University City
'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22University%20City%2C%20San%20Diego%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-117.27740734179687%2C%22east%22%3A-117.13733165820312%2C%22south%22%3A32.807716598044216%2C%22north%22%3A32.93343991028878%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A118673%2C%22regionType%22%3A8%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22isForSaleByAgent%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleByOwner%22%3A%7B%22value%22%3Afalse%7D%2C%22isNewConstruction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleForeclosure%22%3A%7B%22value%22%3Afalse%7D%2C%22isComingSoon%22%3A%7B%22value%22%3Afalse%7D%2C%22isAuction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForRent%22%3A%7B%22value%22%3Atrue%7D%2C%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A13%7D&wants={%22cat1%22:[%22mapResults%22]}&requestId=2',

# Point Loma Heights
'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Point%20Loma%20Heights%2C%20San%20Diego%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-117.26828542089844%2C%22east%22%3A-117.19824757910156%2C%22south%22%3A32.712628024693494%2C%22north%22%3A32.775579212293984%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A268410%2C%22regionType%22%3A8%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22isForSaleByAgent%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleByOwner%22%3A%7B%22value%22%3Afalse%7D%2C%22isNewConstruction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleForeclosure%22%3A%7B%22value%22%3Afalse%7D%2C%22isComingSoon%22%3A%7B%22value%22%3Afalse%7D%2C%22isAuction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForRent%22%3A%7B%22value%22%3Atrue%7D%2C%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A14%7D&wants={%22cat1%22:[%22mapResults%22]}&requestId=2',

# Sunset Cliffs
'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Sunset%20Cliffs%2C%20San%20Diego%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-117.26853596044921%2C%22east%22%3A-117.23351703955078%2C%22south%22%3A32.71162978577175%2C%22north%22%3A32.74311129178905%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A118387%2C%22regionType%22%3A8%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22isForSaleByAgent%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleByOwner%22%3A%7B%22value%22%3Afalse%7D%2C%22isNewConstruction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleForeclosure%22%3A%7B%22value%22%3Afalse%7D%2C%22isComingSoon%22%3A%7B%22value%22%3Afalse%7D%2C%22isAuction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForRent%22%3A%7B%22value%22%3Atrue%7D%2C%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A15%7D&wants={%22cat1%22:[%22mapResults%22]}&requestId=2',

# Roseville - Fleet Ridge
'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Roseville%20-%20Fleet%20Ridge%2C%20San%20Diego%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-117.25019346044922%2C%22east%22%3A-117.21517453955079%2C%22south%22%3A32.71296853997149%2C%22north%22%3A32.74444957332917%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A117770%2C%22regionType%22%3A8%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22isForSaleByAgent%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleByOwner%22%3A%7B%22value%22%3Afalse%7D%2C%22isNewConstruction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleForeclosure%22%3A%7B%22value%22%3Afalse%7D%2C%22isComingSoon%22%3A%7B%22value%22%3Afalse%7D%2C%22isAuction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForRent%22%3A%7B%22value%22%3Atrue%7D%2C%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A15%7D&wants={%22cat1%22:[%22mapResults%22]}&requestId=2',

# La Playa
'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22La%20Playa%2C%20San%20Diego%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-117.25025946044921%2C%22east%22%3A-117.21524053955078%2C%22south%22%3A32.6993070503695%2C%22north%22%3A32.73079290623636%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A116026%2C%22regionType%22%3A8%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22isForSaleByAgent%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleByOwner%22%3A%7B%22value%22%3Afalse%7D%2C%22isNewConstruction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleForeclosure%22%3A%7B%22value%22%3Afalse%7D%2C%22isComingSoon%22%3A%7B%22value%22%3Afalse%7D%2C%22isAuction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForRent%22%3A%7B%22value%22%3Atrue%7D%2C%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A15%7D&wants={%22cat1%22:[%22mapResults%22]}&requestId=2',

# Coronado
'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Coronado%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-117.31057418359376%2C%22east%22%3A-117.03042281640626%2C%22south%22%3A32.52417772524916%2C%22north%22%3A32.77624714613177%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A17587%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22isForSaleByAgent%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleByOwner%22%3A%7B%22value%22%3Afalse%7D%2C%22isNewConstruction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleForeclosure%22%3A%7B%22value%22%3Afalse%7D%2C%22isComingSoon%22%3A%7B%22value%22%3Afalse%7D%2C%22isAuction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForRent%22%3A%7B%22value%22%3Atrue%7D%2C%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D&wants={%22cat1%22:[%22mapResults%22]}&requestId=2',

# Scripps Ranch
'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Scripps%20Ranch%2C%20San%20Diego%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-117.12406034179688%2C%22east%22%3A-116.98398465820313%2C%22south%22%3A32.845706231678875%2C%22north%22%3A32.97137568711849%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A117980%2C%22regionType%22%3A8%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22isForSaleByAgent%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleByOwner%22%3A%7B%22value%22%3Afalse%7D%2C%22isNewConstruction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleForeclosure%22%3A%7B%22value%22%3Afalse%7D%2C%22isComingSoon%22%3A%7B%22value%22%3Afalse%7D%2C%22isAuction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForRent%22%3A%7B%22value%22%3Atrue%7D%2C%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A13%7D&wants={%22cat1%22:[%22mapResults%22]}&requestId=2',

# Sorrento Valley
'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Sorrento%20Valley%2C%20San%20Diego%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-117.22968742089844%2C%22east%22%3A-117.15964957910157%2C%22south%22%3A32.87249449680829%2C%22north%22%3A32.93533252578935%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A275401%2C%22regionType%22%3A8%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22isForSaleByAgent%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleByOwner%22%3A%7B%22value%22%3Afalse%7D%2C%22isNewConstruction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleForeclosure%22%3A%7B%22value%22%3Afalse%7D%2C%22isComingSoon%22%3A%7B%22value%22%3Afalse%7D%2C%22isAuction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForRent%22%3A%7B%22value%22%3Atrue%7D%2C%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A14%7D&wants={%22cat1%22:[%22mapResults%22]}&requestId=2',

# Mira Mesa
'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Mira%20Mesa%2C%20San%20Diego%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-117.17645342089844%2C%22east%22%3A-117.10641557910157%2C%22south%22%3A32.888018413356164%2C%22north%22%3A32.95084542796568%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A116625%2C%22regionType%22%3A8%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22isForSaleByAgent%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleByOwner%22%3A%7B%22value%22%3Afalse%7D%2C%22isNewConstruction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleForeclosure%22%3A%7B%22value%22%3Afalse%7D%2C%22isComingSoon%22%3A%7B%22value%22%3Afalse%7D%2C%22isAuction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForRent%22%3A%7B%22value%22%3Atrue%7D%2C%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A14%7D&wants={%22cat1%22:[%22mapResults%22]}&requestId=2',
]

headers = {
    'authority': 'www.zillow.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'dnt': '1',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}

for url in urls:
    filename = re.search('(?<=%22)(-|\w|%2[C0])+CA',url).group()+"_zillow_rent.csv"
    cleanName = re.sub('(-|%2.)+','_',filename)
    print(f'Preparing to write {cleanName}')
    response = requests.get(url,headers=headers)
    sleep(3)
    try:
        data = json.loads(response.text)
    except:
        print(response.content)
        exit()
    results = data['cat1']['searchResults']['mapResults']
    rows = []
    for home in results:
        try:
            homeType = home['hdpData']['homeInfo']['homeType']
            price = home['hdpData']['homeInfo']['price']
        except:
            continue
        detailUrl = "https://zillow.com"+home['detailUrl']
        zpid = home['zpid']
        #price = home['price'] # using instead the price from hdpData below
        #priceLabel = home['priceLabel']
        beds = home['beds']
        baths = home['baths']
        area = home['area']
        statusType = home['statusType']
        statusText = home['statusText']
        listingType = home['listingType']
        availabilityDate = home['availabilityDate']
        # homeType = home['hdpData']['homeInfo']['homeType'] 
        # image / other media
        imgSrc = home['imgSrc']
        if "google" in imgSrc:
            imgSrc = ""
        try:
            hasImage = home['hasImage']
        except:
            hasImage = ""
        hasVideo = home['hasVideo']
        variableData = home['variableData']
        # location data
        address = home['address']
        city = home['hdpData']['homeInfo']['city']
        state = home['hdpData']['homeInfo']['state']
        zipcode = home['hdpData']['homeInfo']['zipcode']
        lat = home['hdpData']['homeInfo']['latitude']
        long = home['hdpData']['homeInfo']['longitude']
        # OTHER
        #hdpData = home['hdpData'] # housing developer pro - data
        #shouldShowZestimateAsPrice = home['shouldShowZestimateAsPrice']
        #pgapt = home['pgapt']
        #sgapt = home['sgapt']
        #has3DModel = home['has3DModel']
        #isHomeRec = home['isHomeRec']
        #hasAdditionalAttributions = home['hasAdditionalAttributions']
        #dateSold = home['hdpData']['homeInfo']['dateSold']
        #daysOnZillow = home['hdpData']['homeInfo']['daysOnZillow']
        #homeStatus = home['hdpData']['homeInfo']['homeStatus']
        #homeStatusForHDP = home['hdpData']['homeInfo']['homeStatusForHDP']
        #isPreforeclosureAuction = home['hdpData']['homeInfo']['isPreforeclosureAuction']
        #price = home['hdpData']['homeInfo']['price'] # assessed first for efficiency's sake
        #priceForHDP = home['hdpData']['homeInfo']['priceForHDP']
        #zestimate = home['hdpData']['homeInfo']['zestimate']
        #rentZestimate = home['hdpData']['homeInfo']['rentZestimate']
        #taxAssessedValue = home['hdpData']['homeInfo']['taxAssessedValue']

        row = [ price, beds, baths, area, address, city, state, zipcode, lat,
                long, zpid, statusType, statusText, listingType,
                availabilityDate, homeType, detailUrl, hasVideo, hasImage,
                imgSrc, #variableData,
        ]
        rows.append(row)

    with open(cleanName+"_zillow_rent.csv",'w') as f:
        csvwriter = csv.writer(f,delimiter=",",quoting=csv.QUOTE_MINIMAL)
        topRow = [ "price", "beds", "baths", "area", "address", "city",
                "state", "zipcode", "lat", "long", "zpid", "statusType",
                "statusText", "listingType", "availabilityDate", "homeType",
                "detailUrl", "hasVideo", "hasImage", "imgSrc", #"variableData",
        ]
        csvwriter.writerow(topRow)
        for row in sorted(rows, key=lambda x: x[0]):
            csvwriter.writerow(row)
