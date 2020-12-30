import csv
import random
import math
import operator
import pandas as pd
import numpy as np

class Dataloader:
    def __init__(self, path):
        self.data = pd.read_csv(path)
        self.length = len(self.data)
        self.drop_address()
        #self.feature, self.label = self.get_feature_label()
        self.normalize()
        self.pre_process()
        #self.bias()
        #print(self.data.head())
    
    def drop_address(self):
        self.data = self.data.drop(columns=['Address'])
    
    def normalize(self):#max-min renomalization
        pass

    def pre_process(self):
        self.data['bias'] = np.array([1 for i in range(len(self.data))])
     
    def train_val_split(self):
        split = math.floor(0.7*len(self.data))
        return self.data.iloc[:split], self.data.iloc[split:]


class LinearRegression:
    def __init__(self, path='./USA_Housing.csv'):
        self.dataloader = Dataloader(path)
        self.train, self.val = self.dataloader.train_val_split()#pd
        self.W = self.initialize_w()#ndarray
        #print(self.train, self.val)
        #print(self.W)
    
    def initialize_w(self):
        w = np.random.rand(5+1,1)
        return w
    
    def gradient_descend(self, train_x, train_y, w):#one step update batch_gd, x-(n by a), y-(n by 1) ndarray
        lr = 0.0001
        gradient_temp = np.zeros((5+1,1))
         #(np.dot(train_x, w)-train_y) * np.transpose(train_x)
        for i in range(len(train_x)):   
            temp = np.dot(train_x[i,:], w) * train_x[i,:].reshape(len(train_x[i,:]), 1)
            temp2 = train_y[i] * train_x[i,:].reshape(len(train_x[i,:]), 1)
            gradient_temp += (temp - temp2)
        print('gd', gradient_temp/len(train_x))
        w_new = w - lr*gradient_temp/len(train_x)

        return w_new
    
    def sgd(self, train_x, train_y, w):#one step update batch_gd, x-(n by a), y-(n by 1) ndarray
        lr = 0.0001
        print('w', w)
        gradient_temp = np.zeros((5+1,1))
         #(np.dot(train_x, w)-train_y) * np.transpose(train_x) 
        temp = np.dot(train_x, w) * train_x.reshape(len(train_x), 1)
        temp2 = train_y * train_x.reshape(len(train_x), 1)
        gradient_temp = (temp - temp2)
        w_new = w - lr*gradient_temp
        print('new', w_new)
        print('g',gradient_temp )
        return w_new
    
    def stop_criteria(self, w1, w2):#check stop condition for gd iteractions
        tolerance = 0.001
        delta = w1-w2
        print('stop',np.sum(delta))
        if abs(np.sum(delta))<=tolerance:
            return True
        else:
            return False
        
    
    def fit_gd(self):
        epochs = 10000
        train_x = self.train[['bias','Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms','Avg. Area Number of Bedrooms', 'Area Population']].values
        train_y = self.train['Price'].values
        w = self.W
        for i in range(epochs):
            idx = random.randint(0,len(train_x))
            w_new = self.sgd(train_x[idx], train_y[idx], w)
            mse = self.get_mse(train_x, train_y, w_new)
            print(mse)
            
            if self.stop_criteria(w, w_new):
                break
            w = w_new
        self.W = w_new


    def fit(self):  
        train_x = self.train[['bias','Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms','Avg. Area Number of Bedrooms', 'Area Population']].values
        train_y = self.train['Price'].values
        temp = np.linalg.inv(np.dot(np.transpose(train_x), train_x))
        temp2 = np.dot(np.transpose(train_x),train_y)
        w = np.dot(temp,temp2)
        self.W = w
        mse = self.get_mse(train_x, train_y, w)
        print(w, mse)


    def get_mse(self, x, y, w):
        pred_y = np.dot(x, w)
        mse = np.sum((pred_y-y)*(pred_y-y))
        return mse

    def validate(self, val_x, val_y):#validation
        test_x = val_x[['bias','Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms','Avg. Area Number of Bedrooms', 'Area Population']].values()
        test_y = val_y['Price'].values()
        pred_y = np.dot(test_x, self.W)
        mse = np.sum((pred_y-test_y)*(pred_y-test_y))
        return mse
    
    def test(self, x):#test unseen data  ####add 1 later to x
        x = x[['bias','Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms','Avg. Area Number of Bedrooms', 'Area Population']].values()
        pred_y = np.dot(x, self.W)
        return pred_y
        
        
        
 
    

if __name__ == '__main__':
    lr = LinearRegression()
    lr.fit()
    #print('MSE:', lr.get_mse())