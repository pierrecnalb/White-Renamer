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

import ActionManager
import FileManager
import TestCasesModel

class TestCases(unittest.TestCase):
    """TestCases used to verify the functions from the module 'ActionManager'."""
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
        self.files_collection = FileManager.FilesCollection(self.directory, recursion, show_hidden_files, sorting_criteria, reverse_order)
        self.files_list = []
        self.actions = []

#    def test_main_uppercase(self):
#        self.init(True, False, "name", False)
#        action_descriptor = ActionManager.CaseChangeAction
#        files = self.files_collection
#        action_args = {'case_choice' : 'uppercase', 'first_letter': False, 'after_symbols': False}
#        self.apply_actions(action_descriptor, action_args, 'folder')
#        self.apply_actions(action_descriptor, action_args, 'file')
#        self.apply_actions(action_descriptor, action_args, 'extension')
#        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
#        self.compare_with_model_file(TestCasesModel.Main_Uppercase)
#
#    def test_main_lowercase(self):
#        self.init(True, False, "name", False)
#        action_descriptor = ActionManager.CaseChangeAction
#        files = self.files_collection
#        action_args = {'case_choice' : 'lowercase', 'first_letter': False, 'after_symbols': False}
#        self.apply_actions(action_descriptor, action_args, 'folder')
#        self.apply_actions(action_descriptor, action_args, 'file')
#        self.apply_actions(action_descriptor, action_args, 'extension')
#        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
#        self.compare_with_model_file(TestCasesModel.Main_Lowercase)
#
#    def test_main_delete(self):
#        """Delete first letter for folders, second for files and third for extension."""
#        self.init(True, False, "name", False)
#        action_descriptor = ActionManager.CharacterDeletionAction
#        files = self.files_collection
#        action_args_folder = {'starting_position' : 0, 'ending_position' : 1}
#        action_args_file = {'starting_position' : 1, 'ending_position' : 2}
#        action_args_extension = {'starting_position' : 2, 'ending_position' : 3}
#        self.apply_actions(action_descriptor, action_args_folder, 'folder')
#        self.apply_actions(action_descriptor, action_args_file, 'file')
#        self.apply_actions(action_descriptor, action_args_extension, 'extension')
#        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
#        self.compare_with_model_file(TestCasesModel.Main_Delete)
#
#    def test_main_replace_without_regex(self):
#        """Replace e with 3 and .txt with .ogg."""
#        self.init(True, False, "name", False)
#        action_descriptor = ActionManager.CharacterReplacementAction
#        files = self.files_collection
#        action_args_folder = {'old_char' : 'e', 'new_char' : '3', 'regex': False}
#        action_args_file = {'old_char' : 'e', 'new_char' : '3', 'regex': False}
#        action_args_extension = {'old_char' : '.txt', 'new_char' : '.ogg', 'regex': False}
#        self.apply_actions(action_descriptor, action_args_folder, 'folder')
#        self.apply_actions(action_descriptor, action_args_file, 'file')
#        self.apply_actions(action_descriptor, action_args_extension, 'extension')
#        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
#        self.compare_with_model_file(TestCasesModel.Main_Replace_without_regex)
#
#    def test_main_insert(self):
#        """Insert A at position 0 for folder, position 3 for files and position 99 for extension."""
#        self.init(True, False, "name", False)
#        action_descriptor = ActionManager.CharacterInsertionAction
#        files = self.files_collection
#        action_args_folder = {'new_char' : 'A', 'index': 0}
#        action_args_file = {'new_char' : 'A', 'index': 3}
#        action_args_extension = {'new_char' : 'A', 'index': 99}
#        self.apply_actions(action_descriptor, action_args_folder, 'folder')
#        self.apply_actions(action_descriptor, action_args_file, 'file')
#        self.apply_actions(action_descriptor, action_args_extension, 'extension')
#        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
#        self.compare_with_model_file(TestCasesModel.Main_Insert)
#
#    def test_main_custom_name(self):
#        """Name all folders 'folder', files 'file' and extensions '.ext'."""
#        self.init(True, False, "name", False)
#        action_descriptor = ActionManager.CustomNameAction
#        files = self.files_collection
#        action_args_folder = {'new_name' : 'folder'}
#        action_args_file = {'new_name' : 'file'}
#        action_args_extension = {'new_name' : '.ext'}
#        self.apply_actions(action_descriptor, action_args_folder, 'folder')
#        self.apply_actions(action_descriptor, action_args_file, 'file')
#        self.apply_actions(action_descriptor, action_args_extension, 'extension')
#        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
#        self.compare_with_model_file(TestCasesModel.Main_CustomName)

    def test_main_folder_name(self):
        """Use foldername for folders, files and for extensions."""
        self.init(True, False, "name", False)
        action_descriptor = ActionManager.FolderNameUsageAction
        files = self.files_collection
        action_args_folder = {}
        action_args_file = {}
        action_args_extension = {}
        self.apply_actions(action_descriptor, action_args_folder, 'folder')
        self.apply_actions(action_descriptor, action_args_file, 'file')
        self.apply_actions(action_descriptor, action_args_extension, 'extension')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Main_FolderName)

