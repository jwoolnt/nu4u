from re import sub

from scrapy import Spider, Request, Selector
from scrapy.http import HtmlResponse

from nu4data.items import CourseItem, PreReqs


class CoursesSpider(Spider):
    name = "courses"

    def start_requests(self):
        if "production" in dir(self): yield Request("https://catalogs.northwestern.edu/undergraduate/courses-az/")
        yield Request("https://catalogs.northwestern.edu/undergraduate/courses-az/afst/", self.parse_subject_page)

    def parse(self, response: HtmlResponse):
        links = response.css(".letternav-head + ul a")

        yield from response.follow_all(links, self.parse_subject_page)

    def parse_subject_page(self, response: HtmlResponse):
        course_blocks = response.css(".courseblock")

        for course_block in course_blocks:
            (code, name, units) = self.parse_title(course_block)
            description = course_block.css(".courseblockdesc::text").get()
            prereqs = self.parse_prereqs(course_block)

            yield CourseItem(code, name, units, description, prereqs)

    def parse_title(self, course_block: Selector) -> tuple[str, str, int]:
        words = course_block.css("strong::text").get().split()

        code = words[0] + " " + words[1]
        name = " ".join(words[2:-2])
        units: int
        try:
            units = int(words[-2][-1])
        except ValueError as error:
            self.logger.error(error)
            units = -1

        return (code, name, units)

    def parse_prereqs(self, course_block: Selector) -> PreReqs:
        html = course_block.css(".courseblockextra").get()
        if html is None or "Prerequisite" not in html: return None

        tidy_text = sub("<[^>]*>", "", html).strip()
        tidy_text = sub("\s", " ", tidy_text)
        tidy_text = tidy_text.removeprefix("Prerequisite: ")

        return tidy_text
