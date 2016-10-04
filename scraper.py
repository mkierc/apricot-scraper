from lxml import html
import requests
import datetime
requests.packages.urllib3.disable_warnings()


class Scraper:
    def main(self):
        date = datetime.datetime.now()
        slownik = self.get_slownik()
        print date.strftime('%Y.%m.%d')
        for item in slownik:
            cena = self.get_cena(slownik.get(item))
            print '\t%s:\t%s' % (item, cena)


    # element do podp*dolenia: cena
    #  <span style="color:inherit;font-size:inherit;"
    #   property="gr:hasCurrencyValue"
    #   datatype="xsd:float"
    #   itemprop="price"
    #   content="1859.00">
    #       1859,00
    # </span>
    @staticmethod
    def get_cena(adres_strony):
        page = requests.get(adres_strony)
        tree = html.fromstring(page.content)
        cena = tree.xpath('//span[@itemprop="price"]/text()')
        return cena[0]


    # slownik produktow do podp*dolenia:
    @staticmethod
    def get_slownik():
        slownik = {
            'GTX 1080': 'https://www.morele.net/karta-graficzna-gigabyte-geforce-cuda-gtx1080-xtreme-8gb-gddr5-256-bit-dvi-hdmi-3xdp-gv-n1080xtreme-w-8gd-987876/',
            'GTX 980TI': 'https://www.morele.net/karta-graficzna-msi-geforce-gtx-980ti-6gb-gddr5-384-bit-3x-dp-hdmi-dvi-i-gtx980ti-6gd5-v1-754511/'
        }
        return slownik


Scraper().main()
