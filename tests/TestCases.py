#!/usr/bin/python3
# -*- coding: utf-8 -*-

# import re
import os
import sys
import shutil
import unittest
from . import TestCasesModel
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# print(path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))))
# sys.path.append('/home/pierre/Documents/Programs/white-renamer/whiterenamer')
import whiterenamer
import file_tests
import RenamingType

# import whiterenamer
# from whiterenamer.model import action_manager, Controller, FileSystem
# #from whiterenamer.ui import Controller
# from . import TestCasesModel


class TestCases(unittest.TestCase):
    def setUp(self):
        self.root_folder = os.path.dirname(__file__)
        self.renamer = whiterenamer.whiterenamer(self.root_folder)
        file_tests.create(root_name)

    def tearDown(self):
        if(os.path.exists(self.root_folder)):
            shutil.rmtree(self.root_folder)

    def _get_filenames(self):
        scanned_files = []
        self._scan_directory(self.root_folder, scanned_files)
        return scanned_files

    def _scan_directory(self, path, scanned_files):
        input_path = os.path.abspath(path)
        directory_files = os.listdir(input_path)
        for filename in directory_files:
            filepath = os.path.join(input_path, filename)
            scanned_files.append(os.path.relpath(filepath, input_path))
            if os.path.isdir(filepath):
                self._scan_directory(filepath, scanned_files)

    def _rename_and_verify(self, renamer, test_case_model):
        self.renamer.invoke_actions()
        self.renamer.batch_rename()
        renamed_filenames = self._get_filenames()
        self.assertCountEqual(renamed_filenames, test_case_model)

    def test_original_name(self):
        """Makes sure that orginal name keeps the original name."""
        self.renamer.action_collection.append(RenamingType.foldername, "OriginalName")
        self._rename_and_verify(renamer, TestCasesModel.Main_OriginalName)

    def test_main_uppercase(self):
        """Make all letters uppercase"""
        self.renamer.action_collection.append("UpperCase", scope=filename|foldername|extension)
        self._rename_and_verify(renamer, TestCasesModel.Main_Uppercase)

    def test_main_lowercase(self):
        """Make all letters lowercase"""
        self.renamer.action_collection.append("LowerCase", scope=filename|foldername|extension)
        self._rename_and_verify(renamer, TestCasesModel.Main_Lowercase)

    def test_main_titlecase(self):
        """Make first letters Titlecase after space, underscore, dash and period."""
        self.renamer.action_collection.append("TitleCase", scope=filename|foldername|extension)
        self._rename_and_verify(renamer, TestCasesModel.Main_Titlecase)

    def test_main_delete(self):
        """Delete first letter for folders, second for files and third for extension."""
        self.renamer.action_collection.append("CharacterDeletion",  string_range=StringRange(0, 1))
        self.renamer.action_collection.append(RenamingType.filename, "CharacterDeletion", StringRange(1, 2))
        self.renamer.action_collection.append(RenamingType.extension, "CharacterDeletion", StringRange(2, 3))
        self._rename_and_verify(renamer, TestCasesModel.Main_Delete)

    def test_main_replace_without_regex(self):
        """Replace e with 3 and .txt with .ogg."""
        self.renamer.action_collection.append(RenamingType.foldername, "FindAndReplace", "e", "3", False)
        self.renamer.action_collection.append(RenamingType.filename, "FindAndReplace", "e", "3", False)
        self.renamer.action_collection.append(RenamingType.extension, "FindAndReplace", "txt", "ogg", False)
        self._rename_and_verify(renamer, TestCasesModel.Main_Replace_without_regex)

    def test_main_replace_with_regex(self):
        """Replace folder digit with 99, file "file" with "fhis" and extension word with "pdf"."""
        self.renamer.action_collection.append(RenamingType.foldername, "FindAndReplace", "\\d", "99", True)
        self.renamer.action_collection.append(RenamingType.filename, "FindAndReplace", "file", "fhis", True)
        self.renamer.action_collection.append(RenamingType.extension, "FindAndReplace", "\\w.*", "pdf", True)
        self._rename_and_verify(renamer, TestCasesModel.Main_Replace_with_regex)

    def test_main_insert(self):
        """Insert A at position 0 for folder, position 3 for files and position 99 for extension."""
        self.renamer.action_collection.append(RenamingType.foldername, "CharacterInsertion", "A", 0)
        self.renamer.action_collection.append(RenamingType.filename, "CharacterInsertion", "A", 3)
        self.renamer.action_collection.append(RenamingType.extension, "CharacterInsertion", "A", None)
        self._rename_and_verify(renamer, TestCasesModel.Main_Insert)

    def test_main_folder_name(self):
        """Use foldername for folders, files."""
        self.renamer.action_collection.append(RenamingType.foldername, "CharacterInsertion", "A", 0)
        self.renamer.action_collection.append(RenamingType.filename, "CharacterInsertion", "A", 3)
        self._rename_and_verify(renamer, TestCasesModel.Main_FolderName)
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
        action_args_prefix = {'new_name': 'prefix '}
        action_args_suffix = {'new_name': ' suffix'}
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
        action_args_folder = {'start_index': 0, 'increment': 1, 'digit_number': 1}
        action_args_prefix = {'start_index': 2, 'increment': 4, 'digit_number': 2}
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
        action_args = {'start_index': 0, 'increment': 1, 'digit_number': 0}
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
        action_args = {'start_index': 0, 'increment': 1, 'digit_number': 0}
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
        action_args = {'new_name': 'éèùà€ç'}
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
        action_args = {'time_format': '%Y-%m-%d %H:%M:%S'}
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

    # def test_main_undo(self):
    #     """Name all folders 'folder', files 'file' and extensions '.ext'. and undo the actions after renaming."""
    #     self.init("TestCase1", True, False, "name", False)
    #     action_descriptor = action_manager.CustomNameAction
    #     files = self.files_collection
    #     action_args_folder = {'new_name': 'folder'}
    #     action_args_file = {'new_name': 'file'}
    #     action_args_extension = {'new_name': '.ext'}
    #     self.apply_actions(action_descriptor, action_args_folder, 'prefix', 'folder')
    #     self.apply_actions(action_descriptor, action_args_file, 'prefix', 'file')
    #     self.apply_actions(action_descriptor, action_args_extension, 'extension', 'file')
    #     self.controller.batch_undo()
    #     self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        # self.compare_with_model_file(TestCasesModel.Main_OriginalName)

if __name__ == '__main__':
    unittest.main()
