import numpy as np 
import pandas as pd 
from sklearn.model_selection import train_test_split
import yaml

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

		

class NeuralNet:
	def __init__(self, config_path):

		"""
			Args:

				config_path (string): Path to configuration yaml file

		"""

		# Read configuration yaml
		with open(config_path) as file:
			self.config = yaml.load(file, Loader=yaml.FullLoader)

		# initialize list to store weights and biases
		self.weights = []


		# Function to initialize weights and biases
		def init_weights(in_dim, out_dim, batch_size):
			W = np.random.normal(0, 0.1, size=(in_dim, out_dim))
			b = np.random.normal(0, 0.1, size =(batch_size, out_dim))
			self.weight.append((W, b))

		# initialize weights and biases
		for i in self.config:
			if 'Linear' in i:
				init_weights(i['Linear'][0], i['Linear'][1])

	def Linear(self, x, W, b):
		"""
			Method for Linear layer
		"""
		return np.matmul(x, W) + b

	def ReLU(self,x):
		"""
			Method for ReLU activation
		"""
		return np.maximum(0, x)

	def Softmax(self, x):
		"""
			Method for Softmax activation
		"""
		return np.exp(x)/np.sum(np.exp(x))


	def forward(self, x):

		layer = 0
		for i in self.config:
			if 'Linear' in i:
				x = self.Linear(x, i['Linear'][0], i['Linear'][1])
			elif i == 'ReLU':
				x = self.ReLU(x)
			elif i == 'Softmax':
				x = self.Softmax(x)

		return x


















if __name__ == "__main__":
	data = CreateDataset("https://raw.githubusercontent.com/jbrownlee/Datasets/master/wheat-seeds.csv")
	
	nn = NeuralNet('config.yml')
	print(nn.config, '\n \n \n \n')

	for i in nn.config['Layers']:
		print('Linear'in i)

	#print(data.X_train.shape, data.X_test.shape, data.y_train.shape, data.y_test.shape)

	#print(data[0])





