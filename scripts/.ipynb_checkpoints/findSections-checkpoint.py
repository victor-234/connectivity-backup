import numpy as np

def mergePages(raw_text, start, end):
    out = ""
    out_dict = {}
    page_length = 0
    if ("," not in str(start)) & ("," not in str(end)):
        page_length = int(end) - int(start)
        for page in raw_text.keys():
            if (int(page) >= int(start)) & (int(page) <= int(end)):
                out += raw_text[page] + " "
                out_dict[page] = raw_text[page]
    else:
        for startMult, endMult in zip(start.split(','), end.split(',')):
            page_length += int(endMult) - int(startMult) 
            for page in raw_text.keys():
                if (int(page) >= int(startMult)) & (int(page) <= int(endMult)):
                    out += raw_text[page] + " "
                    out_dict[page] = raw_text[page]
            
    return out, out_dict, page_length


def mergeOtherPages(doc):
    out = ""
    out_dict = {}
    if True not in [(',' in str(x)) for x in np.array([doc.mda_begin, doc.mda_end, doc.fs_begin, doc.fs_end, doc.audit_begin, doc.audit_end])]:
        for page in doc.clean_text_dict.keys():
            if (int(page) not in range(int(doc.mda_begin), int(doc.mda_end)+1)) & (int(page) not in range(int(doc.fs_begin), int(doc.fs_end)+1)) & (int(page) not in range(int(doc.audit_begin), int(doc.audit_end)+1)):
                out += doc.clean_text_dict[page] + " "
                out_dict[page] = doc.clean_text_dict[page]
                
    else:
        all_pages = set(range(1,int(doc.n_pages)))
        excl_pages = []
        
        pages = [(doc.mda_begin, doc.mda_end), (doc.fs_begin, doc.fs_end), (doc.audit_begin, doc.audit_end)]
        for elem in pages:
            if ("," not in str(elem[0])):
                excl_pages.append(elem)
            else:
                for startMult, endMult in zip(elem[0].split(','), elem[1].split(',')):
                    excl_pages.append((float(startMult), float(endMult)))

        excl_pages_set = set()
        for r1, r2 in excl_pages:
            excl_pages_set.update(set(range(int(r1), int(r2)+1)))

        other_pages = sorted(all_pages.difference(excl_pages_set))
        
        for page in doc.clean_text_dict.keys():
            if page in other_pages:
                out += doc.clean_text_dict[page] + " "

    return out, out_dict


def findSections(docs):
    """
    Merges the pages text of the three sections together to make it searchable.
    Returns an amended docs DF
    
    """
    
    unzipped_mda                = [mergePages(r,s,e) for r,s,e in zip(docs.clean_text_dict, docs.mda_begin, docs.mda_end)]
    threelists_mda              = [[i for i,j,k in unzipped_mda], [j for i,j,k in unzipped_mda], [k for i,j,k in unzipped_mda]]
    docs.loc[:, 'mda_text']     = threelists_mda[0]
    docs.loc[:, 'mda_text_dict']= threelists_mda[1]
    docs.loc[:, 'mda_length']   = threelists_mda[2]

    unzipped_fs                 = [mergePages(r,s,e) for r,s,e in zip(docs.clean_text_dict, docs.fs_begin, docs.fs_end)]
    threelists_fs               = [[i for i,j,k in unzipped_fs], [j for i,j,k in unzipped_fs], [k for i,j,k in unzipped_fs]]
    docs.loc[:, 'fs_text']      = threelists_fs[0]
    docs.loc[:, 'fs_text_dict'] = threelists_fs[1]
    docs.loc[:, 'fs_length']    = threelists_fs[2]

    unzipped_audit                 = [mergePages(r,s,e) for r,s,e in zip(docs.clean_text_dict, docs.audit_begin, docs.audit_end)]
    threelists_audit               = [[i for i,j,k in unzipped_audit], [j for i,j,k in unzipped_audit], [k for i,j,k in unzipped_audit]]
    docs.loc[:, 'audit_text']      = threelists_audit[0]
    docs.loc[:, 'audit_text_dict'] = threelists_audit[1]
    docs.loc[:, 'audit_length']    = threelists_audit[2]

    unzipped_other                  = [mergeOtherPages(doc) for _,doc in docs.iterrows()]
    twolists_other                  = [[i for i,j in unzipped_other], [j for i,j in unzipped_other]]
    docs.loc[:, 'other_text']       = twolists_other[0]
    docs.loc[:, 'other_text_dict']  = twolists_other[1]
    #docs['other_length'] = docs['n_pages'] - docs['mda_length'] - docs['fs_length'] - docs['audit_length']
    
    return docs