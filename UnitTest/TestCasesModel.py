#author : pierrecnalb
#copyright pierrecnalb
import os
Main_Uppercase = [
os.path.join("TestDirectory","FILE WITH É È.TXT"),
os.path.join("TestDirectory","FILE.WITH.DOTS.TXT"),
os.path.join("TestDirectory","FILE_WITH_UNDERSCORE.TXT"),
os.path.join("TestDirectory","FOLDER 2"),
os.path.join("TestDirectory","FOLDER1"),
os.path.join("TestDirectory","FOLDER1","FOLDER1-FILE1.TXT"),
os.path.join("TestDirectory","FOLDER1","FOLDER1-SUB FILE #2.TXT"),
os.path.join("TestDirectory","FOLDER1","SUB FOLDER_1"),
os.path.join("TestDirectory","FOLDER1","SUB FOLDER_1","SUB FILE 1.TXT"),
os.path.join("TestDirectory","FOLDER1","SUB FOLDER_1","SUB FILE 2.TXT"),
os.path.join("TestDirectory","FOLDER1","SUB.FOLDER 2"),
os.path.join("TestDirectory","L'APPOSTROPHE.TXT")]

Main_Lowercase = [
os.path.join("TestDirectory","file with é è.txt"),
os.path.join("TestDirectory","file.with.dots.txt"),
os.path.join("TestDirectory","file_with_underscore.txt"),
os.path.join("TestDirectory","folder 2"),
os.path.join("TestDirectory","folder1"),
os.path.join("TestDirectory","folder1","folder1-file1.txt"),
os.path.join("TestDirectory","folder1","folder1-sub file #2.txt"),
os.path.join("TestDirectory","folder1","sub folder_1"),
os.path.join("TestDirectory","folder1","sub folder_1","sub file 1.txt"),
os.path.join("TestDirectory","folder1","sub folder_1","sub file 2.txt"),
os.path.join("TestDirectory","folder1","sub.folder 2"),
os.path.join("TestDirectory","l'appostrophe.txt")]

#delete first letter for folders, second for files and third for extension.
Main_Delete = [
os.path.join("TestDirectory","fle with é è.tt"),
os.path.join("TestDirectory","fle.with.dots.tt"),
os.path.join("TestDirectory","fle_with_underscore.tt"),
os.path.join("TestDirectory","lappostrophe.tt"),
os.path.join("TestDirectory","older 2"),
os.path.join("TestDirectory","OLDER1"),
os.path.join("TestDirectory","OLDER1","flder1-file1.tt"),
os.path.join("TestDirectory","OLDER1","flder1-sub file #2.tt"),
os.path.join("TestDirectory","OLDER1","ub fOlder_1"),
os.path.join("TestDirectory","OLDER1","ub fOlder_1","sb file 1.tt"),
os.path.join("TestDirectory","OLDER1","ub fOlder_1","sb file 2.tt"),
os.path.join("TestDirectory","OLDER1","ub.FOLDER 2")]

#replace e with 3 and .txt with .ogg.
Main_Replace_without_regex = [
os.path.join("TestDirectory","fil3 with é è.ogg"),
os.path.join("TestDirectory","fil3.with.dots.ogg"),
os.path.join("TestDirectory","fil3_with_und3rscor3.ogg"),
os.path.join("TestDirectory","fold3r 2"),
os.path.join("TestDirectory","FOLDER1"),
os.path.join("TestDirectory","FOLDER1","fold3r1-fil31.ogg"),
os.path.join("TestDirectory","FOLDER1","fold3r1-sub fil3 #2.ogg"),
os.path.join("TestDirectory","FOLDER1","sub fOld3r_1"),
os.path.join("TestDirectory","FOLDER1","sub fOld3r_1","sub fil3 1.ogg"),
os.path.join("TestDirectory","FOLDER1","sub fOld3r_1","sub fil3 2.ogg"),
os.path.join("TestDirectory","FOLDER1","sub.FOLDER 2"),
os.path.join("TestDirectory","l'appostroph3.ogg")]

