from bs4 import BeautifulSoup, Comment, Doctype
import re
from verbosing import th_verbose


def transform_site(verbose):
    if verbose:
        print(th_verbose.get('transforming'))

    try:
        with open('site.html', encoding="utf-8") as raw_html_file:
            soup = BeautifulSoup(raw_html_file, 'html.parser')

        for tag in soup.select('script'):
            tag.decompose()

        for node in soup.find_all(text=lambda text: isinstance(text, Comment)):
            node.extract()

        for item in soup.contents:
            if isinstance(item, Doctype):
                item.extract()

        for node in soup.find_all(text=lambda x: x.strip()):
            node.replace_with("<span class='text_to_classify_79660''>{}</span>".format(node))

        for i, element in enumerate(soup.find_all()):
            element['unique__index'] = i

        soup_string = str(soup)
        soup_string = re.sub("&lt;span class='text_to_classify_79660''&gt;",
                             "<span class='text_to_classify_79660'>",
                             soup_string)
        soup_string = re.sub("&lt;/span&gt;", "</span>",
                             soup_string)

        with open('site.html', "w", encoding='utf-8') as edited_html_file:
            edited_html_file.write(soup_string)
    except Exception as e:
        if verbose:
            print(e)

# Sources:
# https://stackoverflow.com/questions/28208123/remove-unnecessary-tag-content-from-html-source-using-scrapy
# https://stackoverflow.com/questions/23299557/beautiful-soup-4-remove-comment-tag-and-its-content
# https://stackoverflow.com/questions/47172262/strip-doctype-from-html-using-beautifulsoup4
# https://stackoverflow.com/questions/30302956/edit-text-from-html-with-beautifulsoup
