#!/bin/bash
project_dir=/nancy/projects/reward_competition_extention
experiment_dir=/nancy/projects/reward_competition_extention/results/2023_06_15_sleap_preprocessing

round_number=round_1

cd ${experiment_dir}

model_directory=/nancy/projects/reward_competition_extention/models/akmese_cohort/baseline_medium_rf.bottomup

video_directory=/nancy/projects/reward_competition_extention/data/videos/reencoded

# Inference
echo "inference ${video_directory}"
for full_path in ${video_directory}/*/*fixed.mp4; do
    echo ${full_path}

    dir_name=$(dirname ${full_path})
    file_name=${full_path##*/}
    base_name="${file_name%.mp4}"

    sleap-track ${full_path} --tracking.tracker flow \
    --tracking.similarity iou --tracking.match greedy \
    --tracking.clean_instance_count 2 \
    --tracking.target_instance_count 2 \
    -m ${model_directory} \
    -o ${experiment_dir}/proc/predicted_frames/${round_number}/${base_name}.2_subj.${round_number}.predicted_frames.slp

   sleap-track ${full_path} --tracking.tracker flow \
    --tracking.similarity iou --tracking.match greedy \
    --tracking.clean_instance_count 1 \
    --tracking.target_instance_count 1 \
    -m ${model_directory} \
    -o ${experiment_dir}/proc/predicted_frames/${round_number}/${base_name}.1_subj.${round_number}.predicted_frames.slp

done

echo All Done!