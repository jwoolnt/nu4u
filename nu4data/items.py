# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass

type PreReqs = None | str

@dataclass
class CourseItem:
	code: str
	name: str
	units: int
	description: str
	prereqs: PreReqs
