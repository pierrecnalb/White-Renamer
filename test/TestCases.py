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
    def setUp(self):
        """Initialisation of the input arguments."""
        directory = os.path.join(os.getcwd(), "Documents","Programs","White-Renamer","test","Test Directory")
        self.files = Renamer.FilesCollection(directory, False)
        self.liste = list(range(10))
        self.actions = []

    def uppercase_folder_test(self):
        action_descriptor = Renamer.OriginalName
        files = self.files
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
        self.data = self.files.get_files()
        self.populate_actions(action_descriptor, action_args, path_type)
        input_path.call_actions(self.actions, self.data)

