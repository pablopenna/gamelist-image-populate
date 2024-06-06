import xml.etree.ElementTree as ElementTree
import argparse
import sys
import os
import shutil
from pathlib import Path

def _initParameterParser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description='What the program does',
        epilog='Text at the bottom of help'
    )
    parser.add_argument(
        "--folder", 
        help="A folder which contains the ROMs and gamelist.xml to update", 
        required=True
    )
    parser.add_argument(
        "--gamelist-file", 
        help="The name of the gamelist file",
        default="gamelist.xml",
        required=False
    )
    return parser

def _getTargetFileFromArguments(folderPath: str, fileName: str):
    return os.path.join(folderPath, fileName)

def _backupOriginalFile(filepath: str):
    shutil.copy2(filepath, filepath+".bak")

def _openGamelistAsXml(filepath: str):
    return ElementTree.parse(filepath)

def _getGameListFromXmlRoot(root: ElementTree.Element):
    return root.iter("game")

def _getNameFromGameEntry(gameEntry: ElementTree.Element):
    return gameEntry.find("name").text

def _getPathFromGameEntry(gameEntry: ElementTree.Element):
    return gameEntry.find("path").text

def _getFilenameFromGameEntry(gameEntry: ElementTree.Element):
    gamePath = Path(_getPathFromGameEntry(gameEntry))
    return gamePath.stem

def _getImageFromGameEntry(gameEntry: ElementTree.Element):
    return gameEntry.find("image")

def _doesGameEntryHasImageTag(gameEntry: ElementTree.Element):
    return _getImageFromGameEntry(gameEntry) != None

def _processGameEntry(baseFolder:str, gameEntry: ElementTree.Element):
    if _doesGameEntryHasImageTag(gameEntry):
        return
    _addImageToGameEntry(baseFolder, gameEntry)

def _addImageToGameEntry(baseFolder:str, gameEntry: ElementTree.Element):
    imagePath = _getImagePathForGame(baseFolder, gameEntry)
    if imagePath != None:
        image = ElementTree.SubElement(gameEntry, "image")
        image.text = imagePath

def _getImagePathForGame(baseFolder:str, gameEntry: ElementTree.Element):
    imageFilePath = _getFilepathForImageMatchingGameFilename(
        baseFolder, 
        gameEntry
    ) or _getFilepathForImageMatchingGameName(
        baseFolder, 
        gameEntry
    )
    if imageFilePath == None:
        print("Could not find existing image for {}".format(_getNameFromGameEntry(gameEntry)))
    else:
        print("Found image at {} for {}".format(imageFilePath, _getNameFromGameEntry(gameEntry)))
        imageFilePath = _makeFilepathRelative(imageFilePath, baseFolder)
        print("Transformed to relative path: {}".format(imageFilePath))
    return imageFilePath

def _getFilepathForImageMatchingGameName(baseFolder:str, gameEntry: ElementTree.Element):
    return _getFilepathForImageWithName(baseFolder, _getNameFromGameEntry(gameEntry))

def _getFilepathForImageMatchingGameFilename(baseFolder:str, gameEntry: ElementTree.Element):
    return _getFilepathForImageWithName(baseFolder, _getFilenameFromGameEntry(gameEntry))

def _getFilepathForImageWithName(baseFolder:str, name: str):
    extension = ".png"
    imagesFolderName = "images"
    imagePath = os.path.join(baseFolder, imagesFolderName, name + extension)
    print("Trying path {}".format(imagePath))
    return imagePath if Path(imagePath).exists() else None

def _makeFilepathRelative(filepath: str, baseFolder: str):
    return "./{}".format(os.path.relpath(filepath, baseFolder))

def _removeImageFromGameEntry(gameEntry: ElementTree.Element):
    imageTag = _getImageFromGameEntry(gameEntry)
    gameEntry.remove(imageTag)

if __name__ == "__main__":
    argParser = _initParameterParser()
    args = argParser.parse_args()
    
    baseFolder = os.path.join(os.getcwd(), args.folder)
    filepath = _getTargetFileFromArguments(args.folder, args.gamelist_file)
    _backupOriginalFile(filepath)

    gamelistXml = _openGamelistAsXml(filepath)
    root = gamelistXml.getroot()
    print(root)

    for game in _getGameListFromXmlRoot(root):
        _processGameEntry(baseFolder, game)
        #_removeImageFromGameEntry(game)

    gamelistXml.write(filepath)



