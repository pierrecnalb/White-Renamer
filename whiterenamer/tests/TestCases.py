#author : pierrecnalb
#copyright pierrecnalb
import unittest
import re
import random
import os
import sys
import shutil
import pdb
import io
sys.path.append('/home/pierre/Documents/Programs/White-Renamer/')

from whiterenamer.model import action_manager, Controller, FileSystem
#from whiterenamer.ui import Controller
import TestCasesModel

class TestCases(unittest.TestCase):
    """TestCases used to verify the functions from the module 'action_manager'."""
    def setUp(self):
        self.root_folder = os.path.dirname(__file__)

    def init(self, directory, recursion, show_hidden_files, sorting_criteria, reverse_order, files_type = ["*.*"], name_filter = ""):
        """Initialisation of the input arguments."""
        shutil.copytree(os.path.join(self.root_folder, directory), os.path.join(self.root_folder,"TestDirectory"))
        self.directory = os.path.join(os.path.dirname(__file__),"TestDirectory")
        self.recursion = recursion
        self.show_hidden_files = show_hidden_files
        self.sorting_criteria = sorting_criteria
        self.reverse_order = reverse_order
        self.files_type = files_type
        self.name_filter = name_filter
        self.files_system = FileSystem(self.directory, self.recursion)
        self.files_collection = self.files_system.generate_files_system_view(show_hidden_files, self.files_type, self.name_filter, self.sorting_criteria, self.reverse_order)
        self.controller = Controller(self.files_collection)
        self.files_list = []
        self.actions = []

    def test_main_original(self):
        """Test to be sure that orginalnameaction is not doing anything."""
        self.init("TestCase1", True, False, "name", False)
        action_descriptor = action_manager.OriginalNameAction
        files = self.files_collection
        action_args = {}
        self.apply_actions(action_descriptor, action_args, 'folder', 'folder')
        self.apply_actions(action_descriptor, action_args, 'file', 'file')
        self.apply_actions(action_descriptor, action_args, 'extension','file')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Main_OriginalName)
# 
    def test_main_uppercase(self):
        """Make all letters uppercase"""
        self.init("TestCase1", True, False, "name", False)
        action_descriptor = action_manager.UpperCaseAction
        files = self.files_collection
        action_args = {}
        self.apply_actions(action_descriptor, action_args, 'folder', 'folder')
        self.apply_actions(action_descriptor, action_args, 'file', 'file')
        self.apply_actions(action_descriptor, action_args, 'extension', 'file')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Main_Uppercase)
# # # 
    def test_main_lowercase(self):
        """Make all letters lowercase"""
        self.init("TestCase1", True, False, "name", False)
        action_descriptor = action_manager.LowerCaseAction
        files = self.files_collection
        action_args = {}
        self.apply_actions(action_descriptor, action_args, 'folder', 'folder')
        self.apply_actions(action_descriptor, action_args, 'file', 'file')
        self.apply_actions(action_descriptor, action_args, 'extension', 'file')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Main_Lowercase)
# # # # 
    def test_main_titlecase(self):
        """Make first letters Titlecase after space, underscore, dash and period."""
        self.init("TestCase1", True, False, "name", False)
        action_descriptor = action_manager.TitleCaseAction
        files = self.files_collection
        action_args = {'first_letter': True, 'after_symbols': ' -_.'}
        self.apply_actions(action_descriptor, action_args, 'folder', 'folder')
        self.apply_actions(action_descriptor, action_args, 'file', 'file')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Main_TitleCase)
# # # 
    def test_main_delete(self):
        """Delete first letter for folders, second for files and third for extension."""
        self.init("TestCase1", True, False, "name", False)
        action_descriptor = action_manager.CharacterDeletionAction
        files = self.files_collection
        action_args_folder = {'starting_position' : 0, 'ending_position' : 1}
        action_args_file = {'starting_position' : 1, 'ending_position' : 2}
        action_args_extension = {'starting_position' : 2, 'ending_position' : 3}
        self.apply_actions(action_descriptor, action_args_folder, 'folder', 'folder')
        self.apply_actions(action_descriptor, action_args_file, 'file', 'file')
        self.apply_actions(action_descriptor, action_args_extension, 'extension', 'file')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Main_Delete)
