#author : pierrecnalb
#copyright pierrecnalb
import os
Main_OriginalName = [
os.path.join("TestDirectory","file with é è.txt"),
os.path.join("TestDirectory","file.with.dots.txt"),
os.path.join("TestDirectory","file_with_underscore.txt"),
os.path.join("TestDirectory","FOLDER1"),
os.path.join("TestDirectory","FOLDER1","folder1-file1.txt"),
os.path.join("TestDirectory","FOLDER1","folder1-sub file #2.txt"),
os.path.join("TestDirectory","FOLDER1","sub fOlder_1"),
os.path.join("TestDirectory","FOLDER1","sub fOlder_1","sub file 1.txt"),
os.path.join("TestDirectory","FOLDER1","sub fOlder_1","sub file 2.txt"),
os.path.join("TestDirectory","l'appostrophe.txt")]

Main_Uppercase = [
os.path.join("TestDirectory","FILE WITH É È.TXT"),
os.path.join("TestDirectory","FILE.WITH.DOTS.TXT"),
os.path.join("TestDirectory","FILE_WITH_UNDERSCORE.TXT"),
os.path.join("TestDirectory","FOLDER1"),
os.path.join("TestDirectory","FOLDER1","FOLDER1-FILE1.TXT"),
os.path.join("TestDirectory","FOLDER1","FOLDER1-SUB FILE #2.TXT"),
os.path.join("TestDirectory","FOLDER1","SUB FOLDER_1"),
os.path.join("TestDirectory","FOLDER1","SUB FOLDER_1","SUB FILE 1.TXT"),
os.path.join("TestDirectory","FOLDER1","SUB FOLDER_1","SUB FILE 2.TXT"),
os.path.join("TestDirectory","L'APPOSTROPHE.TXT")]

Main_Lowercase = [
os.path.join("TestDirectory","file with é è.txt"),
os.path.join("TestDirectory","file.with.dots.txt"),
os.path.join("TestDirectory","file_with_underscore.txt"),
os.path.join("TestDirectory","folder1"),
os.path.join("TestDirectory","folder1","folder1-file1.txt"),
os.path.join("TestDirectory","folder1","folder1-sub file #2.txt"),
os.path.join("TestDirectory","folder1","sub folder_1"),
os.path.join("TestDirectory","folder1","sub folder_1","sub file 1.txt"),
os.path.join("TestDirectory","folder1","sub folder_1","sub file 2.txt"),
os.path.join("TestDirectory","l'appostrophe.txt")]

Main_TitleCase = [
os.path.join("TestDirectory","File With É È.txt"),
os.path.join("TestDirectory","File.With.Dots.txt"),
os.path.join("TestDirectory","File_With_Underscore.txt"),
os.path.join("TestDirectory","FOLDER1"),
os.path.join("TestDirectory","FOLDER1","Folder1-File1.txt"),
os.path.join("TestDirectory","FOLDER1","Folder1-Sub File #2.txt"),
os.path.join("TestDirectory","FOLDER1","Sub FOlder_1"),
os.path.join("TestDirectory","FOLDER1","Sub FOlder_1","Sub File 1.txt"),
os.path.join("TestDirectory","FOLDER1","Sub FOlder_1","Sub File 2.txt"),
os.path.join("TestDirectory","L'appostrophe.txt")]
#delete first letter for folders, second for files and third for extension.
Main_Delete = [
os.path.join("TestDirectory","fle with é è.tx"),
os.path.join("TestDirectory","fle.with.dots.tx"),
os.path.join("TestDirectory","fle_with_underscore.tx"),
os.path.join("TestDirectory","lappostrophe.tx"),
os.path.join("TestDirectory","OLDER1"),
os.path.join("TestDirectory","OLDER1","flder1-file1.tx"),
os.path.join("TestDirectory","OLDER1","flder1-sub file #2.tx"),
os.path.join("TestDirectory","OLDER1","ub fOlder_1"),
os.path.join("TestDirectory","OLDER1","ub fOlder_1","sb file 1.tx"),
os.path.join("TestDirectory","OLDER1","ub fOlder_1","sb file 2.tx")]

