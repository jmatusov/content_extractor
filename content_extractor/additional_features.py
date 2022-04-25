import pandas as pd
from content_extractor.verbosing import af_verbose
from content_extractor.constants import BOILERPLATE_CLASSES_IDS


def is_boilerplate_class_or_id(text):
    if any(string in text.lower() for string in BOILERPLATE_CLASSES_IDS):
        return 1
    else:
        return 0


def additional_features(df, verbose):
    if verbose:
        print(af_verbose.get('calculating'))

    selected_parents = ['tr', 'td', 'b', 'i', 'article', 'p', 'h1']

    df = df.join(pd.DataFrame(
        {
            'element_td': 0,
            'element_p': 0,
            'element_b': 0,
            'element_small': 0,
            'element_em': 0,
            'element_h1': 0,
            'element_cite': 0,
            'element_a': 0,
            'element_li': 0,
            'element_strong': 0,
            'element_label': 0,
            'element_span': 0,
            'element_h2': 0,
            'element_i': 0,
            'element_u': 0,
            'boilerplate_class': 0,
            'boilerplate_class_in_path': 0,
            'has_selected_parent': 0
        }, index=df.index
    ))

    list_of_elements = ['td', 'p', 'b', 'small', 'em', 'h1', 'cite', 'a', 'li', 'strong', 'label', 'span', 'h2', 'i', 'u']
    
    for index, row in df.iterrows():
        if row['element'] in list_of_elements:
            df.at[index, f'element_{row["element"]}'] = 1
        
        if row['element_parent'] in selected_parents:
            df.at[index, 'has_selected_parent'] = 1
            
        df.at[index, 'boilerplate_class'] = is_boilerplate_class_or_id(str(row['element_class']))
        df.at[index, 'boilerplate_class_in_path'] = is_boilerplate_class_or_id(str(row['full_path']))

    return df
