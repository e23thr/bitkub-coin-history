#!/bin/sh

BASE_DIR=$(dirname "$0")


cd $BASE_DIR


current_file=$(date +"%FT%H.txt")

sleep 120 # cron must set to hourly minus 1 minute

git add data_history/${current_file}
git commit -m "Added data_history/${current_file}"
echo "data_history/${current_file}" >> .gitignore
git add .gitignore
git commit -m "Ignore data_history/${current_file}"
git push
git update-index --assume-unchanged data_history/${current_file}
rm data_history/$current_file # to keep disk free
