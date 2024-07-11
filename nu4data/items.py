from typing import Optional

from scrapy import Item, Field


class CoursesItem(Item):
	code: str = Field()
	name: str = Field()
	units: int = Field()
	description: str = Field()
	prereqs: Optional[str] = Field()