#replace e with 3 and .txt with .ogg.
Main_Replace_without_regex = [
os.path.join("TestDirectory","fil3 with é è.ogg"),
os.path.join("TestDirectory","fil3.with.dots.ogg"),
os.path.join("TestDirectory","fil3_with_und3rscor3.ogg"),
os.path.join("TestDirectory","FOLDER1"),
os.path.join("TestDirectory","FOLDER1","fold3r1-fil31.ogg"),
os.path.join("TestDirectory","FOLDER1","fold3r1-sub fil3 #2.ogg"),
os.path.join("TestDirectory","FOLDER1","sub fOld3r_1"),
os.path.join("TestDirectory","FOLDER1","sub fOld3r_1","sub fil3 1.ogg"),
os.path.join("TestDirectory","FOLDER1","sub fOld3r_1","sub fil3 2.ogg"),
os.path.join("TestDirectory","l'appostroph3.ogg")]

#Replace folder digit with 99, file "file" with "fhis" and extension word with "pdf".
Main_Replace_with_regex = [
os.path.join("TestDirectory","fhis with é è.pdf"),
os.path.join("TestDirectory","fhis.with.dots.pdf"),
os.path.join("TestDirectory","fhis_with_underscore.pdf"),
os.path.join("TestDirectory","FOLDER99"),
os.path.join("TestDirectory","FOLDER99","folder1-fhis1.pdf"),
os.path.join("TestDirectory","FOLDER99","folder1-sub fhis #2.pdf"),
os.path.join("TestDirectory","FOLDER99","sub fOlder_99"),
os.path.join("TestDirectory","FOLDER99","sub fOlder_99","sub fhis 1.pdf"),
os.path.join("TestDirectory","FOLDER99","sub fOlder_99","sub fhis 2.pdf"),
os.path.join("TestDirectory","l'appostrophe.pdf")]

#Insert A at position 0 for folder, position 3 for files and position 99 for extension.
Main_Insert = [
os.path.join("TestDirectory","AFOLDER1"),
os.path.join("TestDirectory","AFOLDER1","Asub fOlder_1"),
os.path.join("TestDirectory","AFOLDER1","Asub fOlder_1","subA file 1.txtA"),
os.path.join("TestDirectory","AFOLDER1","Asub fOlder_1","subA file 2.txtA"),
os.path.join("TestDirectory","AFOLDER1","folAder1-file1.txtA"),
os.path.join("TestDirectory","AFOLDER1","folAder1-sub file #2.txtA"),
os.path.join("TestDirectory","filAe with é è.txtA"),
os.path.join("TestDirectory","filAe.with.dots.txtA"),
os.path.join("TestDirectory","filAe_with_underscore.txtA"),
os.path.join("TestDirectory","l'aAppostrophe.txtA")]

#Name all folders 'folder', files 'file' and extensions '.ext'.
# Main_CustomName = [
# os.path.join("TestDirectory","file (1).ext"),
# os.path.join("TestDirectory","file (2).ext"),
# os.path.join("TestDirectory","file (3).ext"),
# os.path.join("TestDirectory","file.ext"),
# os.path.join("TestDirectory","folder (1)"),
# os.path.join("TestDirectory","folder (1)","file (1).ext"),
# os.path.join("TestDirectory","folder (1)","file.ext"),
# os.path.join("TestDirectory","folder (1)","folder"),
# os.path.join("TestDirectory","folder (1)","folder/file (1).ext"),
# os.path.join("TestDirectory","folder (1)","folder/file.ext"),
# os.path.join("TestDirectory","folder (1)","folder (1)")]

#use lowercase foldername for folders, uppercase foldername for files and untouched foldername f.
Main_FolderName = [
os.path.join("TestDirectory","TestDirectoryfile with é è.txt"),
os.path.join("TestDirectory","TestDirectoryfile.with.dots.txt"),
os.path.join("TestDirectory","TestDirectoryfile_with_underscore.txt"),
os.path.join("TestDirectory","TestDirectoryFOLDER1"),
os.path.join("TestDirectory","TestDirectoryFOLDER1","FOLDER1folder1-file1.txt"),
os.path.join("TestDirectory","TestDirectoryFOLDER1","FOLDER1folder1-sub file #2.txt"),
os.path.join("TestDirectory","TestDirectoryFOLDER1","FOLDER1sub fOlder_1"),
os.path.join("TestDirectory","TestDirectoryFOLDER1","FOLDER1sub fOlder_1","sub fOlder_1sub file 1.txt"),
os.path.join("TestDirectory","TestDirectoryFOLDER1","FOLDER1sub fOlder_1","sub fOlder_1sub file 2.txt"),
os.path.join("TestDirectory","TestDirectoryl'appostrophe.txt")]
#Add a prefix 'prefix ' and a suffix ' suffix'.
Main_Custom_Prefix_Suffix = [
os.path.join("TestDirectory","FOLDER1"),
os.path.join("TestDirectory","FOLDER1","prefix folder1-file1 suffix.txt"),
os.path.join("TestDirectory","FOLDER1","prefix folder1-sub file #2 suffix.txt"),
os.path.join("TestDirectory","FOLDER1","sub fOlder_1"),
os.path.join("TestDirectory","FOLDER1","sub fOlder_1","prefix sub file 1 suffix.txt"),
os.path.join("TestDirectory","FOLDER1","sub fOlder_1","prefix sub file 2 suffix.txt"),
os.path.join("TestDirectory","prefix file with é è suffix.txt"),
os.path.join("TestDirectory","prefix file.with.dots suffix.txt"),
os.path.join("TestDirectory","prefix file_with_underscore suffix.txt"),
os.path.join("TestDirectory","prefix l'appostrophe suffix.txt")]


