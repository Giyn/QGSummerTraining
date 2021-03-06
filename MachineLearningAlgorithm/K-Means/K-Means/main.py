# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 17:29:34 2020

@author: Giyn
"""

import pandas as pd
import numpy as np
from KMeans import KMeansClassifier
import matplotlib.pyplot as plt


if __name__=="__main__":
    data_X = pd.read_csv(r"iris.csv")
    data_X = data_X.drop(data_X.columns[4], axis=1)
    data_X = np.array(data_X)

    k = 3
    clf = KMeansClassifier(k) # 实例化KMeansClassifier类
    clf.fit(data_X) # 训练模型
    cents = clf._centroids
    labels = clf._labels
    sse = clf._sse
    colors = ['r','y','b']
    for i in range(k):
        index = np.nonzero(labels==i)[0]
        x0 = data_X[index, 0]
        x1 = data_X[index, 1]
        y_i = i
        for j in range(len(x0)):
            plt.scatter(x0[j], x1[j], color=colors[i])
        plt.scatter(cents[i,0], cents[i,1], marker='x', color=colors[i], linewidths=7)

    plt.title("SSE={:.2f}".format(sse))
    plt.axis([4.2,8.2,1.8,4.6])
    outname = "./K-Means.png"
    plt.savefig(outname)
    plt.show()