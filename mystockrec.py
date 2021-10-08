from random import randint
import time
from time import sleep
import datetime
import yfinance as yf
import openpyxl
import pandas as pd
import numpy as np

# Def for reading the ticker file as csv: csv_ticker('filename.csv', 'columnname')
def csv_ticker(csv_file, ticker_col):
    df = pd.read_csv(csv_file)
    df_tick = df[ticker_col].drop_duplicates(keep='first').dropna()
    return df_tick

# Def for reading the ticker file as xlsx: xlsx_ticker('filename.xlsx', 'columnname') returns "df_tick"
def xlsx_ticker(xlsx_file, ticker_col):
    df = pd.read_excel(xlsx_file)
    df_tick = df[ticker_col].drop_duplicates(keep='first').dropna()
    return df_tick

# Def for reading collected data after preprocessing through “def info()“ and “def fin()“
def csv_df(csv_file):
    df = pd.read_csv(csv_file)
    return df

def xlsx_df(xlsx_file):
    df = pd.read_excel(xlsx_file)
    return df

# Def for data export
def export_xlsx(df):
    now = datetime.datetime.now()
    now = now.strftime("%Y.%m.%d %H_%M_%S")
    len_df = str(len(df))
    return df.to_excel('df_'+'_'+len_df+'_'+now+'.xlsx'), print('Successfully stored as xlsx')

# First the ticker lists have to be created, 
# the ticker df_tick are then used to download the financial information with the info and fin functions.
# Def for reading the ticker file as csv: csv_ticker('filename.csv', 'columnname')
def csv_ticker(csv_file, ticker_col):
    df = pd.read_csv(csv_file)
    df_tick = df[ticker_col].drop_duplicates(keep='first').dropna()
    return df_tick

# Def for reading the ticker file as xlsx: xlsx_ticker('filename.xlsx', 'columnname') returns "df_tick"
def xlsx_ticker(xlsx_file, ticker_col):
    df = pd.read_excel(xlsx_file)
    df_tick = df[ticker_col].drop_duplicates(keep='first').dropna()
    return df_tick

#Example tickers: ticker_list = ['BZ6.F',	'DUE.DE',	'EXL.DE',	'COP.DE',	'NFN.DE',	'MED.SW',
#                'SAP.DE',	'EVT.DE',	'AAG.DE',	'LPK.DE',	'OSP2.DE',	'ADN1.DE',	'SHF.DE',	
#               'SANT.DE',	'AOF.DE'] # example list
# Dict. ticker_info_dict has to be created to store information coming from .info function
# Within dict. values have to be iterable (lists, tuples, dict., sets) values returned from .info have to be 
# transformed into list. List of 308 ticker took circa 25 min.

def info(df):
    ticker_info_dict = {}
    ticker_info_dict2 = {}
    info_list = []
    total_number = 0
    total_passed = 0
    
    for tick in df:
        try:
            ticker_item = yf.Ticker(tick)
            ticker_info_dict = ticker_item.info
            print('Starting to loop through dict. of', tick)

            for key, value in ticker_info_dict.items():
                ticker_info_dict2[key] = [value]

            a = pd.DataFrame.from_dict(ticker_info_dict2)
            info_list.append(a)
               
            total_number = total_number + 1
            print('Nr: ' + str(total_number), tick)
        except Exception as e:
            total_passed = total_passed + 1
            print('Nr: ' + str(total_passed), tick, 'Passed!', e)
            #passed_df.append(tick, e)
            #passed_df.append([ticker, e]) # e text of exception, to understand reason why passed
            pass
    df_info = pd.concat(info_list, sort=False)  # transform info_list into df
    df_info.fillna(0)
    
    
    print('Start saving stock data...')

    #Create variables for specific naming of file, to not overwrite data
    #Later file shall be overwritten or appended for purpose of updating
    now = datetime.datetime.now()
    now = now.strftime("%Y.%m.%d %H_%M_%S")
    len_df = str(len(df))

# fin(df) takes your tickers df and gets the PnL, balance sheet and CF information

