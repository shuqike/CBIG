"""Written by Shuqi Ke shuqik[at]andrew.cmu.edu
"""
from pathlib import Path
from argparse import ArgumentParser, Namespace
import numpy as np


def get_args():
    args = ArgumentParser()
    args.add_argument(
        "--bold-time-span", type=int, default=120,
        help="The number of time points in the BOLD data"
    )
    args.add_argument("--out-dir", type=str)
    """
    out-dir:
    The input censor lists are assumed to exist in the following way:
    <out_dir>/data_list/censor_list/sub?_sess?.txt
    Each line in above file corresponds to the full path of the censor
    list of each run. For example, if the subject 1 has 2 sessions and
    session 2 has 2 runs then there should be:
    <out_dir>/data_list/censor_list/sub1_sess1.txt
    <out_dir>/data_list/censor_list/sub1_sess2.txt
    and sub1_sess2.txt should have two lines:
    <path_to_fMRI_data>/<censor_filename_of_run_1>
    <path_to_fMRI_data>/<censor_filename_of_run_2>
    Please note that the censor file shouled be a text file contains a
    single column with binary numbers and its length is the number of 
    timepoints. The outliers are indicated by 0s and will be flaged out
    when compute the profiles. If the user don't want to (or don't have)
    the censor lists, please leave the <out_dir>/data_list/censor_list as
    an exmpty folder."
    """
    args = args.parse_args()
    args.out_dir = Path(args.out_dir)
    return args


if __name__ == "__main__":
    args = get_args()
    args.censor_dir = args.out_dir / "generate_profiles_and_ini_params" / "data_list" / "censor_list"
    args.censor_dir.mkdir(parents=True, exist_ok=True)
    for sub_id in range(30):
        sub = str(int(sub_id+1))
        for sess in [1, 2]:
            # Generate dummy censor data
            data_dir = Path(f"/home/pbfs18/Documents/shuqi_code/data_bases/BSC_Numbered/{sub.strip()}/ses-01/qc")
            data_dir.mkdir(parents=True, exist_ok=True)
            data_path = data_dir / f"sub{sub.strip()}_sess{sess}_bld002_FDRMS0.2_DVARS50_motion_outliers.txt"
            with data_path.open(mode="w", encoding="utf-8") as data_file:
                data_file.writelines("\n".join(["1"] * args.bold_time_span))
            # Generate censor list file
            censor_list_path = args.censor_dir / f"sub{sub_id+1}_sess{sess}.txt"
            with censor_list_path.open(mode="w", encoding="utf-8") as censor_list_file:
                censor_list_file.write(str(data_path))
