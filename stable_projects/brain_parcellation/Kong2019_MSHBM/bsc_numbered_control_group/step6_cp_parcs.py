"""Written by Shuqi Ke shuqik[at]andrew.cmu.edu
"""
from pathlib import Path
from copy import deepcopy
from argparse import ArgumentParser, Namespace
import numpy as np
import h5py
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import min_weight_full_bipartite_matching
from scipy.optimize import linear_sum_assignment


NUM_NETWORKS = 17


def get_args():
    args = ArgumentParser()
    args.add_argument("--parc1", type=str)
    args.add_argument("--parc2", type=str)
    args = args.parse_args()
    args.parc1 = Path(args.parc1)
    args.parc2 = Path(args.parc2)
    return args


def build_bipartite_graph(parc1, parc2):
    bi_graph = np.zeros((NUM_NETWORKS+1, NUM_NETWORKS+1), dtype=int)
    idx1 = []
    idx2 = []
    for i in range(NUM_NETWORKS+1):
        idx1.append(set(np.where(parc1 == i)[0]))
        idx2.append(set(np.where(parc2 == i)[0]))
    for i in range(NUM_NETWORKS+1):
        for j in range(NUM_NETWORKS+1):
            bi_graph[i,j] = len(idx1[i].intersection(idx2[j]))
    return bi_graph


def evaluate_best_match(parc1, parc2):
    """
    Use the modified Jonker-Volgenant algorithm with no initialization.
    Reference:
    [1] DF Crouse. On implementing 2D rectangular assignment algorithms. IEEE Transactions on Aerospace and Electric Systems, 52(4):1679-1696, August 2016, DOI:10.1109/TAES.2016.140952
    """
    bi_graph = build_bipartite_graph(parc1, parc2)
    assign_result = linear_sum_assignment(-np.asarray(bi_graph, dtype=int))
    num_assign_vertex = 0
    for i in range(NUM_NETWORKS+1):
        num_assign_vertex += bi_graph[assign_result[0][i],assign_result[1][i]]
    return num_assign_vertex / len(parc1)


if __name__ == "__main__":
    args = get_args()
    with h5py.File(args.parc1, "r") as file:
        lh_parc1  = np.squeeze(np.asarray(file["lh_labels"], dtype=int))
        rh_parc1  = np.squeeze(np.asarray(file["rh_labels"], dtype=int))
    with h5py.File(args.parc2, "r") as file:
        lh_parc2 = np.squeeze(np.asarray(file["lh_labels"], dtype=int))
        rh_parc2  = np.squeeze(np.asarray(file["rh_labels"], dtype=int))
    print(np.mean([
        evaluate_best_match(lh_parc1, lh_parc2),
        evaluate_best_match(rh_parc1, rh_parc2),
    ]))
