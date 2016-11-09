#!/bin/bash

raw_repo=$1
target_repo=$2

chunk_duration=20

if [ ! -d "$raw_repo" ]; then
  echo "$raw_repo doesn't exist !!!"
  exist 1
fi

if [ ! -d "$target_repo" ]; then
  mkdir -p "$target_repo"
fi

raw_repo_pattern=`sed "s/\//\\\//g" <<< "$raw_repo"`
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 video/cn-ZH/news/single_clear_.mp4
for video_path in $(find "$raw_repo" -name "*.mp4"); do
  target_path=`sed 's/\.mp4//' <<< "${video_path/$raw_repo_pattern/$target_repo}"`
  target_folder=`dirname "$target_path"`
  if [ ! -d "$target_folder" ]; then
    mkdir -p "$target_folder"
  fi
  video_length=$( ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $video_path )
  video_length=${video_length%.*}
  start_time=0
  echo "$video_length"
  while (( $start_time < $video_length ))
  do
    echo "processing $video_path to $target_folder""_$start_time.flac"
    ffmpeg "${@:3}"  -i "$video_path" -sample_fmt s16 -ac 1 \
           -ar 16000 -vn -ss "$start_time" -t "$chunk_duration" \
           "$target_path""_$start_time.flac"
    start_time=$[$start_time + $chunk_duration]
  done
done
