#!/bin/sh
BASEDIR=$(dirname "$0")
echo "Starting cronjob at $(date)" 

echo "Starting extract phase"
python3 $BASEDIR/extract/main.py
echo "Extract phase finished"

echo "Starting load phase"
python3 $BASEDIR/load/mongodb/main.py
echo "Load phase finished"

echo "Cleaning up the volume mount"
python3 $BASEDIR/extract/clean_mount.py
echo "Done cleaning up the volume mount"


echo "Finished cronjob at $(date)" 