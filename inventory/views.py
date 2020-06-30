from django.shortcuts import render
#from .models import Inventory
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
import xlrd 
import os
import datetime
import glob
import pandas as pd
import numpy as np
from django.http import HttpResponse


# Create your views here.
def home_normal(request):    
    return render(request, 'inventory/home_normal.html')


def home_simple(request):    
    return render(request, 'inventory/home_simple.html')


def home_current_usage(request):    
    return render(request, 'inventory/home_current_usage.html')


def stock_normal(request):
    #jobs = Job.objects
    #return render(request, 'inventory/home.html', {'jobs': jobs})
    form_parms = request.GET
    bbd_range = form_parms['bbd_range']
    location = form_parms['location']
    code = form_parms['code']
    product_name = form_parms['product_name']
    pallet = form_parms['pallet']    
    df_result, pallet_qty = read_excel(bbd_range, location, code, product_name, pallet)                
    #return HttpResponse(df_result.to_html())
    return render(request, 'inventory/stock_normal.html', {'df_result': df_result, 'pallet_qty' : pallet_qty} )

def stock_simple(request):
    form_parms = request.GET
    bbd_range = form_parms['bbd_range']
    #location = form_parms['location']
    code = form_parms['code']
    product_name = form_parms['product_name']       
    sort_by = form_parms['sort_by']
    df_result = read_excel_for_stock_simple(bbd_range, location, code, product_name, sort_by)      
    #os.chdir(r"\\192.168.20.50\AlexServer\SD共有\ボタニーパレット")
    os.chdir('/home/siwanpark/ExcelData/')
    excel_result = 'SCM_Stock_Expiring' + str(datetime.date.today()) + '.xlsx'
    df_result.to_excel(excel_result)                          
    return render(request, 'inventory/stock_simple.html', {'df_result': df_result} )


def tf_stock(request):
    tf_code_list = ['TF01B', 'CLV06', 'TF77', 'TF74', 'TF15', 'BEC03', 'BEC02', 'TFB2A', 'TFB25',
                 'TFB26', 'TFS01', 'TF34C', 'RUM05', 'TF83', 'TF83A', 'TF83B', 'TF83D', 'TF83E',
                 'TF83G', 'TF97', 'TF98', 'TF88', 'TF66Material', 'TF100', 'OCP69', 'ZN07',
                 'TF61', 'TF102', 'CFS01', 'CFS02', 'TF103', 'TF104']
    df_result = read_excel_for_tfstock(tf_code_list)
    return render(request, 'inventory/tf_stock.html', {'df_result': df_result} )


def daily_stock(request):    
    df_result = read_excel_for_daily_stock()    
    #os.chdir('/home/siwanpark/ExcelData/')
    os.chdir(r"\\192.168.20.50\AlexServer\SD共有\ボタニーパレット")
    excel_result = 'Daily_Stock_' + str(datetime.date.today()) + '.xlsx'
    df_result.to_excel(excel_result)
    return render(request, 'inventory/daily_stock.html', {'df_result': df_result} )


def current_usage(request):
    form_parms = request.GET    
    code = form_parms['code']
    product_name = form_parms['product_name']       
    sort_by = form_parms['sort_by']
    df_result = read_excel_for_current_usage(code, product_name, sort_by)            
    return render(request, 'inventory/current_usage.html', {'df_result': df_result} )    


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
    os.chdir(r"\\192.168.20.50\AlexServer\SD共有\ボタニーパレット\SF_Stock")             
    #os.chdir('/home/siwanpark/ExcelData/Alex/')
    excel_files = glob.glob('*.xls*')
    all_df = pd.DataFrame()
    selected_df = pd.DataFrame()
    for excel_file in excel_files:        
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
    os.chdir(r"\\192.168.20.50\AlexServer\SD共有\ボタニーパレット\SF_Stock")             
    #os.chdir('/home/siwanpark/ExcelData/Alex/')
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


