from django.shortcuts import render
#from .models import Inventory
from dateutil.parser import parse
import xlrd 
import os
import datetime
import glob
import pandas as pd
import numpy as np
from django.http import HttpResponse


# Create your views here.
def home(request):    
    return render(request, 'inventory/home.html')


def stock(request):
    #jobs = Job.objects
    #return render(request, 'inventory/home.html', {'jobs': jobs})
    form_parms = request.GET
    location = form_parms['location']
    code = form_parms['code']
    product_name = form_parms['product_name']
    pallet = form_parms['pallet']
    print(location)
    df_result, pallet_qty = read_excel(location, code, product_name, pallet)            
    
    #return HttpResponse(df_result.to_html())
    return render(request, 'inventory/stock.html', {'df_result': df_result, 'pallet_qty' : pallet_qty} )


def tf_stock(request):
    tf_code_list = ['TF01B', 'CLV06', 'TF77', 'TF74', 'TF15', 'BEC03', 'BEC02', 'TFB2A', 'TFB25',
                 'TFB26', 'TFS01', 'TF34C', 'RUM05', 'TF83', 'TF83A', 'TF83B', 'TF83D', 'TF83E',
                 'TF83G', 'TF97', 'TF98', 'TF88', 'TF66Material', 'TF100', 'OCP69', 'ZN07',
                 'TF61', 'TF102', 'CFS01', 'CFS02', 'TF103', 'TF104']
    df_result = read_excel_for_tfstock(tf_code_list)
    return render(request, 'inventory/tf_stock.html', {'df_result': df_result} )


def daily_stock(request):    
    df_result = read_excel_for_daily_stock()
    print(df_result)
    os.chdir('/home/siwanpark/ExcelData/')
    excel_result = 'Daily_Stock_' + str(datetime.date.today()) + '.xlsx'
    df_result.to_excel(excel_result)
    return render(request, 'inventory/daily_stock.html', {'df_result': df_result} )



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


def convert_excel_date(excel_book, excel_date):
    ms_bbd_date_number = excel_date
    year, month, day, hour, minute, second = xlrd.xldate_as_tuple(ms_bbd_date_number, excel_book.datemode)
    py_date = datetime.datetime(year, month, day, hour, minute, second)
    return py_date


def read_excel_for_tfstock(code_list):
    #os.chdir(r"\\192.168.20.50\AlexServer\SD共有\ボタニーパレット\Siwan\StockFiles")
             
    os.chdir('/home/siwanpark/ExcelData/Alex/')
    excel_files = glob.glob('*.xls*')
    all_df = pd.DataFrame()
    selected_df = pd.DataFrame()
    for excel_file in excel_files:
        # Give the location of the file 
        #file_path = "Alex 2019 09 AUG D12-14.xlsm"
        #print(excel_file)
        file_name = excel_file.split('.')[0]
        df = generate_data_frame(excel_file, file_name)  #generate data frame
        # calculate number of pallets
        all_df = pd.concat([all_df, df], ignore_index=True)
        #os.chdir('/home/siwanpark/ExcelData/Alex/')
    
    all_df['unit'] = all_df['unit'].str.upper()
    for code in code_list:
        temp_df = all_df[['location', 'code', 'ITEM1', 'unit', 'NewBalance']]
        temp_df = temp_df[temp_df['code'].str.upper() == code.upper()]
        
        temp_df = temp_df.groupby(['location', 'code', 'ITEM1', 'unit']).agg('sum').reset_index()
        
        selected_df = pd.concat([selected_df, temp_df], ignore_index=True)
   
    #all_df = all_df.reset_index()
    #all_df.drop(axis=1, inplace=True)    
    #sselected_df = selected_df.groupby([ 'location', 'code', 'unit']).agg('sum')
    #print(selected_df)
    return selected_df


