#!/bin/sh

BASE_DIR=$(dirname "$0")


cd $BASE_DIR


current_file=$(date +"%F.txt")

# sleep 120 # cron must set to 23:50 daily

git add .
git commit -m "Added history/${current_file}"
#git push 

echo "history/${current_file}" >> .gitignore
git add .
git commit -m "Ignore history/{current_file}"
