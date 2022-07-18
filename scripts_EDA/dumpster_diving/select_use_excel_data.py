
import xlwings as xw


def select_use_excel_data():

    df_quick = xw.load(index=False)
    return df_quick
