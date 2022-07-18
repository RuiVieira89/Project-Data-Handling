# openpyxl
# install openpyxl-image-loader
# interesting repo https://github.com/Sven-Bo?tab=repositories

# get the data
# organize it
# return

import os
import pandas as pd
import numpy as np

from openpyxl_image_loader import SheetImageLoader

from Scraper_excel import Scraper
from Cluster import Cluster

import matplotlib.pyplot as plt


dir_path = "C:\\Users\\RVI4590\\Toyota Motor Europe\\099E_Engine - Documents\\19_TMMP-SUPPORT\\Oil level gage - Difficult to insert into guide"
dir_path = 'C:\\Users\\RVI4590\\Toyota Motor Europe\\099E_Engine - Documents\\10_VE VA activity\\2021_VA_activity\\Working-files\\Individual-items\\GPF Hose\\Tape-localise\\1_ECI RELEASE'

dir_path = 'C:\\Users\\vieir\\OneDrive - DEM.UMINHO.PT\\00_RESEARCH TEG\\1_Paper João oliveira'

PROJ_DIR = dir_path
KEY_WORD = ''
FILE_TYPE = '.xlsx'

# gets raw data
raw_data = Scraper(PROJ_DIR, KEY_WORD, FILE_TYPE).iterator()

print('clean data')

books = raw_data


def count_nan_str_num(truth_table):
    # returns the number of elements that are:
    # [#NaN, #strings, #numbers]

    if len(truth_table) == 0:
        return

    column_type = []

    for column in truth_table.columns:
        nanCounter = 0
        trueCounter = 0
        falseCounter = 0

        for element in truth_table.index:
            if pd.isnull(truth_table[column][element]):
                nanCounter = nanCounter + 1
            if truth_table[column][element]:
                trueCounter = trueCounter + 1
            if not truth_table[column][element]:
                falseCounter = falseCounter + 1

        column_type.append([nanCounter, trueCounter, falseCounter])
    return column_type  # [#NaN, #strings, #numbers]

# Remove useless characters
# Extract relevant content from a Series
# Check NaN values
# Change the type of your Series

# spec_chars = ["!",'"',"#","%","&","'","(",")",
#               "*","+",",","-",".","/",":",";","<",
#               "=",">","?","@","[","\\","]","^","_",
#               "`","{","|","}","~","–"]
# for char in spec_chars:
#     df['title'] = df['title'].str.replace(char, ' ')

# with column type and truth table -> ID labels and features


for book in books:

    for sheet in book['Data']:
        # book['Data'][sheet] #  individual raw data
        # check for strings
        string_truth_table = book['Data'][sheet].applymap(
            lambda x: int(1) if type(x) == str else int(0), na_action='ignore'
            ).fillna(value=int(2), method=None, inplace=False).astype(int)
        column_type = count_nan_str_num(string_truth_table)
        np.argmax(column_type, axis=1)

        print('here')

        if len(string_truth_table) < 100:
            # list of point [xpos, ypos, type of data]
            string_truth_table_for_cluster = np.zeros([
                string_truth_table.shape[0]*string_truth_table.shape[1], 3
                ])
            pos = 0
            for index in string_truth_table.index:
                for column in string_truth_table.columns:
                    string_truth_table_for_cluster[pos] = [
                        column, index, string_truth_table[column][index]
                        ]
                    pos = pos + 1

            db_cluster = Cluster(string_truth_table_for_cluster
                                 ).cluster_OPTICS(plot=True)

            exit(0)

# gess labeling
#   - just title on top
#   - just title on side
#   - title on top and side

# df.columns
# df.index

# 'book_name': file,
# 'Data': self.return_dataframe(file)

exit(0)

files = os.listdir(PROJ_DIR)
files = [i for i in files if i.endswith(KEY_WORD + FILE_TYPE)]

df = pd.DataFrame([])
df_file = [None] * len(files)
i = 0
for file in files:
    file_dir = os.path.join(PROJ_DIR, file)

    #xls = xlrd.open_workbook(file_dir, on_demand=True)
    #print(xls.sheet_names()) # <- remeber: xlrd sheet_names is a function, not a property

    xls_file = pd.ExcelFile(file_dir)
    df_file[i] = pd.read_excel(xls_file, engine='openpyxl',index_col=None)
    i = i + 1

df = pd.concat(df_file)

df.columns


def convertXLS2CSV(aFile):
    '''converts a MS Excel file to csv w/ the same name in the same directory'''

    import win32com.client, os
    from win32com.client import constants as c
    excel = win32com.client.Dispatch('Excel.Application')

    fileDir, fileName = os.path.split(aFile)
    nameOnly = os.path.splitext(fileName)
    newName = nameOnly[0] + ".csv"
    outCSV = os.path.join(fileDir, newName)
    workbook = excel.Workbooks.Open(aFile)
    workbook.SaveAs(outCSV, c.xlCSVMSDOS) # 24 represents xlCSVMSDOS
    workbook.Close(False)
    excel.Quit()
    del excel