def fin(df):
        balance_list = []
        cashflow_list = []
        financials_list = []
        total_number = 0
        total_passed = 0
        passed_df = []
        
        for tick in df:
            try:
                ticker = yf.Ticker(tick)
                a = ticker.balancesheet.T   # T stands for transpose
                if a.index.dtype.kind == 'M':  # Check if ticker is valid, if no data can be found then index.dtype
                                               # is an object and index is filled 
                                               # with ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
                    a.insert(0, 'ticker', tick)
                    b = ticker.cashflow.T
                    b.insert(0, 'ticker', tick)
                    c = ticker.financials.T
                    c.insert(0, 'ticker', tick)

                    balance_list.append(a)
                    cashflow_list.append(b)
                    financials_list.append(c)

                    total_number = total_number + 1
                    print('Nr: ' + str(total_number), tick)
                else:
                    total_passed = total_passed + 1
                    print('Nr: ' + str(total_passed), tick, 
                          'Passed! Ticker is empty or has no datetime index with index.dtype:', a.index.dtype)
            except Exception as e:
                total_passed = total_passed + 1
                print('Nr: ' + str(total_passed), tick, 'Passed!', e)
                #passed_df.append(tick, e)
                #passed_df.append([ticker, e]) # e text of exception, to understand reason why passed
                pass

        df_balance = pd.concat(balance_list, sort=False)
        df_balance.insert(1, 'Date', pd.DatetimeIndex(df_balance.index).date) # Add try except for date column issue
        df_balance.fillna(0)

        df_cashflow = pd.concat(cashflow_list, sort=False)
        df_cashflow.insert(1, 'Date', pd.DatetimeIndex(df_cashflow.index).date)
        df_cashflow.fillna(0)

        df_financials = pd.concat(financials_list, sort=False)
        df_financials.insert(1, 'Date', pd.DatetimeIndex(df_financials.index).date)
        df_financials.fillna(0)
        try:
            df_passed = pd.concat(passed_df, sort=False)
        except Exception as e:
            print(e)
            pass
        print('Start saving stock data...')
        #df_pass = pd.DataFrame(Screener.globalpass, index=None, columns={'Ticker', 'Error'})
        
        #Create variables for specific naming of the files, to not overwrite data
        #Later files shall be overwritten or appended for purpose of updating
        now = datetime.datetime.now()
        now = now.strftime("%Y.%m.%d %H_%M_%S")
        len_df = str(len(df))
        
        df_balance.to_csv('balance_'+len_df+'_'+now+'.csv')
        df_cashflow.to_csv('cashflow_'+len_df+'_'+now+'.csv')
        df_financials.to_csv('financials_'+len_df+'_'+now+'.csv')
        
        print('Stock data saved!')
        
        #Writer not needed, as analysis will be conducted with CSV format
        #writer = pd.ExcelWriter('merge.xlsx')
        #df_balance.to_excel(writer, 'Balances', index=False)
        #df_cashflow.to_excel(writer, 'Cashflows', index=False)
        #df_financials.to_excel(writer, 'Financials', index=False)
        #writer.save()


