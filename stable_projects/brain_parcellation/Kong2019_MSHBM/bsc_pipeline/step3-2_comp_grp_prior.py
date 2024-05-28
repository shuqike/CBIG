"""Written by Shuqi Ke shuqik[at]andrew.cmu.edu
"""
from pathlib import Path
from copy import deepcopy
from argparse import ArgumentParser, Namespace
import numpy as np
import h5py


NUM_NETWORKS = 17


def get_args():
    args = ArgumentParser()
    args.add_argument("--out-dir", type=str)
    args.add_argument("--num-rand-init", type=int)
    args.add_argument("--num-iter", type=int)
    args = args.parse_args()
    args.out_dir = Path(args.out_dir)
    return args


def dice(x, y):
    return np.sum(np.asarray(x) == np.asarray(y))


def switch_20(x, a, b):
    x = np.asarray(x)
    x[x == a] *= 20
    x[x == b] = a
    x[x == a*20] = b
    return x


def permute_parc(x, y):
    mx_dice = dice(x, y)
    flag = True
    while flag:
        flag = False
        for i in range(NUM_NETWORKS+1):
            for j in range(i+1, NUM_NETWORKS+1):
                tmp = switch_20(deepcopy(y), i, j)
                if dice(x, tmp) > mx_dice:
                    y = tmp
                    mx_dice = dice(x, y)
                    flag = True
                    break
            if flag: break
    return mx_dice / len(x), y


if __name__ == "__main__":
    args = get_args()
    lh_parcs = []
    for grp_name in ["s1_e2", "s3_e4"]:
        with h5py.File(args.out_dir / "generate_profiles_and_ini_params" / "group" / f"group_{grp_name}_r{args.num_rand_init}_iter{args.num_iter}.mat", "r") as file:
            lh_parcs.append(np.squeeze(np.asarray(file["lh_labels"], dtype=int)))
    best_dice, lh_parcs[1] = permute_parc(lh_parcs[0], lh_parcs[1])
    print(best_dice)
