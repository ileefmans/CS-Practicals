import numpy as np 
import pandas as pd 
from sklearn.model_selection import train_test_split

# for loading data only
import torch 




class CreateDataset(torch.utils.data.Dataset):

	"""
		Class to create torch data set to be used in train/test loader
	"""

	def __init__(self, path, train=True):

		"""
			Args:

				path (string): Path to data

				train (boolean): True if creating training set, False if creating test set 

		"""

		# Read dataset
		self.dataframe = pd.read_csv(path)

		# Seperate features and target
		self.X = self.dataframe.iloc[:,:-1]
		self.y = self.dataframe.iloc[:,-1]

		# Train/Test split with set random state so split will be the same each time
		self.X_train, self.X_test,  self. y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.33, random_state=42)

		# Convert to numpy arrays
		self.X_train, self.X_test, self.y_train, self.y_test = np.array(self.X_train), np.array(self.X_test), np.array(self.y_train), np.array(self.y_test)

		# Initialize train boolean
		self.train = train

	def __len__(self):
		"""
			Method overiding length of dataset
		"""
		if self.train:
			return self.X_train.shape[0]
		else:
			return self.X_test.shape[0]

	def __getitem__(self, index):

		"""
			Method overiding indexing of an observation 
		"""

		if self.train:
			return self.X_train[index,:], self.y_train[index]
		else:
			return self.X_test[index,:], self.y_test[index]

		










if __name__ == "__main__":
	data = CreateDataset("https://raw.githubusercontent.com/jbrownlee/Datasets/master/wheat-seeds.csv")
	


	#print(data.X_train.shape, data.X_test.shape, data.y_train.shape, data.y_test.shape)

	#print(data[0])





