# TODO
# only for xlsx files for now

import os
import pandas as pd
import tabula as tb
import re


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


class StringParser:
    def __init__(self, input_string, num_rows, num_cols):
        self.input_string = input_string
        self.num_rows = num_rows
        self.num_cols = num_cols
        
    def extract_numerical_data(self):
        # Use regular expression to extract numerical data from string
        numerical_data = re.findall(r'\d+\.\d+|\d+', self.input_string)
        return numerical_data
        
    def fill_dataframe(self):
        # Extract numerical data from string
        numerical_data = self.extract_numerical_data()
        
        # Calculate the total number of elements needed in the dataframe
        num_elements = self.num_rows * self.num_cols
        
        # Make sure we have enough numerical data to fill the dataframe
        if len(numerical_data) < num_elements:
            raise ValueError('Not enough numerical data to fill dataframe')
        
        # Create dataframe with specified dimensions
        df = pd.DataFrame(columns=['col{}'.format(i+1) for i in range(self.num_cols)])
        
        # Fill dataframe with numerical data
        for i in range(self.num_rows):
            start = i * self.num_cols
            end = start + self.num_cols
            row_data = numerical_data[start:end]
            df.loc[i] = row_data
        
        return df


import torch
import torch.nn as nn
import pandas as pd
import re

class PDFDataOrganizer(nn.Module):
    def __init__(self, table_regex_list, num_regex_list):
        super(PDFDataOrganizer, self).__init__()
        self.table_regex_list = table_regex_list
        self.num_regex_list = num_regex_list
        
    def forward(self, input_string):
        # Split input string into lines
        lines = input_string.split('\n')
        
        # Initialize empty dataframe and numerical data dictionary
        df = pd.DataFrame()
        num_dict = {}
        
        # Process each line in the input string
        for line in lines:
            # Check if the line matches any of the table regular expressions
            for regex in self.table_regex_list:
                if re.match(regex, line):
                    # If the line matches a table regular expression, parse it into a dataframe
                    df = pd.read_csv(pd.compat.StringIO(line), delimiter='\s+')
                    
                    # Rename columns to remove any special characters or spaces
                    df.columns = [re.sub('[^0-9a-zA-Z]+', '', col) for col in df.columns]
                    
                    # Break out of the loop, since we've found a table
                    break
                    
            # If the line doesn't match a table regular expression, check if it contains numerical data
            if not df.empty:
                # If a table has already been found, associate any numerical data on this line with its context
                for regex in self.num_regex_list:
                    match = re.search(regex, line)
                    if match:
                        num = float(match.group(1))
                        context = match.group(2)
                        for col in df.columns:
                            if col.lower() in context.lower():
                                num_dict[col] = num
            else:
                # If a table hasn't been found yet, check if the line contains text data
                pass  # TODO: Implement text data parsing
            
        # Convert numerical data dictionary to pandas series and append to dataframe
        num_series = pd.Series(num_dict)
        df = df.append(num_series, ignore_index=True)
        
        return df


import torch
import torch.nn as nn
import pandas as pd
import re

import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize

class PDFOrganizer(nn.Module):
    def __init__(self, embedding_dim, hidden_dim, output_dim):
        super(PDFOrganizer, self).__init__()
        
        # Text processing layer
        self.text_embedding = nn.Embedding(num_embeddings=10000, embedding_dim=embedding_dim)
        self.text_rnn = nn.LSTM(input_size=embedding_dim, hidden_size=hidden_dim, batch_first=True)
        
        # Numerical processing layer
        self.numerical_rnn = nn.LSTM(input_size=1, hidden_size=hidden_dim, batch_first=True)
        self.numerical_output = nn.Linear(hidden_dim, output_dim)
        
        # Table processing layer
        self.table_output = nn.Linear(10, output_dim)
    
    def forward(self, input_string):
        # Preprocess input string
        numerical_data = re.findall(r'[0-9]+(?:\.[0-9]*)?', input_string)
        text_data = word_tokenize(input_string)
        table_data = pd.read_csv(r"C:\Users\vieir\OneDrive\Documentos\00_TEST\calculo diario.csv")
        
        # Associate numerical data with nearest text token
        numerical_indices = []
        for num in numerical_data:
            num_index = input_string.find(num)
            nearest_token = min(text_data, key=lambda x: abs(input_string.find(x)-num_index))
            nearest_token_index = text_data.index(nearest_token)
            numerical_indices.append((num, nearest_token_index))
        
        # Text processing
        #text_embeddings = self.text_embedding(text_data)
        input_indices_tensor = torch.tensor(text_data)
        text_embeddings = self.text_embedding(input_indices_tensor)
        _, (text_hn, _) = self.text_rnn(text_embeddings)
        text_output = text_hn.squeeze()[numerical_indices]
        
        # Numerical processing
        numerical_inputs = torch.tensor([float(num) for num in numerical_data]).unsqueeze(0)
        _, (numerical_hn, _) = self.numerical_rnn(numerical_inputs)
        numerical_output = self.numerical_output(numerical_hn.squeeze())
        
        # Table processing
        table_output = self.table_output(table_data)
        
        # Concatenate output
        output = torch.cat([text_output, numerical_output, table_output], dim=0)
        
        return output

