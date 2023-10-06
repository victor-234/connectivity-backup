import pandas as pd

def cleanText(raw_text):
    out = raw_text.replace("-\n", "").replace("\n", " ").replace("\t", " ").replace("  ", " "
    ).replace("ˇ", "").replace("†", "").replace("˙", "").replace("ˆ", "").replace("˘", "").replace("˜", "").replace("˚", ""
    ).replace("‡", "").replace("ƒ", "").replace("⁄", "").replace("˛", "").replace("‰", "").replace("˝", "").replace("“", ""
    ).replace("ž", "").replace("š", "").replace("¢", "").replace("ł", "").replace("ÿ", "").replace("•", "").replace("’", ""
    ).replace("œ", "").replace("ﬂ", "").replace("–", "").replace("™", "").replace("ﬁ", "").replace("ı", "").replace("›", ""
    ).replace("‹", "").replace("€", "").replace("−", "").replace("¥", "").replace("—", "").replace("…", "").replace("‘", ""
    ).replace("„", "").replace("”", "").replace("‚", "").replace("£", "").replace("¤", "").replace("¦", "").replace("¬", ""
    ).replace("¡", "").replace("§", "").replace("¨", "").replace("ª", "").replace("©", "").replace("¿", "").replace("±", ""
    ).replace("º", "").replace("´", "").replace("®", "").replace("°", "").replace("¸", "").replace("¶", "").replace("î", ""
    ).replace("ã", "").replace("æ", "").replace("ì", "").replace("µ", "").replace("ò", "").replace("ð", "").replace("·", ""
    ).replace("«", "").replace("ç", "").replace("á", "").replace("»", "").replace("¯", "").replace("ó", "").replace("ô", ""
    ).replace("í", "").replace("è", "").replace("½", "").replace("ë", "").replace("å", "").replace("¹", "").replace("²", ""
    ).replace("³", "").replace("¼", "").replace("-", "").replace("¾", "").replace("â", "").replace("û", "").replace("ý", ""
    ).replace("ê", "").replace("ï", "").replace("à", "").replace("×", "").replace("_", "").replace("..", "").replace("++", ""
    ).replace("|", "").replace("//", "").replace("\\", "").replace("--", "").replace("#", "").replace("&", "").replace("*", ""
    ).replace("!", "").replace("=", "").replace(">", "").replace("@", "").replace("?", "").replace("œ", "").replace("œ", ""
    ).lower().strip()
    
    return out


def updateAndCleanText(docs_cleaned_old, raw_texts_final):
    
    docs_cleaned_new = pd.DataFrame(columns=['document_id', 'status', 'n_pages', 'clean_text_dict', 'clean_text_full', 'clean_text_pageLims', 'clean_text_len', 'contains_text', 'avgCleanTextPerPage'])
    
    for document_id, row in raw_texts_final.iterrows():
        if (document_id not in docs_cleaned_old.index) and (row.status == "fine"):
            n_pages = len(row.raw_text.keys())
            clean_text_dict = {}
            clean_text_full = ""
            clean_text_pageLims = []
            
            for page in row.raw_text.keys():
                clean = cleanText(row.raw_text[page])
                clean_text_dict[page] = clean
                clean_text_full      += clean
                clean_text_pageLims.append(len(clean))
                
            docs_cleaned_new.loc[len(docs_cleaned_new)] = [
                document_id,
                row.status,
                n_pages,
                clean_text_dict,
                clean_text_full,
                clean_text_pageLims,
                len(clean_text_full),
                clean_text_full.find(""),
                len(clean_text_full) / n_pages
            ]
        
        elif (document_id in docs_cleaned_old.index) and (docs_cleaned_old.loc[document_id].status == "fine"):
                docs_cleaned_new.loc[len(docs_cleaned_new)] = [
                document_id,
                docs_cleaned_old.loc[document_id].status,
                docs_cleaned_old.loc[document_id].n_pages,
                docs_cleaned_old.loc[document_id].clean_text_dict,
                docs_cleaned_old.loc[document_id].clean_text_full,
                docs_cleaned_old.loc[document_id].clean_text_pageLims,
                len(docs_cleaned_old.loc[document_id].clean_text_full),
                docs_cleaned_old.loc[document_id].clean_text_full.find(""),
                len(docs_cleaned_old.loc[document_id].clean_text_full) / docs_cleaned_old.loc[document_id].n_pages]
            
        else:
            docs_cleaned_new.loc[len(docs_cleaned_new)] = [document_id, None, None, None, None, None, None, None, None]

    docs_cleaned_new['clean_text_pageLimsCum'] = [pd.Series(docs_cleaned_new.loc[idx].clean_text_pageLims).cumsum().values for idx in docs_cleaned_new.index]
    docs_cleaned_new.set_index('document_id', inplace=True)
            
    return docs_cleaned_new