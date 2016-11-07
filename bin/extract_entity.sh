#!/bin/bash
. "$(greadlink -m "$0/../config.sh")"

text_repo=$1
target_repo=$2

if [ ! -d "$text_repo" ]; then
  echo "$text_repo doesn't exist !!!"
  exist 1
fi

if [ ! -d "$target_repo" ]; then
  mkdir -p "$target_repo"
fi

text_repo_pattern=`sed "s/\//\\\//g" <<< "$text_repo"`

for text_path in $(find "$text_repo" -name "*.txt"); do
  target_path=`sed 's/.txt/.json/' <<< "${text_path/$text_repo_pattern/$target_repo}"`
  target_folder=`dirname "$target_path"`
  if [ ! -d "$target_folder" ]; then
    mkdir -p "$target_folder"
  fi
  echo "processing $text_path to $target_path"
  python $ROOT/python/api_clients/nlp.py "${@:3}" \
    --output_file "$target_path" \
    $text_path
done
