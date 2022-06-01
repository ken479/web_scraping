import argparse
import os
from scrapy.cmdline import execute

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
            'sentence.csv'
        ]
    )
except SystemExit:
    pass