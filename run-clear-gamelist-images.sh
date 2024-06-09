#!/bin/bash

# Go to the folder where this script is located
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

python3 GamelistImagePopulate/main.py --folder /roms2/ --clear-images > gamelist-image-populate.log 2>&1
echo "Finished!" >> gamelist-image-populate.log
