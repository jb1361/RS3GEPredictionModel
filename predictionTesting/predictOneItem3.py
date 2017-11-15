import time
import sqlite3
import pandas as pd
import numpy as np
import scipy as sp
from scipy import stats
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

traindataframes = []
testDataFrame = []

#this defines how many items we are looking at
#max = 20
predicted_Item = 0

#def predict_next_day():
	#return 0
	
def denormalize_features(features):
	frames = []
	denormalized_features = []
	trend_feature = []
	for i,r in enumerate(traindataframes):
		price_col = r['Current_price']
		price_col = price_col[predicted_Item:predicted_Item+1].values
		price_col = price_col[0]
		change_col = r['Today_price']
		change_col = change_col[predicted_Item:predicted_Item+1]
		
		today_trend = r['Today_trend']
		today_trend = today_trend[predicted_Item:predicted_Item+1]
		
		#parse data and remove + sign
		for j in change_col:
			if '+' in j:
				t = j.replace('+','')
				change_col = change_col.replace(str(j),t)
		for j in change_col:
			change_col = change_col.replace(str(j),float(j))
		change_col = change_col[predicted_Item]
			
		
		initial_price = price_col - change_col
		closing_price = (features[0][i] + 1) * initial_price
		denormalized_features.append(float(closing_price))	
		
		for j in today_trend:
			if (j == 'neutral'):
				trend_feature.append(float(0))
			elif(j == 'positive'):
				trend_feature.append(float(1))
			elif(j == 'negative'):
				trend_feature.append(float(-1))
		
	features = [denormalized_features, trend_feature]
	features = np.array(features)
	
	return features

def gradient_descent():
	global traindataframes
	global testDataFrame
	prediction_frame = testDataFrame[0]
	prediction_frame = prediction_frame['Current_price']
	prediction_frame = prediction_frame[predicted_Item:predicted_Item+1]
	prediction_frame = prediction_frame[predicted_Item]
	
	#=================================================================================================
	#get features
	#this takes the closing price and the initial price Current_price = initial today price is the change is price 
	#that day. So we take closing minus today change to get initial
	#we then normalize this data
	values_feature = []
	normalized_features = []
	trend_feature = []
	for i in traindataframes:
		
		price_col = i['Current_price']
		price_col = price_col[predicted_Item:predicted_Item+1].values
		price_col = price_col[0]
		change_col = i['Today_price']
		change_col = change_col[predicted_Item:predicted_Item+1]
		
		today_trend = i['Today_trend']
		today_trend = today_trend[predicted_Item:predicted_Item+1]
		
		#parse data and remove + sign
		for j in change_col:
			if '+' in j:
				t = j.replace('+','')
				change_col = change_col.replace(str(j),t)
		for j in change_col:
			change_col = change_col.replace(str(j),float(j))
		change_col = change_col[predicted_Item]
		#part that gets the initial and closing
		values_feature.append(price_col)
		initial_price = price_col - change_col
		closing_price = price_col
		normalized = ((closing_price/initial_price)-1)
		normalized_features.append(normalized)
		
		for j in today_trend:
			if (j == 'neutral'):
				trend_feature.append(float(0))
			elif(j == 'positive'):
				trend_feature.append(float(1))
			elif(j == 'negative'):
				trend_feature.append(float(-1))
	#frames.append([normalized_features, trend_feature])
		
	#get features
	features = [normalized_features, trend_feature]
	features_array = np.array(features)
	#===================================================================================================

	#get values
	values_array = np.array(values_feature)
	#===================================================================================================
	
	m = len(values_array)
	alpha = 0.00001
	num_iterations = 300000
	
	#2 is the number of features
	theta_descent = [0.5,0.5]
	cost_history = []
	#actual gradient descent part
	for i in range(num_iterations):
		#hypothesis
		predicted_values = np.dot(features_array.transpose(), theta_descent)
	
		#next theta
		theta_descent = theta_descent - alpha/m * np.dot((predicted_values-values_array), features_array.transpose())
		
		#get "corectness"
		sum_of_square_errors = np.square(np.dot(features_array.transpose(), theta_descent) - values_array).sum()
		cost = sum_of_square_errors / (2 * m)
		cost_history.append(cost)
		#this causes lag
		if(i % 1000 == 0):
			print('Epoch: ' + str(i/1000) + ' : ' + 'Cost: ' + str(cost_history[i]))
		
		
	#all output and debugging 
	cost_history = pd.Series(cost_history)
	
	predictions = np.dot(features_array.transpose(), theta_descent)
	#predictions = predicted(features_array, theta_descent)
	print('============================================')
	print('Cost History: ', cost_history)
	print('Theta Descent: ',theta_descent)
	print('Alpha: ', alpha)
	print('Iterations: ',num_iterations)

	data_predictions = (predictions- values_array)**2
	mean = values_array.mean()
	sq_mean = ((values_array - mean)**2).sum()
	
	r = 1 - (data_predictions / sq_mean).sum()
	print('R: ', r)
	
	#denormalize data
	features = denormalize_features(features)
	predictions = np.dot(features.transpose(), theta_descent)
	print('Value day before: ',features[0][-1:])
	print('Actual Price: ', values_array)
	print('Predicted price change percentage: ',predictions)
	#predictions = (1+predictions) * features[0][-1:]


	
	
	print('============================================')
	fig, ax = plt.subplots()
	ax.plot(values_array,'o',markersize = 1, color = 'green', label = 'Actual Price')
	ax.plot(predictions,'o',markersize = 1, color = 'blue', label = 'Predicted Price')
	plt.legend()
	fig2, ax2 = plt.subplots()
	ax2.plot(cost_history,'o',markersize = 1, color = 'blue')
	plt.show()
	#===================================================================================================
	
	
def get_Data():
        global traindataframes
        global testDataFrame
        tables = []
        con = sqlite3.connect("GE_Data.db")
        cur = con.cursor()
        table = cur.execute("select name from sqlite_master where type = 'table'")
      
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
	
get_Data()
gradient_descent()
#predict()