# USER INPUT PART
# Data load for user input
def data_load_user_input():
    df = xlsx_df('df__734_2021.10.07 00_06_06.xlsx')
    #display(df.loc[0:3,'Unnamed: 0'])
    #df.info()
    #df.head()

    # Clean data set
    df['shortName'] = df['shortName'].astype('str')
    df['shortName'] = df['shortName'].apply(lambda x: x.upper().translate({ord(c): "" for c in "!?/[]|{}.:()'\""}))
    df.drop(['Unnamed: 0','Unnamed: 0.1'], axis=1, inplace=True)

    # Select columns
    df = df[['shortName','symbol','cluster','sector','Rank_CFoEV_RoA',
             'revenueGrowth','earningsGrowth','SalesoEV_in_%','beta']]
    #return df
    
    # Start of user input part
    br = '\n' # if needed variable for string literal line break, put {nl} if new line is needed
    shortName_input = input(" What company do you want to check? ")
    shortName_input = shortName_input.upper()
    comp_match = df[df['shortName'].str.contains(shortName_input)]
    if len(comp_match) == 1:
        print()
        print(f"{comp_match.loc[1:,'shortName'].values[0]} was found in the database.")
        time.sleep(1)
        print()
        print("Let's take a closer look.")
        
        time.sleep(1)
        print()
        print(f"{comp_match.loc[1:,'shortName'].values[0]} is in cluster" 
              f" {comp_match.loc[1:,'cluster'].values[0]:.0f}"
              #f"sector {comp_match.loc[1:,'sector'].values[0]} " 
              f" and was ranked on overall position {comp_match.loc[1:,'Rank_CFoEV_RoA'].values[0]:.0f}"
              f" out of {len(df)} companies.")
        
        time.sleep(1)
        display(comp_match)
        
        time.sleep(1)
        print()
        print(f"Top ranked companies in cluster {comp_match.loc[1:,'cluster'].values[0]:.0f} are:")
        #display(df[df['cluster'].isin([int(comp_match.loc[1:,'cluster'])])].nsmallest(10,['Rank_CFoEV_RoA']))
        
        df_usr = df[df['cluster'].isin([int(comp_match.loc[1:,'cluster'])])].nsmallest(10,['Rank_CFoEV_RoA'])
        df_usr = df_usr.append(comp_match)
        df_usr.drop_duplicates(inplace=True)
        df_usr = df_usr.nsmallest(11,['Rank_CFoEV_RoA'])
        display(df_usr)
    elif len(comp_match) > 1:
        print()
        print(f"Several companies were found.")
        
        time.sleep(1)
        display(comp_match)
        symbol_input = input(f"Please select only one by typing the symbol of the company.")
        symbol_input = symbol_input.upper()
        try:
            comp_match = df.loc[df['symbol'] == symbol_input]
            print()
            print(f"{comp_match.loc[1:,'shortName'].values[0]} was found in the database.")
            
            time.sleep(1)
            print(f"{comp_match.loc[1:,'shortName'].values[0]} is in cluster"
                  f"{comp_match.loc[1:,'cluster'].values[0]:.0f}"
                  #f"sector {comp_match.loc[1:,'sector'].values[0]} "
                  f" and was ranked on overall position {comp_match.loc[1:,'Rank_CFoEV_RoA'].values[0]:.0f}"
                  f" out of {len(df)} companies.")
            
            time.sleep(1)
            display(comp_match)
            
            time.sleep(1)
            print()
            print(f"Top ranked companies in cluster {comp_match.loc[1:,'cluster'].values[0]} are:")
            #display(df[df['cluster'].isin([int(comp_match.loc[1:,'cluster'])])].nsmallest(10,['Rank_CFoEV_RoA']))
            
            df_usr = df[df['cluster'].isin([int(comp_match.loc[1:,'cluster'])])].nsmallest(10,['Rank_CFoEV_RoA'])
            df_usr = df_usr.append(comp_match)
            df_usr.drop_duplicates(inplace=True)
            df_usr = df_usr.nsmallest(11,['Rank_CFoEV_RoA'])
            display(df_usr)
        except:
            pass
    else:
        print('Sorry, your company is not in the database and has to be downloaded first, try again.')
        user_try_again = input('Do you want to try again? Type y for yes or n for no')
        if user_try_again == 'y':
            get_input()
        else:
            print("Thanks for using stock recommender")

    #'EV_calc','EV_52high','EV_52low','SalesoEV_in_%','EBITDAoEV_in_%','CFoEV_in_%','Rank_SalesoEV','Rank_EBITDAoEV','Rank_CFoEV','Rank_RoA','Rank_CFoEV_RoA'
    #df = df[['sector', 'cluster','fullTimeEmployees', 'city', 'state', 'country', 'industry','EV_calc','EV_52high','EV_52low','SalesoEV_in_%','EBITDAoEV_in_%','CFoEV_in_%','Rank_SalesoEV',
    # 'Rank_EBITDAoEV','Rank_CFoEV','Rank_RoA','Rank_CFoEV_RoA', 'ebitdaMargins', 'profitMargins', 'grossMargins', 'operatingCashflow', 'revenueGrowth', 'operatingMargins', 'ebitda', 
    # 'targetLowPrice', 'recommendationKey', 'grossProfits', 'freeCashflow', 'targetMedianPrice', 'currentPrice', 'earningsGrowth', 'returnOnAssets', 'numberOfAnalystOpinions', 
    # 'targetMeanPrice', 'debtToEquity', 'targetHighPrice', 'totalCash', 'totalDebt', 'totalRevenue', 'financialCurrency', 'recommendationMean', 'exchange', 'shortName', 'longName', 
    # 'symbol', 'market', 'enterpriseToRevenue', 'enterpriseToEbitda', 'sharesOutstanding', 'sharesShort', 'fundFamily', 'heldPercentInstitutions', 'priceToBook', 'heldPercentInsiders', 
    # 'beta', 'enterpriseValue', 'earningsQuarterlyGrowth', 'forwardPE', 'sharesShortPriorMonth', 'trailingAnnualDividendYield', 'payoutRatio', 'trailingAnnualDividendRate', 'dividendRate', 
    # 'currency', 'trailingPE', 'marketCap', 'fiftyTwoWeekHigh', 'fiftyTwoWeekLow']]

