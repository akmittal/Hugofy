#!/bin/bash

while getopts r:m:d: OPT
do
  case $OPT in
    "r" ) FLG_G="TRUE" ; REPOSITORY="$OPTARG" ;;
    "m" ) FLG_M="TRUE" ; COMMIT_MESSAGE="$OPTARG" ;;
    "d" ) FLG_D="TRUE" ; DIRECTORY="$OPTARG" ;;
  esac
done

cd $DIRECTORY

echo -e "\033[0;32mDeploying updates to GitHub...\033[0m"

# Build the project.
hugo

# Add changes to git.
git add -A

# Commit changes.
msg="rebuilding site `date`"
if [ FLG_M ]
  then msg=$COMMIT_MESSAGE
fi
git commit -m "$msg"
# Push source and build repos.
remote_repository="origin"
if [ FLG_M ]
  then remote_repository=$REPOSITORY
fi
git push $remote_repository master
git subtree push --prefix=public $remote_repository gh-pages
