from scrapy import Item, Field


class CoursesItem(Item):
	code: str = Field()
	name: str = Field()
	units: int = Field()
	description: str = Field()
	# TODO: prereqs: Optional[str] = Field()
