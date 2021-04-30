import argparse
import os
import numpy as np
import copy
import csv
import pickle

from pprint import pprint

from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer, random_center_initializer
from pyclustering.cluster.kmeans import kmeans
from pyclustering.utils.metric import type_metric, distance_metric
from pyclustering.cluster import cluster_visualizer_multidim

"""
parser = argparse.ArgumentParser(description='Kmenas')
parser.add_argument('--k', type=int, help='number of k in kmeans')
parser.add_argument('--coord_weight', type=int, help='weight of coordinates')
parser.add_argument('--name', type=str, help='pickle object name for saving')

args = parser.parse_args()
"""


class Cluster():
    def __init__(self,
                 data,
                 amount_centers=5,
                 distance_metric="l2",
                 display=False):

        self.amount_centers = amount_centers
        self.display = display
        self.distance_metric = distance_metric
        self.data = data

    def initialize(self):
        amount_centers = self.amount_centers
        amount_candidates = kmeans_plusplus_initializer.FARTHEST_CENTER_CANDIDATE
        data = copy.deepcopy(self.data)
        centroid_initializer = kmeans_plusplus_initializer(data=data,
                                                           amount_centers=amount_centers,
                                                           amount_candidates=amount_candidates)

        self.centroid_initializer = centroid_initializer.initialize()

    @staticmethod
    def cosine_similarity(point1, point2):
        print(point1.shape)
        print(point2.shape)

        if len(point1.shape) > 1:
            channels, _ = point1.shape

            results = []
            for idx in range(channels):

                point1_1 = point1[idx,:]
                point2_1 = point2[idx,:]
                cosine_sim = np.dot(point1_1, point2_1)/(np.linalg.norm(point1_1)*np.linalg.norm(point2_1))
                results.append(np.array([cosine_sim]))
            
            results = tuple(results)
            concat_result = np.concatenate(results)
            return concat_result
        else:
            return np.dot(point1, point2)/(np.linalg.norm(point1)*np.linalg.norm(point2))

    def process(self):

        self.initialize()
        data = copy.deepcopy(self.data)

        if self.distance_metric == "l2":
            metric = distance_metric(type_metric.EUCLIDEAN)
        elif self.distance_metric == "l1":
            metric = distance_metric(type_metric.MANHATTAN)
        elif self.distance_metric == "cosine":
            metric = distance_metric(type_metric.USER_DEFINED, func=self.cosine_similarity)

        kmeans_obj = kmeans(data=data,
                            initial_centers=self.centroid_initializer,
                            metric=metric)
        kmeans_obj.process()

        """
        if self.display:
            visualizer = cluster_visualizer_multidim()
            visualizer.append_clusters(
                clusters=clusters, data=self.data)
            visualizer.append_cluster(centers, marker='*', markersize=20)
            visualizer.show()
        """

        return kmeans_obj


if __name__ == "__main__":

    # k = args.k
    # coord_weight = args.coord_weight
    # name = args.name

    coord_weights = [i for i in range(1, 11)]
    ks = [i for i in range(5, 200)]
    scale_factor = 1

    fast_text_dict = {}
    with open('raw/final_cut_sent_0613.csv', 'r') as csvfile:
        fast_text_reader = csv.reader(csvfile)
        for idx, rows in enumerate(fast_text_reader):
            if idx == 0:
                for row in rows:
                    fast_text_dict[row] = []
                fast_text_dict["normalized_concat_vec"] = []

            else:
                if not rows[3]:
                    continue
                fast_text_dict["id"].append(rows[0])
                fast_text_dict["created_at"].append(rows[1])
                fast_text_dict["text"].append(rows[2])

                # Coordinates string to float list
                str_sliced_coordinates = rows[3][1:-1]
                str_removed_newline_coordinates = rows[3][1:-1].rstrip()
                str_splited_coordinates = str_removed_newline_coordinates.split(
                    ",")
                str_splited_coordinates = [str_coord.replace(" ", "") for str_coord in str_splited_coordinates]
                try:
                    float_coordinates_list = [float(str_coordinate) for str_coordinate in str_splited_coordinates]
                except:
                    print(str_splited_coordinates)
                    exit()
                fast_text_dict["coordinates"].append(float_coordinates_list)
                fast_text_dict["region"].append(rows[4])
                fast_text_dict["img_url"].append(rows[5])
                fast_text_dict["preprocessed"].append(rows[6])

                # Embedding Vector string to float list
                str_sliced_embedding_vec = rows[7][1:-1]
                str_removed_newline_embedding_vec = str_sliced_embedding_vec.rstrip()
                str_splited_embedding_vec = str_removed_newline_embedding_vec.split(
                    " ")
                str_removed_space_embedding_vec = []
                for str_vec in str_splited_embedding_vec:
                    if str_vec != '':
                        str_removed_space_embedding_vec.append(
                            str_vec.rstrip())
                float_embedding_vec_list = [
                    scale_factor * float(str_vec) for str_vec in str_removed_space_embedding_vec]
                #print(float_embedding_vec_list)
                #print(len(float_embedding_vec_list))
                
                fast_text_dict["embedding_vec"].append(
                    float_embedding_vec_list)

                embedding_vec_array = np.array(
                    float_embedding_vec_list, dtype=np.float64)
                coordinates_array = np.array(
                    float_coordinates_list, dtype=np.float64)
                concat_vector = np.concatenate(
                    (embedding_vec_array, coordinates_array))
                normalized_concat_vector = scale_factor * (concat_vector / 180)
                fast_text_dict["normalized_concat_vec"].append(
                    normalized_concat_vector)

    
    for coord_weight in coord_weights:

        for idx, concat_vec in enumerate(fast_text_dict["normalized_concat_vec"]):
            concat_vec[-1] = coord_weight * concat_vec[-1]
            concat_vec[-2] = coord_weight * concat_vec[-2]
            fast_text_dict["normalized_concat_vec"][idx] = concat_vec

        for k in ks:
            print("START {}-k_{}-weights".format(k, coord_weight))
            #data = fast_text_dict["normalized_concat_vec"]
            data = np.array(fast_text_dict["embedding_vec"], dtype=np.float64)
            
            k_means = Cluster(data,
                              amount_centers=k,
                              distance_metric="l1",
                              display=False)

            kmeans_result = k_means.process()

            # save
            with open('data/k-{}_weight-{}_data.pickle'.format(str(k), str(coord_weight)), 'wb') as f:
                pickle.dump(fast_text_dict, f)

            with open('data/k-{}_weight-{}_kmeans_object.pickle'.format(str(k), str(coord_weight)), 'wb') as f:
                pickle.dump(kmeans_result, f)
        exit()
