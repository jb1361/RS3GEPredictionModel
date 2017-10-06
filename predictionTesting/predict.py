import time
import sqlite3
import pandas as pd
import numpy as np
import scipy as sp
from scipy import stats
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

'''
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import (RandomTreesEmbedding, RandomForestClassifier, GradientBoostingClassifier)
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve
from sklearn.pipeline import make_pipeline
'''
traindataframes = []
testDataFrame = []


def predict():
	return



def cost():
	cost = 0
	return cost
	
	
def gradient_descent():
	global traindataframes
	global testDataFrame
	
	#get initial data
	initial_df = traindataframes[0]
	id_col = initial_df['Id']
	price_col = initial_df['Current_price']
	trend_col = initial_df['Current_trend']
	today_price_col = initial_df['Today_price']
	today_trend_col = initial_df['Today_trend']
	
	#remove +signs
	for i in today_price_col:
		if '+' in i:
			temp = i.replace('+','')
			today_price_col = today_price_col.replace(str(i),temp)
	#convert to floats
	for i in today_price_col:
		today_price_col = today_price_col.replace(str(i),float(i))
	
	
	#make the size(rows)equal to the other data sets
	a = [0.0]
	df = pd.DataFrame(a)
	price_col = price_col.append(df,ignore_index = True)
	today_price_col = today_price_col.append(df,ignore_index = True)
	
	#print(today_price_col)
	#print('==================================================================')
	
	#print(price_col)
	#print(today_price_col)
	#print('==================================================================')
	
	#convert data into usable form and put into dataframe
	frames = [price_col,today_price_col]
	data_df = pd.concat(frames,axis=1)
	
	#get features
	features = data_df
	features = (features - features.mean())/features.std()
	
	#values
	value_df = traindataframes[1]
	value_price = value_df['Current_price']
	value_today = value_df['Today_price']
	
	#remove +signs
	for i in value_today:
		if '+' in i:
			temp = i.replace('+','')
			value_today = value_today.replace(str(i),temp)
	#convert to floats
	for i in value_today:
		value_today = value_today.replace(str(i),float(i))
			
	values = [value_price,value_today]
	values = pd.DataFrame(values).transpose()
	values =(values - values.mean())/values.std()

	m = len(values)
	#features['ones'] = np.ones(m)
	

	features_array = np.array(features)
	values_array = np.array(values)
	
	alpha = 0.1
	num_iterations = 20
	
	theta_descent = np.zeros(len(features.columns))
	print(features_array.shape)
	print(theta_descent.shape)
	cost_history = []

	for i in range(num_iterations):
		predicted_value = np.dot(features_array, theta_descent)
		theta_descent = theta_descent + alpha/m * np.dot(values_array - predicted_value, features_array)
		sum_of_square_errors = np.square(np.dot(features_array, theta_descent) - values_array).sum()
		cost = sum_of_square_errors / (2 * m)
		cost_history.append(cost)

	cost_history = pd.Series(cost_history)
	predictions = np.dot(features_array, theta_descent)

	print('============================================')
	print('Cost History: ', cost_history)
	print('Predictions: ',predictions)
	print('Alpha: ', alpha)
	print('Iterations: ',num_iterations)
	#===========================
	#7 ===================================
	data_predictions = np.sum((values - predictions)**2)
	mean = np.mean(values)
	sq_mean = np.sum((values - mean)**2)

	r = 1 - data_predictions / sq_mean
	print('R: ', r)
	print()


def get_Data():
        global traindataframes
        global testDataFrame
        tables = []
        con = sqlite3.connect("GE_Data.db")
        cur = con.cursor()
        table = cur.execute("select name from sqlite_master where type = 'table'")
       # print('Tables in db: ' + str(tables.fetchall()))
       # print(tables.fetchall())
        for i in table.fetchall():
                tables.append(i[0])
        for i in tables[:-1]:
               # print('DFs: ' + str(i))
                q = "select * from " + i + " ORDER BY Id"
                traindataframes.append(pd.read_sql(q,con))
        for i in tables[-1:]:
               # print('TestDF: ' + str(i))
                q = "select * from " + i + " ORDER BY Id"
                testDataFrame.append(pd.read_sql(q,con))
        cur.close()
        con.close()
       # with pd.option_context('display.max_columns', 1000,'display.max_rows',20,'display.width', 10000):
               # for i in dataframes:
                     #   print('DF')
                     #   print(i)
               # print('TestDF')
               # print(testDataFrame)
               # for i in dataframes:
                        #print(i)

	
get_Data()
gradient_descent()
#predict()