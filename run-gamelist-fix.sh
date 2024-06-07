#!/bin/bash

# Go to the folder where this script is located
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

python3 gamelist-image-populate.py --folder /roms2/cps1 > run-gamelist-fix.log 2>&1
echo "Finished!" >> run-gamelist-fix.log