#    def test_main_custom_prefix_suffix(self):
#        """Add a prefix 'prefix ' and a suffix ' suffix'."""
#        self.init(True, False, "name", False)
#        action_descriptor = ActionManager.CustomNameAction
#        files = self.files_collection
#        action_args_prefix = {'new_name' : 'prefix '}
#        action_args_suffix = {'new_name' : ' suffix'}
#        self.apply_actions(action_descriptor, action_args_prefix, 'prefix')
#        self.apply_actions(action_descriptor, action_args_suffix, 'suffix')
#        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
#        self.compare_with_model_file(TestCasesModel.Main_Custom_Prefix_Suffix)
#
#    #def test_main_foldername_prefix_suffix(self):
#    #    """Add prefix with foldername  and one suffix with foldername."""
#    #    self.init(True, False, "name", False)
#    #    action_descriptor = ActionManager.FolderNameUsageAction
#    #    files = self.files_collection
#    #    action_args_prefix = {}
#    #    action_args_suffix = {}
#    #    self.apply_actions(action_descriptor, action_args_prefix, 'prefix')
#    #    self.apply_actions(action_descriptor, action_args_suffix, 'suffix')
#    #    self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
#    #    self.compare_with_model_file(TestCasesModel.Main_FolderName_Prefix_Suffix)
#
#    def test_main_counter_sort_by_name(self):
#        """Folder with counter from 0 and inc = 1, prefix from 2 and inc = 4. Sorted by name."""
#        self.init(True, False, "name", False)
#        action_descriptor = ActionManager.Counter
#        files = self.files_collection
#        action_args_folder = {'start_index' : 0, 'increment': 1}
#        action_args_prefix = {'start_index' : 2, 'increment': 4}
#        self.apply_actions(action_descriptor, action_args_folder, 'folder')
#        self.apply_actions(action_descriptor, action_args_prefix, 'prefix')
#        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
#        self.compare_with_model_file(TestCasesModel.Main_Counter_Name_Sort)
#
#    def test_main_counter_sort_reverse_by_name(self):
#        """Folder with counter from 0 and inc = 1, file from 0 and inc = 1. Sorted by name in reverse order."""
#        self.init(True, False, "name", True)
#        action_descriptor = ActionManager.Counter
#        files = self.files_collection
#        action_args = {'start_index' : 0, 'increment': 1}
#        self.apply_actions(action_descriptor, action_args, 'folder')
#        self.apply_actions(action_descriptor, action_args, 'file')
#        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
#        self.compare_with_model_file(TestCasesModel.Main_Counter_Reverse_Name_Sort)
#
#    def test_main_counter_sort_by_size(self):
#        """Folder with counter from 0 and inc = 1, file from 0 and inc = 1. Sorted by size."""
#        self.init(True, False, "size", False)
#        action_descriptor = ActionManager.Counter
#        files = self.files_collection
#        action_args = {'start_index' : 0, 'increment': 1}
#        self.apply_actions(action_descriptor, action_args, 'folder')
#        self.apply_actions(action_descriptor, action_args, 'file')
#        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
#        self.compare_with_model_file(TestCasesModel.Main_Counter_Size_Sort)
#
#    def test_accent_encoding(self):
#        """Use accent and special characters to see if the encoding is supported."""
#        self.init(True, False, "name", False)
#        action_descriptor = ActionManager.CustomNameAction
#        files = self.files_collection
#        action_args = {'new_name' : 'éèùà€ç'}
#        self.apply_actions(action_descriptor, action_args, 'file')
#        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
#        self.compare_with_model_file(TestCasesModel.Accent_Encoding)

    def compare_with_model_file(self, model_file):
        shutil.rmtree(self.directory)
        print(self.files_list)
        print(model_file)
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



