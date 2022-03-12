from joblib import load
from transform_html import transform_site
from additional_features import additional_features
from classify import classify
from download_site import HtmlSpider
from extract_features import FeatureSpider
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer
import pandas as pd
from verbosing import ce_verbose
from generate_output import generate_output


class ContentExtractor:
    def __init__(self, output_type='full', clf='rfc', verbose=True):
        """
        :param output_type: 'full', 'content', 'none', default='full
        :param clf: 'rfc' or 'svm', default='rfc
        :param verbose: bool, default=True
        """
        self.url = None

        if not isinstance(output_type, str) or output_type is None:
            self.output_type = 'full'
        elif output_type == 'full':
            self.output_type = 'full'
        elif output_type == 'content':
            self.output_type = 'content'
        elif output_type == 'none':
            self.output_type = 'none'
        else:
            self.output_type = 'full'

        if clf == 'rfc':
            self.clf = load('my_dataset_best_random_forest_clf.joblib')
        elif clf == 'svc':
            self.clf = load('my_dataset_best_svm_clf.joblib')
        else:
            self.clf = load('my_dataset_best_random_forest_clf.joblib')

        if isinstance(verbose, bool):
            self.verbose = verbose
        else:
            self.verbose = True

    def start(self, url):
        """
        :param url: url to scrape and classify
        :return: classified text + features, optionally generates output
        """
        @defer.inlineCallbacks
        def crawl():
            yield runner.crawl(HtmlSpider, url=self.url, verbose=self.verbose)
            transform_site(self.verbose)
            yield runner.crawl(FeatureSpider, result=extraction_result, verbose=self.verbose)
            reactor.stop()

        if isinstance(url, str) and url is not None:
            self.url = url
        else:
            raise AttributeError('url is not type str or is None')

        extraction_result = []
        runner = CrawlerRunner()
        crawl()
        reactor.run()

        assert len(extraction_result) > 0, ce_verbose.get('assert')

        features = pd.DataFrame(extraction_result,
                                columns=['url_hash', 'is_content', 'text', 'text_length', 'text_punctuation',
                                         'word_count', 'avg_sentence_len', 'element', 'element_class',
                                         'element_id', 'element_class_count', 'element_id_count',
                                         'element_parent', 'path', 'full_path', 'index_path', 'desc_nav:',
                                         'desc_header', 'desc_footer', 'desc_li', 'desc_table', 'desc_h1', 'desc_h2',
                                         'desc_h3', 'desc_h4', 'desc_h5', 'desc_h6', 'desc_a', 'desc_title',
                                         'desc_article', 'boilerplate_text', 'contains_word_char', 'element_depth',
                                         'children_count', 'siblings_count'])

        features = additional_features(features, self.verbose)

        predicted = classify(features.copy(), self.clf, self.verbose)
        features['is_content'] = predicted

        if self.verbose != 'none':
            generate_output(features, self.output_type, self.verbose)

        return features

        # TODO verbose
        # TODO save output
        # TODO spojit do odseku
        # TODO pre <a> tahat href
