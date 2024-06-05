import xml.etree.ElementTree as ElementTree
import argparse
import sys
import os
import shutil

def initParameterParser() -> argparse.ArgumentParser:
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

def getTargetFileFromArguments(folderPath: str, fileName: str):
    return os.path.join(folderPath, fileName)

def backupOriginalFile(filepath: str):
    shutil.copy2(filepath, filepath+".bak")

def openGamelistAsXml(filepath: str):
    return ElementTree.parse(filepath)

def getGameListFromXmlRoot(root: ElementTree.Element):
    return root.iter("game")

def addImageToGameEntry(gameEntry: ElementTree.Element):
    image = ElementTree.SubElement(gameEntry, "image")
    image.text = "placeholder"
    

if __name__ == "__main__":
    print("hello world")

    argParser = initParameterParser()
    args = argParser.parse_args()
    
    filepath = getTargetFileFromArguments(args.folder, args.gamelist_file)
    backupOriginalFile(filepath)

    gamelistFile = openGamelistAsXml(filepath)
    root = gamelistFile.getroot()
    print(root)

    for game in getGameListFromXmlRoot(root):
        print("====GAME====")
        print("tag: ")
        print(game.tag)
        print("attrib: ")
        print(game.attrib)
        addImageToGameEntry(game)
        for prop in game:
            print(prop.tag)
            print(prop.attrib)
            print(prop.text)

    gamelistFile.write(filepath)



