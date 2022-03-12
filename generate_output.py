from verbosing import ge_verbose
import pandas as pd


def generate_output(df, output_type, verbose):
    if output_type == 'full':
        if verbose:
            print(ge_verbose.get('full'))
        generate_full_output(df)
    else:
        if verbose:
            print(ge_verbose.get('content'))
        generate_content_output(df)


def generate_full_output(data):
    data.to_csv('result.csv')


def generate_content_output(data):
    data = data.loc[data['is_content'] == 1]
    assert len(data) > 0, ge_verbose.get('assert')

    data.to_csv('result.csv')

    print(ge_verbose.get('process'))

    data = data[['text', 'index_path']]
    data = data.join(pd.DataFrame(
        {
            'checked': 0,
            'group_id': '',
        }, index=data.index
    ))

    for i, row in data.iterrows():
        parent_index_path = row['index_path']

        for j, row2 in data.iterrows():
            if i == j or row2['checked'] == 1:
                continue
            if parent_index_path in row2['index_path']:
                data.at[j, 'checked'] = 1
                data.at[j, 'group_id'] = parent_index_path

                data.at[i, 'checked'] = 1
                data.at[i, 'group_id'] = parent_index_path

    data.loc[data['checked'] == 0, 'group_id'] = data['index_path']
    breakpoint()