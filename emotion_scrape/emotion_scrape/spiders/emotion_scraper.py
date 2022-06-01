import re

import nltk
import scrapy
from nrclex import NRCLex

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


class EmotionScraperSpider(scrapy.Spider):
    name = 'emotion_scraper'

    def __init__(self, *args, **kwargs):
        super(EmotionScraperSpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs.get('start_urls')]

    def parse(self, response):
        print('something is here')

        title = response.xpath('//div[@id="top-col-story"]//h1/text()').get()
        title = self.removeCharacters(title)
        emotion = NRCLex(title)
        if (len(emotion.affect_dict) == 0):
            pass
        else:
            yield {
                'sentence': title.strip(),
                "detection": {"score": emotion.top_emotions, "word_list": emotion.affect_dict}
            }

        subtitle = response.xpath('//div[@id="top-col-story"]//h2/text()').get()
        subtitle = self.removeCharacters(subtitle)
        emotion = NRCLex(subtitle)
        if (len(emotion.affect_dict) == 0):
            pass
        else:
            yield {
                'sentence': subtitle.strip(),
                "detection": {"score": emotion.top_emotions, "word_list": emotion.affect_dict}
            }

        mainDiv = response.xpath('//div[@id="main-col"]')
        descriptions = [' '.join(line.strip() for line in p.xpath('.//text()').extract() if line.strip()) for p in
                        mainDiv.xpath('.//p')]
        descriptions = re.split(r'(?<=\w\.)\s', descriptions[0])
        descriptions = self.removeCharacters(descriptions)
        for sentence in descriptions:
            sentence = self.removeCharacters(sentence)
            emotion = NRCLex(sentence)
            if (len(emotion.affect_dict) == 0):
                pass
            else:
                yield {
                    'sentence': sentence.strip(),
                    "detection": {"score": emotion.top_emotions, "word_list": emotion.affect_dict}
                }

        otherTopics = response.xpath('//ul[@class="stories"]//div[@class="top-col-story"]')
        response.xpath('//div[@id="main-col"]//p//text()').extract()

        for i in range(1, len(otherTopics)):
            headLineDiv = f'(//ul[@class="stories"]//div[@class="top-col-story"]//div[@class="headline"]//text())[{i}]'
            subheadLineDiv = f'(//ul[@class="stories"]//div[@class="top-col-story"]//div[@class="standfirst"]//text())[{i}]'
            paragraphDiv = f'(//ul[@class="stories"]//li)[{i}]//div[@class="body"]//p//text()'

            headline = response.xpath(headLineDiv).get()
            headline = self.removeCharacters(headline)
            emotion = NRCLex(headline)
            if (len(emotion.affect_dict) == 0):
                pass
            else:
                yield {
                    'sentence': headline.strip(),
                    "detection": {"score": emotion.top_emotions, "word_list": emotion.affect_dict}
                }

            subheadline = response.xpath(subheadLineDiv).get()
            subheadline = self.removeCharacters(subheadline)
            emotion = NRCLex(subheadline)
            if (len(emotion.affect_dict) == 0):
                pass
            else:
                yield {
                    'sentence': subheadline.strip(),
                    "detection": {"score": emotion.top_emotions, "word_list": emotion.affect_dict}
                }

            paragraph = response.xpath(paragraphDiv).extract()
            paragraph = [' '.join(line.strip() for line in paragraph if line.strip())]
            paragraph = re.split(r'(?<=\w\.)\s', paragraph[0])
            paragraph = self.removeCharacters(paragraph)

            for sentence in paragraph:
                sentence = self.removeCharacters(sentence)
                emotion = NRCLex(sentence)
                if (len(emotion.affect_dict) == 0):
                    pass
                else:
                    yield {
                        'sentence': sentence.strip(),
                        "detection": {"score": emotion.top_emotions, "word_list": emotion.affect_dict}
                    }

    def removeCharacters(self, sentence):
        if '\\' in sentence:
            sentence = sentence.replace('\\', '')

        elif '\"' in sentence:
            sentence = sentence.replace('\"', '')

        return sentence

    def detectEmotion(self, sentence):
        emotion = NRCLex(sentence)
        if (len(emotion.affect_dict) == 0):
            pass
        else:
            yield {
                'sentence': sentence,
                "detection": {"score": emotion.top_emotions, "word_list": emotion.affect_dict}
            }
