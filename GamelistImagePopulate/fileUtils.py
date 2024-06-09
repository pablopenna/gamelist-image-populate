import os
import shutil
from pathlib import Path

backupFileExtension = ".bak"

def getSubdirectories(filepath: str):
    for it in os.scandir(filepath):
        if it.is_dir():
            yield it

def doesFileExists(filepath: str):
    return Path(filepath).exists()

def doesFileBackupExists(filepath: str):
    return Path(_getBackupFile(filepath)).exists()

def backupFile(filepath: str):
    backupFile = _getBackupFile(filepath)
    print("[INFO] Backing up file {} to {}".format(filepath, backupFile))
    shutil.copy2(filepath, backupFile)

def _getBackupFile(file:str):
    return file + backupFileExtension

def getFilePathFrom(folderPath: str, fileName: str):
    return os.path.join(folderPath, fileName)

def getFilePathForImageWithName(baseFolder:str, imagesFolderName: str, imageFileName: str, imageExtension: str):
    imagePath = os.path.join(baseFolder, imagesFolderName, imageFileName + imageExtension)
    imagePath = getFilePathFrom(os.path.join(baseFolder, imagesFolderName), imageFileName+imageExtension)
    print("[INFO] Trying path {}".format(imagePath))
    return imagePath if doesFileExists(imagePath) else None

def makeFilePathRelative(filepath: str, baseFolder: str):
    relativePath = os.path.join(os.path.curdir, os.path.relpath(filepath, baseFolder))
    return relativePath if not isFilePathRelative(filepath) else filepath

def isFilePathRelative(filepath: str):
    return not os.path.isabs(filepath)

def printFileContents(filepath: str):
    with open(filepath) as reader:
        print("================")
        print(reader.read())
        print("================")