#!/bin/bash
. "$(greadlink -m "$0/../config.sh")"

audio_repo=$1
target_repo=$2

if [ ! -d "$audio_repo" ]; then
  echo "$audio_repo doesn't exist !!!"
  exist 1
fi

if [ ! -d "$target_repo" ]; then
  mkdir -p "$target_repo"
fi

audio_repo_pattern=`sed "s/\//\\\//g" <<< "$audio_repo"`

for audio_path in $(find "$audio_repo" -name "*.flac"); do
  target_path=`sed 's/flac/txt/' <<< "${audio_path/$audio_repo_pattern/$target_repo}"`
  target_folder=`dirname "$target_path"`
  if [ ! -d "$target_folder" ]; then
    mkdir -p "$target_folder"
  fi
  echo "processing $audio_path to $target_path"
  python $ROOT/python/api_clients/speech.py "${@:3}" \
    --output_file "$target_path" \
    $audio_path
done
