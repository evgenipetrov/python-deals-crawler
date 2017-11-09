# -*- coding: utf-8 -*-
import re
import string

from deals_crawler.items import DealsCrawlerItem
from amazon.api import AmazonAPI
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider
from selenium import webdriver

amazon = AmazonAPI('', '', '')


def split_in_chunks(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def get_deal_info(asins):
    chunks = split_in_chunks(asins, 10)
    products = []
    for chunk in chunks:
        item_id = ','.join(chunk)
        try:
            products += amazon.lookup(ItemId=item_id)
        except:
            pass

    return products


class AmazonSpider(CrawlSpider):
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome(chrome_options=options)

    name = 'AmazonSpider'
    allowed_domains = ['amazon.com']
    start_urls = [
        'https://www.amazon.com/gp/goldbox/ref=gbps_ftr_s-3_792e_wht_468642?gb_f_GB-SUPPLE=dealStates:AVAILABLE%252CWAITLIST%252CWAITLISTFULL,enforcedCategories:468642']

    def parse(self, response):
        self.driver.get(response.url)
        deal_container_elements = self.driver.find_elements_by_xpath(
            '//div[contains (@class, "dealContainer")]/a[contains (@class, "link-normal")]')

        asins = []
        for deal_container_element in deal_container_elements:
            url = deal_container_element.get_attribute('href')
            search = re.search(r'/(B[A-Z0-9]{9})/', url)
            try:
                asin = (search.group(1))
                asins.append(asin)
            except:
                pass

        deals = get_deal_info(asins=asins)
        for deal in deals:
            item_loader = ItemLoader(item=DealsCrawlerItem(), response=response)

            deal_title = ''.join(map(str, deal.title)).strip().splitlines()
            item_loader.add_value('title', deal_title)

            deal_url = deal.offer_url
            item_loader.add_value('url', deal_url)

            deal_image = str(deal.medium_image_url)
            item_loader.add_value('image', deal_image)

            deal_listed_price = deal.list_price[0]
            item_loader.add_value('listed_price', deal_listed_price)

            deal_current_price = str(deal.formatted_price)
            item_loader.add_value('current_price', deal_current_price)

            deal_store = 'amazon'
            item_loader.add_value('store', deal_store)

            item = item_loader.load_item()
            yield item
