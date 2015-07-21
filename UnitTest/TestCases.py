#author : pierrecnalb
#copyright pierrecnalb
import unittest
import random
import os
import sys
import shutil
import pdb
import io
sys.path.append('/home/pierre/Documents/Programs/White-Renamer/')

import Renamer
import TestCasesModel

#Main_Uppercase = [
#os.path.join("TestDirectory","FILE WITH É È.TXT"),
#os.path.join("TestDirectory","FILE.WITH.DOTS.TXT"),
#os.path.join("TestDirectory","FILE_WITH_UNDERSCORE.TXT"),
#os.path.join("TestDirectory","FOLDER 2"),
#os.path.join("TestDirectory","FOLDER1"),
#os.path.join("TestDirectory","FOLDER1","FOLDER1-FILE1.TXT"),
#os.path.join("TestDirectory","FOLDER1","FOLDER1-SUB FILE #2.TXT"),
#os.path.join("TestDirectory","FOLDER1","SUB FOLDER_1"),
#os.path.join("TestDirectory","FOLDER1","SUB FOLDER_1","SUB FILE 1.TXT"),
#os.path.join("TestDirectory","FOLDER1","SUB FOLDER_1","SUB FILE 2.TXT"),
#os.path.join("TestDirectory","FOLDER1","SUB.FOLDER 2"),
#os.path.join("TestDirectory","L'APPOSTROPHE.TXT")]
#
#Main_Lowercase = [
#os.path.join("TestDirectory","file with é è.txt"),
#os.path.join("TestDirectory","file.with.dots.txt"),
#os.path.join("TestDirectory","file_with_underscore.txt"),
#os.path.join("TestDirectory","folder 2"),
#os.path.join("TestDirectory","folder1"),
#os.path.join("TestDirectory","folder1","folder1-file1.txt"),
#os.path.join("TestDirectory","folder1","folder1-sub file #2.txt"),
#os.path.join("TestDirectory","folder1","sub folder_1"),
#os.path.join("TestDirectory","folder1","sub folder_1","sub file 1.txt"),
#os.path.join("TestDirectory","folder1","sub folder_1","sub file 2.txt"),
#os.path.join("TestDirectory","folder1","sub.folder 2"),
#os.path.join("TestDirectory","l'appostrophe.txt")]
#
##delete first letter for folders, second for files and third for extension.
#Main_Delete = [
#os.path.join("TestDirectory","fle with é è.tt"),
#os.path.join("TestDirectory","fle.with.dots.tt"),
#os.path.join("TestDirectory","fle_with_underscore.tt"),
#os.path.join("TestDirectory","lappostrophe.tt"),
#os.path.join("TestDirectory","older 2"),
#os.path.join("TestDirectory","OLDER1"),
#os.path.join("TestDirectory","OLDER1","flder1-file1.tt"),
#os.path.join("TestDirectory","OLDER1","flder1-sub file #2.tt"),
#os.path.join("TestDirectory","OLDER1","ub fOlder_1"),
#os.path.join("TestDirectory","OLDER1","ub fOlder_1","sb file 1.tt"),
#os.path.join("TestDirectory","OLDER1","ub fOlder_1","sb file 2.tt"),
#os.path.join("TestDirectory","OLDER1","ub.FOLDER 2")]
#
##replace e with 3 and .txt with .ogg.
#Main_Replace_without_regex = [
#os.path.join("TestDirectory","fil3 with é è.ogg"),
#os.path.join("TestDirectory","fil3.with.dots.ogg"),
#os.path.join("TestDirectory","fil3_with_und3rscor3.ogg"),
#os.path.join("TestDirectory","fold3r 2"),
#os.path.join("TestDirectory","FOLDER1"),
#os.path.join("TestDirectory","FOLDER1","fold3r1-fil31.ogg"),
#os.path.join("TestDirectory","FOLDER1","fold3r1-sub fil3 #2.ogg"),
#os.path.join("TestDirectory","FOLDER1","sub fOld3r_1"),
#os.path.join("TestDirectory","FOLDER1","sub fOld3r_1","sub fil3 1.ogg"),
#os.path.join("TestDirectory","FOLDER1","sub fOld3r_1","sub fil3 2.ogg"),
#os.path.join("TestDirectory","FOLDER1","sub.FOLDER 2"),
#os.path.join("TestDirectory","l'appostroph3.ogg")]
#
##Insert A at position 0 for folder, position 3 for files and position 99 for extension.
#Main_Insert = [
#os.path.join("TestDirectory","Afolder 2"),
#os.path.join("TestDirectory","AFOLDER1"),
#os.path.join("TestDirectory","AFOLDER1","Asub fOlder_1"),
#os.path.join("TestDirectory","AFOLDER1","Asub fOlder_1","subA file 1.txtA"),
#os.path.join("TestDirectory","AFOLDER1","Asub fOlder_1","subA file 2.txtA"),
#os.path.join("TestDirectory","AFOLDER1","Asub.FOLDER 2"),
#os.path.join("TestDirectory","AFOLDER1","folAder1-file1.txtA"),
#os.path.join("TestDirectory","AFOLDER1","folAder1-sub file #2.txtA"),
#os.path.join("TestDirectory","filAe with é è.txtA"),
#os.path.join("TestDirectory","filAe.with.dots.txtA"),
#os.path.join("TestDirectory","filAe_with_underscore.txtA"),
#os.path.join("TestDirectory","l'aAppostrophe.txtA")]
#
##Name all folders 'folder', files 'file' and extensions '.ext'.
#Main_CustomName = [
#os.path.join("TestDirectory","file (1).ext"),
#os.path.join("TestDirectory","file (2).ext"),
#os.path.join("TestDirectory","file (3).ext"),
#os.path.join("TestDirectory","file.ext"),
#os.path.join("TestDirectory","folder"),
#os.path.join("TestDirectory","folder (1)"),
#os.path.join("TestDirectory","folder (1)","file (1).ext"),
#os.path.join("TestDirectory","folder (1)","file.ext"),
#os.path.join("TestDirectory","folder (1)","folder"),
#os.path.join("TestDirectory","folder (1)","folder/file (1).ext"),
#os.path.join("TestDirectory","folder (1)","folder/file.ext"),
#os.path.join("TestDirectory","folder (1)","folder (1)")]
#
##use lowercase foldername for folders, uppercase foldername for files and untouched foldername for extensions.
#Main_FolderName = [
#os.path.join("TestDirectory","testdirectory"),
#os.path.join("TestDirectory","testdirectory (1)"),
#os.path.join("TestDirectory","testdirectory (1)","folder1"),
#os.path.join("TestDirectory","testdirectory (1)","folder1","SUB FOLDER_1 (1)sub fOlder_1"),
#os.path.join("TestDirectory","testdirectory (1)","folder1","SUB FOLDER_1sub fOlder_1"),
#os.path.join("TestDirectory","testdirectory (1)","folder1 (1)"),
#os.path.join("TestDirectory","testdirectory (1)","FOLDER1 (1)FOLDER1"),
#os.path.join("TestDirectory","testdirectory (1)","FOLDER1FOLDER1"),
#os.path.join("TestDirectory","TESTDIRECTORY (1)TestDirectory"),
#os.path.join("TestDirectory","TESTDIRECTORY (2)TestDirectory"),
#os.path.join("TestDirectory","TESTDIRECTORY (3)TestDirectory"),
#os.path.join("TestDirectory","TESTDIRECTORYTestDirectory")]
#
##Add a prefix 'prefix ' and a suffix ' suffix'.
#Main_Custom_Prefix_Suffix = [
#os.path.join("TestDirectory","folder 2"),
#os.path.join("TestDirectory","FOLDER1"),
#os.path.join("TestDirectory","FOLDER1","prefix folder1-file1 suffix.txt"),
#os.path.join("TestDirectory","FOLDER1","prefix folder1-sub file #2 suffix.txt"),
#os.path.join("TestDirectory","FOLDER1","sub fOlder_1"),
#os.path.join("TestDirectory","FOLDER1","sub fOlder_1","prefix sub file 1 suffix.txt"),
#os.path.join("TestDirectory","FOLDER1","sub fOlder_1","prefix sub file 2 suffix.txt"),
#os.path.join("TestDirectory","FOLDER1","sub.FOLDER 2"),
#os.path.join("TestDirectory","prefix file with é è suffix.txt"),
#os.path.join("TestDirectory","prefix file.with.dots suffix.txt"),
#os.path.join("TestDirectory","prefix file_with_underscore suffix.txt"),
#os.path.join("TestDirectory","prefix l'appostrophe suffix.txt")]
#
##Add two prefixes with foldername (first uppercase, second lowercase) and one suffix with foldername untouched.
#Main_FolderName_Prefix_Suffix = [
#os.path.join("TestDirectory","folder 2"),
#os.path.join("TestDirectory","FOLDER1"),
#os.path.join("TestDirectory","FOLDER1","FOLDER1folder1folder1-file1FOLDER1.txt"),
#os.path.join("TestDirectory","FOLDER1","FOLDER1folder1folder1-sub file #2FOLDER1.txt"),
#os.path.join("TestDirectory","FOLDER1","sub fOlder_1"),
#os.path.join("TestDirectory","FOLDER1","sub fOlder_1","SUB FOLDER_1sub folder_1sub file 1sub fOlder_1.txt"),
#os.path.join("TestDirectory","FOLDER1","sub fOlder_1","SUB FOLDER_1sub folder_1sub file 2sub fOlder_1.txt"),
#os.path.join("TestDirectory","FOLDER1","sub.FOLDER 2"),
#os.path.join("TestDirectory","TESTDIRECTORYtestdirectoryfile with é èTestDirectory.txt"),
#os.path.join("TestDirectory","TESTDIRECTORYtestdirectoryfile.with.dotsTestDirectory.txt"),
#os.path.join("TestDirectory","TESTDIRECTORYtestdirectoryfile_with_underscoreTestDirectory.txt"),
#os.path.join("TestDirectory","TESTDIRECTORYtestdirectoryl'appostropheTestDirectory.txt")]
#
##Folder with counter from 0 and inc = 1, prefix from 2 and inc = 4. Sorted by name.
#Main_Counter_Name_Sort = [
#os.path.join("TestDirectory","0"),
#os.path.join("TestDirectory","1"),
#os.path.join("TestDirectory","1","0"),
#os.path.join("TestDirectory","1","0","2sub file 1.txt"),
#os.path.join("TestDirectory","1","0","6sub file 2.txt"),
#os.path.join("TestDirectory","1","1"),
#os.path.join("TestDirectory","1","2folder1-file1.txt"),
#os.path.join("TestDirectory","1","6folder1-sub file #2.txt"),
#os.path.join("TestDirectory","10file_with_underscore.txt"),
#os.path.join("TestDirectory","14l'appostrophe.txt"),
#os.path.join("TestDirectory","2file with é è.txt"),
#os.path.join("TestDirectory","6file.with.dots.txt")]
#
##Folder with counter from 0 and inc = 1, file from 0 and inc = 1. Sorted by name in reverse order.
#Main_Counter_Reverse_Name_Sort = [
#os.path.join("TestDirectory","3.txt"),
#os.path.join("TestDirectory","2.txt"),
#os.path.join("TestDirectory","1.txt"),
#os.path.join("TestDirectory","1"),
#os.path.join("TestDirectory","0.txt"),
#os.path.join("TestDirectory","0"),
#os.path.join("TestDirectory","0","1.txt"),
#os.path.join("TestDirectory","0","1"),
#os.path.join("TestDirectory","0","1","1.txt"),
#os.path.join("TestDirectory","0","1","0.txt"),
#os.path.join("TestDirectory","0","0.txt"),
#os.path.join("TestDirectory","0","0")]
#
##Folder with counter from 0 and inc = 1, file from 0 and inc = 1. Sorted by size.
#Main_Counter_Size_Sort = [
#os.path.join("TestDirectory","0.txt"),
#os.path.join("TestDirectory","1.txt"),
#os.path.join("TestDirectory","2.txt"),
#os.path.join("TestDirectory","3.txt"),
#os.path.join("TestDirectory","0"),
#os.path.join("TestDirectory","1"),
#os.path.join("TestDirectory","1","0.txt"),
#os.path.join("TestDirectory","1","1.txt"),
#os.path.join("TestDirectory","1","0"),
#os.path.join("TestDirectory","1","1"),
#os.path.join("TestDirectory","1","1","1.txt"),
#os.path.join("TestDirectory","1","1","0.txt")]
#
class TestCases(unittest.TestCase):
    """TestCases used to verify the functions from the module 'Renamer'."""
    def setUp(self):
        self.root_folder = os.path.dirname(__file__)
        shutil.copytree(os.path.join(self.root_folder, "TestCase1"), os.path.join(self.root_folder,"TestDirectory"))
        self.directory = os.path.join(os.path.dirname(__file__),"TestDirectory")


    def init(self, recursion, show_hidden_files, sorting_criteria, reverse_order):
        """Initialisation of the input arguments."""
        self.recursion = recursion
        self.show_hidden_files = show_hidden_files
        self.sorting_criteria = sorting_criteria
        self.reverse_order = reverse_order
        self.files_collection = Renamer.FilesCollection(self.directory, recursion, show_hidden_files, sorting_criteria, reverse_order)
        self.files_list = []
        self.actions = []

    def test_main_uppercase(self):
        self.init(True, False, "name", False)
        action_descriptor = Renamer.CaseChangeAction
        files = self.files_collection
        action_args = {'case_choice' : 'uppercase', 'first_letter': False, 'after_symbols': False}
        self.apply_actions(action_descriptor, action_args, 'folder')
        self.apply_actions(action_descriptor, action_args, 'file')
        self.apply_actions(action_descriptor, action_args, 'extension')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Main_Uppercase)

    def test_main_lowercase(self):
        self.init(True, False, "name", False)
        action_descriptor = Renamer.CaseChangeAction
        files = self.files_collection
        action_args = {'case_choice' : 'lowercase', 'first_letter': False, 'after_symbols': False}
        self.apply_actions(action_descriptor, action_args, 'folder')
        self.apply_actions(action_descriptor, action_args, 'file')
        self.apply_actions(action_descriptor, action_args, 'extension')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Main_Lowercase)

    def test_main_delete(self):
        """Delete first letter for folders, second for files and third for extension."""
        self.init(True, False, "name", False)
        action_descriptor = Renamer.CharacterDeletionAction
        files = self.files_collection
        action_args_folder = {'starting_position' : 0, 'ending_position' : 1}
        action_args_file = {'starting_position' : 1, 'ending_position' : 2}
        action_args_extension = {'starting_position' : 2, 'ending_position' : 3}
        self.apply_actions(action_descriptor, action_args_folder, 'folder')
        self.apply_actions(action_descriptor, action_args_file, 'file')
        self.apply_actions(action_descriptor, action_args_extension, 'extension')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Main_Delete)

    def test_main_replace_without_regex(self):
        """Replace e with 3 and .txt with .ogg."""
        self.init(True, False, "name", False)
        action_descriptor = Renamer.CharacterReplacementAction
        files = self.files_collection
        action_args_folder = {'old_char' : 'e', 'new_char' : '3', 'regex': False}
        action_args_file = {'old_char' : 'e', 'new_char' : '3', 'regex': False}
        action_args_extension = {'old_char' : '.txt', 'new_char' : '.ogg', 'regex': False}
        self.apply_actions(action_descriptor, action_args_folder, 'folder')
        self.apply_actions(action_descriptor, action_args_file, 'file')
        self.apply_actions(action_descriptor, action_args_extension, 'extension')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Main_Replace_without_regex)

    def test_main_insert(self):
        """Insert A at position 0 for folder, position 3 for files and position 99 for extension."""
        self.init(True, False, "name", False)
        action_descriptor = Renamer.CharacterInsertionAction
        files = self.files_collection
        action_args_folder = {'new_char' : 'A', 'index': 0}
        action_args_file = {'new_char' : 'A', 'index': 3}
        action_args_extension = {'new_char' : 'A', 'index': 99}
        self.apply_actions(action_descriptor, action_args_folder, 'folder')
        self.apply_actions(action_descriptor, action_args_file, 'file')
        self.apply_actions(action_descriptor, action_args_extension, 'extension')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Main_Insert)

    def test_main_custom_name(self):
        """Name all folders 'folder', files 'file' and extensions '.ext'."""
        self.init(True, False, "name", False)
        action_descriptor = Renamer.CustomNameAction
        files = self.files_collection
        action_args_folder = {'new_name' : 'folder'}
        action_args_file = {'new_name' : 'file'}
        action_args_extension = {'new_name' : '.ext'}
        self.apply_actions(action_descriptor, action_args_folder, 'folder')
        self.apply_actions(action_descriptor, action_args_file, 'file')
        self.apply_actions(action_descriptor, action_args_extension, 'extension')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Main_CustomName)

    def test_main_folder_name(self):
        """Use foldername for folders, files and for extensions."""
        self.init(True, False, "name", False)
        action_descriptor = Renamer.FolderNameUsageAction
        files = self.files_collection
        action_args_folder = {}
        action_args_file = {}
        action_args_extension = {}
        self.apply_actions(action_descriptor, action_args_folder, 'folder')
        self.apply_actions(action_descriptor, action_args_file, 'file')
        self.apply_actions(action_descriptor, action_args_extension, 'extension')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Main_FolderName)

    def test_main_custom_prefix_suffix(self):
        """Add a prefix 'prefix ' and a suffix ' suffix'."""
        self.init(True, False, "name", False)
        action_descriptor = Renamer.CustomNameAction
        files = self.files_collection
        action_args_prefix = {'new_name' : 'prefix '}
        action_args_suffix = {'new_name' : ' suffix'}
        self.apply_actions(action_descriptor, action_args_prefix, 'prefix')
        self.apply_actions(action_descriptor, action_args_suffix, 'suffix')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Main_Custom_Prefix_Suffix)

    def test_main_foldername_prefix_suffix(self):
        """Add prefix with foldername  and one suffix with foldername."""
        self.init(True, False, "name", False)
        action_descriptor = Renamer.FolderNameUsageAction
        files = self.files_collection
        action_args_prefix = {}
        action_args_suffix = {}
        self.apply_actions(action_descriptor, action_args_prefix, 'prefix')
        self.apply_actions(action_descriptor, action_args_suffix, 'suffix')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Main_FolderName_Prefix_Suffix)

    def test_main_counter_sort_by_name(self):
        """Folder with counter from 0 and inc = 1, prefix from 2 and inc = 4. Sorted by name."""
        self.init(True, False, "name", False)
        action_descriptor = Renamer.Counter
        files = self.files_collection
        action_args_folder = {'start_index' : 0, 'increment': 1}
        action_args_prefix = {'start_index' : 2, 'increment': 4}
        self.apply_actions(action_descriptor, action_args_folder, 'folder')
        self.apply_actions(action_descriptor, action_args_prefix, 'prefix')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Main_Counter_Name_Sort)

    def test_main_counter_sort_reverse_by_name(self):
        """Folder with counter from 0 and inc = 1, file from 0 and inc = 1. Sorted by name in reverse order."""
        self.init(True, False, "name", True)
        action_descriptor = Renamer.Counter
        files = self.files_collection
        action_args = {'start_index' : 0, 'increment': 1}
        self.apply_actions(action_descriptor, action_args, 'folder')
        self.apply_actions(action_descriptor, action_args, 'file')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Main_Counter_Reverse_Name_Sort)

    def test_main_counter_sort_reverse_by_name(self):
        """Folder with counter from 0 and inc = 1, file from 0 and inc = 1. Sorted by size."""
        self.init(True, False, "size", False)
        action_descriptor = Renamer.Counter
        files = self.files_collection
        action_args = {'start_index' : 0, 'increment': 1}
        self.apply_actions(action_descriptor, action_args, 'folder')
        self.apply_actions(action_descriptor, action_args, 'file')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Main_Counter_Size_Sort)

    def compare_with_model_file(self, model_file):
        shutil.rmtree(self.directory)
        self.assertEqual(self.files_list, model_file)

    def apply_actions(self, action_descriptor, action_args, path_type):
        self.actions = []
        self.populate_actions(action_descriptor, action_args, path_type)
        self.files_collection.process_file_system_tree_node(self.actions)
        self.files_collection.batch_rename()

    def populate_actions(self, action_descriptor, action_args, path_type):
        """Populate the list of actions with one specified Action and the defined parameters."""
        action_instance = action_descriptor(path_type, **action_args)
        self.actions.append(action_instance)


    def scan_directory(self, input_path, sorting_criteria, reverse_order):
        input_path = os.path.abspath(input_path)
        directory_files = sorted(os.listdir(input_path), key = lambda file : self.files_collection.get_file_sorting_criteria(os.path.join(input_path, file), sorting_criteria), reverse=reverse_order)
        for filename in directory_files:
            filepath = os.path.join(input_path, filename)
            if filename[0] == '.' and not self.show_hidden_files:
                continue
            if os.path.isdir(filepath):
                self.files_list.append(os.path.relpath(filepath, self.root_folder))
                if (not self.recursion):
                    continue
                else:
                    self.scan_directory(filepath, sorting_criteria, reverse_order)
            else:
                self.files_list.append(os.path.relpath(filepath, self.root_folder))


if __name__ == '__main__':
    unittest.main()



