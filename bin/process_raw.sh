#!/bin/bash

raw_repo=$1
target_repo=$2

if [ ! -d "$raw_repo" ]; then
  echo "$raw_repo doesn't exist !!!"
  exist 1
fi

if [ ! -d "$target_repo" ]; then
  mkdir -p "$target_repo"
fi

raw_repo_pattern=`sed "s/\//\\\//g" <<< "$raw_repo"`

for video_path in $(find "$raw_repo" -name "*.mp4"); do
  target_path=`sed 's/mp4/flac/' <<< "${video_path/$raw_repo_pattern/$target_repo}"`
  target_folder=`dirname "$target_path"`
  if [ ! -d "$target_folder" ]; then
    mkdir -p "$target_folder"
  fi
  echo "processing $video_path to $target_folder"
  ffmpeg -i "$video_path" -sample_fmt s16 -ac 1 -ar 16000  -vn "$target_path"
done



