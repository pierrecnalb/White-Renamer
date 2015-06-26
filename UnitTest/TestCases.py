#author : pierrecnalb
#copyright pierrecnalb
import unittest
import random
import os
import sys
sys.path.append('/home/pierre/Documents/Programs/White-Renamer/')
import Renamer

class TestCases(unittest.TestCase):
    """TestCases used to verify the functions from the module 'Renamer'."""
    def set_up(self, recursion, show_hidden_files, sorting_criteria, reverse_order):
        """Initialisation of the input arguments."""

        self.directory = os.path.join(os.path.dirname(__file__),"Test Directory")
        self.files_collection = Renamer.FilesCollection(self.directory, recursion, show_hidden_files, sorting_criteria, reverse_order)
        self.liste = list(range(10))
        self.actions = []



    def test_uppercase_folder(self):
        self.set_up(True, False, "name", False)
        action_descriptor = Renamer.OriginalName
        files = self.files_collection
        action_args = {'untouched' : False, 'uppercase': True, 'lowercase': False, 'titlecase': False}
        self.apply_actions(files, action_descriptor, action_args, 'file')
        print(files)
        self.assertEqual(files, list(range(10)))

    def populate_actions(self, action_descriptor, action_args, path_type):
        """Populate the list of actions with one specified Action and the defined parameters."""
        action_instance = action_descriptor(path_type, **action_args)
        self.actions.append(action_instance)

    def apply_actions(self, input_path, action_descriptor, action_args, path_type):
        self.actions = []
        self.populate_actions(action_descriptor, action_args, path_type)
        self.files_collection.process_file_system_tree_node(self.actions)

if __name__ == '__main__':
    unittest.main()



