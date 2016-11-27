from lxml import html
from config import with_proxy
from config import dont_save_data
from config import dont_download_data
from products import product_dict
import requests
import datetime
import pickle
import time
import random

requests.packages.urllib3.disable_warnings()


# tandetny scraper do cen z morele.net
#
#
#   ,--.*,--.
#  /         \  /\
# |           |/  \
#  \         //___/'-._
#   '.__.__,'      "._/
#
#   apricot-scraper by mkierc

# todo: obsluga bledow http
# todo: wysylanie powiadomienia w przypadku bledu

class Scraper:
    def main(self):
        current_date = datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')
        input_dict = self.get_current_datafile()

        print 'previous datafile: ' + str(input_dict)

        # get new prices
        current_prices = {}
        for item in product_dict:
            key = item
            value = self.get_price(product_dict.get(item))
            current_prices.update({key: value})

        print 'new data: ' + str(current_prices)

        # add new prices to the dictionary
        input_dict.update({current_date: current_prices})

        print 'new datafile: ' + str(input_dict)
        if not dont_save_data:
            self.write_datafile(input_dict)

    # element to "scrape" the price off of ;)
    #  <span style="color:inherit;font-size:inherit;"
    #   property="gr:hasCurrencyValue"
    #   datatype="xsd:float"
    #   itemprop="price"
    #   content="1859.00">
    #       1859,00
    # </span>
    @staticmethod
    def get_price(url):
        if not dont_download_data:
            # timeout to avoid cloudflare from banning the scrapers ip
            time.sleep(random.randint(1, 4))
            proxies = {}
            if with_proxy:
                proxies = {
                    'http': 'http://192.168.132.10:8080',
                    'https': 'http://192.168.132.10:8080',
                }
            page = requests.get(url, proxies=proxies)
            tree = html.fromstring(page.content)
            price = tree.xpath('//div[@itemprop="price"]/@content')
            return float(price[0])
        else:
            return round(random.uniform(2000, 6000), 2)

    # read data from datafile.raw
    @staticmethod
    def get_current_datafile():
        with open(name='datafile.raw', mode='r') as input_handle:
            input_dict = pickle.loads(input_handle.read())
        return input_dict

    # write data to datafile.raw
    @staticmethod
    def write_datafile(new_dict):
        with open(name='datafile.raw', mode='w') as output_handle:
            pickle.dump(new_dict, output_handle)


Scraper().main()
