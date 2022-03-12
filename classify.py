import pandas as pd
from verbosing import clf_verbose

def classify(df, clf, verbose):
    if verbose:
        print(clf_verbose.get('classifying'))
    df.drop(['url_hash', 'element_class', 'element_id', 'path', 'full_path', 'is_content', 'index_path',
             'desc_h4', 'desc_h5', 'desc_h6', 'text', 'element', 'element_parent'], axis=1, inplace=True)

    predicted = clf.predict(df)

    return predicted
