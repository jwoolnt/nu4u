from itemadapter import ItemAdapter


class CoursesPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        return item