# # # # 
    def test_main_replace_without_regex(self):
        """Replace e with 3 and .txt with .ogg."""
        self.init("TestCase1", True, False, "name", False)
        action_descriptor = action_manager.CharacterReplacementAction
        files = self.files_collection
        action_args_folder = {'old_char' : 'e', 'new_char' : '3', 'regex': False}
        action_args_file = {'old_char' : 'e', 'new_char' : '3', 'regex': False}
        action_args_extension = {'old_char' : 'txt', 'new_char' : 'ogg', 'regex': False}
        self.apply_actions(action_descriptor, action_args_folder, 'folder','folder')
        self.apply_actions(action_descriptor, action_args_file, 'file', 'file')
        self.apply_actions(action_descriptor, action_args_extension, 'extension', 'file')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Main_Replace_without_regex)
# # # # 
    def test_main_replace_with_regex(self):
        """Replace folder digit with 99, file "file" with "fhis" and extension word with "pdf"."""
        self.init("TestCase1", True, False, "name", False)
        action_descriptor = action_manager.CharacterReplacementAction
        files = self.files_collection
        action_args_folder = {'old_char' : '\\d', 'new_char' : '99', 'regex': True}
        action_args_file = {'old_char' : 'file', 'new_char' : 'fhis', 'regex': True}
        action_args_extension = {'old_char' : '\\w.*', 'new_char' : 'pdf', 'regex': True}
        self.apply_actions(action_descriptor, action_args_folder, 'folder', 'folder')
        self.apply_actions(action_descriptor, action_args_file, 'file', 'file')
        self.apply_actions(action_descriptor, action_args_extension, 'extension', 'file')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Main_Replace_with_regex)
# # # # 
    def test_main_insert(self):
        """Insert A at position 0 for folder, position 3 for files and position 99 for extension."""
        self.init("TestCase1", True, False, "name", False)
        action_descriptor = action_manager.CharacterInsertionAction
        files = self.files_collection
        action_args_folder = {'new_char' : 'A', 'index': 0}
        action_args_file = {'new_char' : 'A', 'index': 3}
        action_args_extension = {'new_char' : 'A', 'index': 99}
        self.apply_actions(action_descriptor, action_args_folder, 'folder', 'folder')
        self.apply_actions(action_descriptor, action_args_file, 'file', 'file')
        self.apply_actions(action_descriptor, action_args_extension, 'extension', 'file')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Main_Insert)
# # 
    def test_main_undo(self):
        """Name all folders 'folder', files 'file' and extensions '.ext'. and undo the actions after renaming."""
        self.init("TestCase1", True, False, "name", False)
        action_descriptor = action_manager.CustomNameAction
        files = self.files_collection
        action_args_folder = {'new_name' : 'folder'}
        action_args_file = {'new_name' : 'file'}
        action_args_extension = {'new_name' : '.ext'}
        self.apply_actions(action_descriptor, action_args_folder, 'prefix', 'folder')
        self.apply_actions(action_descriptor, action_args_file, 'prefix', 'file')
        self.apply_actions(action_descriptor, action_args_extension, 'extension', 'file')
        self.controller.batch_undo()
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Main_OriginalName)
# # # 
    def test_main_folder_name(self):
        """Use foldername for folders, files."""
        self.init("TestCase1", True, False, "name", False)
        action_descriptor = action_manager.FolderNameUsageAction
        files = self.files_collection
        action_args_folder = {}
        action_args_file = {}
        action_args_extension = {}
        self.apply_actions(action_descriptor, action_args_file, 'prefix', 'file')
        self.apply_actions(action_descriptor, action_args_folder, 'prefix', 'folder')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Main_FolderName)
