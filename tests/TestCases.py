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
import FileTestCreator
import RenamingType

# import whiterenamer
# from whiterenamer.model import action_manager, Controller, FileSystem
# #from whiterenamer.ui import Controller
# from . import TestCasesModel


class TestCases(unittest.TestCase):
    def setUp(self):
        self.root_folder = os.path.dirname(__file__)

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
        renamer.invoke_actions()
        renamer.batch_rename()
        renamed_filenames = self._get_filenames()
        self.assertCountEqual(renamed_filenames, test_case_model)
        shutil.rmtree(self.root_folder)

    def test_original_name(self):
        """Makes sure that orginal name keeps the original name."""
        renamer = whiterenamer.whiterenamer(self.root_folder)
        renamer.action_collection.append_action(RenamingType.foldername, "OriginalName")
        self._rename_and_verify(renamer, TestCasesModel.Main_OriginalName)

    def test_main_uppercase(self):
        """Make all letters uppercase"""
        renamer = whiterenamer.whiterenamer(self.root_folder)
        renamer.action_collection.append_action(RenamingType.foldername, "UpperCase")
        renamer.action_collection.append_action(RenamingType.filename, "UpperCase")
        renamer.action_collection.append_action(RenamingType.extension, "UpperCase")
        self._rename_and_verify(renamer, TestCasesModel.Main_Uppercase)

    def test_main_lowercase(self):
        """Make all letters lowercase"""
        renamer = whiterenamer.whiterenamer(self.root_folder)
        renamer.action_collection.append_action(RenamingType.foldername, "LowerCase")
        renamer.action_collection.append_action(RenamingType.filename, "LowerCase")
        renamer.action_collection.append_action(RenamingType.extension, "LowerCase")
        self._rename_and_verify(renamer, TestCasesModel.Main_Lowercase)

    def test_main_titlecase(self):
        """Make first letters Titlecase after space, underscore, dash and period."""
        renamer = whiterenamer.whiterenamer(self.root_folder)
        renamer.action_collection.append_action(RenamingType.foldername, "TitleCase")
        renamer.action_collection.append_action(RenamingType.filename, "TitleCase")
        renamer.action_collection.append_action(RenamingType.extension, "TitleCase")
        self._rename_and_verify(renamer, TestCasesModel.Main_Titlecase)

    def test_main_delete(self):
        """Delete first letter for folders, second for files and third for extension."""
        renamer = whiterenamer.whiterenamer(self.root_folder)
        renamer.action_collection.append_action(RenamingType.foldername, "CharacterDeletion", StringRange(0, 1))
        renamer.action_collection.append_action(RenamingType.filename, "CharacterDeletion", StringRange(1, 2))
        renamer.action_collection.append_action(RenamingType.extension, "CharacterDeletion", StringRange(2, 3))
        self._rename_and_verify(renamer, TestCasesModel.Main_Delete)

    def test_main_replace_without_regex(self):
        """Replace e with 3 and .txt with .ogg."""
        renamer = whiterenamer.whiterenamer(self.root_folder)
        renamer.action_collection.append_action(RenamingType.foldername, "FindAndReplace", "e", "3", False)
        renamer.action_collection.append_action(RenamingType.filename, "FindAndReplace", "e", "3", False)
        renamer.action_collection.append_action(RenamingType.extension, "FindAndReplace", "txt", "ogg", False)
        self._rename_and_verify(renamer, TestCasesModel.Main_Replace_without_regex)

    def test_main_replace_with_regex(self):
        """Replace folder digit with 99, file "file" with "fhis" and extension word with "pdf"."""
        renamer = whiterenamer.whiterenamer(self.root_folder)
        renamer.action_collection.append_action(RenamingType.foldername, "FindAndReplace", "\\d", "99", True)
        renamer.action_collection.append_action(RenamingType.filename, "FindAndReplace", "file", "fhis", True)
        renamer.action_collection.append_action(RenamingType.extension, "FindAndReplace", "\\w.*", "pdf", True)
        self._rename_and_verify(renamer, TestCasesModel.Main_Replace_with_regex)

    def test_main_insert(self):
        """Insert A at position 0 for folder, position 3 for files and position 99 for extension."""
        renamer = whiterenamer.whiterenamer(self.root_folder)
        renamer.action_collection.append_action(RenamingType.foldername, "CharacterInsertion", "A", 0)
        renamer.action_collection.append_action(RenamingType.filename, "CharacterInsertion", "A", 3)
        renamer.action_collection.append_action(RenamingType.extension, "CharacterInsertion", "A", None)
        self._rename_and_verify(renamer, TestCasesModel.Main_Insert)

    def test_main_folder_name(self):
        """Use foldername for folders, files."""
        renamer = whiterenamer.whiterenamer(self.root_folder)
        renamer.action_collection.append_action(RenamingType.foldername, "CharacterInsertion", "A", 0)
        renamer.action_collection.append_action(RenamingType.filename, "CharacterInsertion", "A", 3)
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
