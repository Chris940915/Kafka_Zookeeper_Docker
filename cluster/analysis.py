import os
import pickle

import numpy as np
import json
from pprint import pprint
from cluster import Cluster

from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer, random_center_initializer
from pyclustering.cluster.kmeans import kmeans
from pyclustering.utils.metric import type_metric, distance_metric
from pyclustering.cluster import cluster_visualizer_multidim

if __name__ == "__main__":
    prefix = "data"
    kmenas_result_path = "k-5_weight-1_kmeans_object.pickle"
    datapath = "k-5_weight-1_data.pickle"

    kmeans_filepath = os.path.join(prefix, kmenas_result_path)
    kmeans_datapath = os.path.join(prefix, datapath)

    with open(kmeans_filepath, "rb") as f:
        k_means_obj = pickle.load(f)

    with open(kmeans_datapath, "rb") as f:
        data = pickle.load(f)

    normalized_concat_vec = data["normalized_concat_vec"]

    # print(dir(kmeans_obj))
    centers = k_means_obj.get_centers()
    clusters = k_means_obj.get_clusters()
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
        
        """
        top_k = 10
        if len(distances) >= 10:
            elements_idxs = np.argpartition(distances, top_k)
            elements_idxs = elements_idxs[:top_k]
        else:
            elements_idxs = [i for i in range(len(distances))]
        """
        elements_idxs = [i for i in range(len(distances))]
        vocabulary = {} 
        for elements_idx in elements_idxs:
            region = data["region"][elements_idx]
            text = data["text"][elements_idx]
            preprocessed = data["preprocessed"][elements_idx]

            preprocessed = preprocessed[1:-1].replace(" ", "").replace("'", "").split(",")
            
            for word in preprocessed:
                if word in ["amp"]:
                    continue
                if word not in vocabulary.keys():
                    vocabulary[word] = 1
                else: 
                    vocabulary[word] += 1
            #print("----------------------------------------")
            #print(preprocessed)
            #print(text, end="\n\n")
            #print("----------------------------------------")
        
        max_val = 0
        min_val = 200
        for key in vocabulary:
            if vocabulary[key] > max_val:
                max_val = vocabulary[key]

            if vocabulary[key] < min_val:
                min_val = vocabulary[key]

        vocabulary["max"] = max_val
        vocabulary["min"] = min_val

        for key in vocabulary:
            if key in ["max", "min"]:
                continue
            vocabulary[key] = ((vocabulary[key] - min_val) / max_val)
        
        for key in vocabulary:                            
            if 0.01 <= vocabulary[key] <= 0.1:
                print("{} : {}".format(key, vocabulary[key]))

        print("\n\n\n")
        for key in vocabulary:
            if key in ["floyd", "black", "george", "blm"]:                
                print("{}:{}".format(key, vocabulary[key]))
        
        print("Scale of Groups -> {}".format(len(distances)))
        print("========================================", end="\n\n")
