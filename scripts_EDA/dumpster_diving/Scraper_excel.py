# TODO
# only for xlsx files for now
# give

import os
import pandas as pd


class Scraper:
    # template for getting RAW excel data in a folder
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

        return df_file

    def iterator(self):

        df_file = [None] * len(self.files)

        for i, file in enumerate(self.files):
            df_file[i] = {
                'book_name': file,
                'Data': self.return_dataframe(file)
                }

        return df_file
