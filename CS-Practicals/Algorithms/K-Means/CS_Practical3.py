import numpy as np
from matplotlib import pyplot as plt



class KMeans:
    def __init__(self, data):
        self.data = data

    def distance(self, p1, p2):
        return np.linalg.norm(p1-p2)

    def average(self, matrix):
        ones = np.ones((1, matrix.shape[0]))
        average = np.matmul(ones, matrix)*(1/matrix.shape[0])
        return average

    def forward(self, k, initialize=True, clusters=None):
        # Randomly select k points    NEED TO FIX  UNSUPORTED FOR THIS LARGE OF AN ARRAY

        if initialize==True:
            cluster_idx = np.random.choice(range(self.data.shape[0]), size=k)
        #Create clusters using k randomly selected points
            clusters = []
            for i in cluster_idx:
                clusters.append(self.data[i,:])

        #Need to fill in case where we are computing centroid based on clusters
        else:
            pass

    
        # Loop through data to calculate distance from clusters
        for i in range(self.data.shape[0]):
            if i not in cluster_idx:

                # find shortest distance (cluster index, distance)
                minimum = None
                for i in range(len(clusters)):
                    if clusters[i].shape ==(data.shape[1],):
                        clusters[i] = clusters[i].reshape(1,data.shape[1])
                    dist = self.distance(self.data[i,:], clusters[i][0,:])
                    if minimum ==None:
                        minimum = (i, dist)
                    elif minimum[1]>dist:
                        minimum = (i, dist)

                # concatonate data point to correct cluster
                clusters[minimum[0]] = np.concatenate((clusters[minimum[0]].reshape(-1,self.data.shape[1]), self.data[i,:].reshape(1,self.data.shape[1])), axis=0)
                #print(clusters[minimum[0]])
        return clusters













    # initialize and fit
    # Find the current cluster each data belongs to
    # Update cluster centers
    # new_cluster 

class DataGeneration:
    def ambers_random_data(self):
        np.random.seed(1)
        x = 2
        data1 = np.random.normal(size=(100, 2)) + [ x, x]
        data2 = np.random.normal(size=(100, 2)) + [ x,-x]
        data3 = np.random.normal(size=(100, 2)) + [-x,-x]
        data4 = np.random.normal(size=(100, 2)) + [-x, x]
        data  = np.concatenate((data1, data2, data3, data4))
        np.random.shuffle(data)
        return data

#plots
    #def elbow plot:
        #ax.set_xlabel("Number of Clusters")
        #ax.set_ylabel("Distortion")
        #print("Showing the elbow plot. Close the plot window to continue.")
        #plt.show()
    #def kmeans cluster plot: 
        #get num of clusters
        #ax.scatter(
        #ax.legend()
        #plt.show()
if __name__ == "__main__":
    generator = DataGeneration()
    data = generator.ambers_random_data()
    k_means = KMeans(data)
    
    print(len(k_means.forward(4)[0]))

    
    # k_means = KMeans(generator.data)
    # k_means.elbow()
    # k = input("Choose number of clusters: ")
    # k_means.initialize(int(k))
    # k_means.fit()
    # k_means.plot()