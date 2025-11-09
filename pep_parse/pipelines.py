import csv
import datetime
import os

from collections import defaultdict


class PepParsePipeline:
    def __init__(self):
        self.status_count = defaultdict(int)
        self.total_count = 0

    def open_spider(self, spider):
        feeds_config = spider.settings.get('FEEDS', {})
        if feeds_config:
            first_feed_uri = list(feeds_config.keys())[0]
            self.results_dir = os.path.dirname(first_feed_uri)
        else:
            self.results_dir = 'results'
        os.makedirs(self.results_dir, exist_ok=True)

    def process_item(self, item, spider):
        status = item.get('status', 'Unknown')
        self.status_count[status] += 1
        self.total_count += 1
        return item

    def close_spider(self, spider):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(
            self.results_dir, f'status_summary_{current_time}.csv')
        self.write_status_summary(filename)

    def write_status_summary(self, filename):
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Статус', 'Количество'])
            for status, count in self.status_count.items():
                writer.writerow([status, count])
            writer.writerow(['Total', self.total_count])