def read_excel_for_daily_stock():
    os.chdir('/home/siwanpark/ExcelData/Alex/')
    excel_files = glob.glob('Daily*.xls*')
    all_df = pd.DataFrame()
    result_df = pd.DataFrame()

    for excel_file in excel_files:
        #print(excel_file)
        file_name = excel_file.split('.')[0]
        df = generate_data_frame(excel_file, file_name)  #generate data frame        
        all_df = pd.concat([all_df, df], ignore_index=True)        
    
    all_df['unit'] = all_df['unit'].str.upper()    
    temp_df = all_df[['location', 'code', 'ITEM1', 'unit', 'NewBalance']]    
    result_df = temp_df.groupby(['code', 'ITEM1', 'unit']).agg('sum').reset_index()    
        
    print(result_df)
    return result_df



def read_excel(location, code, product_name, pallet):
    # Change directory
    #os.chdir(r"\\192.168.20.50\AlexServer\SD共有\ボタニーパレット\Siwan\StockFiles")
             
    os.chdir('/home/siwanpark/ExcelData/Alex/')
    excel_files = glob.glob('*.xls*')
    all_df = pd.DataFrame()
    for excel_file in excel_files:
        # Give the location of the file 
        #file_path = "Alex 2019 09 AUG D12-14.xlsm"
        #print(excel_file)
        file_name = excel_file.split('.')[0]
        df = generate_data_frame(excel_file, file_name)  #generate data frame
        # calculate number of pallets
        all_df = pd.concat([all_df, df], ignore_index=True)
        #os.chdir('/home/siwanpark/ExcelData/Alex/')

    if location != '':
        all_df = all_df[all_df['location'].str.upper() == location.upper()]
        
    if code != '':
        all_df = all_df[all_df['code'].str.upper() == code.upper()]
    
    if product_name != '':        
        all_df = all_df[(all_df['ITEM1'].str.upper()).str.contains(product_name.upper())]
    
    if pallet != '':
        all_df = all_df[(all_df['pallet'].str.upper()).str.contains(pallet.upper())]

    #all_df = all_df.reset_index()
    #all_df.drop(axis=1, inplace=True)    
    return all_df, len(all_df['pallet'].unique())

def generate_data_frame(file_path, file_name):    
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
        if sheet.cell(i, 5).ctype == 3:
            inward_date = convert_excel_date(wb, sheet.cell(i, 5).value).date()
        else:
            inward_date = sheet.cell(i, 5).value
        # Convert excel date to python date       
        if sheet.cell(i, 18).ctype == 3:            
            bbd_date = convert_excel_date(wb, sheet.cell(i, 18).value).date()
            #print('{} - {}'.format(sheet.cell(i, 18).ctype, py_date))
        else:
            bbd_date = sheet.cell(i, 18).value
            #print('{} - {}'.format(sheet.cell(i, 18).ctype, sheet.cell(i, 18).value))     
            #              
        if ('Freezer' in file_name or 'Lucky' in file_name or 'OSP' in file_name or 'SR' in file_name or 'KKS' in file_name or 'Daily' in file_name):            
            product_type = 'FRZ'
        else:            
            product_type = 'DRY'     
            
        # Assign location of storage
        if 'Lucky' in file_name:     
            location = 'LW'
        elif 'OSP' in file_name :
            location = 'OSP'  		           
        elif 'KKS' in file_name:
            location = 'KKS'  	        
        elif 'HELLMANN' in file_name:
            location = 'HE'  		    
        elif 'HAISON' in file_name:
            location = 'HS'  	
        elif 'HUBX' in file_name:
            location = 'HX'     
        elif 'Alex' in file_name:
            location = 'Alex'	    
        elif 'Daily' in file_name:
            location = 'Alex(D)'	    
        
        stock_data = {'location': location, 'pallet': sheet.cell(i, 3).value, 'code' : sheet.cell(i, 4).value, 'origin' : sheet.cell(i, 0).value, 
                      'product_type': product_type, 'Inward' : inward_date, 'ITEM1' : sheet.cell(i, 9).value,  
                      'unit': sheet.cell(i, 13).value, 'pickup' : sheet.cell(i, 14).value, 'NewBalance' : sheet.cell(i, 15).value, 
                      'pmemo' : sheet.cell(i, 17).value, 'bbd' : bbd_date }                        
        stock_list.append(stock_data)
        i += 1
    result = pd.DataFrame(stock_list)    
    result['pallet'] = result['pallet'].astype(str)
    #result['Inward'] = pd.to_datetime(result['Inward']).dt.date
    return result
