import pandas as pd


def mergeManualCollections(paths):
    cols = ['document_id', 'name_comp', 'company_id', 'who', 'year', 'mda_begin', 'mda_end', 'fs_begin', 'fs_end', 'audit_begin', 'audit_end', 'href_doc']
    out = []
    
    for path in paths:
        temp = pd.read_csv(path)
        if 'index' in temp.columns:
            # if there is an 'index' columns, this means the sheet contains
            # some non-SRN docs that do not have a document_id
            # which means we have to build it
            idxs = temp[temp.document_id.isna()].index
            temp.loc[idxs, 'document_id'] = [f"{compid}_{year}" for compid, year in zip(temp.loc[idxs]['company_id'], temp.loc[idxs]['year'])]
        
        temp.set_index('document_id', inplace=True)
        temp.drop(columns=temp.columns.difference(cols), inplace=True)
        out.append(temp)
    
    out_df = pd.concat(out)
    
    return out_df


# manual_collections.to_json('manual_collections.json')


# # LMU Cologne documents
# docs_lmucgn = pd.read_csv('../../data/connectivity-manual_collection - lmu_cologne - 20230926.csv', index='index')
# docs_lmucgn = docs_lmucgn[['document_id', 'name_comp', 'year', 'mda_begin', 'mda_end', 'fs_begin', 'fs_end', 'audit_begin', 'audit_end', 'href_doc']]
# docs_lmucgn['uni'] = 'lmucgn'

# # Different stages for IESE documents
# docs_iese_main = pd.read_csv('data/connectivity-manual_collection-iese - main - 20230926.csv')
# docs_iese_second_round = pd.read_csv('data/connectivity-manual_collection-iese - main - 20230926.csv')

# docs_iese = docs_iese[['document_id', 'name_comp', 'year', 'mda_begin', 'mda_end', 'fs_begin', 'fs_end', 'audit_begin', 'audit_end', 'href_doc']]
# docs_iese['uni'] = 'iese'




# # Merge together and save as cleaned data
# handCodedSections = pd.concat([docs_iese, docs_lmucgn], ignore_index=True)
# handCodedSections.to_parquet('handCodedSections.parquet.gzip', compression='gzip')