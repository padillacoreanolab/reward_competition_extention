
#!/bin/bash
input_directory=/scratch/back_up/reward_competition_extention/standard_reward_competition

for full_path in ${input_directory}/*/*/*.h264; do
    echo Currently working on: ${full_path}
    dir_name=$(dirname ${full_path})
    file_name=${full_path##*/}
    base_name="${file_name%.h264}"

    echo Directory: ${dir_name}
    echo File Name: ${file_name}
    echo Base Name: ${base_name}

    mp4_out_path=${dir_name}/${base_name}.original.mp4
    echo Converting h264 to mp4
    ffmpeg -framerate 24 -i ${full_path} -c copy ${mp4_out_path}
    echo Reencoding mp4
    ffmpeg -y -i ${mp4_out_path} -c:v libx264 -pix_fmt yuv420p -preset superfast -crf 23 ${dir_name}/${base_name}.fixed.mp4

done

echo All Done!


