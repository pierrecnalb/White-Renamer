#author : pierrecnalb
#copyright pierrecnalb
import unittest
import random
import os
import sys
import io
sys.path.append('/home/pierre/Documents/Programs/White-Renamer/')
import Renamer

class TestCases(unittest.TestCase):
    """TestCases used to verify the functions from the module 'Renamer'."""
    def set_up(self, recursion, show_hidden_files, sorting_criteria, reverse_order):
        """Initialisation of the input arguments."""

        self.directory = os.path.join(os.path.dirname(__file__))
        self.create_folder("TestCase1")
        self.directory = os.path.join(os.path.dirname(__file__),"TestCase1")
        self.create_folder("FOLDER1")
        self.create_folder(os.path.join("FOLDER1","sub fOlder_1"))
        self.create_folder(os.path.join("FOLDER1","sub.FOLDER 2"))
        self.create_folder("folder 2")
        self.create_file("file.with.dots.txt")
        self.create_file("file with é è.txt")
        self.create_file("file_with_underscore.txt")
        self.create_file("l'appostrophe.txt")
        self.create_file(os.path.join("FOLDER1","folder1-file1.txt"))
        self.create_file(os.path.join("FOLDER1","folder1-sub file #2.txt"))
        self.create_file(os.path.join("FOLDER1","sub fOlder_1","sub file 1"))
        self.create_file(os.path.join("FOLDER1","sub fOlder_1","sub file 2"))
        self.files_collection = Renamer.FilesCollection(directory, recursion, show_hidden_files, sorting_criteria, reverse_order)
        self.liste = list(range(10))
        self.actions = []

    def create_file(self, name):
        file = io.open(os.path.join(self.directory, name), 'x')
        file.write(name)
        file.close()

    def create_folder(self, name):
        os.makedirs(os.path.join(self.directory, name))

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