# # 
    def test_main_custom_prefix_suffix(self):
        """Add a prefix 'prefix ' and a suffix ' suffix'."""
        self.init("TestCase1", True, False, "name", False)
        action_descriptor = action_manager.CustomNameAction
        files = self.files_collection
        action_args_prefix = {'new_name' : 'prefix '}
        action_args_suffix = {'new_name' : ' suffix'}
        self.apply_actions(action_descriptor, action_args_prefix, 'prefix', 'file')
        self.apply_actions(action_descriptor, action_args_suffix, 'suffix', 'file')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Main_Custom_Prefix_Suffix)
# # # 
    def test_main_counter_sort_by_name(self):
        """Folder with counter from 0 and inc = 1, prefix from 2 and inc = 4. Sorted by name."""
        self.init("TestCase1", True, False, "name", False)
        action_descriptor = action_manager.Counter
        files = self.files_collection
        action_args_folder = {'start_index' : 0, 'increment': 1, 'digit_number':1}
        action_args_prefix = {'start_index' : 2, 'increment': 4, 'digit_number':2}
        self.apply_actions(action_descriptor, action_args_folder, 'folder', 'folder')
        self.apply_actions(action_descriptor, action_args_prefix, 'prefix', 'file')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Main_Counter_Name_Sort)
# # 
    def test_main_counter_sort_reverse_by_name(self):
        """Folder with counter from 0 and inc = 1, file from 0 and inc = 1. Sorted by name in reverse order."""
        self.init("TestCase1", True, False, "name", True)
        action_descriptor = action_manager.Counter
        files = self.files_collection
        action_args = {'start_index' : 0, 'increment': 1, 'digit_number':0}
        self.apply_actions(action_descriptor, action_args, 'suffix', 'folder')
        self.apply_actions(action_descriptor, action_args, 'suffix', 'file')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Main_Counter_Reverse_Name_Sort)
# # 
    def test_main_counter_sort_by_size(self):
        """Folder with counter from 0 and inc = 1, file from 0 and inc = 1. Sorted by size."""
        self.init("TestCase1", True, False, "size", False)
        action_descriptor = action_manager.Counter
        files = self.files_collection
        action_args = {'start_index' : 0, 'increment': 1, 'digit_number':0}
        self.apply_actions(action_descriptor, action_args, 'prefix', 'folder')
        self.apply_actions(action_descriptor, action_args, 'prefix', 'file')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Main_Counter_Size_Sort)
# # # 
    def test_accent_encoding(self):
        """Use accent and special characters to see if the encoding is supported."""
        self.init("TestCase1", True, False, "name", False)
        action_descriptor = action_manager.CustomNameAction
        files = self.files_collection
        action_args = {'new_name' : 'éèùà€ç'}
        self.apply_actions(action_descriptor, action_args, 'suffix', 'file')
        self.apply_actions(action_descriptor, action_args, 'suffix', 'folder')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Accent_Encoding)
