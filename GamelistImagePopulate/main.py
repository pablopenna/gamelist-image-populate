from arguments import parseParameters
from xmlProcessing import processAllSubfolders, processSingleFolder

if __name__ == "__main__":
    args = parseParameters()
    
    if args.process_single_folder:
        processSingleFolder(
            folder = args.folder, 
            gamelistFile = args.gamelist_file, 
            clearImages = args.clear_images, 
            dryrun = args.dry_run, 
            overwrite = args.overwrite,
            imageFolderName=args.images_folder_name
        )
    else:
        processAllSubfolders(
            folder = args.folder, 
            gamelistFile = args.gamelist_file, 
            clearImages = args.clear_images, 
            dryrun = args.dry_run, 
            overwrite = args.overwrite,
            imageFolderName=args.images_folder_name
        )
