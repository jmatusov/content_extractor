import scrapy
from content_extractor.verbosing import ds_verbose


class HtmlSpider(scrapy.Spider):
    name = 'html_spider'

    custom_settings = {
        'LOG_LEVEL': 'DEBUG',
    }

    def __init__(self, url, verbose=True, **kwargs):
        self.start_urls = [url]
        self.verbose = verbose
        super().__init__(**kwargs)

    def parse(self, response, **kwargs):
        if self.verbose:
            print(ds_verbose.get('downloading'))
        try:
            with open('site.html', 'w', encoding="utf-8") as html_file:
                html_file.write(response.text)
                assert response.text is not None, ds_verbose.get('assert')
        except Exception as e:
            print(e)
