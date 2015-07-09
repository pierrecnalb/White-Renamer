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

Main_Uppercase = [
os.path.join("TestDirectory","FILE WITH É È.TXT"),
os.path.join("TestDirectory","FILE.WITH.DOTS.TXT"),
os.path.join("TestDirectory","FILE_WITH_UNDERSCORE.TXT"),
os.path.join("TestDirectory","FOLDER 2"),
os.path.join("TestDirectory","FOLDER1"),
os.path.join("TestDirectory","FOLDER1","FOLDER1-FILE1.TXT"),
os.path.join("TestDirectory","FOLDER1","FOLDER1-SUB FILE #2.TXT"),
os.path.join("TestDirectory","FOLDER1","SUB FOLDER_1"),
os.path.join("TestDirectory","FOLDER1","SUB FOLDER_1/SUB FILE 1.TXT"),
os.path.join("TestDirectory","FOLDER1","SUB FOLDER_1/SUB FILE 2.TXT"),
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
os.path.join("TestDirectory","folder1","sub folder_1/sub file 1.txt"),
os.path.join("TestDirectory","folder1","sub folder_1/sub file 2.txt"),
os.path.join("TestDirectory","folder1","sub.folder 2"),
os.path.join("TestDirectory","l'appostrophe.txt")]

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
        action_descriptor = Renamer.OriginalName
        files = self.files_collection
        action_args = {'untouched' : False, 'uppercase': True, 'lowercase': False, 'titlecase': False}
        self.apply_actions(files, action_descriptor, action_args, 'folder')
        self.apply_actions(files, action_descriptor, action_args, 'file')
        self.apply_actions(files, action_descriptor, action_args, 'extension')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(Main_Uppercase)

    def test_main_lowercase(self):
        self.init(True, False, "name", False)
        action_descriptor = Renamer.OriginalName
        files = self.files_collection
        action_args = {'untouched' : False, 'uppercase': False, 'lowercase': True, 'titlecase': False}
        self.apply_actions(files, action_descriptor, action_args, 'folder')
        self.apply_actions(files, action_descriptor, action_args, 'file')
        self.apply_actions(files, action_descriptor, action_args, 'extension')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(Main_Lowercase)

    def compare_with_model_file(self, model_file):
        self.assertEqual(self.files_list, model_file)
        shutil.rmtree(self.directory)

    def apply_actions(self, files_collection, action_descriptor, action_args, path_type):
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