#Insert A at position 0 for folder, position 3 for files and position 99 for extension.
Main_Insert = [
os.path.join("TestDirectory","Afolder 2"),
os.path.join("TestDirectory","AFOLDER1"),
os.path.join("TestDirectory","AFOLDER1","Asub fOlder_1"),
os.path.join("TestDirectory","AFOLDER1","Asub fOlder_1","subA file 1.txtA"),
os.path.join("TestDirectory","AFOLDER1","Asub fOlder_1","subA file 2.txtA"),
os.path.join("TestDirectory","AFOLDER1","Asub.FOLDER 2"),
os.path.join("TestDirectory","AFOLDER1","folAder1-file1.txtA"),
os.path.join("TestDirectory","AFOLDER1","folAder1-sub file #2.txtA"),
os.path.join("TestDirectory","filAe with é è.txtA"),
os.path.join("TestDirectory","filAe.with.dots.txtA"),
os.path.join("TestDirectory","filAe_with_underscore.txtA"),
os.path.join("TestDirectory","l'aAppostrophe.txtA")]

#Name all folders 'folder', files 'file' and extensions '.ext'.
Main_CustomName = [
os.path.join("TestDirectory","file (1).ext"),
os.path.join("TestDirectory","file (2).ext"),
os.path.join("TestDirectory","file (3).ext"),
os.path.join("TestDirectory","file.ext"),
os.path.join("TestDirectory","folder"),
os.path.join("TestDirectory","folder (1)"),
os.path.join("TestDirectory","folder (1)","file (1).ext"),
os.path.join("TestDirectory","folder (1)","file.ext"),
os.path.join("TestDirectory","folder (1)","folder"),
os.path.join("TestDirectory","folder (1)","folder/file (1).ext"),
os.path.join("TestDirectory","folder (1)","folder/file.ext"),
os.path.join("TestDirectory","folder (1)","folder (1)")]

#use lowercase foldername for folders, uppercase foldername for files and untouched foldername for extensions.
Main_FolderName = [
os.path.join("TestDirectory","TestDirectory"),
os.path.join("TestDirectory","TestDirectory (1)"),
os.path.join("TestDirectory","TestDirectory (1)","FOLDER1"),
os.path.join("TestDirectory","TestDirectory (1)","FOLDER1","sub fOlder_1 (1)sub fOlder_1"),
os.path.join("TestDirectory","TestDirectory (1)","FOLDER1","sub fOlder_1sub fOlder_1"),
os.path.join("TestDirectory","TestDirectory (1)","FOLDER1 (1)"),
os.path.join("TestDirectory","TestDirectory (1)","FOLDER1 (1)FOLDER1"),
os.path.join("TestDirectory","TestDirectory (1)","FOLDER1FOLDER1"),
os.path.join("TestDirectory","TestDirectory (1)TestDirectory"),
os.path.join("TestDirectory","TestDirectory (2)TestDirectory"),
os.path.join("TestDirectory","TestDirectory (3)TestDirectory"),
os.path.join("TestDirectory","TestDirectoryTestDirectory")]

#Add a prefix 'prefix ' and a suffix ' suffix'.
Main_Custom_Prefix_Suffix = [
os.path.join("TestDirectory","folder 2"),
os.path.join("TestDirectory","FOLDER1"),
os.path.join("TestDirectory","FOLDER1","prefix folder1-file1 suffix.txt"),
os.path.join("TestDirectory","FOLDER1","prefix folder1-sub file #2 suffix.txt"),
os.path.join("TestDirectory","FOLDER1","sub fOlder_1"),
os.path.join("TestDirectory","FOLDER1","sub fOlder_1","prefix sub file 1 suffix.txt"),
os.path.join("TestDirectory","FOLDER1","sub fOlder_1","prefix sub file 2 suffix.txt"),
os.path.join("TestDirectory","FOLDER1","sub.FOLDER 2"),
os.path.join("TestDirectory","prefix file with é è suffix.txt"),
os.path.join("TestDirectory","prefix file.with.dots suffix.txt"),
os.path.join("TestDirectory","prefix file_with_underscore suffix.txt"),
os.path.join("TestDirectory","prefix l'appostrophe suffix.txt")]

