# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

def convert_duration_to_minutes_movies(duration):
    if 'h' in duration:
        hours, minutes = duration.split('h')
        if 'm' in minutes:
            total_minutes = int(hours) * 60 + int(minutes[:-1])
        else:
            total_minutes = int(hours) * 60
    else:
        total_minutes = int(duration.split('m')[0])
    return total_minutes

def convert_duration_to_minutes_series(duration):
    hours = 0
    minutes = 0
    for i in range(len(duration)):
        n = duration[i].strip()
        if n.isdigit():
            if i < len(duration)-1 and duration[i+1].strip() == 'hour':
                hours = int(n)
            elif i > 0 and duration[i-1].strip() == 'hour':
                continue
            else:
                minutes = int(n)
        elif n == 'hour':
            continue
        elif n == 'minutes':
            continue
        else:
            pass
    total_minutes = hours * 60 + minutes
    return total_minutes


class ImdbscraperPipeline:
    def process_item(self, item, spider):
        # adapter = ItemAdapter(item)
        spider_name = spider.name
        if spider_name == 'spidermovies':
            item['duration'] = convert_duration_to_minutes_movies(item['duration'])
        elif spider_name == 'spiderseries':
            item['duration'] = convert_duration_to_minutes_series(item['duration'])
        return item
    
