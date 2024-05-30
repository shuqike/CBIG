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

for run in {1,2,3}; do
    while read sub; do
        # fMRI data
        lh_fmri="/home/pbfs18/Documents/shuqi_code/data_bases/BSC_DeepPrep_2317/${sub}/ses-01/func/${sub}_ses-01_task-rest_run-0${run}_hemi-L_space-fsaverage5_desc-postproc_bold.nii.gz"

        echo $lh_fmri >> $out_dir/generate_profiles_and_ini_params/data_list/fMRI_list/lh_sub${sub}_sess${run}.txt

        rh_fmri="/home/pbfs18/Documents/shuqi_code/data_bases/BSC_DeepPrep_2317/${sub}/ses-01/func/${sub}_ses-01_task-rest_run-0${run}_hemi-R_space-fsaverage5_desc-postproc_bold.nii.gz"

        echo $rh_fmri >> $out_dir/generate_profiles_and_ini_params/data_list/fMRI_list/rh_sub${sub}_sess${run}.txt
    done < /home/pbfs18/Documents/shuqi_code/data_bases/BSC_DeepPrep_2317/sub_list.txt
done

######################################################
# Copy initialization parameters into output directory
######################################################

rsync -az $CBIG_CODE_DIR/stable_projects/brain_parcellation/Kong2019_MSHBM/examples/input/group \
$out_dir/estimate_group_priors

##############################
# Create validation fMRI lists 
##############################
mkdir -p $out_dir/generate_individual_parcellations/data_list/validation_fMRI_list

for run in {4,5}; do
    while read sub; do
        # fMRI data
        lh_fmri="/home/pbfs18/Documents/shuqi_code/data_bases/BSC_DeepPrep_2317/${sub}/ses-01/func/${sub}_ses-01_task-rest_run-0${run}_hemi-L_space-fsaverage5_desc-postproc_bold.nii.gz"

        echo $lh_fmri >> $out_dir/generate_individual_parcellations/data_list/validation_fMRI_list/lh_sub${sub}_sess${run}.txt

        rh_fmri="/home/pbfs18/Documents/shuqi_code/data_bases/BSC_DeepPrep_2317/${sub}/ses-01/func/${sub}_ses-01_task-rest_run-0${run}_hemi-R_space-fsaverage5_desc-postproc_bold.nii.gz"

        echo $rh_fmri >> $out_dir/generate_individual_parcellations/data_list/validation_fMRI_list/rh_sub${sub}_sess${run}.txt
    done < /home/pbfs18/Documents/shuqi_code/data_bases/BSC_DeepPrep_2317/sub_list.txt
done

########################################
# Generate profile lists of example data
########################################

mkdir -p $out_dir/estimate_group_priors/profile_list/training_set
mkdir -p $out_dir/generate_individual_parcellations/profile_list/test_set
mkdir -p $out_dir/generate_individual_parcellations/profile_list/validation_set
