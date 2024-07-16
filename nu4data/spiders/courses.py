from typing import Iterable
from scrapy import Spider, Request
from scrapy.http import HtmlResponse

from nu4data.loaders import CoursesLoader


class CoursesSpider(Spider):
    name = "courses"
    # start_urls = [
    #     "https://catalogs.northwestern.edu/undergraduate/courses-az/",
    # ]

    def start_requests(self) -> Iterable[Request]:
        yield Request("https://catalogs.northwestern.edu/undergraduate/courses-az/afst/", self.parse_subject_page)

    def parse(self, response: HtmlResponse):
        yield from response.follow_all(
            response.css(".letternav-head + * a"),
            self.parse_subject_page
        )

    def parse_subject_page(self, response: HtmlResponse):
        for course_block_selector in response.css(".courseblock"):
            loader = CoursesLoader(selector=course_block_selector)

            title_selector = "strong::text"
            description_selector = ".courseblockdesc"
            prereqs_selector = ".courseblockextra.noindent"
            # TODO: ".courseblockextra:not(.noindent)"

            loader.add_css("code", title_selector, re=r"[A-Z_]+\s\d+(?:-(?:\d|[A-Z]{2}))*")
            loader.add_css("name", title_selector, re=r"(?:(?<=-\d\s)|(?<=-[A-Z]{2}\s)).+(?=\s\()")
            loader.add_css("units", title_selector, re=r"(?<=\()\d+(?:\.\d+)?(?:-\d+(?:\.\d+)?)?(?=\s)")
            loader.add_css("description", description_selector)
            loader.add_css("requirements", prereqs_selector, re=r"(?<=Prerequisite:\s).+") # TODO: Is this regex necessary?
            yield loader.load_item()
