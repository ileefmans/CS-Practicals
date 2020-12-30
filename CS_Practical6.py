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
        self.feature, self.label = self.get_feature_label()
        self.normalize()
        self.bias()

    def drop_address(self):
        self.data.drop(columns=["Address"], inplace=True)

    def get_feature_label(self):
        label = pd.DataFrame(self.data.Price)
        feature = self.data.drop(columns=["Price"])
        return feature, label

    def normalize(self):
        self.label = (self.label - self.label.min()) / (
            self.label.max() - self.label.min()
        )
        self.feature = (self.feature - self.feature.min()) / (
            self.feature.max() - self.feature.min()
        )
        # self.label = np.array(self.label).reshape(self.length, 1)
        # self.feature = np.array(self.feature)

    def bias(self):

        # bias = np.ones((self.length, 1))
        # self.feature = np.concatenate((self.feature, bias), axis = 1)

        bias = [1 for i in range(self.length)]
        self.feature["bias"] = bias

    def train_val_split(self):

        train_idx = random.sample(list(range(self.length)), 3500)

        train_feature = np.array(
            self.feature.loc[self.feature.index.isin(train_idx), :]
        )
        train_label = np.array(
            self.label.loc[self.label.index.isin(train_idx), :]
        ).reshape(3500, 1)
        val_feature = np.array(self.feature.loc[~self.feature.index.isin(train_idx), :])
        val_label = np.array(
            self.label.loc[~self.label.index.isin(train_idx), :]
        ).reshape(1500, 1)

        return (
            (train_feature, train_label),
            (val_feature, val_label),
            self.feature.columns,
        )


class LinearRegression:
    def __init__(self, path="./USA_Housing.csv"):
        self.dataloader = Dataloader(path)
        self.train, self.val, self.columns = self.dataloader.train_val_split()
        self.beta = None
        self.mse = None

    def fit(self):

        # TRAIN
        # ------------------------------------------------------------
        X = self.train[0]
        X_ = np.transpose(X)
        y = self.train[1]

        self.beta = np.matmul(np.matmul(np.linalg.inv(np.matmul(X_, X)), X_), y)

        y_hat = np.matmul(X, self.beta)

        train_error = (np.linalg.norm(y - y_hat) ** 2) * (1 / y.shape[0])

        # ----------------------------------------------------------------

        # VAL
        X_val = self.val[0]
        y_val = self.val[1]

        y_hat_val = np.matmul(X_val, self.beta)

        val_error = (np.linalg.norm(y_val - y_hat_val) ** 2) * (1 / y_val.shape[0])
        self.mse = val_error

        print(
            "\nRESULTS:\n\nTRAIN ERROR: {} \nVAL ERROR: {}\n \n".format(
                train_error, val_error
            )
        )

        # -----------------------------------------------------------

        # RE-FIT ON BOTH TRAIN AND VAL SET

        X_whole = np.concatenate((X, X_val), axis=0)
        y_whole = np.concatenate((y, y_val), axis=0)
        X_whole_ = np.transpose(X_whole)

        self.beta = np.matmul(
            np.matmul(np.linalg.inv(np.matmul(X_whole_, X_whole)), X_whole_), y_whole
        )

    def get_mse(self):
        return self.mse

    def summary(self):
        display = pd.DataFrame(["Coef:"])
        display.rename(columns={0: "  "}, inplace=True)
        # display.rename(columns = {0:self.columns[0]}, inplace=True)
        for i in range(len(self.columns)):
            # if i!=0:
            display[self.columns[i]] = self.beta[i]
        print(display)

    def predict(self, X):
        """X and y should be numpy arrays, X should have a column of 1s for bias"""
        y_hat = np.matmul(X, self.beta)

        return y_hat


if __name__ == "__main__":

    lr = LinearRegression()

    lr.fit()
    lr.summary()

    print("MSE:", lr.get_mse())