# 
    def test_image_date(self):
        """Use image metadata to retrieve the original date."""
        self.init("images", True, False, "name", False)
        action_descriptor = action_manager.ImageDateTimeOriginal
        files = self.files_collection
        action_args = {'time_format' : '%Y-%m-%d %H:%M:%S'}
        self.apply_actions(action_descriptor, action_args, 'file', 'file')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Image_Date)
    def test_image_xdimension(self):
        """Use image metadata to retrieve the width."""
        self.init("images", True, False, "name", False)
        action_descriptor = action_manager.ImageXDimension
        files = self.files_collection
        action_args = {}
        self.apply_actions(action_descriptor, action_args, 'prefix', 'file')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Image_XDimension)
    def test_image_ydimension(self):
        """Use image metadata to retrieve the length."""
        self.init("images", True, False, "name", False)
        action_descriptor = action_manager.ImageYDimension
        files = self.files_collection
        action_args = {}
        self.apply_actions(action_descriptor, action_args, 'prefix', 'file')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Image_YDimension)
    def test_image_iso(self):
        """Use image metadata to retrieve the iso."""
        self.init("images", True, False, "name", False)
        action_descriptor = action_manager.ImageISO
        files = self.files_collection
        action_args = {}
        self.apply_actions(action_descriptor, action_args, 'prefix', 'file')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Image_ISO)
    def test_image_model(self):
        """Use image metadata to retrieve the camera model."""
        self.init("images", True, False, "name", False)
        action_descriptor = action_manager.ImageCameraModel
        files = self.files_collection
        action_args = {}
        self.apply_actions(action_descriptor, action_args, 'prefix', 'file')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Image_Camera)

    def test_music_artist(self):
        """Use image metadata to retrieve the camera model."""
        self.init("music", True, False, "name", False)
        action_descriptor = action_manager.MusicArtist
        files = self.files_collection
        action_args = {}
        self.apply_actions(action_descriptor, action_args, 'prefix', 'file')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Music_Artist)
    def test_music_album(self):
        """Use image metadata to retrieve the camera model."""
        self.init("music", True, False, "name", False)
        action_descriptor = action_manager.MusicAlbum
        files = self.files_collection
        action_args = {}
        self.apply_actions(action_descriptor, action_args, 'prefix', 'file')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Music_Album)
    def test_music_year(self):
        """Use image metadata to retrieve the camera model."""
        self.init("music", True, False, "name", False)
        action_descriptor = action_manager.MusicYear
        files = self.files_collection
        action_args = {}
        self.apply_actions(action_descriptor, action_args, 'prefix', 'file')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Music_Year)
    def test_music_genre(self):
        """Use image metadata to retrieve the camera model."""
        self.init("music", True, False, "name", False)
        action_descriptor = action_manager.MusicGenre
        files = self.files_collection
        action_args = {}
        self.apply_actions(action_descriptor, action_args, 'file', 'file')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Music_Genre)
    def test_music_track(self):
        """Use image metadata to retrieve the camera model."""
        self.init("music", True, False, "name", False)
        action_descriptor = action_manager.MusicTrack
        files = self.files_collection
        action_args = {}
        self.apply_actions(action_descriptor, action_args, 'file', 'file')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Music_Track)
    def test_music_title(self):
        """Use image metadata to retrieve the camera model."""
        self.init("music", True, False, "name", False)
        action_descriptor = action_manager.MusicTitle
        files = self.files_collection
        action_args = {}
        self.apply_actions(action_descriptor, action_args, 'file', 'file')
        self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        self.compare_with_model_file(TestCasesModel.Music_Title)

    def compare_with_model_file(self, model_file):
        self.assertCountEqual(self.files_list, model_file)
        shutil.rmtree(self.directory)

    def apply_actions(self, action_descriptor, action_args, path_type, file_or_folder):
        self.actions = []
        self.populate_actions(action_descriptor, action_args, path_type)
        self.controller.batch_update(self.actions, file_or_folder)
        self.controller.batch_rename()

    def populate_actions(self, action_descriptor, action_args, path_type):
        """Populate the list of actions with one specified Action and the defined parameters."""
        action_instance = action_descriptor(path_type, **action_args)
        self.actions.append(action_instance)

    def scan_directory(self, input_path, sorting_criteria, reverse_order):
        input_path = os.path.abspath(input_path)
        directory_files = sorted(os.listdir(input_path), key = lambda file : self.get_sorting_key(os.path.join(input_path,file)), reverse=reverse_order)
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
                self.files_list.append(os.path.relpath(filepath, self.root_folder ))

    def natural_sort(self, filename):
        """ Sorts the given iterable in the way that is expected.
        """
        convert = lambda text: int(text) if text.isdigit() else text
        alphanum_key = [convert(c) for c in re.split('([0-9]+)', filename)]
        return alphanum_key

    def get_sorting_key(self, path):
        """
        Criteria to sort the files.
        Parameters:
            --tree_node: path to the specified file/folder.
            --sorting_criteria: string that specifies the sorting criteria. Default is 'name'. Possible values are : name, size, creation_date and modified_date.
        """
        if self.sorting_criteria == "size":
            return os.path.getsize(path)
        elif self.sorting_criteria == "modified_date":
            return os.path.getmtime(path)
        elif self.sorting_criteria ==  "creation_date":
            return os.path.getctime(path)
        elif self.sorting_criteria == "name":
            return self.natural_sort(os.path.basename(path))
        else:
            return None

if __name__ == '__main__':
    unittest.main()



