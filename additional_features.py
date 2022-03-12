import pandas as pd
from verbosing import af_verbose
from constants import BOILERPLATE_CLASSES_IDS


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

    for index, row in df.iterrows():
        match row['element']:
            case 'td':
                df.at[index, 'element_td'] = 1
            case 'p':
                df.at[index, 'element_p'] = 1
            case 'b':
                df.at[index, 'element_b'] = 1
            case 'small':
                df.at[index, 'element_small'] = 1
            case 'em':
                df.at[index, 'element_em'] = 1
            case 'h1':
                df.at[index, 'element_h1'] = 1
            case 'cite':
                df.at[index, 'element_cite'] = 1
            case 'a':
                df.at[index, 'element_a'] = 1
            case 'li':
                df.at[index, 'element_li'] = 1
            case 'strong':
                df.at[index, 'element_strong'] = 1
            case 'label':
                df.at[index, 'element_label'] = 1
            case 'span':
                df.at[index, 'element_span'] = 1
            case 'h2':
                df.at[index, 'element_h2'] = 1
            case 'i':
                df.at[index, 'element_i'] = 1
            case 'u':
                df.at[index, 'element_u'] = 1
        if row['element_parent'] in selected_parents:
            df.at[index, 'has_selected_parent'] = 1
        df.at[index, 'boilerplate_class'] = is_boilerplate_class_or_id(str(row['element_class']))
        df.at[index, 'boilerplate_class_in_path'] = is_boilerplate_class_or_id(str(row['full_path']))

    return df
