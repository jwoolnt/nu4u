import scrapy


class CoursesSpider(scrapy.Spider):
    name = "courses"
    start_urls = ["https://catalogs.northwestern.edu/undergraduate/courses-az/"]

    def parse(self, response):
        links = response.css(".letternav-head + ul a")
        yield from response.follow_all(links, self.parse_courses)

    def parse_courses(self, response):
        course_blocks = response.css(".courseblock")
        for course_block in course_blocks:
            raw_title = course_block.css(".courseblocktitle strong::text").get()
            if raw_title is None: continue
            tidy_title = raw_title.replace("\xa0", " ").strip()

            yield {
                "title": tidy_title,
                "description": course_block.css(".courseblockdesc::text").get()
            }
