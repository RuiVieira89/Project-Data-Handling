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
            
                print(f'{book_name} Before: {file["Data"][book_name].isna().sum().sum()}')
                
                # Drops an entire axis of NaN
                file['Data'][book_name].dropna(axis=0, how='all', thresh=None, 
                                    subset=None, inplace=True)
                file['Data'][book_name].dropna(axis=1, how='all', thresh=None, 
                                    subset=None, inplace=True)
                
                print(f'{book_name} After: {file["Data"][book_name].isna().sum().sum()}')
                
        return files

    def iterator(self):

        df_file = [None] * len(self.files)

        for i, file in enumerate(self.files):
            df_file[i] = {
                'book_name': file,
                'Data': self.return_dataframe(file)
                }
        
        df_file_data = self.clean_nan_rows(df_file)

        return df_file_data
