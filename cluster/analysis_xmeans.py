import os
import pickle

import numpy as np

from cluster import Cluster

from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer, random_center_initializer
from pyclustering.cluster.kmeans import kmeans
from pyclustering.cluster.xmeans import xmeans
from pyclustering.utils.metric import type_metric, distance_metric
from pyclustering.cluster import cluster_visualizer_multidim

if __name__ == "__main__":
    prefix = "data"
    kmenas_result_path = "xmeans_weight-1_xmeans_object.pickle"
    datapath = "xmeans_weight-1_data.pickle"

    kmeans_filepath = os.path.join(prefix, kmenas_result_path)
    kmeans_datapath = os.path.join(prefix, datapath)

    with open(kmeans_filepath, "rb") as f:
        x_means_obj = pickle.load(f)

    with open(kmeans_datapath, "rb") as f:
        data = pickle.load(f)

    normalized_concat_vec = data["normalized_concat_vec"]

    # print(dir(kmeans_obj))
    centers = x_means_obj.get_centers()
    clusters = x_means_obj.get_clusters()
    # print(len(centers))
    # for i in range(10):
    #     print(len(clusters[i]))
    
    k = len(centers)
    print("TOTAL K : {}".format(k))
    for idx in range(k):
        print("CLUSTER K -> {}".format(idx))
        center = np.array(centers[idx], dtype=np.float64)
        distances = []
        for cluster_idx in clusters[idx]:
            #point = normalized_concat_vec[cluster_idx]
            point = np.array(data["embedding_vec"][cluster_idx], dtype=np.float64)
       
            distance = np.linalg.norm(center - point, 2)
            distances.append(distance)

        distances = np.array(distances, dtype=np.float64)
        if len(distances) == 0:
            print("distances is 0")
            continue
        
        top_k = 20
        if len(distances) >= 21:
            elements_idxs = np.argpartition(distances, top_k)
            elements_idxs = elements_idxs[:top_k]
        else:
            elements_idxs = [i for i in range(len(distances))]

        for elements_idx in elements_idxs:
            region = data["region"][elements_idx]
            text = data["text"][elements_idx]
            preprocessed = data["preprocessed"][elements_idx]

            #print("----------------------------------------")
            print(preprocessed)
            print(text, end="\n\n")
            #print("----------------------------------------")
        print("Scale of Groups -> {}".format(len(distances)))
        print("========================================", end="\n\n")