#Add prefix with foldername and one suffix with foldername.
Main_FolderName_Prefix_Suffix = [
os.path.join("TestDirectory","folder 2"),
os.path.join("TestDirectory","FOLDER1"),
os.path.join("TestDirectory","FOLDER1","FOLDER1folder1-file1FOLDER1.txt"),
os.path.join("TestDirectory","FOLDER1","FOLDER1folder1-sub file #2FOLDER1.txt"),
os.path.join("TestDirectory","FOLDER1","sub fOlder_1"),
os.path.join("TestDirectory","FOLDER1","sub fOlder_1","sub fOlder_1sub file 1sub fOlder_1.txt"),
os.path.join("TestDirectory","FOLDER1","sub fOlder_1","sub fOlder_1sub file 2sub fOlder_1.txt"),
os.path.join("TestDirectory","FOLDER1","sub.FOLDER 2"),
os.path.join("TestDirectory","TestDirectoryfile with é èTestDirectory.txt"),
os.path.join("TestDirectory","TestDirectoryfile.with.dotsTestDirectory.txt"),
os.path.join("TestDirectory","TestDirectoryfile_with_underscoreTestDirectory.txt"),
os.path.join("TestDirectory","TestDirectoryl'appostropheTestDirectory.txt")]

#Folder with counter from 0 and inc = 1, prefix from 2 and inc = 4. Sorted by name.
Main_Counter_Name_Sort = [
os.path.join("TestDirectory","0"),
os.path.join("TestDirectory","1"),
os.path.join("TestDirectory","1","0"),
os.path.join("TestDirectory","1","0","2sub file 1.txt"),
os.path.join("TestDirectory","1","0","6sub file 2.txt"),
os.path.join("TestDirectory","1","1"),
os.path.join("TestDirectory","1","2folder1-file1.txt"),
os.path.join("TestDirectory","1","6folder1-sub file #2.txt"),
os.path.join("TestDirectory","10file_with_underscore.txt"),
os.path.join("TestDirectory","14l'appostrophe.txt"),
os.path.join("TestDirectory","2file with é è.txt"),
os.path.join("TestDirectory","6file.with.dots.txt")]

#Folder with counter from 0 and inc = 1, file from 0 and inc = 1. Sorted by name in reverse order.
Main_Counter_Reverse_Name_Sort = [
os.path.join("TestDirectory","3.txt"),
os.path.join("TestDirectory","2.txt"),
os.path.join("TestDirectory","1.txt"),
os.path.join("TestDirectory","1"),
os.path.join("TestDirectory","0.txt"),
os.path.join("TestDirectory","0"),
os.path.join("TestDirectory","0","1.txt"),
os.path.join("TestDirectory","0","1"),
os.path.join("TestDirectory","0","1","1.txt"),
os.path.join("TestDirectory","0","1","0.txt"),
os.path.join("TestDirectory","0","0.txt"),
os.path.join("TestDirectory","0","0")]

#Folder with counter from 0 and inc = 1, file from 0 and inc = 1. Sorted by size.
Main_Counter_Size_Sort = [
os.path.join("TestDirectory","0.txt"),
os.path.join("TestDirectory","1.txt"),
os.path.join("TestDirectory","2.txt"),
os.path.join("TestDirectory","3.txt"),
os.path.join("TestDirectory","0"),
os.path.join("TestDirectory","1"),
os.path.join("TestDirectory","1","0.txt"),
os.path.join("TestDirectory","1","1.txt"),
os.path.join("TestDirectory","1","0"),
os.path.join("TestDirectory","1","1"),
os.path.join("TestDirectory","1","1","1.txt"),
os.path.join("TestDirectory","1","1","0.txt")]

