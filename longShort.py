#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 22:13:00 2018

@author: arpit
"""

import pandas as pd
import numpy as np
import quandl

quandl.ApiConfig.api_key = '_LZWycgx37qgoPKc2BKw'
quandl.ApiConfig.api_version = '2015-04-09'


with open("./fnoStocks.txt") as fp:  
   retProfit = 0
   retLoss = 0
   lines = fp.readlines()
   for line in lines:
       stock = "NSE/" + line.rstrip()
       df = quandl.get(stock, start_date="2010-01-01", collapse="monthly")
       df['return'] = (df['Close'] - df['Open']) / df['Open']
       df['returnShifted'] =  df['return'].shift(1)   
       df.dropna(inplace=True)
       df.to_csv(line + ".csv")
   
       retProfit = np.absolute(np.sum(df[((df['return'] > 0) & (df['returnShifted'] < 0))]['returnShifted'])) + \
           np.sum(df[((df['return'] < 0) & (df['returnShifted'] > 0))]['returnShifted'])
       retLoss = -(np.sum(df[((df['return'] > 0) & (df['returnShifted'] > 0))]['returnShifted'])) + \
           np.sum(df[((df['return'] < 0) & (df['returnShifted'] < 0))]['returnShifted'])    
       retProfitCount = df[((df['return'] > 0) & (df['returnShifted'] < 0))].shape[0] + \
           df[((df['return'] < 0) & (df['returnShifted'] > 0))].shape[0]
       retLossCount = df[((df['return'] > 0) & (df['returnShifted'] > 0))].shape[0] + \
           df[((df['return'] < 0) & (df['returnShifted'] < 0))].shape[0]
       print("Scrip = %s TotalReturn = %f +veRet = %f +veRetCount = %d -veRet = %f -veRetCount = %d" \
             %(line, retProfit + retLoss, retProfit, retProfitCount, retLoss, retLossCount)) 

       