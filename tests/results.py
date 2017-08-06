import os
OriginalName = set([
    os.path.join("file with é è.txt"), os.path.join("file.with.dots.txt"),
    os.path.join("file_with_underscore.txt"), os.path.join("FOLDER1"),
    os.path.join("FOLDER1", "folder1-file1.txt"),
    os.path.join("FOLDER1", "folder1-sub file #2.txt"), os.path.join("FOLDER1", "sub fOlder_1"),
    os.path.join("FOLDER1", "sub fOlder_1", "sub file 1.txt"),
    os.path.join("FOLDER1", "sub fOlder_1", "sub file 2.txt"), os.path.join("l'appostrophe.txt")
])

Uppercase = set([
    os.path.join("FILE WITH É È.TXT"), os.path.join("FILE.WITH.DOTS.TXT"),
    os.path.join("FILE_WITH_UNDERSCORE.TXT"), os.path.join("FOLDER1"),
    os.path.join("FOLDER1", "FOLDER1-FILE1.TXT"),
    os.path.join("FOLDER1", "FOLDER1-SUB FILE #2.TXT"), os.path.join("FOLDER1", "SUB FOLDER_1"),
    os.path.join("FOLDER1", "SUB FOLDER_1", "SUB FILE 1.TXT"),
    os.path.join("FOLDER1", "SUB FOLDER_1", "SUB FILE 2.TXT"), os.path.join("L'APPOSTROPHE.TXT")
])

Lowercase = set([
    os.path.join("file with é è.txt"), os.path.join("file.with.dots.txt"),
    os.path.join("file_with_underscore.txt"), os.path.join("folder1"),
    os.path.join("folder1", "folder1-file1.txt"),
    os.path.join("folder1", "folder1-sub file #2.txt"), os.path.join("folder1", "sub folder_1"),
    os.path.join("folder1", "sub folder_1", "sub file 1.txt"),
    os.path.join("folder1", "sub folder_1", "sub file 2.txt"), os.path.join("l'appostrophe.txt")
])

Titlecase = set([
    os.path.join("File With É È.txt"), os.path.join("File.With.Dots.txt"),
    os.path.join("File_With_Underscore.txt"), os.path.join("Folder1"),
    os.path.join("Folder1", "Folder1-File1.txt"),
    os.path.join("Folder1", "Folder1-Sub File #2.txt"), os.path.join("Folder1", "Sub Folder_1"),
    os.path.join("Folder1", "Sub Folder_1", "Sub File 1.txt"),
    os.path.join("Folder1", "Sub Folder_1", "Sub File 2.txt"), os.path.join("L'appostrophe.txt")
])

Delete = set([
    os.path.join("fle with é è.tx"), os.path.join("fle.with.dots.tx"),
    os.path.join("fle_with_underscore.tx"), os.path.join("lappostrophe.tx"), os.path.join("OLDER1"),
    os.path.join("OLDER1", "flder1-file1.tx"), os.path.join("OLDER1", "flder1-sub file # 2.tx"),
    os.path.join("OLDER1", "ub fOlder_1"), os.path.join("OLDER1", "ub fOlder_1", "sb file 1.tx"),
    os.path.join("OLDER1", "ub fOlder_1", "sb file 2.tx")
])

Replace_without_regex = set([
    os.path.join("fil3 with é è.ogg"), os.path.join("fil3.with.dots.ogg"),
    os.path.join("fil3_with_und3rscor3.ogg"), os.path.join("FOLDER1"),
    os.path.join("FOLDER1", "fold3r1-fil31.ogg"),
    os.path.join("FOLDER1", "fold3r1-sub fil3 # 2.ogg"), os.path.join("FOLDER1", "sub fOld3r_1"),
    os.path.join("FOLDER1", "sub fOld3r_1", "sub fil3 1.ogg"),
    os.path.join("FOLDER1", "sub fOld3r_1", "sub fil3 2.ogg"), os.path.join("l'appostroph3.ogg")
])

Replace_with_regex = set([
    os.path.join("fhis with é è.pdf"), os.path.join("fhis.with.dots.pdf"),
    os.path.join("fhis_with_underscore.pdf"), os.path.join("FOLDER99"),
    os.path.join("FOLDER99", "folder1-fhis1.pdf"),
    os.path.join("FOLDER99", "folder1-sub fhis # 2.pdf"), os.path.join("FOLDER99", "sub fOlder_99"),
    os.path.join("FOLDER99", "sub fOlder_99", "sub fhis 1.pdf"),
    os.path.join("FOLDER99", "sub fOlder_99", "sub fhis 2.pdf"), os.path.join("l'appostrophe.pdf")
])

