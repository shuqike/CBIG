out_dir=`realpath ${1}`
mkdir -p $out_dir/generate_individual_parcellations/profile_list/test_set
for sess in {1..2}; do
    for sub in {1..30}; do
        lh_profile="/home/pbfs18/Documents/shuqi_code/data_bases/bsc_numbered_output_GSP_parc_control_group/generate_profiles_and_ini_params/profiles/sub${sub}/sess${sess}/lh.sub${sub}_sess${sess}_fsaverage5_roifsaverage3.surf2surf_profile.nii.gz"

        echo $lh_profile >> $out_dir/generate_individual_parcellations/profile_list/test_set/lh_sess${sess}.txt

        rh_profile="/home/pbfs18/Documents/shuqi_code/data_bases/bsc_numbered_output_GSP_parc_control_group/generate_profiles_and_ini_params/profiles/sub${sub}/sess${sess}/rh.sub${sub}_sess${sess}_fsaverage5_roifsaverage3.surf2surf_profile.nii.gz"

        echo $rh_profile >> $out_dir/generate_individual_parcellations/profile_list/test_set/rh_sess${sess}.txt
    done
done