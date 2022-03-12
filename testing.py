from content_extractor import ContentExtractor

extractor = ContentExtractor(verbose=True, output_type='content')
extractor.start(url='https://screenrant.com/murder-mystery-2-perfect-adam-sandler/')
print()
