import pandas as pd

def updateRawTexts(raw_texts_old, raw_texts_newDict):
    """
    Somewhat lengthy function (rather a script) to update the raw_text.json based
    on the new entries. Somehow, just concatenating the two dfs did not work, therefore
    the loop.
    
    """
    
    raw_texts_new = pd.DataFrame(
        index  = raw_texts_newDict.keys(),
        data   = raw_texts_newDict.values(), 
        columns= ['raw_text', 'status']
    )
    
    raw_texts_merged = raw_texts_new.merge(
        raw_texts_old, 
        how='outer',
        left_index=True, right_index=True, 
        indicator=True, 
        suffixes=('_new', '_old')
    ).query('_merge != "right_only"')
    
    raw_texts_final = pd.DataFrame(columns=['document_id', 'raw_text', 'status'])

    for idx, row in raw_texts_merged[raw_texts_merged['status_new'] == "exists"].iterrows():
        raw_texts_final.loc[len(raw_texts_final)] = [idx, row.raw_text_old, row.status_old]

    for idx, row in raw_texts_merged[raw_texts_merged['status_new'] == "fine"].iterrows():
        raw_texts_final.loc[len(raw_texts_final)] = [idx, row.raw_text_new, row.status_new]

    for idx, row in raw_texts_merged[raw_texts_merged['status_new'].str.startswith('problem_')].iterrows():
        raw_texts_final.loc[len(raw_texts_final)] = [idx, None, row.status_new]

    raw_texts_final.set_index('document_id', inplace=True)
    
    return raw_texts_final
    