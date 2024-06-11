# gamelist-image-populate
Process a gamelist.xml file adding image entries.
**IMPORTANT: Only works for gamelist.xml files with the EmulationStation format**

Works best with [Skraper](https://www.skraper.net/) -> on the `Gamelist` tab select `EmulationStation Gamelist.xml`.

### Requirements
1. A EmulationStation instalation, either on your PC or on a handheld device.
2. If running this from your PC, python 3.x (tried and tested with 3.7 and 3.13). WSL is recommended if using Windows.
3. If running on a game console device (e.g. R36S), it will only work if the OS has python 3.x installed.
4. The images for each system need to be on a subfolder of said system. e.g. If my CPS1 ROMs are under /roms2/cps1 the images will need to be under that (e.g. /roms2/cps1/images/). A folder with the name `images` is recommended. If not, you can provide a custom name via the `--images-folder-name` argument.
5. The images need to have the same name as the game file or the name game (without taking into account the extension). e.g. If I have a "King of Dragons" ROM file named `kod.zip` and the name of the game in the gamelist.xml file is `King of Dragons (rev. 2)`, the image name will need to be `kod.png` or `King of Dragons (rev. 2).png`.

Python versions lower than 3.7 might not work.

Tried and tested on a Panel 4 R36S.

### Instructions for running the script
Can be used either from your PC pointing to the mounted sdcard of your game console or directly from within the game console itself.

#### On PC
1. Mount the file system where all the EmulationStation ROMs and gamelist.xml are.
2. Run the script providing the path to said filesystem via the `--folder` argument.

As an example, given a dual SD setup where all my ROMs are in a separate SD card from the OS and the latter mounts on letter `E:`, I would run the following:

```
python GamelistImagePopulate/main.py --folder /mnt/e/
```

#### On a Game Console

1. Copy the `GamelistImagePopulate/` folder under `tools/`. 
2. Also create a `.sh` file containing the command you want to run. You can check `run-gamelist-image-populate.sh` or `run-clear-gamelist-images.sh` for examples. In the end the result would be something like:
```
/
- roms2/
  - tools/
    - run-gamelist-image-populate.sh
    - GamelistImagePopulate/
```
3. Run the script created in the previous step from the console. If you have ArkOS, go to `Config > Tools` and choose the script. If you followed the example of the sample scripts provided, you can check the log file to see if it run successfully.
4. At least in ArkOS, you will need to :
  * Go into one of the systems (e.g. CPS1)
  * Press Select (Options menu)
  * Choose `UPDATE GAMES LISTS`

After that, the games should display the images you have under your images folder.

#### Accepted arguments
```
usage: GamelistImagePopulate/main.py [-h] --folder FOLDER
                                     [--images-folder-name IMAGES_FOLDER_NAME]
                                     [--gamelist-file GAMELIST_FILE]
                                     [--use-default-image] [--dry-run]
                                     [--clear-images] [--overwrite]
                                     [--process-single-folder]

Processes one or more folders containing a gamelist XML file in the
EmulationStation format. When doing so, searches for images in subfolders and
if it finds matching images for the game entries in the XML file, it adds the
configuration needed to use said images.

optional arguments:
  -h, --help            show this help message and exit

  --folder FOLDER       The parent folder which contains all the ROM folders.
                        Usually located at /roms or /roms2. If '--process-
                        single-folder' is provided, to program will only
                        process the folder provided and will not search
                        subfolders for gamelist XML files.

  --images-folder-name IMAGES_FOLDER_NAME
                        The name of the subfolder which holds the images per
                        folder scanned. Defaults to 'images'

  --gamelist-file GAMELIST_FILE
                        The name of the gamelist file. Defaults to
                        gamelist.xml

  --use-default-image   If no image is found for a game, it will use a
                        default.png image in the images folder (if it exists).
                        Defaults to False

  --dry-run             For testing. Does not modify any file. Defaults to
                        False

  --clear-images        Removes all image entries from the file instead.
                        Defaults to False

  --overwrite           Overwrites existing image entries in the gamelist.xml file.
                        Defaults to False

  --process-single-folder
                        Only processes the provided folder instead of
                        recursively searching all subfolders for gamelist.xml
                        files. This way, a single platform can be processed.
                        Defaults to False

Examples: 

python GamelistImagePopulate/main.py --folder /roms2/cps1 --process-single-folder
python GamelistImagePopulate/main.py --folder /roms2
python GamelistImagePopulate/main.py --folder /roms2/cps1 --process-single-folder --clear-images
``` 

### Multiple images for same game setup
1. Run Skraper for different regions (e.g. US and JP) setting a different output folder for each
2. Have different scripts under `tools/` with which to run GamelistImagePopulate, one for each region. This can be done via the `images-folder-name` argument.
3. Run the script for the region you want to apply the images for.
4. Profit?

### Checking if python is installed on your handheld device
Create a script like the following and run it from your console. You can do so by placing the script under `tools/`. It should be listed when going to `Config > Tools`.

```
#!/bin/bash

# Go to the folder where this script is located
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

python --version > python.log
python3 --version >> python.log
```

After running the script, check the contents of the log file.