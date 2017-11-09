# -*- coding: utf-8 -*-

import logging

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker

from db.connection import Deals, db_connect, create_deals_table

logger = logging.getLogger(__name__)


class DealsCrawlerPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_deals_table(engine=engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        deal = Deals(**item)
        deal_in_db = session.query(Deals).filter_by(url=deal.url).first()
        if deal_in_db is None:
            try:
                session.add(deal)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()
        else:
            logger.info("<-------------------------------------------->")
            logger.info(deal_in_db.title)
            logger.info("<---------ALREADY IN ------------------------->")
        return item
