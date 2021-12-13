#!/bin/sh

BASE_DIR=$(dirname "$0")


cd $BASE_DIR


current_file=$(date +"%FT%H.txt")

sleep 120 # cron must set to hourly minus 1 minute

git add .
git commit -m "Added data_history/${current_file}"
git push

echo "data_history/${current_file}" >> .gitignore
git add .
git commit -m "Ignore data_history/${current_file}"
git push

rm data_history/$current_file # to keep disk free
