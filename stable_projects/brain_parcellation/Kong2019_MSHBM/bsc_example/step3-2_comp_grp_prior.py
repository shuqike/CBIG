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
    args.add_argument("--out-dir", type=str)
    args.add_argument("--num-rand-init", type=int)
    args.add_argument("--num-iter", type=int)
    args = args.parse_args()
    args.out_dir = Path(args.out_dir)
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
    return idx1, idx2, bi_graph


def evaluate_best_match(parc1, parc2):
    """
    LAPJVsp algorithm (scipy.sparse.csgraph.min_weight_full_bipartite_matching) doesn't work
    Use the modified Jonker-Volgenant algorithm with no initialization.
    Reference:
    [1] DF Crouse. On implementing 2D rectangular assignment algorithms. IEEE Transactions on Aerospace and Electric Systems, 52(4):1679-1696, August 2016, DOI:10.1109/TAES.2016.140952
    """
    idx1, idx2, bi_graph = build_bipartite_graph(parc1, parc2)
    # print([len(i) for i in idx1])
    # print("\n".join(["\t".join([str(j) for j in i]) for i in bi_graph.tolist()]))
    # match_result = min_weight_full_bipartite_matching(csr_matrix(bi_graph), maximize=True)
    # num_match_vertex = 0
    # for i in range(NUM_NETWORKS+1):
    #     num_match_vertex += bi_graph[match_result[0][i],match_result[1][i]]
    assign_result = linear_sum_assignment(-np.asarray(bi_graph, dtype=int))
    num_assign_vertex = 0
    for i in range(NUM_NETWORKS+1):
        num_assign_vertex += bi_graph[assign_result[0][i],assign_result[1][i]]
    # return num_match_vertex, len(parc1), num_match_vertex / len(parc1), match_result[1], num_assign_vertex, len(parc1), num_assign_vertex / len(parc1), assign_result[1]
    return f"dice={num_assign_vertex / len(parc1)}\nmatch={assign_result[1]}"


def dice(x, y):
    return np.sum(np.asarray(x) == np.asarray(y))


def switch_50(x, a, b):
    x = np.asarray(x)
    x[x == a] += 50
    x[x == b] = a
    x[x == a+50] = b
    return x


def permute_parc(x, y):
    mx_dice = dice(x, y)
    flag = True
    id_track = np.arange(NUM_NETWORKS+1)
    while flag:
        flag = False
        for i in range(NUM_NETWORKS+1):
            for j in range(i+1, NUM_NETWORKS+1):
                tmp = switch_50(deepcopy(y), i, j)
                if dice(x, tmp) > mx_dice:
                    y = tmp
                    mx_dice = dice(x, y)
                    id_track[i], id_track[j] = id_track[j], id_track[i]
                    flag = True
                    break
            if flag: break
    return f"dice={mx_dice / len(x)}\n", f"match={id_track}"


if __name__ == "__main__":
    args = get_args()
    lh_parcs = []
    for grp_name in ["s1_e2", "s3_e4"]:
        with h5py.File(args.out_dir / "generate_profiles_and_ini_params" / "group" / f"group_{grp_name}_r{args.num_rand_init}_iter{args.num_iter}.mat", "r") as file:
            lh_parcs.append(np.squeeze(np.asarray(file["lh_labels"], dtype=int)))
    print(evaluate_best_match(lh_parcs[0], lh_parcs[1]))
    # print(permute_parc(lh_parcs[0], lh_parcs[1]))
