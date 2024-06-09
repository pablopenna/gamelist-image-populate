import xml.etree.ElementTree as ElementTree
from pathlib import Path

from fileUtils import backupFile, doesFileBackupExists, doesFileExists, getFilePathForImageWithName, getFilePathFrom, getSubdirectories, makeFilePathRelative

defaultImageExtension = ".png"

def processAllSubfolders(folder: str, gamelistFile: str, clearImages: bool, dryrun: bool, overwrite: bool, imageFolderName: str):
    for subdirectory in getSubdirectories(folder):
        processSingleFolder(subdirectory, gamelistFile, clearImages, dryrun, overwrite, imageFolderName)

def processSingleFolder(folder: str, gamelistFile: str, clearImages: bool, dryrun: bool, overwrite: bool, imageFolderName: str):
    print("[INFO] processing folder {} with gamelistFileName={}, clearImages={}, dryrun={}, overwrite={}, imageFolderName={}".format(folder, gamelistFile, clearImages, dryrun, overwrite, imageFolderName))
    pathToGamelistFile = getFilePathFrom(folder, gamelistFile)
    if not doesFileExists(pathToGamelistFile):
        print("[ERROR] Could not find gamelist file at %s. Skipping..." % pathToGamelistFile)
        return
    
    if not doesFileBackupExists(pathToGamelistFile):
        backupFile(pathToGamelistFile)
    else:
        print("[INFO] Backup file for {} already exists. Skipping backup.".format(pathToGamelistFile))
 
    gamelistXml = _openGamelistAsXml(pathToGamelistFile)
    root = gamelistXml.getroot()

    for game in _getGameEntriesFromXmlRoot(root):
        if clearImages:
            removeImageFromGameEntry(game)
        else:
            _processGameEntry(folder, game, overwrite, imageFolderName)

    if not dryrun:
        gamelistXml.write(pathToGamelistFile)

def _openGamelistAsXml(filepath: str):
    return ElementTree.parse(filepath)

def _getGameEntriesFromXmlRoot(root: ElementTree.Element):
    if root.tag != "gameList":
        print("[ERROR] XML format not supported (%s). Please provide an EmulationStation gamelist.xml" % root.tag)
        return iter(())
    return root.iter("game")

def _processGameEntry(baseFolder:str, gameEntry: ElementTree.Element, overwrite: bool, imageFolderName: str):
    if _doesGameEntryHasImageTag(gameEntry) and not overwrite:
        print("[WARN] Game {} already has image entry and overwrite flag is False. Skipping...".format(_getGameNameFromGameEntry(gameEntry)))
        return
    _addImageToGameEntry(baseFolder, gameEntry, imageFolderName)

def removeImageFromGameEntry(gameEntry: ElementTree.Element):
    imageTag = _getImageFromGameEntry(gameEntry)
    if imageTag != None:
        gameEntry.remove(imageTag)

def _getGameNameFromGameEntry(gameEntry: ElementTree.Element):
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

def _addImageToGameEntry(baseFolder:str, gameEntry: ElementTree.Element, imageFolderName: str):
    imagePath = _getImagePathForGame(baseFolder, gameEntry, imageFolderName)
    if imagePath != None:
        image = ElementTree.SubElement(gameEntry, "image")
        image.text = imagePath

def _getImagePathForGame(baseFolder:str, gameEntry: ElementTree.Element, imageFolderName: str):
    imageFilePath = _getFilepathForImageMatchingGameFilename(
        baseFolder, 
        gameEntry,
        imageFolderName
    ) or _getFilepathForImageMatchingGameName(
        baseFolder, 
        gameEntry,
        imageFolderName
    )
    if imageFilePath == None:
        print("[WARN] Could not find existing image for {}".format(_getGameNameFromGameEntry(gameEntry)))
    else:
        print("[INFO] Found image at {} for {}".format(imageFilePath, _getGameNameFromGameEntry(gameEntry)))
        imageFilePath = makeFilePathRelative(imageFilePath, baseFolder)
        print("[INFO] Transformed to relative path: {}".format(imageFilePath))
    return imageFilePath

def _getFilepathForImageMatchingGameName(baseFolder:str, gameEntry: ElementTree.Element, imageFolderName: str):
    return getFilePathForImageWithName(baseFolder, imageFolderName, _getGameNameFromGameEntry(gameEntry), defaultImageExtension)

def _getFilepathForImageMatchingGameFilename(baseFolder:str, gameEntry: ElementTree.Element, imageFolderName: str):
    return getFilePathForImageWithName(baseFolder, imageFolderName, _getFilenameFromGameEntry(gameEntry), defaultImageExtension)
