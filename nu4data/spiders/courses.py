from scrapy import Spider, Request
from scrapy.http import HtmlResponse

from nu4data.items import CourseItem


class CoursesSpider(Spider):
    name = "courses"

    def start_requests(self):
        if "production" in dir(self): yield Request("https://catalogs.northwestern.edu/undergraduate/courses-az/")
        yield Request("https://catalogs.northwestern.edu/undergraduate/courses-az/arabic/", self.parse_subject_page)

    def parse(self, response: HtmlResponse):
        links = response.css(".letternav-head + ul a")

        yield from response.follow_all(links, self.parse_subject_page)

    def parse_subject_page(self, response: HtmlResponse):
        course_blocks = response.css(".courseblock")

        for course_block in course_blocks:
            raw_title = course_block.css(".courseblocktitle strong::text").get()
            (code, name, units) = self.tidy_title(raw_title)

            description = course_block.css(".courseblockdesc::text").get()

            # TODO: Parse PreReqs

            yield CourseItem(code, name, units, description)

    def tidy_title(self, raw_title: str) -> tuple[str, str, int]:
        title_words = raw_title.split()

        code = title_words[0] + " " + title_words[1]
        name = " ".join(title_words[2:-2])
        units: int
        try:
            units = int(title_words[-2][-1])
        except ValueError:
            # TODO: Log Error
            units = -1

        return (code, name, units)
