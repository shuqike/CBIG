"""Written by Shuqi Ke shuqik[at]andrew.cmu.edu
TODO: add FC computation
"""
from pathlib import Path
from argparse import ArgumentParser, Namespace


def get_args():
    args = ArgumentParser()
    args.add_argument(
        "--seed-mesh", type=str, default="fsaverage3",
        help="The resolution of seed regions, e.g. 'fsaverage3'. If the data is in fsaverage surface (e.g. fsaverage5/6), the seed_mesh should be defined by fsaverage surface in the same resolution as the data space, or lower resolution, e.g. fsaverage3/4.")
    args.add_argument(
        "--targ-mesh", type=str, default="fsaverage5",
        help="The surface space of fMRI data, e.g. 'fsaverage5'. The data is allowed to be in fsaverage space (e.g. fsaverage4/5/6, fsaverage)."
    )
    args.add_argument(
        "--sub-list-file", type=str,
        help="The path of a txt file containing a list of subjects"
    )
    args.add_argument(
        "--threshold", type=float, default=0.1,
        help="The threshold for binarization (string, e.g. '0.1'). threshold=0.1 means indices with the highest 10% correlations will be set to 1, others will be set to 0."
    )
    args.add_argument(
        "--split", action="store_true",
        help="This flag is used to split 1 session into 2 sub-sessions to create two profiles for each sub-session. The two sub-sessions will be the first half and the other half. The flag should be used if the user want to apply MS-HBM model on 1 session fMRI data."
    )
    args.add_argument("--out-dir", type=str)
    """
    out-dir:
    The input fMRI data lists are assumed to exist in the following way:
    For data in fsaverage space:
    <out_dir>/data_list/fMRI_list/lh_sub?_sess?.txt
    <out_dir>/data_list/fMRI_list/rh_sub?_sess?.txt
    Each line in above files corresponds to the full path of the fMRI
    data of each run. For example, if the subject 1 in fsaverage5 has 2 sessions and session 2 has 2 runs then there should be:
    <out_dir>/data_list/fMRI_list/lh_sub1_sess1.txt
    <out_dir>/data_list/fMRI_list/rh_sub1_sess1.txt
    <out_dir>/data_list/fMRI_list/lh_sub1_sess2.txt
    <out_dir>/data_list/fMRI_list/rh_sub1_sess2.txt
    and lh_sub1_sess2.txt should have two lines:
    <path_to_fMRI_data>/lh*<fMRI_filename_of_run_1>.nii.gz
    <path_to_fMRI_data>/lh*<fMRI_filename_of_run_2>.nii.gz

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
    args.sub_list_file = Path(args.sub_list_file)
    args.out_dir = Path(args.out_dir)
    return args


def generate_index(mesh: str) -> int:
    if "fsaverage" in mesh:
        return 10*(2**(2*int(mesh[-1])))+2
    else:
        raise NotImplementedError


def generate_profile(args: Namespace, sub: str, sess: int):
    profile_dir = args.out_dir / "profiles" / ("sub" + sub) / f"sess{sess}"
    profile_dir.mkdir(parents=True, exist_ok=True)
    if "fsaverage" in args.targ_mesh:
        fMRI_list = (
            args.out_dir / "data_list" / "fMRI_list" / f"lh_sub{sub}_sess{sess}.txt",
            args.out_dir / "data_list" / "fMRI_list" / f"rh_sub{sub}_sess{sess}.txt"
        )
    else:
        raise NotImplementedError


if __name__ == "__main__":
    args = get_args()
    with args.sub_list_file.open(mode="r", encoding="utf-8") as sub_list_file:
        sub_list = sub_list_file.readlines()
        for sub in sub_list:
            for sess in [1, 2, 3]:
                generate_profile(args, sub, sess)
