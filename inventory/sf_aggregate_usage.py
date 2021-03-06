#from .models import Inventory
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
import xlrd
import os
import platform
import datetime
import glob
import pandas as pd
import numpy as np


def aggregate_current_month_usage():
    df_result = read_excel_for_current_usage()
    excel_result = 'Current_Usage' + '.xlsx'
    df_result.to_excel(excel_result, index=False)


def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.
    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True
    except ValueError:
        return False


def convert_string_to_date(date_string):
    for date_format in ('%Y-%m-%d %H:%M:%S', '%d-%m-%Y', '%d.%m.%Y', '%Y.%m.%d', '%d.%m.%y', '%d/%m/%Y', '%d/%m/%Y %H:%M:%S'):
        try:
            return datetime.datetime.strptime(date_string, date_format)
        except ValueError:
            #print(date_string)
            pass
    raise ValueError('no valid date format found')


# add file_path parm
def convert_excel_date(excel_book, excel_date, file_path):
    ms_bbd_date_number = excel_date
    # Modified on 28/10/2020
    try:
        year, month, day, hour, minute, second = xlrd.xldate_as_tuple(ms_bbd_date_number, excel_book.datemode)
        py_date = datetime.datetime(year, month, day, hour, minute, second)
        return py_date
    except ValueError:
        print (file_path)
        


def read_excel_for_current_usage():
    if platform.system() == 'Linux':
        os.chdir('/home/siwanpark/ExcelData/Alex/')
    else:
        os.chdir(r"\\192.168.20.50\AlexServer\SD共有\ボタニーパレット\SF_Usage")

    input_files = set(glob.glob('*.xls*'))
    result_file = set(glob.glob('*Current*.xls*'))
    excel_files = list(input_files - result_file)
    all_df = pd.DataFrame()
    for excel_file in excel_files:
        file_name = excel_file.split('.')[0]
        temp_df, update_date = generate_data_frame_for_current_usage(excel_file)  #generate data frame
        df = generate_current_usage(temp_df, file_name, update_date)
        all_df = pd.concat([all_df, df], ignore_index=True)
        #print('{} - {}'.format(excel_file, len(df)))

    last_entry = { 'id' : '', 'update_date' : 'end', 'product_type' : '', 'sf_code' : '', 'inward' : '',
                'origin' : '', 'product_name' : '', 'product_name_jp' : '', 'move' : '', 'unit' : '',
                'pickup_qty' : '', 'memo' : '', 'bbd' : ''}
    df_last_entry = pd.DataFrame(last_entry, index=[0])
    
    all_df = pd.concat([all_df, df_last_entry], ignore_index=True)
    return all_df


def generate_data_frame_for_current_usage(file_path):
    loc = (file_path)
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    update_date = sheet.cell_value(1, 9).split(':')[1]

    update_date = update_date.strip()

    #for i in range(3, sheet.nrows):
    stock_list = []
    i = 4
    while sheet.cell(i, 1).value != 'end':
        # Convert excel date to python date
        if sheet.cell(i, 5).ctype == 3 or sheet.cell(i, 5).ctype == 2:
            inward_date = convert_excel_date(wb, sheet.cell(i, 5).value, file_path).date()
        elif sheet.cell(i, 5).ctype == 0:
            inward_date = datetime.datetime.strptime('01/01/2020', "%d/%m/%Y").date()
        elif sheet.cell(i, 5).ctype == 1:
            inward_date = datetime.datetime.strptime('01/01/2020', "%d/%m/%Y").date()
        else:
            inward_date = datetime.datetime.strptime('01/01/2020', "%d/%m/%Y").date()
        # Convert excel date to python date
        if sheet.cell(i, 18).ctype == 3 or sheet.cell(i, 18).ctype == 2:
            bbd_date = convert_excel_date(wb, sheet.cell(i, 18).value, file_path).date()
        elif sheet.cell(i, 18).ctype == 0:
            bbd_date = inward_date
        elif sheet.cell(i, 18).ctype == 1:
            if sheet.cell(i, 18).value == '-':
                bbd_date = datetime.datetime.strptime('31/12/2099', "%d/%m/%Y").date()
            elif sheet.cell(i, 18).value == 'Check BBD':
                one_year = datetime.timedelta(weeks=52)
                bbd_date = inward_date + one_year
            else:
                one_year = datetime.timedelta(weeks=52)
                bbd_date = inward_date + one_year

        stock_data = {'code' : sheet.cell(i, 4).value, 'origin' : sheet.cell(i, 0).value, 'Inward' : inward_date, 'Movement' : sheet.cell(i, 8).value,
                      'ITEM1' : sheet.cell(i, 9).value, 'ITEM2' : sheet.cell(i, 10).value, 'PreviousBalance' : sheet.cell(i, 12).value,
                      'unit': sheet.cell(i, 13).value, 'pickup' : sheet.cell(i, 14).value, 'NewBalance' : sheet.cell(i, 15).value,
                      'pmemo' : sheet.cell(i, 17).value, 'bbd' : bbd_date }
        stock_list.append(stock_data)
        i += 1
        
    result = pd.DataFrame(stock_list)
    return result, update_date


def generate_current_usage(df, file_name, update_date):
    df['code'].replace('', np.nan, inplace=True)
    df['pickup'].replace('', np.nan, inplace=True)
    df['pmemo'].replace('', np.nan, inplace=True)
    #df.to_csv('test1.csv')pd.concat([all_df, df], ignore_index=True)
    df.dropna(subset=['code', 'pickup', 'pmemo'], how='any', inplace=True)
    #df.to_csv('test2.csv')
    df_preprocessed = df[['code', 'origin', 'Movement', 'ITEM1', 'ITEM2', 'unit', 'pickup', 'pmemo', 'bbd', 'Inward']]
    df_preprocessed['update_date'] = pd.to_datetime(update_date, format='%d/%m/%Y').date()

    if ('Freezer' in file_name or 'Lucky' in file_name or 'OSP' in file_name or 'SR' in file_name or 'KKS' in file_name or 'Daily' in file_name):
        df_preprocessed['product_type'] = 'FRZ'
    else:
        df_preprocessed['product_type'] = 'DRY'

    df_preprocessed['id'] = ''
    df_preprocessed['unit'] = df_preprocessed['unit'].str.lower()
    df_preprocessed = df_preprocessed.reset_index()

    df_preprocessed_usage = df_preprocessed

    data = { 'id' : df_preprocessed_usage['id'], 'update_date' : df_preprocessed_usage['update_date'],
                'product_type' : df_preprocessed_usage['product_type'], 'sf_code' : df_preprocessed_usage['code'], 'inward' : df_preprocessed_usage['Inward'],
                'origin' : df_preprocessed['origin'], 'product_name' : df_preprocessed_usage['ITEM1'], 'product_name_jp' : df_preprocessed['ITEM2'],
                'move' : df_preprocessed_usage['Movement'], 'unit' : df_preprocessed_usage['unit'],
                'pickup_qty' : df_preprocessed_usage['pickup'], 'memo' : df_preprocessed_usage['pmemo'], 'bbd' : df_preprocessed_usage['bbd']}
    df_processed = pd.DataFrame(data)    
    return df_processed

