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
            # TODO: prereqs_selector = ".courseblockextra.noindent"

            loader.add_css("code", title_selector)
            loader.add_css("name", title_selector)
            loader.add_css("units", title_selector)
            loader.add_css("description", description_selector)
            # TODO: loader.add_css("prereqs", prereqs_selector)
            yield loader.load_item()
