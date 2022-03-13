from content_extractor import ContentExtractor

extractor = ContentExtractor(verbose=True, output_type='content')
# extractor.start(url='https://screenrant.com/murder-mystery-2-perfect-adam-sandler/')
extractor.start(url='https://www.aktuality.sk/clanok/rj8g26g/milujete-prirodu-a-zelenu-farbu-tento-rok-vam'
                    '-interierove-trendy-ulahodia-ako-nikdy/')
# extractor.start(url='https://edition.cnn.com/2022/03/12/europe/ukraine-invasion-friends-family-separated-cmd-intl'
#                     '/index.html')

print()
