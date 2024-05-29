########################################
# Generate profile lists of example data
########################################

out_dir=`realpath ${1}`
mkdir -p $out_dir/estimate_group_priors/profile_list/training_set
mkdir -p $out_dir/generate_individual_parcellations/profile_list/test_set
mkdir -p $out_dir/generate_individual_parcellations/profile_list/validation_set

for sess in {1..5}; do
    for sub in {1..30}; do
        lh_profile="$/home/pbfs18/Documents/shuqi_code/data_bases/bsc_numbered_output/generate_profiles_and_ini_params/profiles/sub${sub}/sess${sess}/lh.sub${sub}_sess${sess}_fsaverage5_roifsaverage3.surf2surf_profile.nii.gz"

        echo $lh_profile >> $out_dir/estimate_group_priors/profile_list/training_set/lh_sess${sess}.txt
        echo $lh_profile >> $out_dir/generate_individual_parcellations/profile_list/validation_set/lh_sess${sess}.txt

        rh_profile="$/home/pbfs18/Documents/shuqi_code/data_bases/bsc_numbered_output/generate_profiles_and_ini_params/profiles/sub${sub}/sess${sess}/rh.sub${sub}_sess${sess}_fsaverage5_roifsaverage3.surf2surf_profile.nii.gz"

        echo $rh_profile >> $out_dir/estimate_group_priors/profile_list/training_set/rh_sess${sess}.txt
        echo $rh_profile >> $out_dir/generate_individual_parcellations/profile_list/validation_set/rh_sess${sess}.txt
    done
done
