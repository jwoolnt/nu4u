from itemloaders.processors import MapCompose, TakeFirst
from scrapy.loader import ItemLoader

from nu4data.items import CoursesItem


def clean_html_text(text: str) -> str:
	from re import sub

	clean_text = sub("<[^>]*>", "", text).strip()
	clean_text = sub("\s", " ", clean_text)

	return clean_text


class CoursesLoader(ItemLoader):
	default_item_class = CoursesItem
	default_input_processor = MapCompose(clean_html_text)
	default_output_processor = TakeFirst()
