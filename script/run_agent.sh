#!bin/bash



sample_dir=$(readlink -f ../.) 

echo $sample_dir

export LD_LIBRARY_PATH="$sample_dir/facedetectionapp/hiaiapp/lib:$LD_LIBRARY_PATH"
cd $sample_dir/facedetectionapp/
python main.py