Insert = set([
    os.path.join("AFOLDER1"), os.path.join("AFOLDER1", "Asub fOlder_1"),
    os.path.join("AFOLDER1", "Asub fOlder_1", "subA file 1.txtA"),
    os.path.join("AFOLDER1", "Asub fOlder_1", "subA file 2.txtA"),
    os.path.join("AFOLDER1", "folAder1-file1.txtA"),
    os.path.join("AFOLDER1", "folAder1-sub file # 2.txtA"), os.path.join("filAe with é è.txtA"),
    os.path.join("filAe.with.dots.txtA"), os.path.join("filAe_with_underscore.txtA"),
    os.path.join("l'aAppostrophe.txtA")
])

# Name all folders 'folder', files 'file' and extensions '.ext'.
#  CustomName = set([
#  os.path.join("StandardTestCase","file (1).ext"),
#  os.path.join("StandardTestCase","file (2).ext"),
#  os.path.join("StandardTestCase","file (3).ext"),
#  os.path.join("StandardTestCase","file.ext"),
#  os.path.join("StandardTestCase","folder (1)"),
#  os.path.join("StandardTestCase","folder (1)","file (1).ext"),
#  os.path.join("StandardTestCase","folder (1)","file.ext"),
#  os.path.join("StandardTestCase","folder (1)","folder"),
#  os.path.join("StandardTestCase","folder (1)","folder/file (1).ext"),
#  os.path.join("StandardTestCase","folder (1)","folder/file.ext"),
#  os.path.join("StandardTestCase","folder (1)","folder (1)")]

# use lowercase foldername for folders, uppercase foldername for files and untouched foldername f.
FolderName = set([
    os.path.join("TestDirectoryfile with é è.txt"), os.path.join("TestDirectoryfile.with.dots.txt"),
    os.path.join("TestDirectoryfile_with_underscore.txt"), os.path.join("TestDirectoryFOLDER1"),
    os.path.join("TestDirectoryFOLDER1", "FOLDER1folder1-file1.txt"),
    os.path.join("TestDirectoryFOLDER1", "FOLDER1folder1-sub file # 2.txt"),
    os.path.join("TestDirectoryFOLDER1", "FOLDER1sub fOlder_1"), os.path.join(
        "TestDirectoryFOLDER1", "FOLDER1sub fOlder_1", "sub fOlder_1sub file 1.txt"), os.path.join(
            "TestDirectoryFOLDER1", "FOLDER1sub fOlder_1",
            "sub fOlder_1sub file 2.txt"), os.path.join("TestDirectoryl'appostrophe.txt")
])
# Add a prefix 'prefix ' and a suffix ' suffix'.
Custom_Prefix_Suffix = set([
    os.path.join("FOLDER1"), os.path.join("FOLDER1", "prefix folder1-file1 suffix.txt"),
    os.path.join("FOLDER1", "prefix folder1-sub file # 2 suffix.txt"),
    os.path.join("FOLDER1", "sub fOlder_1"),
    os.path.join("FOLDER1", "sub fOlder_1", "prefix sub file 1 suffix.txt"),
    os.path.join("FOLDER1", "sub fOlder_1", "prefix sub file 2 suffix.txt"),
    os.path.join("prefix file with é è suffix.txt"),
    os.path.join("prefix file.with.dots suffix.txt"),
    os.path.join("prefix file_with_underscore suffix.txt"),
    os.path.join("prefix l'appostrophe suffix.txt")
])

# Folder with counter from 0 and inc = 1, prefix from 2 and inc = 4. Sorted by name.
Counter_Name_Sort = set([
    os.path.join("0"), os.path.join("0", "0"), os.path.join("0", "0", "02sub file 1.txt"),
    os.path.join("0", "0", "06sub file 2.txt"), os.path.join("0", "02folder1-file1.txt"),
    os.path.join("0", "06folder1-sub file # 2.txt"), os.path.join("10file_with_underscore.txt"),
    os.path.join("14l'appostrophe.txt"), os.path.join("02file with é è.txt"),
    os.path.join("06file.with.dots.txt")
])

