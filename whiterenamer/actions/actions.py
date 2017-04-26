#!/usr/bin/python3

import time
import re
from exifread import process_file
from mutagen.easyid3 import EasyID3
import abc
from enum import Enum
from stringrange import StringRange, Tokenizer
from ..filesystem import File, Folder


class Scope(Enum):
    """Specifies the filesystem entity.
    """
    foldername = 1
    filename = 2
    extension = 4


class Action(object):
    """An action modifies the name of a given filesystem node.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, scope=Scope.filename,
                 string_range=StringRange(0, None)):
        """The abstract action.

        Args:
           scope (Scope): Specifies what filesystem entity must be modified.
           string_range (StringRange):
            A portion of the name upon which the action is applied.
        """
        self._scope = scope
        self._string_range = string_range

    @property
    def range(self):
        return self._string_range

    @range.setter
    def range(self, value):
        self._range = value

    @property
    def scope(self):
        return self._scope

    @scope.setter
    def scope(self, value):
        self._scope = value

    @abc.abstractmethod
    def _get_modified_substring(self, filesystem_node, original_substring):
        """Gets the modified portion of the file/folder name.
        The portion is defined by the string_range.
        """

    def _is_scope_valid(self, filesystem_node):
        """
        Specifies whether the given scope
        works with the current filesystem node.
        """
        if (isinstance(filesystem_node, File)):
            if (self._scope is Scope.filename or
                    self._scope is Scope.extension):
                return True
        if (self._scope is Scope.foldername and
                not isinstance(filesystem_node, Folder)):
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
        """Executes the actino on the given filesystem node.

        Args:
            filesystem_node (Node): The node upon which the name will change.
        """
        if (not self._is_scope_valid(filesystem_node)):
            raise Exception("Invalid scope: \
                it cannot be applied to the given filesystem node.")
        original_name = self._get_original_name(filesystem_node)
        tokenizer = Tokenizer(original_name, self._string_range)
        original_substring = tokenizer.selected_token
        modified_substring = self._get_modified_substring(filesystem_node,
                                                          original_substring)
        new_name = (
            tokenizer.first_token + modified_substring + tokenizer.last_token)
        if (self._scope is Scope.extension):
            filesystem_node.new_extension += new_name
        else:
            filesystem_node.new_name += new_name


class OriginalNameAction(Action):
    def __init__(self, scope):
        """Keeps the original name. This action does not do anything.

        Args:
           scope (Scope): Specifies what filesystem entity must be modified.
        """
        super().__init__(scope)

    def _get_modified_substring(self, filesystem_node, original_substring):
        return original_substring


class FindAndReplaceAction(Action):
    def __init__(self,
                 old_value,
                 new_value,
                 is_regex=False,
                 scope=Scope.filename,
                 string_range=StringRange(0, None)):
        """Finds a value and replaces it with the given value.

        Args:
            old_value (string): The string to change.
            new_value (string): The new string that will replace the old_value.
            is_regex (bool): Specifies whether the old_value uses a regex.
            scope (Scope, optional): Specifies what filesystem entity must be
                modified.
            string_range (StringRange, optional): A portion of the name
                upon which the action is applied.
        """
        super().__init__(scope, string_range)
        self._old_value = old_value
        self._new_value = new_value
        self._is_regex = is_regex

    def _get_modified_substring(self, filesystem_node, original_substring):
        if not self._is_regex:
            return original_substring.replace(self._old_value, self._new_value)
        else:
            return re.sub(self._old_value, self._new_value, original_substring)


class TitleCaseAction(Action):
    def __init__(self,
                 is_first_letter_uppercase=True,
                 special_characters="",
                 scope=Scope.filename,
                 string_range=StringRange(0, None)):
        """Titlecases the original name.

        Args:
            is_first_letter_uppercase (bool):
                Specifies whether the first letter should be uppercase
                or lowercase.
            special_characters: list of symbols after which the letters are
                capitalized.
            scope (Scope, optional): Specifies what filesystem entity must be
                modified.
            string_range (StringRange, optional): A portion of the name
                upon which the action is applied.
        """
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
        for special_character_index in self._get_special_character_indices(
                original_substring):
            if special_character_index < len(decomposed_name):
                decomposed_name[special_character_index + 1] = decomposed_name[
                    special_character_index + 1].upper()
        if self._is_first_letter_uppercase:
            decomposed_name[0] = decomposed_name[0].upper()
        modified_sliced_name = ''.join(decomposed_name)
        return modified_sliced_name


class UpperCaseAction(Action):
    def __init__(self, scope=Scope.filename,
                 string_range=StringRange(0, None)):
        """Uppercases the original name.

        Args:
            scope (Scope, optional): Specifies what filesystem entity must be
                modified.
            string_range (StringRange, optional): A portion of the name
                upon which the action is applied.
        """
        super().__init__(scope, string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        return original_substring.upper()


class LowerCaseAction(Action):
    def __init__(self, scope=Scope.filename,
                 string_range=StringRange(0, None)):
        """Lowercases the original name.

        Args:
            scope (Scope, optional): Specifies what filesystem entity must be
                modified.
            string_range (StringRange, optional): A portion of the name
                upon which the action is applied.
        """
        super().__init__(scope, string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        return original_substring.lower()


class CustomNameAction(Action):
    def __init__(self,
                 custom_name,
                 scope=Scope.filename,
                 string_range=StringRange(0, None)):
        """Replace the given portion of the filesystem node with a custom name.
        Can be also used to remove character if en empty string is given.

        Args:
            custom_name (string): The new name to be given.
            scope (Scope, optional): Specifies what filesystem entity must be
                modified.
            string_range (StringRange, optional): A portion of the name
                upon which the action is applied.
        """
        super().__init__(scope, string_range)
        self._custom_name = custom_name

    def _get_modified_substring(self, filesystem_node, original_substring):
        return self._custom_name


class CharacterInsertionAction(CustomNameAction):
    def __init__(self, value, index, scope=Scope.filename):
        """Inserts a string at the given index.

        Args:
            value (string): The string to insert.
            index (int): The position at which the value should be inserted.
            scope (Scope, optional): Specifies what filesystem entity must be
                modified.
            string_range (StringRange, optional): A portion of the name
                upon which the action is applied.
        """
        super().__init__(value, scope, StringRange(index, index))


class CharacterDeletionAction(CustomNameAction):
    def __init__(self, string_range, scope=Scope.filename):
        """Deletes n-character(s) specified by the given string range.

        Args:
            string_range (StringRange): A portion of the name
                upon which the action is applied.
            scope (Scope, optional): Specifies what filesystem entity must be
                modified.
        """
        super().__init__("", scope, string_range)


class FolderNameAction(Action):
    def __init__(self, scope=Scope.filename,
                 string_range=StringRange(0, None)):
        """Use the parent foldername as the new name.

        Args:
            scope (Scope, optional): Specifies what filesystem entity must be
                modified.
            string_range (StringRange): A portion of the name
                upon which the action is applied.
        """
        super().__init__(scope, string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        folder_name = self._file_system_tree_node.parent.modified_basename
        return folder_name


class DateAction(Action):
    def __init__(self,
                 is_modified_date=True,
                 time_format='%Y',
                 scope=Scope.filename,
                 string_range=StringRange(0, None)):
        """ Uses the created or modified date metadata as the new name.

        Args:
            is_modified_date (bool): Specifies whether the modified or
                the created date is used.
            time_format (string): The format to display the date.
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
            scope (Scope, optional): Specifies what filesystem entity can be
                modified.
            string_range (StringRange, optional): A portion of the name
                upon which the action is applied.
        """
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


class CounterAction(Action):
    def __init__(self,
                 start_index,
                 increment,
                 digit_number=1,
                 scope=Scope.filename,
                 string_range=StringRange(0, None)):
        """A counter that is incremented for each files that use it.

        Args:
            start_index (int): The index at which the counter starts.
            increment (int): Specifies the incrementation of the counter
                for each iteration.
            digit_number (int): The number of digit the counter has.
            scope (Scope, optional): Specifies what filesystem entity can be
                modified.
            string_range (StringRange, optional): A portion of the name
                upon which the action is applied.
        """
        super().__init__(scope, string_range)
        self._start_index = start_index
        self._increment = increment
        self._digit_number = digit_number
        self._counter = self._start_index

    def _get_modified_substring(self, filesystem_node, original_substring):
        self._counter += self.increment
        counter = str(self._counter)
        number_length = len(str(counter))
        if (number_length < self.digit_number):
            for i in range(self.digit_number - number_length):
                counter = "0" + counter
        return counter


class GenericImageAction(Action):
    def __init__(self, metadata, string_range=StringRange(0, None)):
        """An abstract action using the image metadata as new name.

        Args:
            metadata (string): The metadata that must be extracted.
            string_range (StringRange, optional): A portion of the name
                upon which the action is applied.
        """
        super().__init__(Scope.filename, string_range)
        self._metadata = metadata
        self._scope = Scope.filename

    def _get_exif_tag(self, filesystem_node):
        file_path = filesystem_node.original_path
        with open(file_path, 'rb') as f:
            tags = process_file(f, details=False, stop_tag=self.metadata)
            exif_tag = tags[self.metadata].values
            return exif_tag


class ImageDateTimeOriginal(GenericImageAction):
    def __init__(self, time_format, string_range=StringRange(0, None)):
        """Uses the image date metadata.

        Args:
            time_format (string): The format to display the date.
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
            string_range (StringRange, optional): A portion of the name
                upon which the action is applied.
        """
        super().__init__('EXIF DateTimeOriginal', string_range)
        self._time_format = time_format

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            exif_tag = self._get_exif_tag(filesystem_node)
            localtime = time.strptime(exif_tag, "%Y:%m:%d %H:%M:%S")
            return time.strftime(self._time_format, localtime)
        except:
            return original_substring


class ImageFNumber(GenericImageAction):
    def __init__(self, string_range=StringRange(0, None)):
        super().__init__('EXIF FNumber', string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            exif_tag = self._get_exif_tag(filesystem_node)
            return str(exif_tag[0].num / exif_tag[0].den)
        except:
            return original_substring


class ImageExposureTime(GenericImageAction):
    def __init__(self, string_range=StringRange(0, None)):
        super().__init__('EXIF ExposureTime', string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            exif_tag = self._get_exif_tag(filesystem_node)
            return str(exif_tag[0].num / exif_tag[0].den)
        except:
            return original_substring


class ImageISO(GenericImageAction):
    def __init__(self, string_range=StringRange(0, None)):
        super().__init__('EXIF ISOSpeedRatings', string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            exif_tag = self._get_exif_tag(filesystem_node)
            return str(exif_tag[0])
        except:
            return original_substring


class ImageCameraModel(GenericImageAction):
    def __init__(self, string_range=StringRange(0, None)):
        super().__init__('Image Model', string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            exif_tag = self._get_exif_tag(filesystem_node)
            return exif_tag
        except:
            return original_substring


class ImageXDimension(GenericImageAction):
    def __init__(self, string_range=StringRange(0, None)):
        super().__init__('EXIF ExifImageWidth', string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            exif_tag = self._get_exif_tag(filesystem_node)
            return str(exif_tag[0])
        except:
            return original_substring


class ImageYDimension(GenericImageAction):
    def __init__(self, string_range=StringRange(0, None)):
        super().__init__('EXIF ExifImageLength', string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            exif_tag = self._get_exif_tag(filesystem_node)
            return str(exif_tag[0])
        except:
            return original_substring


class ImageFocalLength(GenericImageAction):
    def __init__(self, string_range=StringRange(0, None)):
        super().__init__('EXIF FocalLength', string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            exif_tag = self._get_exif_tag(filesystem_node)
            return str(exif_tag[0].num / exif_tag[0].den)
        except:
            return original_substring


class ImageArtist(GenericImageAction):
    def __init__(self, string_range=StringRange(0, None)):
        super().__init__('Image Artist', string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            exif_tag = self._get_exif_tag(filesystem_node)
            return exif_tag
        except:
            return original_substring


class GenericMusicAction(Action):
    def __init__(self, metadata, string_range=StringRange(0, None)):
        super().__init__(Scope.filename, string_range)
        self.metadata = metadata
        self._scope = Scope.filename

    def _get_metadata_tag(self, filesystem_node):
        file_path = filesystem_node.original_path
        audio = EasyID3(file_path)
        return ', '.join(audio[self.metadata])


class MusicArtist(GenericMusicAction):
    def __init__(self, string_range=StringRange(0, None)):
        super().__init__('artist', string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            metadata_tag = self._get_metadata_tag(filesystem_node)
            return metadata_tag
        except:
            return original_substring


class MusicTitle(GenericMusicAction):
    def __init__(self, string_range=StringRange(0, None)):
        super().__init__('title', string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            metadata_tag = self._get_metadata_tag(filesystem_node)
            return metadata_tag
        except:
            return original_substring


class MusicYear(GenericMusicAction):
    def __init__(self, string_range=StringRange(0, None)):
        super().__init__('date', string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            metadata_tag = self._get_metadata_tag(filesystem_node)
            return metadata_tag
        except:
            return original_substring


class MusicAlbum(GenericMusicAction):
    def __init__(self, string_range=StringRange(0, None)):
        super().__init__('album', string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            metadata_tag = self._get_metadata_tag(filesystem_node)
            return metadata_tag
        except:
            return original_substring


class MusicTrack(GenericMusicAction):
    def __init__(self, string_range=StringRange(0, None)):
        super().__init__('tracknumber', string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            metadata_tag = self._get_metadata_tag(filesystem_node)
            return metadata_tag
        except:
            return original_substring


class MusicGenre(GenericMusicAction):
    def __init__(self, string_range=StringRange(0, None)):
        super().__init__('genre', string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            metadata_tag = self._get_metadata_tag(filesystem_node)
            return metadata_tag
        except:
            return original_substring
