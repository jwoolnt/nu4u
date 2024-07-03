# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass

@dataclass
class CourseItem:
	code: str
	name: str
	units: int
	description: str
	# TODO: Add PreReqs Field
	#prereqs: None | str
