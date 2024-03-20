# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

def convert_duration_to_minutes(duration_text):
    if 'h' in duration_text:
        hours, minutes = duration_text.split('h')
        if 'm' in minutes:
            total_minutes = int(hours) * 60 + int(minutes[:-1])
        else:
            total_minutes = int(hours) * 60
    else:
        total_minutes = int(duration_text.split('m')[0])
    return total_minutes

class ImdbscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        duration_text = item['duration']
        total_minutes = convert_duration_to_minutes(duration_text)
        item['duration'] = total_minutes
        return item
    
