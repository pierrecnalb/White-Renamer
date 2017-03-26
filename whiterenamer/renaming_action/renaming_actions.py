#!/usr/bin/python3

import time
import re
from exifread import process_file
from mutagen.easyid3 import EasyID3
import abc
from string_slicer import StringSlicer
from string_range import StringRange


class RenamingAction(object):
    """
Describes how the action is applied on the FileSystemTreeNodes. This class
is inherited by all the specific actions.
    Parameters:
        --name: string that represents where the action will be applied.
    name can be 'folder', 'file', 'prefix', 'suffix' or 'extension'.
        --file_or_folder: specifies where to apply the actions : to the files or the folders.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, string_range=StringRange(0, None)):
        self._string_range = string_range

    @property
    def string_range(self):
        return self._string_range

    def _get_substring(self, original_string):
        return StringSlicer(original_string, self._string_range).sliced_portion

    @abc.abstractmethod
    def _get_modified_substring(self, original_string):
        """Gets the modified portion of the file/folder name.
        The portion is defined by the string_range."""
        raise Exception()

    def execute(self, original_string):
        string_slicer = StringSlicer(original_string, self._string_range)
        new_name = string_slicer.first_portion + self._get_modified_substring(original_string) + string_slicer.last_portion
        return new_name


class FileInfoRenamingAction(RenamingAction):

    def __init__(self, string_range):
        super(string_range)


class FindAndReplaceAction(RenamingAction):
    """
    Replace old_char by new_char in the section of the path.
    string_range can be 'folder', 'file', 'prefix', 'suffix' or 'extension'.
    """
    def __init__(self, old_char, new_char, is_regex, string_range=None):
        super().__init__(string_range)
        self._old_char = old_char
        self._new_char = new_char
        self._is_regex = is_regex

    def _get_modified_substring(self, original_string):
        original_substring = self._get_substring(original_string)
        if not self._is_regex:
            return original_substring.replace(self._old_char, self._new_char)
        else:
            return re.sub(self._old_char, self._new_char, original_substring)


class OriginalNameAction(RenamingAction):
    """Gets the original name."""

    def __init__(self, string_range=None):
        super().__init__(string_range)

    def _get_modified_substring(self, original_string):
        return super()._get_substring(original_string)


class TitleCaseAction(RenamingAction):
    """
    Return the original name with a chosen casing option.
    Parameters:
        --case_choise: option to specify the case : 'uppercase', 'lowercase', 'titlecase'.
        --is_first_letter_uppercase: boolean making first letter uppercase or lowercase.
        --special_characters: list of symbols after which the letters are capitalized.
    """

    def __init__(self, is_first_letter_uppercase=True, special_characters="", string_range=None):
        super().__init__(string_range)
        self._is_first_letter_uppercase = is_first_letter_uppercase
        self._special_characters = special_characters

    def _get_decomposed_name(self, original_string):
        original_substring = self._get_substring(original_string)
        decomposed_name = list(original_substring)
        return decomposed_name

    def _get_special_character_indices(self, original_string):
        decomposed_name = self._get_decomposed_name(original_string)
        special_character_indices = []
        for index, character in enumerate(decomposed_name):
            if character in self._special_characters:
                special_character_indices.append(index)
        return special_character_indices

    def _get_modified_substring(self, original_string):
        print("AAAA" +original_string)
        decomposed_name = self._get_decomposed_name(original_string)
        for special_character_index in self._get_special_character_indices(original_string):
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

    def __init__(self, string_range=None):
        super().__init__(string_range)

    def _get_modified_substring(self, original_string):
        return self._get_substring(original_string).upper()


class LowerCaseAction(RenamingAction):
    """
    Return the original name with a chosen casing option.
    Parameters:
        --case_choise: option to specify the case : 'uppercase', 'lowercase', 'titlecase'.
        --is_first_letter_uppercase: boolean making first letter uppercase or lowercase.
        --special_characters: list of symbols after which the letters are capitalized.
    """

    def __init__(self, string_range=None):
        super().__init__(string_range)

    def _get_modified_substring(self, original_string):
        return self._get_substring(original_string).lower()


class CustomNameAction(RenamingAction):
    """Use a custom name in the filename.
    Can be also used to remove character if en empty string is given.
    """

    def __init__(self, custom_name, string_range=None):
        print(custom_name)
        super().__init__(string_range)
        self._custom_name = custom_name

    def _get_modified_substring(self, original_string):
        print(self._custom_name)
        return self._custom_name


class FolderNameAction(RenamingAction):
    """Use the parent foldername as the filename."""

    def __init__(self, file_system_tree_node, string_range=None):
        super().__init__(string_range)
        self._file_system_tree_node = file_system_tree_node

    def _get_modified_substring(self, original_string):
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

    def __init__(self, file_system_tree_node, is_modified_date=True, time_format='%Y', string_range=None):
        self._file_system_tree_node = file_system_tree_node
        self._is_modified_date = is_modified_date
        self._display_format = time_format

    def _get_modified_substring(self, original_string):
        if self.is_modified_date:
            file_date = self._file_system_tree_node.modified_date
        else:
            # created date
            file_date = self._file_system_tree_node.created_date
        return time.strftime(self.format_display, time.localtime(file_date))


# class Counter(RenamingAction):
#     """Count the number of files starting from start_index with the given increment."""

#     def __init__(self, string, string_range, start_index, increment, digit_number):
#         super().__init__(string, string_range)
#         self._start_index = start_index
#         self._increment = increment
#         self._digit_number = digit_number

#     def _get_modified_substring(self, original_string):
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
    def __init__(self, file_systme_tree_node, metadata, string_range=None):
        super().__init__(string_range)
        self._file_system_tree_node = file_systme_tree_node
        self._metadata = metadata

    def _get_exif_tag(self):
        file_path = self._file_system_tree_node.original_path
        with open(file_path, 'rb') as f:
            tags = process_file(f, details=False, stop_tag=self.metadata)
            exif_tag = tags[self.metadata].values
            return exif_tag


class ImageDateTimeOriginal(GenericImageAction):
    def __init__(self, file_system_tree_node, time_format, string_range=None):
        super().__init__(string_range, file_system_tree_node, 'EXIF DateTimeOriginal')
        self._time_format = time_format

    def _get_modified_substring(self, original_string):
        try:
            exif_tag = self._get_exif_tag()
            localtime = time.strptime(exif_tag, "%Y:%m:%d %H:%M:%S")
            return time.strftime(self._time_format, localtime)
        except:
            return self._get_substring(original_string)


class ImageFNumber(GenericImageAction):
    def __init__(self, file_system_tree_node, string_range=None):
        super().__init__(string_range, file_system_tree_node, 'EXIF FNumber')

    def _get_modified_substring(self, original_string):
        try:
            exif_tag = self._get_exif_tag()
            return str(exif_tag[0].num / exif_tag[0].den)
        except:
            return self._get_substring(original_string)


class ImageExposureTime(GenericImageAction):
    def __init__(self, file_system_tree_node, string_range=None):
        super().__init__(string_range, file_system_tree_node, 'EXIF ExposureTime')

    def _get_modified_substring(self, original_string):
        try:
            exif_tag = self._get_exif_tag()
            return str(exif_tag[0].num / exif_tag[0].den)
        except:
            return self._get_substring(original_string)


class ImageISO(GenericImageAction):
    def __init__(self, file_system_tree_node, string_range=None):
        super().__init__(string_range, file_system_tree_node, 'EXIF ISOSpeedRatings')

    def _get_modified_substring(self, original_string):
        try:
            exif_tag = self._get_exif_tag()
            return str(exif_tag[0])
        except:
            return self._get_substring(original_string)


class ImageCameraModel(GenericImageAction):
    def __init__(self, file_system_tree_node, string_range=None):
        super().__init__(string_range, file_system_tree_node, 'Image Model')

    def _get_modified_substring(self, original_string):
        try:
            exif_tag = self._get_exif_tag()
            return exif_tag
        except:
            return self._get_substring(original_string)


class ImageXDimension(GenericImageAction):
    def __init__(self, file_system_tree_node, string_range=None):
        super().__init__(string_range, file_system_tree_node, 'EXIF ExifImageWidth')

    def _get_modified_substring(self, original_string):
        try:
            exif_tag = self._get_exif_tag()
            return str(exif_tag[0])
        except:
            return self._get_substring(original_string)


class ImageYDimension(GenericImageAction):
    def __init__(self, file_system_tree_node, string_range=None):
        super().__init__(string_range, file_system_tree_node, 'EXIF ExifImageLength')

    def _get_modified_substring(self, original_string):
        try:
            exif_tag = self._get_exif_tag()
            return str(exif_tag[0])
        except:
            return self._get_substring(original_string)


class ImageFocalLength(GenericImageAction):
    def __init__(self, file_system_tree_node, string_range=None):
        super().__init__(string_range, file_system_tree_node, 'EXIF FocalLength')

    def _get_modified_substring(self, original_string):
        try:
            exif_tag = self._get_exif_tag()
            return str(exif_tag[0].num / exif_tag[0].den)
        except:
            return self._get_substring(original_string)


class ImageArtist(GenericImageAction):
    def __init__(self, file_system_tree_node, string_range=None):
        super().__init__(string_range, file_system_tree_node, 'Image Artist')

    def _get_modified_substring(self, original_string):
        try:
            exif_tag = self._get_exif_tag()
            return exif_tag
        except:
            return self._get_substring(original_string)


class GenericMusicAction(RenamingAction):
    def __init__(self, file_system_tree_node, metadata, string_range=None):
        super().__init__(string_range, file_system_tree_node)
        self.metadata = metadata

    def _get_metadata_tag(self):
        file_path = self._file_system_tree_node.original_path
        audio = EasyID3(file_path)
        return ', '.join(audio[self.metadata])


class MusicArtist(GenericMusicAction):
    def __init__(self, file_system_tree_node, string_range=None):
        super().__init__(self, string_range, file_system_tree_node, 'artist')

    def _get_modified_substring(self, original_string):
        try:
            metadata_tag = self._get_metadata_tag()
            return metadata_tag
        except:
            return self._get_substring(original_string)


class MusicTitle(GenericMusicAction):
    def __init__(self, file_system_tree_node, string_range=None):
        super().__init__(string_range, file_system_tree_node, 'title')

    def _get_modified_substring(self, original_string):
        try:
            metadata_tag = self._get_metadata_tag()
            return metadata_tag
        except:
            return self._get_substring(original_string)


class MusicYear(GenericMusicAction):
    def __init__(self, file_system_tree_node, string_range=None):
        super().__init__(self, string_range, file_system_tree_node, 'date')

    def _get_modified_substring(self, original_string):
        try:
            metadata_tag = self._get_metadata_tag()
            return metadata_tag
        except:
            return self._get_substring(original_string)


class MusicAlbum(GenericMusicAction):
    def __init__(self, file_system_tree_node, string_range=None):
        super().__init__(string_range, file_system_tree_node, 'album')

    def _get_modified_substring(self, original_string):
        try:
            metadata_tag = self._get_metadata_tag()
            return metadata_tag
        except:
            return self._get_substring(original_string)


class MusicTrack(GenericMusicAction):
    def __init__(self, file_system_tree_node, string_range=None):
        super().__init__(string_range, file_system_tree_node, 'tracknumber')

    def _get_modified_substring(self, original_string):
        try:
            metadata_tag = self._get_metadata_tag()
            return metadata_tag
        except:
            return self._get_substring(original_string)


class MusicGenre(GenericMusicAction):
    def __init__(self, file_system_tree_node, string_range=None):
        super().__init__(string_range, file_system_tree_node, 'genre')

    def _get_modified_substring(self, original_string):
        try:
            metadata_tag = self._get_metadata_tag()
            return metadata_tag
        except:
            return self._get_substring(original_string)
