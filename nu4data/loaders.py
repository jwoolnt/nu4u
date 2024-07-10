from typing import Optional

from itemloaders.processors import MapCompose, TakeFirst
from scrapy.loader import ItemLoader

from nu4data.items import CoursesItem


def clean_html_text(text: str):
	from re import sub

	clean_text = sub("<[^>]*>", "", text).strip()
	clean_text = sub("\s", " ", clean_text)

	return clean_text


def extract_words(
		text: str,
		i: int,
		j: Optional[int] = None,
		/,
		start_left: bool = True,
		one_word: bool = False,
		separator: str = " "
):
	words = text.split()

	if one_word: return words[i]

	selected_words: list[str]
	if j is None:
		selected_words = words[:i] if start_left else words[i:]
	else:
		selected_words = words[i:j] if start_left else words[j:i]

	return separator.join(selected_words)


class CoursesLoader(ItemLoader):
	default_item_class = CoursesItem
	default_input_processor = MapCompose(clean_html_text)
	default_output_processor = TakeFirst()

	code_in = MapCompose(lambda text: extract_words(text, 2))
	name_in = MapCompose(lambda text: extract_words(text, 2, -2))
	units_in = MapCompose(lambda text: extract_words(text, -2, one_word=True)[-1])
