#!/bin/bash
root_path=`pwd`
weeks_delta=1
author='LyuLumos'

for folder in `ls -I *.sh $root_path`
do
cd "${root_path}/${folder}"
# [[ ! `ls -a` =~ ".git" ]] || echo 'Not a git repository!'
if [[ ! "$(git rev-parse --git-dir 2> /dev/null)" ]]; then echo "${folder} is NOT a git repository!" && continue; fi
git log --all --pretty=format:"- ${folder}@%h: %s (%cn)" --since=${weeks_delta}.weeks #--author=${author}
done

echo "Generate form `date -d -"${weeks_delta} week" +%Y-%m-%d` to `date +%Y-%m-%d`"