# Getting the user input
def get_input():
    br = '\n' # if needed variable for string literal line break, put {nl} if new line is needed
    shortName_input = input(" What company do you want to check? ")
    shortName_input = shortName_input.upper()
    comp_match = df[df['shortName'].str.contains(shortName_input)]
    if len(comp_match) == 1:
        print()
        print(f"{comp_match.loc[1:,'shortName'].values[0]} was found in the database.")
        time.sleep(1)
        print()
        print("Let's take a closer look.")
        
        time.sleep(1)
        print()
        print(f"{comp_match.loc[1:,'shortName'].values[0]} is in cluster" 
              f" {comp_match.loc[1:,'cluster'].values[0]:.0f}"
              #f"sector {comp_match.loc[1:,'sector'].values[0]} "
              f" and was ranked on overall position {comp_match.loc[1:,'Rank_CFoEV_RoA'].values[0]:.0f}.")
        
        time.sleep(1)
        display(comp_match)
        
        time.sleep(1)
        print()
        print(f"Top ranked companies in cluster {comp_match.loc[1:,'cluster'].values[0]:.0f} are:")
        #display(df[df['cluster'].isin([int(comp_match.loc[1:,'cluster'])])].nsmallest(10,['Rank_CFoEV_RoA']))
        
        df_usr = df[df['cluster'].isin([int(comp_match.loc[1:,'cluster'])])].nsmallest(10,['Rank_CFoEV_RoA'])
        df_usr = df_usr.append(comp_match)
        df_usr.drop_duplicates(inplace=True)
        df_usr = df_usr.nsmallest(11,['Rank_CFoEV_RoA'])
        display(df_usr)
    elif len(comp_match) > 1:
        print()
        print(f"Several companies were found.")
        
        time.sleep(1)
        display(comp_match)
        symbol_input = input(f"Please select only one by typing the symbol of the company.")
        symbol_input = symbol_input.upper()
        try:
            comp_match = df.loc[df['symbol'] == symbol_input]
            print()
            print(f"{comp_match.loc[1:,'shortName'].values[0]} was found in the database.")
            
            time.sleep(1)
            print(f"{comp_match.loc[1:,'shortName'].values[0]} is in cluster"
                  f"{comp_match.loc[1:,'cluster'].values[0]:.0f}"
                  #f"sector {comp_match.loc[1:,'sector'].values[0]} "
                  f" and was ranked on overall position {comp_match.loc[1:,'Rank_CFoEV_RoA'].values[0]:.0f}.")
            
            time.sleep(1)
            display(comp_match)
            
            time.sleep(1)
            print()
            print(f"Top ranked companies in cluster {comp_match.loc[1:,'cluster'].values[0]} are:")
            #display(df[df['cluster'].isin([int(comp_match.loc[1:,'cluster'])])].nsmallest(10,['Rank_CFoEV_RoA']))
            
            df_usr = df[df['cluster'].isin([int(comp_match.loc[1:,'cluster'])])].nsmallest(10,['Rank_CFoEV_RoA'])
            df_usr = df_usr.append(comp_match)
            df_usr.drop_duplicates(inplace=True)
            df_usr = df_usr.nsmallest(11,['Rank_CFoEV_RoA'])
            display(df_usr)
        except:
            pass
    else:
        print('Sorry, your company is not in the database and has to be downloaded first, try again.')
        user_try_again = input('Do you want to try again? Type y for yes or n for no')
        if user_try_again == 'y':
            get_input()
        else:
            print("Thanks for using stock recommender")