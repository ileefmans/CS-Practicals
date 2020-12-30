import csv
import random
import math
import operator
import pandas as pd


#data loading option 1
# with open('iris.data', 'rb') as csvfile:
#     lines = csv.reader(csvfile)
#     for row in lines:
#         print ', '.join(row)
#or
#data loading option 2
def loadData() :
    # 0 setosa	1 versicolor 2 virginica
    data = pd.read_csv('iris.csv')
    data.columns = ['seplen', 'sepwid', 'petlen', 'petwid', 'label']
    return data  


# Rescale between 0-1
def rescale(data):
	rescale_list = []
	columns = data.columns
	for i in columns:
		if i!="label":
			data[i] = data[i]/data[i].max()

# Function for Kfold CV
def KfoldCV(data, k):

	fold_size = round(len(data)/k)

	total_accuracy = 0

	for fold in range(k):
		if fold == 0:
			val = data.iloc[:fold_size]
			train = data.iloc[fold_size:]
		elif fold<(k-1):
			val = data.iloc[fold_size*fold: fold_size*(fold+1)]
			train = pd.concat([data.iloc[:fold_size*fold], data.iloc[fold_size*(fold+1):]], ignore_index=True)     
		else:
			val = data.iloc[fold_size*fold:]
			train = data.iloc[:fold*fold_size]

		knn = KNN(train, val, "label", k)

		predictions = knn.forward()
		
		val["predictions"] = predictions

		accuracy = ((val.label == val.predictions).sum())/len(val)

		total_accuracy+=accuracy

	return total_accuracy/k


	



class KNN:
	def __init__(self, data, val_data, label_column_name, k):
		self.label_name = label_column_name
		self.data = data
		self.k = k
		self.val_data = val_data

	def distance(self, a, b):
		diff = a-b
		sum_of_squares = 0
		for i in diff:
			sum_of_squares+= i**2
		return sum_of_squares**(1/2)

	def compare(self, point, candidates):
		

		

		dist_list = []
		for i in range(len(candidates)):
				#candidate to compare to 
				candidate = candidates.iloc[i,:-1]

				dist_list.append((self.distance(point, candidate), i))


		dist_list.sort()

		idxes = list(map(lambda x: x[1], dist_list[:self.k]))
		
		nearest_neighbors = self.data.loc[self.data.index.isin(idxes),:]

		assigned_label = nearest_neighbors.label.value_counts().idxmax()
		
		return assigned_label

		

	def forward(self):
		predictions = []
		for i in range(len(self.val_data)):
			point = self.val_data.iloc[i,:-1]
			

			predictions.append(self.compare(point, self.data))

		return predictions




		












if __name__ =="__main__":

	data = loadData()    

	accuracy = KfoldCV(data, 10)
        
	print('Accuracy: %.3f%%' % (accuracy))




