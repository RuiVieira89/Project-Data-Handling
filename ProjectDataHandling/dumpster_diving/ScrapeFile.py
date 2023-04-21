# TODO
# only for xlsx files for now

import os
import pandas as pd
import tabula as tb


class Scraper:
    # template for getting RAW data in a folder
    # 0th level folder only

    def __init__(self, proj_dir, key_word, file_type):
        # Arguments:
        #
        # key_word - last characters before extension

        self.proj_dir = proj_dir
        self.file_type = file_type

        files_dir = os.listdir(proj_dir)
        self.files = [i for i in files_dir if i.endswith(key_word + file_type)]

        # return files

    def return_dataframe(self, file):
        # this return 1 data frame
        # loop with this func

        file_dir = os.path.join(self.proj_dir, file)

        if self.file_type == '.xlsx':
            xlsx_file = pd.ExcelFile(file_dir)
            df_file = pd.read_excel(xlsx_file, engine='openpyxl',
                                    index_col=None, sheet_name=None,
                                    header=None)

        elif  self.file_type == '.pdf':
            try:
                df_file = tb.read_pdf(
                    file_dir, pages = 'all',
                    #area = (0, 0, 900, 900), 
                    #columns = [0, 0, 900, 900], 
                    #pandas_options={'header': None}, 
                    #stream=True
                    )[0]
            except Exception: # [] empty, so del [0]
                df_file = tb.read_pdf(
                    file_dir, pages = 'all',
                    #area = (0, 0, 900, 900), 
                    #columns = [0, 0, 900, 900], 
                    #pandas_options={'header': None}, 
                    #stream=True
                    )

        return df_file
    
    def clean_nan_rows(self, files):
        for file in files:
            for book_name in file['Data']:
                #file['Data'][book_name]
            
                print(f'{book_name} NAs Before: {file["Data"][book_name].isna().sum().sum()}')
                
                # Drops an entire axis of NaN
                file['Data'][book_name].dropna(axis=0, how='all', thresh=None, 
                                    subset=None, inplace=True)
                file['Data'][book_name].dropna(axis=1, how='all', thresh=None, 
                                    subset=None, inplace=True)
                
                print(f'{book_name} NAs After: {file["Data"][book_name].isna().sum().sum()}')
                
        return files

    def iterator(self, clean_na=True):

        df_file = [None] * len(self.files)

        for i, file in enumerate(self.files):
            df_file[i] = {
                'book_name': file,
                'Data': self.return_dataframe(file)
                }
        
        if clean_na:
            df_file = self.clean_nan_rows(df_file)
        
        return df_file


from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import pandas as pd

class PDFScraper:
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file
        self.data = []
    
    def extract_text(self):
        with open(self.pdf_file, 'rb') as f:
            parser = PDFParser(f)
            doc = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            retstr = StringIO()
            device = TextConverter(rsrcmgr, retstr, laparams=LAParams())
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)
            text = retstr.getvalue()
            self.data = text
    
    def to_dataframe(self):
        lines = self.data.strip().split('\n') 
        df = pd.DataFrame([line.split('\t') for line in lines])
        self.data = df

    def output_values(self):
        return self.data


def get_elements_before_key(arr, key, n_elements=10):
    # find all indices of key in array
    indices = [i for i, x in enumerate(arr) if x == key]
    if len(indices) == 0:
        print(f"{key} not found in array.")
        return None
    
    # get data for each index
    data = []
    for i in indices:
        data.append(arr[max(0, i-n_elements):i])
    
    # create dataframe with one column per index
    cols = [f"Data_{i}" for i in range(len(indices))]
    df = pd.DataFrame(data, columns=cols)
    
    return df


""""
# Implementation example

PATH = r'C:\Users\vieir\OneDrive\Documentos\00_TEST\calculo diario.pdf'
#PATH = r"C:\Users\vieir\Downloads\9020587665.PDF"

scraper = PDFScraper(PATH)
scraper.extract_text()
data_array = scraper.output_values()

print("End")

""""