def read_excel_for_stock_simple(bbd_range, location, code, product_name, sort_by):
    # Change directory    
    os.chdir(r"\\192.168.20.50\AlexServer\SD共有\ボタニーパレット\SF_Stock")             
    #os.chdir('/home/siwanpark/ExcelData/Alex/')
    excel_files = glob.glob('*.xls*')
    all_df = pd.DataFrame()
    for excel_file in excel_files:        
        file_name = excel_file.split('.')[0]
        df = generate_data_frame(excel_file, file_name)  #generate data frame        
        all_df = pd.concat([all_df, df], ignore_index=True)
        #os.chdir('/home/siwanpark/ExcelData/Alex/')

    if location != '':
        all_df = all_df[all_df['location'].str.upper() == location.upper()]
        
    if code != '':
        all_df = all_df[all_df['code'].str.upper() == code.upper()]
    
    if product_name != '':        
        all_df = all_df[(all_df['ITEM1'].str.upper()).str.contains(product_name.upper())]        

    if bbd_range != 'ALL':
        if bbd_range == '1':
            one_month = datetime.date.today() + relativedelta(months=+1)      
            all_df = all_df[all_df['bbd'] <= one_month]            
        elif bbd_range == '2':
            two_month = datetime.date.today() + relativedelta(months=+2)      
            all_df = all_df[all_df['bbd'] <= two_month]            
        elif bbd_range == '3':
            three_month = datetime.date.today() + relativedelta(months=+3)      
            all_df = all_df[all_df['bbd'] <= three_month]            
    
    all_df['unit'] = all_df['unit'].str.upper()        
    result_df = all_df.groupby(['code', 'ITEM1', 'unit', 'bbd']).agg('sum').reset_index()    
    if sort_by == "1":
        result_df = result_df.sort_values(by='bbd',ascending=True)
    elif sort_by == "2":
        result_df = result_df.sort_values(by='bbd',ascending=False)
    elif sort_by == "3":
        result_df = result_df.sort_values(by='code',ascending=True)

    return result_df


def read_excel_for_current_usage(code, product_name, sort_by):
    # Change directory    
    os.chdir(r"\\192.168.20.50\AlexServer\SD共有\ボタニーパレット\SF_Usage")     
    #os.chdir('/home/siwanpark/ExcelData/Alex/')
    excel_files = glob.glob('*.xls*')
    all_df = pd.DataFrame()
    for excel_file in excel_files:        
        file_name = excel_file.split('.')[0]        
        temp_df, update_date = generate_data_frame_for_current_usage(excel_file)  #generate data frame
        #df1 = df.copy(deep=True)
        df = generate_current_usage(temp_df, file_name, update_date) 
        all_df = pd.concat([all_df, df], ignore_index=True)
        #os.chdir('/home/siwanpark/ExcelData/Alex/')
        
    if code != '':
        all_df = all_df[all_df['sf_code'].str.upper() == code.upper()]
    
    if product_name != '':        
        all_df = all_df[(all_df['product_name'].str.upper()).str.contains(product_name.upper())]        
       
    all_df['unit'] = all_df['unit'].str.upper()        
    #result_df = all_df.groupby(['location', 'code', 'ITEM1', 'unit', 'bbd']).agg('sum').reset_index()    

    if sort_by == "1":
        result_df = all_df.sort_values(by='sf_code',ascending=True)
    elif sort_by == "2":
        result_df = all_df.sort_values(by='update_date',ascending=True)
    
    return result_df


