while read sub; do
    for run in {1,2,3,4,5}; do
        # left hemisphere
        s_bold="/home/pbfs18/Documents/shuqi_code/data_bases/BSC_DeepPrep_2317/${sub}/ses-01/func/${sub}_ses-01_task-rest_run-0${run}_hemi-L_space-fsaverage6_desc-postproc_bold.nii.gz"
        t_bold="/home/pbfs18/Documents/shuqi_code/data_bases/BSC_DeepPrep_2317/${sub}/ses-01/func/${sub}_ses-01_task-rest_run-0${run}_hemi-L_space-fsaverage5_desc-postproc_bold.nii.gz"
        mri_surf2surf --hemi lh --srcsubject fsaverage6 --sval ${s_bold} --trgsubject fsaverage5 --tval ${t_bold}

        # right hemisphere
        s_bold="/home/pbfs18/Documents/shuqi_code/data_bases/BSC_DeepPrep_2317/${sub}/ses-01/func/${sub}_ses-01_task-rest_run-0${run}_hemi-R_space-fsaverage6_desc-postproc_bold.nii.gz"
        t_bold="/home/pbfs18/Documents/shuqi_code/data_bases/BSC_DeepPrep_2317/${sub}/ses-01/func/${sub}_ses-01_task-rest_run-0${run}_hemi-R_space-fsaverage5_desc-postproc_bold.nii.gz"
        mri_surf2surf --hemi rh --srcsubject fsaverage6 --sval ${s_bold} --trgsubject fsaverage5 --tval ${t_bold}
    done
done < /home/pbfs18/Documents/shuqi_code/data_bases/BSC_DeepPrep_2317/sub_list.txt