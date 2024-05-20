
import chardet

import pandas as pd


class Get_csv_file:

    def __init__(self, PATH):
        
        self.PATH = PATH
        print(f'{PATH}')
        
    def find_encoding(self, fname):
        r_file = open(fname, 'rb').read()
        result = chardet.detect(r_file)
        charenc = result['encoding']
        return charenc

    def get_data(self):
        my_encoding = self.find_encoding(self.PATH)
        self.df = pd.read_csv(self.PATH, encoding=my_encoding)


