import re, json, os
import PyPDF2, pikepdf

def readTextFromPdf(BASE_PATH, doc_id):
    """
    Tries to read the raw text from BASE_PATH based on doc_id as the identying
    information for the file. 
    Returns:
        - raw text: text per page in a dictionary format: {page number: raw_text}
        - doc_status: info about success of reading
    
    """
    
    DOC_PATH         = BASE_PATH + "/pdf/"
    DOC_PATH_DECRYPT = BASE_PATH + "/pdf-decrypt/"
    
    raw_path = f"{DOC_PATH}{doc_id}.pdf"
    dcr_path = f"{DOC_PATH_DECRYPT}{doc_id}.pdf"
    
    raw_texts = {}
    page_num = 0
    doc_status = "exists"
    
    if not os.path.exists(dcr_path):
        try:
            pdf = pikepdf.open(raw_path)
            pdf.save(dcr_path)
            doc_status = "fine"
        except:
            #print(f"Problem with decrypting {doc_id}")
            doc_status = "problem_decrypting"
        
            return raw_texts, doc_status

        try:
            with open(dcr_path, "rb") as pdfFileObj:
                pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

                while page_num < pdfReader.numPages: 
                    page_obj = pdfReader.getPage(page_num)

                    try:
                        text = page_obj.extractText()
                        raw_texts[page_num] = text
                    except:
                        raw_texts[page_num] = ''
                        #print(f"Problem reading {doc_id} on page {page_num}")

                    page_num += 1
        except:
            #print(f"Problem with opening {doc_id}")
            doc_status = "problem_opening"
            
    return raw_texts, doc_status