# Folder with counter from 0 and inc = 1, file from 0 and inc = 1. Sorted by name in reverse order.
Counter_Reverse_Name_Sort = set([
    os.path.join("file with é è3.txt"), os.path.join("file.with.dots2.txt"),
    os.path.join("file_with_underscore1.txt"), os.path.join("FOLDER10"),
    os.path.join("FOLDER10", "folder1-file11.txt"),
    os.path.join("FOLDER10", "folder1-sub file # 20.txt"),
    os.path.join("FOLDER10", "sub fOlder_10"),
    os.path.join("FOLDER10", "sub fOlder_10", "sub file 11.txt"),
    os.path.join("FOLDER10", "sub fOlder_10", "sub file 20.txt"), os.path.join("l'appostrophe0.txt")
])

# Folder with counter from 0 and inc = 1, file from 0 and inc = 1. Sorted by size.
Counter_Size_Sort = set([
    os.path.join("2file with é è.txt"), os.path.join("1file.with.dots.txt"),
    os.path.join("3file_with_underscore.txt"), os.path.join("0FOLDER1"),
    os.path.join("0FOLDER1", "0folder1-file1.txt"),
    os.path.join("0FOLDER1", "1folder1-sub file # 2.txt"),
    os.path.join("0FOLDER1", "0sub fOlder_1"),
    os.path.join("0FOLDER1", "0sub fOlder_1", "1sub file 1.txt"),
    os.path.join("0FOLDER1", "0sub fOlder_1", "0sub file 2.txt"), os.path.join("0l'appostrophe.txt")
])
# Use accents and special characters to see if the encoding is supported.
Accent_Encoding = set([
    os.path.join("file with é èéèùà€ç.txt"), os.path.join("file.with.dotséèùà€ç.txt"),
    os.path.join("file_with_underscoreéèùà€ç.txt"), os.path.join("FOLDER1éèùà€ç"),
    os.path.join("FOLDER1éèùà€ç", "folder1-file1éèùà€ç.txt"),
    os.path.join("FOLDER1éèùà€ç", "folder1-sub file # 2éèùà€ç.txt"),
    os.path.join("FOLDER1éèùà€ç", "sub fOlder_1éèùà€ç"),
    os.path.join("FOLDER1éèùà€ç", "sub fOlder_1éèùà€ç", "sub file 1éèùà€ç.txt"),
    os.path.join("FOLDER1éèùà€ç", "sub fOlder_1éèùà€ç", "sub file 2éèùà€ç.txt"),
    os.path.join("l'appostropheéèùà€ç.txt")
])

Image_Date = set([
    os.path.join("2013-05-07 15:01:29.jpg"), os.path.join("2013-05-07 15:09:31.jpg"),
    os.path.join("2013-05-07 15:12:31.jpg")
])

Image_XDimension = set([
    os.path.join("4288DSC0001.jpg"), os.path.join("4288DSC0002.jpg"),
    os.path.join("4288DSC0003.jpg")
])

Image_YDimension = set([
    os.path.join("2848DSC0001.jpg"), os.path.join("2848DSC0002.jpg"),
    os.path.join("2848DSC0003.jpg")
])

Image_ISO = set([
    os.path.join("320DSC0001.jpg"), os.path.join("320DSC0002.jpg"), os.path.join("320DSC0003.jpg")
])

Image_Camera = set([
    os.path.join("NIKON D90DSC0001.jpg"), os.path.join("NIKON D90DSC0002.jpg"),
    os.path.join("NIKON D90DSC0003.jpg")
])

Music_Artist = set([
    os.path.join("Pierre Blanc01CompositionFlight19.mp3"),
    os.path.join("Pierre Blanc02CompositionDarkness.mp3")
])

Music_Album = set([
    os.path.join("Pierre Blanc's Album01CompositionFlight19.mp3"),
    os.path.join("Pierre Blanc's Album02CompositionDarkness.mp3")
])

Music_Year = set(
    [os.path.join("201301CompositionFlight19.mp3"), os.path.join("201302CompositionDarkness.mp3")])

Music_Title = set([os.path.join("Flight 19.mp3"), os.path.join("Beyond The Darkness.mp3")])

Music_Genre = set([os.path.join("Post Rock.mp3"), os.path.join("Rock.mp3")])

Music_Track = set([os.path.join("01.mp3"), os.path.join("02.mp3")])
