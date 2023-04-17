# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join

from w3lib.html import remove_tags
import re


def remove_quotaions(value: str):
    return value.replace(u"\u201d", '').replace(u"\u201c", '')


def strip_value(value):
    return value.strip()


def remove_icons(value):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', value).strip()


class AliAbdallItem(scrapy.Item):
    article_body = scrapy.Field(
        input_processor=MapCompose(remove_icons, remove_tags, strip_value, remove_quotaions),
        output_processor=TakeFirst()
    )
    article_name = scrapy.Field(
        input_processor=MapCompose(remove_tags, strip_value, remove_quotaions),
        output_processor=TakeFirst()
    )

    category = scrapy.Field(
        input_processor=MapCompose(remove_icons, remove_tags, remove_quotaions),
        output_processor=Join(',')
    )

    link = scrapy.Field()
