# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 20:01:15 2023

@author: jeeve
"""

from fyers_api import fyersModel,accessToken
from selenium import webdriver
import time
import csv

with open(r'C:\BackTesting Framework Valpha\credentials.csv','r') as file:
    csvfile = csv.reader(file)

    for data in csvfile:
        data = data
file.close()
client_id = data[0]
secret_key = data[1]
redirect_uri = data[2]
def authcode():
    session = accessToken.SessionModel(client_id =client_id,secret_key=secret_key,redirect_uri=redirect_uri,response_type ='code',grant_type ='authorization_code')
    response = session.generate_authcode()
    url1 = response
    browser = webdriver.Chrome()
    browser.get(url1)
    time.sleep(2)
    login = browser.find_element('id','fy_client_id')
    login.send_keys(data[3])
    button = browser.find_element('id','clientIdSubmit')
    button.click()
    time.sleep(20)
    a= browser.current_url
    auth_code = a[48:-11]
    #print("Auth Code :",auth_code)
    
    session.set_token(auth_code)
    response = session.generate_token()
    access_token = response['access_token']
    f = open(r'C:\BackTesting Framework Valpha\authcode.txt','w')
    f.write(access_token)
    f.close()



def login():
    f= open(r'C:\BackTesting Framework Valpha\authcode.txt','r')
    for line in f:
        token = line
    f.close()
    fyers = fyersModel.FyersModel(client_id=client_id,token=token,log_path = r'C:\BackTesting Framework Valpha\logfiles')
    is_async = True 
    a = fyers.get_profile()
    
    if a['s'] == 'ok' :
        print('Login Succesful')
    else :
        print('Login Failed, Generating new Access Key')
        authcode()
    return token
