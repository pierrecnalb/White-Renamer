#author : pierrecnalb
#copyright pierrecnalb
import unittest
import random
import os
import sys
import shutil
import pdb
sys.path.append('/home/pierre/Documents/Programs/White-Renamer/')

import Renamer

class TestCases(unittest.TestCase):
    """TestCases used to verify the functions from the module 'Renamer'."""
    def setUp(self):
        root_folder = os.path.dirname(__file__)
        #shutil.rmtree(self.directory)

        shutil.copytree(os.path.join(root_folder, "TestCase1"), os.path.join(root_folder,"TestDirectory"))
        self.directory = os.path.join(os.path.dirname(__file__),"TestDirectory")


    def init(self, recursion, show_hidden_files, sorting_criteria, reverse_order):
        """Initialisation of the input arguments."""
        self.files_collection = Renamer.FilesCollection(self.directory, recursion, show_hidden_files, sorting_criteria, reverse_order)
        self.liste = list(range(10))
        self.actions = []

    def test_main_uppercase(self):
        self.init(True, False, "name", False)
        action_descriptor = Renamer.OriginalName
        files = self.files_collection
        action_args = {'untouched' : False, 'uppercase': True, 'lowercase': False, 'titlecase': False}

        self.apply_actions(files, action_descriptor, action_args, 'folder')
        self.apply_actions(files, action_descriptor, action_args, 'file')
        self.apply_actions(files, action_descriptor, action_args, 'extension')
        self.assertEqual(files, list(range(10)))

    def apply_actions(self, files_collection, action_descriptor, action_args, path_type):
        self.actions = []
        self.populate_actions(action_descriptor, action_args, path_type)
        self.files_collection.process_file_system_tree_node(self.actions)
        self.files_collection.batch_rename()

    def populate_actions(self, action_descriptor, action_args, path_type):
        """Populate the list of actions with one specified Action and the defined parameters."""
        action_instance = action_descriptor(path_type, **action_args)
        self.actions.append(action_instance)


if __name__ == '__main__':
    unittest.main()



