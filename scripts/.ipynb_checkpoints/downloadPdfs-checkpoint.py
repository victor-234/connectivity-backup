import requests, os

def downloadPdfs(BASE_PATH, to_download):
    """
    Examines already existing documents at BASE_PATH and 
    downloads the list of 'to_download' Pdfs.
        - to_download: zipped list of hrefs and document_ids
    
    """
    DOC_PATH = BASE_PATH + "/pdf/"
    
    doc_statusi = []
    docs_here = [x[:36] for x in os.listdir(DOC_PATH)]
       
    for href, document_id in to_download:
        if document_id not in docs_here:
            try:
                with open(f"{DOC_PATH}{document_id}.pdf", 'wb') as f:
                    f.write(requests.get(href).content)
                doc_status = 'downloaded'
            except:
                doc_status = 'no download'

        else:
            doc_status = 'exists'
        
        doc_statusi.append(doc_status)
    
    return doc_statusi
            
    