# -*- coding: utf-8 -*-
'''
Created on Wed Jan 25 16:40:58 2023

@author: jeeve
'''
from fyerslogin import *
from fyers_api import fyersModel,accessToken
import pandas as pd
import csv
from datetime import datetime,timedelta
import math

with open(r'C:\BackTesting Framework Valpha\credentials.csv','r') as file:
    csvfile = csv.reader(file)

    for data in csvfile:
        data = data
file.close()
client_id = data[0]

access_token = login() #calling the login() function to get access_token
fyers = fyersModel.FyersModel(client_id=client_id,token=access_token,log_path=r"C:\Users\jeeve\Desktop\Algorithm\backtesting\logfiles")

class dataset:
    
    
    def __init__(self,ticker,range_from,range_to,resolution):
        self.ticker = ticker
        self.range_from = range_from
        self.range_to = range_to
        self.resolution = resolution
    
    def historical_data(self):
        d1 = datetime.strptime(self.range_from, "%Y-%m-%d")
        d2 = datetime.strptime(self.range_to, "%Y-%m-%d")
        delta = d2-d1
        if self.resolution == 'D':
            if delta.days > 365:
                dsets = math.ceil(delta.days/365) #calculates the number of times data will need to be requested from the api
                dates = []
                while dsets >= 1: #creates a list of dates with difference being 365 days(between range_from and range_to) due to api limitations
                    dates.append(datetime.strftime(d1,"%Y-%m-%d"))
                    d1 = d1 + timedelta(days = 364)
                    dsets -= 1
                dates.append(self.range_to)
                dsets = math.ceil(delta.days/365)
                i = 0
                dfl = []
                while dsets >=1: #gets the historical data in mutiple requests to bypass api limitations , joins those dataframes and converts the date and time to Asia/Kolkata timezone
                    data_parameters = {"symbol":self.ticker,"resolution":self.resolution,"date_format":"1","range_from":dates[i],"range_to":dates[i+1],"cont_flag":"1"}
                    df = pd.DataFrame(fyers.history(data_parameters)['candles']) #command that uses the data_parameters provided to request data from api and turns the data into a pandas dataframe
                    df1 = df
                    df1 = df1.drop([1,2,3,4,5],axis=1)
                    df1.columns = ['Date']
                    df1= pd.to_datetime(df1['Date'],unit ='s') #converts the epoch time into yyyy-mm-dd
                    df1 = df1.to_frame()
                    df1['Date'] = df1['Date'].dt.tz_localize('UTC')
                    df1['Date'] = df1['Date'].dt.tz_convert('Asia/kolkata') #datetime conversion
                    df = df.drop(0,axis=1)
                    df.columns = ['Open','High','Low','Close','Volume']
                    df['Date'] = df1
                    df = df.reindex(columns=['Date','Open','High','Low','Close','Volume'])
                    dfl.append(df) #appends the dataframe acquired in each request
                    dsets -= 1 
                    i +=1
                final_dataframe = pd.concat(dfl) #concats all the dataframes in the list into a single large dataframe
                final_dataframe =final_dataframe.reset_index()
                final_dataframe = final_dataframe.drop('index',axis=1)
                
            else: # gets the data in a single request and converts the timezone to Asia/Kolkata
                data_parameters = {"symbol":self.ticker,"resolution":self.resolution,"date_format":"1","range_from":self.range_from,"range_to":self.range_to,"cont_flag":"1"}
                df = pd.DataFrame(fyers.history(data_parameters)['candles']) #command that uses the data_parameters provided to request data from api and turns the data into a pandas dataframe
                df1 = df
                df1 = df1.drop([1,2,3,4,5],axis=1)
                df1.columns = ['Date']
                df1= pd.to_datetime(df1['Date'],unit ='s') #converts epoch time into yyyy-mm-dd
                df1 = df1.to_frame()
                df1['Date'] = df1['Date'].dt.tz_localize('UTC')
                df1['Date'] = df1['Date'].dt.tz_convert('Asia/kolkata')
                df = df.drop(0,axis=1)
                df.columns = ['Open','High','Low','Close','Volume']
                df['Date'] = df1
                df = df.reindex(columns=['Date','Open','High','Low','Close','Volume'])
                final_dataframe = df
    
        else:
            if delta.days >100:
                dsets = math.ceil(delta.days/100) #calculates the number of times data will need to be requested from the api
                dates = []
                while dsets >=1: #creates a list of dates with difference being 100 days(between range_from and range_to) due to api limitations
                    dates.append(datetime.strftime(d1,"%Y-%m-%d"))
                    d1 = d1 + timedelta(days = 99)
                    dsets -= 1
                dates.append(self.range_to)
                dsets = math.ceil(delta.days/100)
                i = 0
                dfl = []
                while dsets >=1: #gets the historical data in mutiple requests to bypass api limitations , joins those dataframes and converts the date and time to Asia/Kolkata timezone
                    data_parameters = {"symbol":self.ticker,"resolution":self.resolution,"date_format":"1","range_from":dates[i],"range_to":dates[i+1],"cont_flag":"1"}
                    df = pd.DataFrame(fyers.history(data_parameters)['candles']) #command that uses the data_parameters provided to request data from api and turns the data into a pandas dataframe
                    df1 = df
                    df1 = df1.drop([1,2,3,4,5],axis=1)
                    df1.columns = ['Date']
                    df1= pd.to_datetime(df1['Date'],unit ='s') #converts epoch time to yyyy-mm-dd
                    df1 = df1.to_frame()
                    df1['Date'] = df1['Date'].dt.tz_localize('UTC')
                    df1['Date'] = df1['Date'].dt.tz_convert('Asia/kolkata') #datetime conversion
                    df = df.drop(0,axis=1)
                    df.columns = ['Open','High','Low','Close','Volume']
                    df['Date'] = df1
                    df = df.reindex(columns=['Date','Open','High','Low','Close','Volume'])
                    dfl.append(df) #appends the dataframe acquired in each request to a list
                    dsets -= 1 
                    i +=1
                final_dataframe = pd.concat(dfl) #concats all the dataframes in the list to form a single dataframe 
                final_dataframe =final_dataframe.reset_index()
                final_dataframe = final_dataframe.drop('index',axis=1)
    
            else: # gets the data in a single request and converts the timezone to Asia/Kolkata
                data_parameters = {"symbol":self.ticker,"resolution":self.resolution,"date_format":"1","range_from":self.range_from,"range_to":self.range_to,"cont_flag":"1"}
                df = pd.DataFrame(fyers.history(data_parameters)['candles']) #command that uses the data_parameters provided to request data from api and turns the data into a pandas dataframe
                df1 = df
                df1 = df1.drop([1,2,3,4,5],axis=1)
                df1.columns = ['Date']
                df1= pd.to_datetime(df1['Date'],unit ='s') #converts epoch time into yyyy-mm-dd
                df1 = df1.to_frame()
                df1['Date'] = df1['Date'].dt.tz_localize('UTC')
                df1['Date'] = df1['Date'].dt.tz_convert('Asia/kolkata') #datetime conversion
                df = df.drop(0,axis=1)
                df.columns = ['Open','High','Low','Close','Volume']
                df['Date'] = df1
                df = df.reindex(columns=['Date','Open','High','Low','Close','Volume'])
                final_dataframe = df
                
        return final_dataframe