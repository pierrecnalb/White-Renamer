#!/usr/bin/python3

import time
import re
from exifread import process_file
from mutagen.easyid3 import EasyID3
import abc
from string_tokenizer import StringTokenizer
from string_range import StringRange
import Scope
from file_node import FileNode
from folder_node import FolderNode


class RenamingAction(object):
    """
Describes how the action is applied on the FilesystemNodes. This class
is inherited by all the specific actions.
    Parameters:
        --name: string that represents where the action will be applied.
    name can be 'folder', 'file', 'prefix', 'suffix' or 'extension'.
        --file_or_folder: specifies where to apply the actions : to the files or the folders.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, scope=Scope.filename, string_range=StringRange(0, None)):
        self._scope = scope
        self._string_range = string_range

    @property
    def string_range(self):
        return self._string_range

    @abc.abstractmethod
    def _get_modified_substring(self, filesystem_node, original_substring):
        """Gets the modified portion of the file/folder name.
        The portion is defined by the string_range."""

    def _is_scope_valid(self, filesystem_node):
        if (isinstance(filesystem_node, FileNode)):
            if (self._scope is Scope.filename or self._scope is Scope.extension):
                return True
        if (self._scope is Scope.foldername and not isinstance(filesystem_node, FolderNode)):
            return True
        return False

    def _get_original_name(self, filesystem_node):
        original_name = ""
        if (self._scope is Scope.filename or self._scope is Scope.foldername):
            original_name = filesystem_node.basename
        elif (self._scope is Scope.extension):
            original_name = filesystem_node.extension
        return original_name

    def execute(self, filesystem_node):
        if (not self._is_scope_valid(filesystem_node)):
            raise Exception("Invalid scope: it cannot be applied to the given filesystem node.")
        original_name = self._get_original_name(filesystem_node)
        tokenizer = StringTokenizer(original_name, self._string_range)
        original_substring = tokenizer.selected_token
        modified_substring = self._get_modified_substring(filesystem_node, original_substring)
        new_name = tokenizer.first_token + modified_substring + tokenizer.last_token
        return new_name


class FindAndReplaceAction(RenamingAction):
    """
    Replace old_char by new_char in the section of the path.
    string_range can be 'folder', 'file', 'prefix', 'suffix' or 'extension'.
    """

    def __init__(self, old_char, new_char, is_regex, scope=Scope.filename, string_range=None):
        super().__init__(scope, string_range)
        self._old_char = old_char
        self._new_char = new_char
        self._is_regex = is_regex

    def _get_modified_substring(self, filesystem_node, original_substring):
        if not self._is_regex:
            return original_substring.replace(self._old_char, self._new_char)
        else:
            return re.sub(self._old_char, self._new_char, original_substring)


class OriginalNameAction(RenamingAction):
    """Gets the original name."""

    def __init__(self, scope=Scope.filename, string_range=None):
        super().__init__(scope, string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        return original_substring


class TitleCaseAction(RenamingAction):
    """
    Return the original name with a chosen casing option.
    Parameters:
        --case_choise: option to specify the case : 'uppercase', 'lowercase', 'titlecase'.
        --is_first_letter_uppercase: boolean making first letter uppercase or lowercase.
        --special_characters: list of symbols after which the letters are capitalized.
    """

    def __init__(self, is_first_letter_uppercase=True, special_characters="", scope=Scope.filename, string_range=None):
        super().__init__(scope, string_range)
        self._is_first_letter_uppercase = is_first_letter_uppercase
        self._special_characters = special_characters

    def _get_decomposed_name(self, original_substring):
        decomposed_name = list(original_substring)
        return decomposed_name

    def _get_special_character_indices(self, original_substring):
        decomposed_name = self._get_decomposed_name(original_substring)
        special_character_indices = []
        for index, character in enumerate(decomposed_name):
            if character in self._special_characters:
                special_character_indices.append(index)
        return special_character_indices

    def _get_modified_substring(self, filesystem_node, original_substring):
        decomposed_name = self._get_decomposed_name(original_substring)
        for special_character_index in self._get_special_character_indices(original_substring):
            if special_character_index < len(decomposed_name):
                decomposed_name[special_character_index + 1] = decomposed_name[special_character_index + 1].upper()
        if self._is_first_letter_uppercase:
            decomposed_name[0] = decomposed_name[0].upper()
        modified_sliced_name = ''.join(decomposed_name)
        return modified_sliced_name


class UpperCaseAction(RenamingAction):
    """
    Return the original name with a chosen casing option.
    Parameters:
        --case_choise: option to specify the case : 'uppercase', 'lowercase', 'titlecase'.
        --is_first_letter_uppercase: boolean making first letter uppercase or lowercase.
        --special_characters: list of symbols after which the letters are capitalized.
    """

    def __init__(self, scope=Scope.filename, string_range=None):
        super().__init__(scope, string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        return original_substring.upper()


class LowerCaseAction(RenamingAction):
    """
    Return the original name with a chosen casing option.
    Parameters:
        --case_choise: option to specify the case : 'uppercase', 'lowercase', 'titlecase'.
        --is_first_letter_uppercase: boolean making first letter uppercase or lowercase.
        --special_characters: list of symbols after which the letters are capitalized.
    """

    def __init__(self, scope=Scope.filename, string_range=None):
        super().__init__(scope, string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        return original_substring.lower()


class CustomNameAction(RenamingAction):
    """Use a custom name in the filename.
    Can be also used to remove character if en empty string is given.
    """

    def __init__(self, custom_name, scope=Scope.filename, string_range=None):
        super().__init__(scope, string_range)
        self._custom_name = custom_name

    def _get_modified_substring(self, filesystem_node, original_substring):
        return self._custom_name


class FolderNameAction(RenamingAction):
    """Use the parent foldername as the filename."""

    def __init__(self, scope=Scope.filename, string_range=None):
        super().__init__(scope, string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        folder_name = self._file_system_tree_node.parent.modified_basename
        return folder_name


class DateAction(RenamingAction):
    """
    Use the created or modified date metadata as the filename.
    If is_modified_time = True, the modified date from the file metadata is taken. Otherwise, it is the created date.
    Commonly used format_display are :
    %y  year with century as a decimal number.
    %m  month as a decimal number [01,12].
    %d  day of the month as a decimal number [01,31].
    %h  hour (24-hour clock) as a decimal number [00,23].
    %m  minute as a decimal number [00,59].
    %s  second as a decimal number [00,61].
    %z  time zone offset from utc.
    %a  locale's abbreviated weekday name.
    %a  locale's full weekday name.
    %b  locale's abbreviated month name.
    %b  locale's full month name.
    %c  locale's appropriate date and time representation.
    %i  hour (12-hour clock) as a decimal number [01,12].
    %p  locale's equivalent of either am or pm.
    """

    def __init__(self, is_modified_date=True, time_format='%Y', scope=Scope.filename, string_range=None):
        super().__init__(scope, string_range)
        self._is_modified_date = is_modified_date
        self._display_format = time_format

    def _get_modified_substring(self, filesystem_node, original_substring):
        if self.is_modified_date:
            file_date = self._file_system_tree_node.modified_date
        else:
            # created date
            file_date = self._file_system_tree_node.created_date
        return time.strftime(self.format_display, time.localtime(file_date))


# class Counter(RenamingAction):
#     """Count the number of files starting from start_index with the given increment."""

#     def __init__(self, string, string_range, start_index, increment, digit_number):
#         super().__init__(scope, string, string_range)
#         self._start_index = start_index
#         self._increment = increment
#         self._digit_number = digit_number

#     def _get_modified_substring(self, filesystem_node, original_substring):
#         counter = self.string.rank
#         counter *= self.increment
#         counter += self.start_index
#         counter = str(counter)
#         number_length = len(str(counter))
#         if (number_length < self.digit_number):
#             for i in range(self.digit_number - number_length):
#                 counter = "0" + counter
#         return counter


class GenericImageAction(RenamingAction):
    def __init__(self, metadata, scope=Scope.filename, string_range=None):
        super().__init__(scope, string_range)
        self._metadata = metadata

    def _get_exif_tag(self, filesystem_node):
        file_path = filesystem_node.original_path
        with open(file_path, 'rb') as f:
            tags = process_file(f, details=False, stop_tag=self.metadata)
            exif_tag = tags[self.metadata].values
            return exif_tag


class ImageDateTimeOriginal(GenericImageAction):
    def __init__(self, time_format, scope=Scope.filename, string_range=None):
        super().__init__('EXIF DateTimeOriginal', scope, string_range)
        self._time_format = time_format

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            exif_tag = self._get_exif_tag(filesystem_node)
            localtime = time.strptime(exif_tag, "%Y:%m:%d %H:%M:%S")
            return time.strftime(self._time_format, localtime)
        except:
            return original_substring


class ImageFNumber(GenericImageAction):
    def __init__(self, scope=Scope.filename, string_range=None):
        super().__init__('EXIF FNumber', scope, string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            exif_tag = self._get_exif_tag(filesystem_node)
            return str(exif_tag[0].num / exif_tag[0].den)
        except:
            return original_substring


class ImageExposureTime(GenericImageAction):
    def __init__(self, scope=Scope.filename, string_range=None):
        super().__init__('EXIF ExposureTime', scope, string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            exif_tag = self._get_exif_tag(filesystem_node)
            return str(exif_tag[0].num / exif_tag[0].den)
        except:
            return original_substring


class ImageISO(GenericImageAction):
    def __init__(self, scope=Scope.filename, string_range=None):
        super().__init__('EXIF ISOSpeedRatings', scope, string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            exif_tag = self._get_exif_tag(filesystem_node)
            return str(exif_tag[0])
        except:
            return original_substring


class ImageCameraModel(GenericImageAction):
    def __init__(self, scope=Scope.filename, string_range=None):
        super().__init__('Image Model', scope, string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            exif_tag = self._get_exif_tag(filesystem_node)
            return exif_tag
        except:
            return original_substring


class ImageXDimension(GenericImageAction):
    def __init__(self, scope=Scope.filename, string_range=None):
        super().__init__('EXIF ExifImageWidth', scope, string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            exif_tag = self._get_exif_tag(filesystem_node)
            return str(exif_tag[0])
        except:
            return original_substring


class ImageYDimension(GenericImageAction):
    def __init__(self, scope=Scope.filename, string_range=None):
        super().__init__('EXIF ExifImageLength', scope, string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            exif_tag = self._get_exif_tag(filesystem_node)
            return str(exif_tag[0])
        except:
            return original_substring


class ImageFocalLength(GenericImageAction):
    def __init__(self, scope=Scope.filename, string_range=None):
        super().__init__('EXIF FocalLength', scope, string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            exif_tag = self._get_exif_tag(filesystem_node)
            return str(exif_tag[0].num / exif_tag[0].den)
        except:
            return original_substring


class ImageArtist(GenericImageAction):
    def __init__(self, scope=Scope.filename, string_range=None):
        super().__init__('Image Artist', scope, string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            exif_tag = self._get_exif_tag(filesystem_node)
            return exif_tag
        except:
            return original_substring


class GenericMusicAction(RenamingAction):
    def __init__(self, metadata, scope=Scope.filename, string_range=None):
        super().__init__(scope, string_range)
        self.metadata = metadata

    def _get_metadata_tag(self, filesystem_node):
        file_path = filesystem_node.original_path
        audio = EasyID3(file_path)
        return ', '.join(audio[self.metadata])


class MusicArtist(GenericMusicAction):
    def __init__(self, scope=Scope.filename, string_range=None):
        super().__init__('artist', scope, string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            metadata_tag = self._get_metadata_tag(filesystem_node)
            return metadata_tag
        except:
            return original_substring


class MusicTitle(GenericMusicAction):
    def __init__(self, scope=Scope.filename, string_range=None):
        super().__init__('title', scope, string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            metadata_tag = self._get_metadata_tag(filesystem_node)
            return metadata_tag
        except:
            return original_substring


class MusicYear(GenericMusicAction):
    def __init__(self, scope=Scope.filename, string_range=None):
        super().__init__('date', scope, string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            metadata_tag = self._get_metadata_tag(filesystem_node)
            return metadata_tag
        except:
            return original_substring


class MusicAlbum(GenericMusicAction):
    def __init__(self, scope=Scope.filename, string_range=None):
        super().__init__('album', scope, string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            metadata_tag = self._get_metadata_tag(filesystem_node)
            return metadata_tag
        except:
            return original_substring


class MusicTrack(GenericMusicAction):
    def __init__(self, scope=Scope.filename, string_range=None):
        super().__init__('tracknumber', scope, string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            metadata_tag = self._get_metadata_tag(filesystem_node)
            return metadata_tag
        except:
            return original_substring


class MusicGenre(GenericMusicAction):
    def __init__(self, scope=Scope.filename, string_range=None):
        super().__init__('genre', scope, string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            metadata_tag = self._get_metadata_tag(filesystem_node)
            return metadata_tag
        except:
            return original_substring
