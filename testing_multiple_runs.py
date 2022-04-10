from content_extractor.content_extractor import ContentExtractor
from multiprocessing import Process, Manager


def f(url, e, ns):
    ns.df = e.start(url)


def run_extractor(url, e, ns):
    p = Process(target=f, args=(url, e, ns,))
    p.start()
    p.join()


if __name__ == "__main__":
    url_list = [
        'https://screenrant.com/murder-mystery-2-perfect-adam-sandler/',
        'https://www.aktuality.sk/clanok/rj8g26g/milujete-prirodu-a-zelenu-farbu-tento-rok-vam',
        'https://edition.cnn.com/2022/03/12/europe/ukraine-invasion-friends-family-separated-cmd-intl/index.html'
    ]

    url = 'https://screenrant.com/murder-mystery-2-perfect-adam-sandler/'

    extractor = ContentExtractor(output_type='content', clf='rfc', generate_html=True, verbose=True)

    manager = Manager()
    namespace = manager.Namespace()

    run_extractor(url, extractor, namespace)
    r1 = namespace.df
    run_extractor(url_list, extractor, namespace)
    r2 = namespace.df

    breakpoint()

# src:
# https://stackoverflow.com/questions/41495052/scrapy-reactor-not-restartable
# https://stackoverflow.com/questions/22487296/multiprocessing-in-python-sharing-large-object-e-g-pandas-dataframe-between
