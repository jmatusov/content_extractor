from verbosing import ge_verbose
import pandas as pd
import re
from time import time


def generate_output(df, dic, output_type, verbose):
    if output_type == 'full':
        if verbose:
            print(ge_verbose.get('full'))
        generate_full_output(df)
    else:
        if verbose:
            print(ge_verbose.get('content'))
        generate_content_output(df, dic)


def generate_full_output(data):
    data.to_csv('result.csv')


def generate_content_output(data, dic):
    data = data.loc[data['is_content'] == 1]
    assert len(data) > 0, ge_verbose.get('assert')

    data.to_csv('result.csv')

    print(ge_verbose.get('process'))

    data = data[['text', 'index_path', 'href']]
    data = data.join(pd.DataFrame(
        {
            'checked': 0,
            'group_id': '',
            'tags': ''
        }, index=data.index
    ))

    for i, row in data.iterrows():
        parent_index_path = row['index_path']
        depth = row['index_path'].count('<')
        parent_tag = row['index_path'].rsplit('<', 1)[1]
        parent_tag = parent_tag.replace('>', '')

        for j, row2 in data.iterrows():
            if i == j or row2['checked'] == 1:
                continue
            if parent_index_path in row2['index_path']:
                # element sme este nepriradili do skupiny
                if row2['checked'] == 0:
                    add_to_group(data, i, j, parent_index_path, parent_tag, row2)
                # element bol priradeny, ale nasiel sa lepsi parent
                if row2['checked'] == 1 and row2['index_path'].count('<') > depth:
                    add_to_group(data, i, j, parent_index_path, parent_tag, row2)
                # element uz ma optimalneho parenta
                if row2['checked'] == 1 and row2['index_path'].count('<') <= depth:
                    continue

    # nechecknute data priradi do vlastnej skupiny
    # posledny element v index_path prida to tags
    data.loc[data['checked'] == 0, 'group_id'] = data['index_path']
    data.loc[data['checked'] == 0, 'tags'] =\
        data['index_path'].str.rsplit('<', 1).str[-1].str.replace('>', '').str.split()

    for i, row in data.iterrows():
        prepend = ''
        append = ''

        # skip parent
        if len(row['tags']) == 1:
            continue

        for j, tag in enumerate(row['tags']):
            # skip parent tag
            if j == 0:
                continue
            if dic.get(tag) == 'a':
                prepend += f'<{dic.get(tag)} href="{row["href"]}">'
                append += f'</{dic.get(tag)}>'
            else:
                prepend += f'<{dic.get(tag)}>'
                append += f'</{dic.get(tag)}>'

        data.at[i, 'text'] = prepend + data.at[i, 'text'] + append
        data.at[i, 'tags'] = row['tags'][0].split()

    data['concat_text'] = data.groupby(['group_id'])['text'].transform(lambda x: ' '.join(x))
    data['tags'] = data['tags'].str[0]
    data = data[['tags', 'concat_text', 'href']].drop_duplicates('tags')

    for i, row in data.iterrows():
        prepend = ''
        append = ''

        if dic.get(row["tags"]) == 'a':
            prepend += f'<{dic.get(row["tags"])} href="{row["href"]}">'
            append += f'</{dic.get(row["tags"])}>'
        else:
            prepend += f'<{dic.get(row["tags"])}>'
            append += f'</{dic.get(row["tags"])}>'

        data.at[i, 'concat_text'] = prepend + data.at[i, 'concat_text'] + append

    filename = f'{round(time() * 1000)}.html'
    f = open(filename, 'a', encoding='utf-8')
    f.write("<body><font face='verdana'>")
    f.close()

    for index, row in data.iterrows():
        f = open(filename, 'a', encoding='utf-8')
        f.write(row['concat_text'])
        f.close()

    f = open(filename, 'a', encoding='utf-8')
    f.write('</font></body>')
    f.close()


def add_to_group(data, i, j, parent_index_path, parent_tag, row2):
    additional_elements = re.findall(r'<([0-9]+)>', row2['index_path'].rsplit(parent_tag + '>', 1)[1])
    additional_elements.insert(0, parent_tag)
    data.at[i, 'checked'] = 1
    data.at[i, 'group_id'] = parent_index_path
    data.at[i, 'tags'] = [parent_tag]
    data.at[j, 'checked'] = 1
    data.at[j, 'group_id'] = parent_index_path
    data.at[j, 'tags'] = additional_elements

# Sources
# https://stackoverflow.com/questions/27298178/concatenate-strings-from-several-rows-using-pandas-groupby
# https://stackoverflow.com/questions/33620132/write-each-row-of-pandas-dataframe-into-a-new-text-file-pythonic-way
