import scrapy
import os
from content_extractor.verbosing import ef_verbose
from content_extractor.constants import BOILERPLATE_STRINGS
import re


class FeatureSpider(scrapy.Spider):
    name = 'feature_spider'
    start_urls = []
    uri = 'file:///' + os.path.abspath(os.path.join('site.html'))
    start_urls.append(uri.replace('\\', '/'))

    custom_settings = {
        'LOG_LEVEL': 'DEBUG',
    }

    def __init__(self, result, url, verbose=True, **kwargs):
        super().__init__(**kwargs)
        self.result = result
        self.verbose = verbose
        self.url = url

    def parse(self, response, **kwargs):
        if self.verbose:
            print(ef_verbose.get('extracting'))
        for element in response.xpath('//*[normalize-space(text())]'):

            url_id = self.url
            text_normalized = element.xpath('normalize-space(./text())').get()
            text_length = len(text_normalized)

            # V tomto pripade pozeram parenta, lebo text je zabaleny v <span class='text_to_classify_79660'>
            element_tag = element.xpath('name(..)').get()

            if text_length == 0 or element_tag == 'script' or "<span class='text_to_classify_79660" in text_normalized:
                continue
            text_no_digits = ''.join(filter(lambda x: not x.isdigit(), text_normalized))
            text_punctuation = 1 if re.match(r'^.*[A-Za-z][.?!].*[A-Za-z]*"*$', text_no_digits) is not None else 0
            contains_word_char = 1 if re.match(r'^.*\w.*$', text_normalized) is not None else 0

            word_count = len(text_normalized.split())
            avg_sentence_len = avg_sentence_lenght(text_normalized) if text_punctuation else 0

            # Opat pozeram parenta, lebo tam su spravne tagy
            element_class = element.xpath('../@class').get()
            element_id = element.xpath('../@id').get()

            element_class_count = len(element_class.split()) if element_class is not None else 0
            element_id_count = 1 if element_id is not None else 0

            path = get_path(element)
            full_path = get_full_path(element)
            index_path = get_index_path(element)

            # o element vyssie kvoli <span>
            children_count = element.xpath('count(../text())').extract()
            siblings_count = element.xpath('count(../../text())').extract()

            href = ''
            if element_tag == 'a':
                href = element.xpath('../@href').get()

            self.result.append([
                url_id,
                0,
                text_normalized,
                text_length,
                text_punctuation,
                word_count,
                avg_sentence_len,
                element_tag,
                '' if element_class is None else element_class,
                '' if element_id is None else element_id,
                element_class_count,
                element_id_count,
                element.xpath('name(../..)').get(),  # Parent parenta lebo text je obaleny v <span>
                path,
                full_path,
                index_path,
                1 if '<nav>' in path else 0,
                1 if '<header>' in path else 0,
                1 if '<footer>' in path else 0,
                1 if '<li>' in path else 0,
                1 if '<table>' in path else 0,
                1 if '<h1>' in path else 0,
                1 if '<h2>' in path else 0,
                1 if '<h3>' in path else 0,
                1 if '<h4>' in path else 0,
                1 if '<h5>' in path else 0,
                1 if '<h6>' in path else 0,
                1 if '<a>' in path else 0,
                1 if '<title>' in path else 0,
                1 if '<article>' in path else 0,
                is_boilerplate_text(text_normalized),
                contains_word_char,
                int(path.count('<')) - 2,  # -2 lebo nepocitame <html> a <body>
                children_count[0],
                siblings_count[0],
                href
            ])


def is_boilerplate_text(text):
    if any(text.lower() == string for string in BOILERPLATE_STRINGS):
        return 1
    else:
        return 0


def avg_sentence_lenght(text):
    sentences = re.split('[.?!]', text)
    words = text.split()
    return len(words) / len(sentences)


# Reurns path to element
# e.g.: <html><body><div><ul><li><a>
def get_path(element):
    path = ''
    while element.xpath('name()').get() is not None:
        path = '<' + element.xpath('name()').get() + '>' + path
        element = element.xpath('..')

    return path[:len(path) - 6]  # removes <span> from path


# Returns path to element with class and id values
# e.g.: html[story nytapp-vi-article ] head[ ] title[ ]
def get_full_path(element):
    full_path = ''

    while element.xpath('name()').get() is not None and element.xpath('name()').get() != 'body':
        element_name = element.xpath('name()').get()
        element_class = element.xpath('@class').get()
        element_id = element.xpath('@id').get()

        current_element = element_name + '['
        if element_class is not None:
            current_element = current_element + element_class
        current_element = current_element + ' '
        if element_id is not None:
            current_element = current_element + element_id
        full_path = current_element + '] ' + full_path
        element = element.xpath('..')

    return full_path[:len(full_path) - 30]  # removes <span> from path


def get_index_path(element):
    index_path = ''
    element = element.xpath('..')  # koncovy <span> nema unique__indexm, posuvam sa teda do parenta

    while element.xpath('name()').get() is not None and element.xpath('name()').get() != 'body':
        index_path = '<' + element.xpath('@unique__index').get() + '>' + index_path
        element = element.xpath('..')

    return index_path
