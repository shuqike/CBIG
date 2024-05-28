#!/bin/bash

# This script will generate input data for:
# 1) group priors estimation
# 2) individual parcellation generation
# The user need to specify the output directory, which will later contain two folders:
# 1) estimate_group_priors
# 2) generate_individual_parcellations
# Written by Shuqi Ke shuqik[at]andrew.cmu.edu

##########################
# Specify output directory
##########################

out_dir=`realpath ${1}`
mkdir -p $out_dir/estimate_group_priors
mkdir -p $out_dir/generate_individual_parcellations

#########################################
# Create data lists to generate profiles
#########################################
mkdir -p $out_dir/generate_profiles_and_ini_params/data_list/fMRI_list
mkdir -p $out_dir/generate_profiles_and_ini_params/data_list/censor_list

run=1;
while read sub; do
    # fMRI data
    lh_fmri="/home/pbfs18/Documents/shuqi_code/chef-parcellation/data/BNU/${sub}/preprocess/${sub}/surf/lh.${sub}_task-rest_bold_resid_fsaverage6_sm6_fsaverage5.nii.gz"

    echo $lh_fmri >> $out_dir/generate_profiles_and_ini_params/data_list/fMRI_list/lh_sub${sub}_sess${run}.txt

    rh_fmri="/home/pbfs18/Documents/shuqi_code/chef-parcellation/data/BNU/${sub}/preprocess/${sub}/surf/rh.${sub}_task-rest_bold_resid_fsaverage6_sm6_fsaverage5.nii.gz"

    echo $rh_fmri >> $out_dir/generate_profiles_and_ini_params/data_list/fMRI_list/rh_sub${sub}_sess${run}.txt
done < /home/pbfs18/Documents/shuqi_code/chef-parcellation/data/BNU/sub_list.txt

########################################
# Generate profile lists of example data
########################################

mkdir -p $out_dir/estimate_group_priors/profile_list/training_set
mkdir -p $out_dir/generate_individual_parcellations/profile_list/test_set
mkdir -p $out_dir/generate_individual_parcellations/profile_list/validation_set
