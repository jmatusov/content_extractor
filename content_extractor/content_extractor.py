from joblib import load
from content_extractor.transform_html import transform_site
from content_extractor.additional_features import additional_features
from content_extractor.classify import classify
from content_extractor.download_site import HtmlSpider
from content_extractor.extract_features import FeatureSpider
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer
import pandas as pd
from content_extractor.generate_output import generate_output
import os


class ContentExtractor:
    def __init__(self, output_type='full', clf='rfc', generate_html=True, verbose=True):
        """
        :param output_type: 'full', 'content', 'none', default='full
        :param clf: 'rfc' or 'svm', default='rfc
        :param verbose: bool, default=True
        """

        if not isinstance(output_type, str) or output_type is None:
            self.output_type = 'full'
        elif output_type == 'full':
            self.output_type = 'full'
        elif output_type == 'content':
            self.output_type = 'content'
        else:
            self.output_type = 'full'

        if clf == 'rfc':
            self.clf = load('content_extractor/my_dataset_best_random_forest_clf.joblib')
        elif clf == 'svc':
            self.clf = load('content_extractor/my_dataset_best_svm_clf.joblib')
        else:
            self.clf = load('my_dataset_best_random_forest_clf.joblib')

        if isinstance(verbose, bool):
            self.verbose = verbose
        else:
            self.verbose = True

        if generate_html is False:
            self.generate_html = False
        else:
            self.generate_html = True

    def start(self, url):
        """
        :param url: url to scrape and classify
        :return: dataframe: text + is_content + features, optionally generates output
        """
        @defer.inlineCallbacks
        def crawl():
            yield runner.crawl(HtmlSpider, url=url, verbose=self.verbose)
            transform_site(element_dic, self.verbose)
            yield runner.crawl(FeatureSpider, result=extraction_result, url=url, verbose=self.verbose)
            reactor.stop()

        @defer.inlineCallbacks
        def crawl_list():
            for u in url:
                dic = {}
                yield runner.crawl(HtmlSpider, url=u, verbose=self.verbose)
                transform_site(dic, self.verbose)
                element_dics[u] = dic
                yield runner.crawl(FeatureSpider, result=extraction_result, url=u, verbose=self.verbose)
            reactor.stop()

        if not (isinstance(url, str) or isinstance(url, list)):
            raise ValueError('url not of type string or list')

        element_dic = {}
        element_dics = {}
        extraction_result = []

        runner = CrawlerRunner()

        if isinstance(url, str):
            crawl()
        elif isinstance(url, list):
            crawl_list()

        reactor.run()

        features = pd.DataFrame(extraction_result,
                                columns=['url_hash', 'is_content', 'text', 'text_length', 'text_punctuation',
                                         'word_count', 'avg_sentence_len', 'element', 'element_class',
                                         'element_id', 'element_class_count', 'element_id_count',
                                         'element_parent', 'path', 'full_path', 'index_path', 'desc_nav:',
                                         'desc_header', 'desc_footer', 'desc_li', 'desc_table', 'desc_h1', 'desc_h2',
                                         'desc_h3', 'desc_h4', 'desc_h5', 'desc_h6', 'desc_a', 'desc_title',
                                         'desc_article', 'boilerplate_text', 'contains_word_char', 'element_depth',
                                         'children_count', 'siblings_count', 'href'])

        features = additional_features(features, self.verbose)

        predicted = classify(features.copy(), self.clf, self.verbose)
        features['is_content'] = predicted

        if self.generate_html and isinstance(url, str):
            generate_output(features, element_dic, self.verbose)

        if self.generate_html and isinstance(url, list):
            dfs = [group for _, group in features.groupby('url_hash')]
            for df in dfs:
                generate_output(df, element_dics.get(df['url_hash'].iloc[0]), self.verbose)

        try:
            if os.path.exists('site.html'):
                os.remove('site.html')
        except FileNotFoundError as e:
            pass

        if self.output_type == 'full':
            return features
        else:
            return features.loc[features['is_content'] == 1]

# src:
# https://doc.scrapy.org/en/latest/topics/practices.html#running-multiple-spiders-in-the-same-process
# https://stackoverflow.com/questions/68969814/loop-through-pandas-dataframe-and-split-into-multiple-dataframes-based-on-unique
