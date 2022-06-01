import argparse
import os
from scrapy.cmdline import execute
import uuid

parser = argparse.ArgumentParser(description='Web scrapping for sentences with emotions')
parser.add_argument('--input', required=True)
arg = parser.parse_args()
os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    execute(
        [
            'scrapy',
            'runspider',
            '-a',
            'start_urls=' + arg.input,
            'spiders/emotion_scraper.py',
            '-o',
            'output/sentence_' + str(uuid.uuid4()) +  '.csv'
        ]
    )
except SystemExit:
    pass