#Folder with counter from 0 and inc = 1, prefix from 2 and inc = 4. Sorted by name.
Main_Counter_Name_Sort = [
os.path.join("TestDirectory","0"),
os.path.join("TestDirectory","0","0"),
os.path.join("TestDirectory","0","0","02sub file 1.txt"),
os.path.join("TestDirectory","0","0","06sub file 2.txt"),
os.path.join("TestDirectory","0","02folder1-file1.txt"),
os.path.join("TestDirectory","0","06folder1-sub file #2.txt"),
os.path.join("TestDirectory","10file_with_underscore.txt"),
os.path.join("TestDirectory","14l'appostrophe.txt"),
os.path.join("TestDirectory","02file with é è.txt"),
os.path.join("TestDirectory","06file.with.dots.txt")]

#Folder with counter from 0 and inc = 1, file from 0 and inc = 1. Sorted by name in reverse order.
Main_Counter_Reverse_Name_Sort = [
os.path.join("TestDirectory","file with é è3.txt"),
os.path.join("TestDirectory","file.with.dots2.txt"),
os.path.join("TestDirectory","file_with_underscore1.txt"),
os.path.join("TestDirectory","FOLDER10"),
os.path.join("TestDirectory","FOLDER10","folder1-file11.txt"),
os.path.join("TestDirectory","FOLDER10","folder1-sub file #20.txt"),
os.path.join("TestDirectory","FOLDER10","sub fOlder_10"),
os.path.join("TestDirectory","FOLDER10","sub fOlder_10","sub file 11.txt"),
os.path.join("TestDirectory","FOLDER10","sub fOlder_10","sub file 20.txt"),
os.path.join("TestDirectory","l'appostrophe0.txt")]

#Folder with counter from 0 and inc = 1, file from 0 and inc = 1. Sorted by size.
Main_Counter_Size_Sort = [
os.path.join("TestDirectory","2file with é è.txt"),
os.path.join("TestDirectory","1file.with.dots.txt"),
os.path.join("TestDirectory","3file_with_underscore.txt"),
os.path.join("TestDirectory","0FOLDER1"),
os.path.join("TestDirectory","0FOLDER1","0folder1-file1.txt"),
os.path.join("TestDirectory","0FOLDER1","1folder1-sub file #2.txt"),
os.path.join("TestDirectory","0FOLDER1","0sub fOlder_1"),
os.path.join("TestDirectory","0FOLDER1","0sub fOlder_1","1sub file 1.txt"),
os.path.join("TestDirectory","0FOLDER1","0sub fOlder_1","0sub file 2.txt"),
os.path.join("TestDirectory","0l'appostrophe.txt")]
#Use accents and special characters to see if the encoding is supported.
Accent_Encoding = [
os.path.join("TestDirectory","file with é èéèùà€ç.txt"),
os.path.join("TestDirectory","file.with.dotséèùà€ç.txt"),
os.path.join("TestDirectory","file_with_underscoreéèùà€ç.txt"),
os.path.join("TestDirectory","FOLDER1éèùà€ç"),
os.path.join("TestDirectory","FOLDER1éèùà€ç","folder1-file1éèùà€ç.txt"),
os.path.join("TestDirectory","FOLDER1éèùà€ç","folder1-sub file #2éèùà€ç.txt"),
os.path.join("TestDirectory","FOLDER1éèùà€ç","sub fOlder_1éèùà€ç"),
os.path.join("TestDirectory","FOLDER1éèùà€ç","sub fOlder_1éèùà€ç","sub file 1éèùà€ç.txt"),
os.path.join("TestDirectory","FOLDER1éèùà€ç","sub fOlder_1éèùà€ç","sub file 2éèùà€ç.txt"),
os.path.join("TestDirectory","l'appostropheéèùà€ç.txt")]
