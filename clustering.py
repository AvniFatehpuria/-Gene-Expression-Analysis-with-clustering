"""
Library of clustering algorithms - these algorithms expect a list of lists as input
"""
from math import sqrt
import numpy as np
from scipy.stats import multivariate_normal

def initMeans(data, k):
     np.random.shuffle(data)
     return data[:k]

def eStep(data, k, means, alphas, sigmas):
    h_array = []
    #data.shape = (data.size) # just making it a 1d array to make indexing easy
    for i in range(len(data)):
        hvalues = np.empty(k)
        denominator = 0.0
        for j in range(k):
             denominator += (alphas[j]*multivariate_normal.pdf(data[i], means[j], sigmas))
        for j in range(k):
             hvalues[j] = (alphas[j]*multivariate_normal.pdf(data[i], means[j], sigmas)/denominator)
        h_array.append(hvalues)
    return h_array

def normalization(data):
    for j in range(len(data[0])):
        sum = 0
        for i in range(len(data)):
            sum += data[i][j]**2
        length = sqrt(sum)
        for i in range(len(data)):
            data[i][j] = data[i][j]/length
    return data


def mStep(probabilities, means, alphas, data, k):
    probarray = np.array(probabilities)
    denominators= probarray.sum(axis=0)
    #print means
    for j in range(k):
        numerator = 0
        for i in range(len(data)):
            numerator += probarray[i,j]*data[i]
        means[j] = (numerator/denominators[j])
        #print means[j]
        #print numerator/denominators[j]
    totalprob = denominators.sum()
    for j in range(k):
        alphas[j] = denominators[j]/totalprob
    #print means
    return (means, alphas)

def SSE(means, points):
     
     sum = 0
     for i in range(len(means)):
          for x in range(len(points)):
               distance = dist(means[i],points[x])
               print means[i], points[x]
               print distance
               sum += distance**2
     return sum

def AIC(sse,k,m):
     return sse + 2*(k*m)
               
               
def dist(x, y) :
    #function that returns the euclidian distance
    square_Dist = 0

    for i in range(len(x)-1):
        square_Dist += (float(x[i]) - float(y[i]))**2
    print square_Dist
    return sqrt(square_Dist)

def EM(dataset, k):
    npdata = np.array(dataset)
    means = initMeans(npdata, k)
    alphas = [(1.0/k)]*k
    npdata = np.array(dataset)
    cov = np.cov((npdata.T))
    sigmas = np.diag(cov)
    for i in range(50):
        #print i
        #print means
        oldmeans = np.copy(means)
        #print means, alphas
        probabilities = eStep(npdata, k, means, alphas, sigmas)
        (means, alphas) = mStep(probabilities, means, alphas, npdata, k)
        #print means, alphas
        #print oldmeans, means
        if abs(np.sum(np.subtract(oldmeans, means))) < .0001:
            break
    return (means, np.array(probabilities))

if __name__ == "__main__":
    data = [[4,1],[4,3],[6,2],[8,8]]
    data = normalization(data)
    #print data
    k = 2
    EM(data, k)