def read_excel(bbd_range, location, code, product_name, pallet):
    # Change directory    
    os.chdir(r"\\192.168.20.50\AlexServer\SD共有\ボタニーパレット\SF_Stock")   
    #os.chdir('/home/siwanpark/ExcelData/Alex/')
    excel_files = glob.glob('*.xls*')
    all_df = pd.DataFrame()
    for excel_file in excel_files:        
        file_name = excel_file.split('.')[0]
        df = generate_data_frame(excel_file, file_name)  #generate data frame        
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

    if bbd_range != 'ALL':
        if bbd_range == '1':
            one_month = datetime.date.today() + relativedelta(months=+1)      
            all_df = all_df[all_df['bbd'] <= one_month]            
        elif bbd_range == '2':
            two_month = datetime.date.today() + relativedelta(months=+2)      
            all_df = all_df[all_df['bbd'] <= two_month]            
        elif bbd_range == '3':
            three_month = datetime.date.today() + relativedelta(months=+3)      
            all_df = all_df[all_df['bbd'] <= three_month]            

    #all_df = all_df.reset_index()
    #all_df.drop(axis=1, inplace=True)    
    return all_df, len(all_df['pallet'].unique())


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
        #if sheet.cell(i, 5).ctype == 3:
        #    inward_date = convert_excel_date(wb, sheet.cell(i, 5).value)
        #else:
        #    inward_date = sheet.cell(i, 5).value
        if sheet.cell(i, 5).ctype == 3 or sheet.cell(i, 5).ctype == 2:
            inward_date = convert_excel_date(wb, sheet.cell(i, 5).value).date()
        elif sheet.cell(i, 5).ctype == 0:
            inward_date = datetime.datetime.strptime('01/01/2020', "%d/%m/%Y").date()
        elif sheet.cell(i, 5).ctype == 1:
            inward_date = datetime.datetime.strptime('01/01/2020', "%d/%m/%Y").date()
        else:
            inward_date = datetime.datetime.strptime('01/01/2020', "%d/%m/%Y").date()                        
        # Convert excel date to python date
        #if sheet.cell(i, 18).ctype == 3:
        #    bbd_date = convert_excel_date(wb, sheet.cell(i, 18).value)
        #else:
        #    bbd_date = sheet.cell(i, 18).value
        if sheet.cell(i, 18).ctype == 3 or sheet.cell(i, 18).ctype == 2:
            bbd_date = convert_excel_date(wb, sheet.cell(i, 18).value).date()
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
    #df.to_csv('test1.csv')
    df.dropna(subset=['code', 'pickup', 'pmemo'], how='any', inplace=True)
    #df.to_csv('test2.csv')
    df_preprocessed = df[['code', 'origin', 'Movement', 'ITEM1', 'ITEM2', 'unit', 'pickup', 'pmemo', 'bbd']]
    df_preprocessed['update_date'] = pd.to_datetime(update_date, format='%d/%m/%Y')

    if ('Freezer' in file_name or 'Lucky' in file_name or 'OSP' in file_name or 'SR' in file_name or 'KKS' in file_name or 'Daily' in file_name):
        df_preprocessed['product_type'] = 'FRZ'
    else:
        df_preprocessed['product_type'] = 'DRY'

    df_preprocessed['id'] = ''
    df_preprocessed['unit'] = df_preprocessed['unit'].str.lower()
    df_preprocessed = df_preprocessed.reset_index()

    df_preprocessed_usage = df_preprocessed

    data = { 'id' : df_preprocessed_usage['id'], 'update_date' : df_preprocessed_usage['update_date'],
                'product_type' : df_preprocessed_usage['product_type'], 'sf_code' : df_preprocessed_usage['code'],
                'origin' : df_preprocessed['origin'], 'product_name' : df_preprocessed_usage['ITEM1'], 'product_name_jp' : df_preprocessed['ITEM2'],
                'move' : df_preprocessed_usage['Movement'], 'unit' : df_preprocessed_usage['unit'],
                'pickup_qty' : df_preprocessed_usage['pickup'], 'memo' : df_preprocessed_usage['pmemo'], 'bbd' : df_preprocessed_usage['bbd']}
    df_processed = pd.DataFrame(data)
    #processed_file_name = file_name + '_processed_usage.xlsx'
    #os.chdir('/home/siwanpark/ExcelData/convert_xlsm_to_csv/uploading_file')
    #os.chdir(r"\\192.168.20.50\AlexServer\SD共有\ボタニーパレット\Siwan\StockFiles\working_place\uploading_files")
    #df_processed.to_excel(processed_file_name)
    return df_processed


def generate_data_frame(file_path, file_name):    
    loc = (file_path)     
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(0)     
    update_date = sheet.cell_value(1, 9).split(':')[1]
    
    update_date = update_date.strip()
   
    #for i in range(3, sheet.nrows):  
    stock_list = []
    i = 4
    #inward_date = '2020-02-01'
    #bbd_date = '2020-01-01'
    while sheet.cell(i, 1).value != 'end':    
        # Convert excel date cell to python date              
        if sheet.cell(i, 5).ctype == 3 or sheet.cell(i, 5).ctype == 2:
            inward_date = convert_excel_date(wb, sheet.cell(i, 5).value).date()
        elif sheet.cell(i, 5).ctype == 0:
            inward_date = datetime.datetime.strptime('01/01/2020', "%d/%m/%Y").date()
        elif sheet.cell(i, 5).ctype == 1:
            inward_date = datetime.datetime.strptime('01/01/2020', "%d/%m/%Y").date()
        else:
            inward_date = datetime.datetime.strptime('01/01/2020', "%d/%m/%Y").date()
        
        # Convert excel date to python date       
        print('{} | {} | {}'.format(type(inward_date), sheet.cell(i, 18).value, sheet.cell(i, 18).ctype))
        if sheet.cell(i, 18).ctype == 3 or sheet.cell(i, 18).ctype == 2:               
            bbd_date = convert_excel_date(wb, sheet.cell(i, 18).value).date()            
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
