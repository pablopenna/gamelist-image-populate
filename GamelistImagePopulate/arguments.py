import argparse
from sys import argv

def _initParameterParser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=argv[0],
        description="Processes one or more folders containing a gamelist XML file in the EmulationStation format. When doing so, searches for images in subfolders and if it finds matching images for the game entries in the XML file, it adds the configuration needed to use said images.",
        epilog="""Examples:
        `gamelist-image-populate --folder /roms2/cps1 --process-single-folder`
        `gamelist-image-populate --folder /roms2`
        `gamelist-image-populate --folder /roms2/cps1 --process-single-folder --clear-images`
        """
    )
    parser.add_argument(
        "--folder", 
        help="The parent folder which contains all the ROM folders. Usually located at /roms or /roms2. If '--process-single-folder' is provided, to program will only process the folder provided and will not search subfolders for gamelist XML files.", 
        required=True
    )
    parser.add_argument(
        "--images-folder-name", 
        help="The name of the subfolder which holds the images per folder scanned. Defaults to 'images'",
        default="images",
        required=False
    )
    parser.add_argument(
        "--gamelist-file", 
        help="The name of the gamelist file. Defaults to gamelist.xml",
        default="gamelist.xml",
        required=False
    )
    parser.add_argument(
        "--dry-run", 
        help="For testing. Does not modify any file. Defaults to False",
        action="store_const",
        const=True,
        default=False,
        required=False
    )
    parser.add_argument(
        "--clear-images", 
        help="Removes all image entries from the file instead. Defaults to false",
        action="store_const",
        const=True,
        default=False,
        required=False
    )
    parser.add_argument(
        "--overwrite", 
        help="Overwrites existing image entries in the file. Defaults to false",
        action="store_const",
        const=True,
        default=False,
        required=False
    )
    parser.add_argument(
        "--process-single-folder", 
        help="Only processes the provided folder instead of recursively searching all subfolders for gamelist.xml files. This way, a single platform can be processed. Defaults to False",
        action="store_const",
        const=True,
        default=False,
        required=False
    )
    return parser

def parseParameters():
    parser = _initParameterParser()
    arguments = parser.parse_args()
    print("[INFO] arguments: " + str(arguments))
    return arguments
