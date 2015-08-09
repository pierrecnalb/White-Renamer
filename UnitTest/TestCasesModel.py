#author : pierrecnalb
#copyright pierrecnalb
import os
Main_OriginalName = [
os.path.join("TestDirectory","file with é è.txt"),
os.path.join("TestDirectory","file.with.dots.txt"),
os.path.join("TestDirectory","file_with_underscore.txt"),
os.path.join("TestDirectory","folder 2"),
os.path.join("TestDirectory","FOLDER1"),
os.path.join("TestDirectory","FOLDER1","folder1-file1.txt"),
os.path.join("TestDirectory","FOLDER1","folder1-sub file #2.txt"),
os.path.join("TestDirectory","FOLDER1","sub fOlder_1"),
os.path.join("TestDirectory","FOLDER1","sub fOlder_1","sub file 1.txt"),
os.path.join("TestDirectory","FOLDER1","sub fOlder_1","sub file 2.txt"),
os.path.join("TestDirectory","FOLDER1","sub.FOLDER 2"),
os.path.join("TestDirectory","l'appostrophe.txt")]

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

Main_TitleCase = [
os.path.join("TestDirectory","File With É È.txt"),
os.path.join("TestDirectory","File.With.Dots.txt"),
os.path.join("TestDirectory","File_With_Underscore.txt"),
os.path.join("TestDirectory","Folder 2"),
os.path.join("TestDirectory","FOLDER1"),
os.path.join("TestDirectory","FOLDER1","Folder1-File1.txt"),
os.path.join("TestDirectory","FOLDER1","Folder1-Sub File #2.txt"),
os.path.join("TestDirectory","FOLDER1","Sub FOlder_1"),
os.path.join("TestDirectory","FOLDER1","Sub FOlder_1","Sub File 1.txt"),
os.path.join("TestDirectory","FOLDER1","Sub FOlder_1","Sub File 2.txt"),
os.path.join("TestDirectory","FOLDER1","Sub.FOLDER 2"),
os.path.join("TestDirectory","L'appostrophe.txt")]
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

#Replace folder digit with 99, file "file" with "fhis" and extension word with "pdf".
Main_Replace_with_regex = [
os.path.join("TestDirectory","fhis with é è.pdf"),
os.path.join("TestDirectory","fhis.with.dots.pdf"),
os.path.join("TestDirectory","fhis_with_underscore.pdf"),
os.path.join("TestDirectory","folder 99"),
os.path.join("TestDirectory","FOLDER99"),
os.path.join("TestDirectory","FOLDER99","folder1-fhis1.pdf"),
os.path.join("TestDirectory","FOLDER99","folder1-sub fhis #2.pdf"),
os.path.join("TestDirectory","FOLDER99","sub fOlder_99"),
os.path.join("TestDirectory","FOLDER99","sub fOlder_99","sub fhis 1.pdf"),
os.path.join("TestDirectory","FOLDER99","sub fOlder_99","sub fhis 2.pdf"),
os.path.join("TestDirectory","FOLDER99","sub.FOLDER 99"),
os.path.join("TestDirectory","l'appostrophe.pdf")]

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

#use lowercase foldername for folders, uppercase foldername for files and untouched foldername f.
Main_FolderName = [
os.path.join("TestDirectory","TestDirectory"),
os.path.join("TestDirectory","TestDirectory (1)"),
os.path.join("TestDirectory","TestDirectory (1)","FOLDER1"),
os.path.join("TestDirectory","TestDirectory (1)","FOLDER1","sub fOlder_1 (1).txt"),
os.path.join("TestDirectory","TestDirectory (1)","FOLDER1","sub fOlder_1.txt"),
os.path.join("TestDirectory","TestDirectory (1)","FOLDER1 (1)"),
os.path.join("TestDirectory","TestDirectory (1)","FOLDER1 (1).txt"),
os.path.join("TestDirectory","TestDirectory (1)","FOLDER1.txt"),
os.path.join("TestDirectory","TestDirectory (1).txt"),
os.path.join("TestDirectory","TestDirectory (2).txt"),
os.path.join("TestDirectory","TestDirectory (3).txt"),
os.path.join("TestDirectory","TestDirectory.txt")]

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

#Use accents and special characters to see if the encoding is supported.
Accent_Encoding = [
os.path.join("TestDirectory","folder 2"),
os.path.join("TestDirectory","FOLDER1"),
os.path.join("TestDirectory","FOLDER1","sub fOlder_1"),
os.path.join("TestDirectory","FOLDER1","sub fOlder_1","éèùà€ç (1).txt"),
os.path.join("TestDirectory","FOLDER1","sub fOlder_1","éèùà€ç.txt"),
os.path.join("TestDirectory","FOLDER1","sub.FOLDER 2"),
os.path.join("TestDirectory","FOLDER1","éèùà€ç (1).txt"),
os.path.join("TestDirectory","FOLDER1","éèùà€ç.txt"),
os.path.join("TestDirectory","éèùà€ç (1).txt"),
os.path.join("TestDirectory","éèùà€ç (2).txt"),
os.path.join("TestDirectory","éèùà€ç (3).txt"),
os.path.join("TestDirectory","éèùà€ç.txt")]

