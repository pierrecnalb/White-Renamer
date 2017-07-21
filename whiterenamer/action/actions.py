#!/usr/bin/python3

import time
import re
import abc
from exifread import process_file
from mutagen.easyid3 import EasyID3
from .scope import Targets, StringRange, Tokenizer
from ..filesystem import File, Folder


class Action(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, target=Targets.filename, string_range=StringRange(0, None)):
        """ An abstract action that modifies the name of a given filesystem node

        Args:
           target (Targets): Specifies what target must be modified.
           string_range (StringRange):
            A portion of the target name upon which the action is applied.
        """
        self._target = target
        self._string_range = string_range

    @property
    def range(self):
        """Gets the portion of the target name upon which the action is applied."""
        return self._string_range

    @range.setter
    def range(self, value):
        """Sets the portion of the target name upon which the action is applied."""
        self._range = value

    @property
    def target(self):
        """ Gets the target (file, folder, extension) for which this action must be applied."""
        return self._target

    @target.setter
    def target(self, value):
        """ Sets the target (file, folder, extension) for which this action must be applied."""
        self._target = value

    @abc.abstractmethod
    def _get_modified_substring(self, filesystem_node, original_substring):
        """Gets the modified portion of the file/folder name.
        (The portion is defined by the string_range.)
        This method must be overriden by all subclasses.
        The new name for the given range must be returned by this method.
        Thus, any new action must inherit from the Action class and implement the logic
        of the action in this overriden method.
        """

    def _is_target_valid(self, filesystem_node):
        """
        Specifies whether the given target
        works with the current filesystem node.
        """
        is_file = isinstance(filesystem_node, File)
        if (is_file):
            return (self._target is Targets.filename or self._target is Targets.extension)
        else:
            return (self._target is Targets.foldername)

    def _get_original_name(self, filesystem_node):
        original_name = ""
        if (self._target is Targets.filename or self._target is Targets.foldername):
            original_name = filesystem_node.original_path.basename
        elif (self._target is Targets.extension):
            original_name = filesystem_node.original_path.extension
        return original_name

    def execute(self, filesystem_node):
        """Executes the action on the given filesystem node.
        This modifies the name of the FileSystemNode object.

        Args:
            filesystem_node (FileSystemNode): The node upon which the name will change.
        """

        if (not self._is_target_valid(filesystem_node)):
            # Invalid target: it cannot be applied to the given filesystem node.
            print("is not target valid")
            return
        original_name = self._get_original_name(filesystem_node)
        tokenizer = Tokenizer(original_name, self._string_range)
        original_substring = tokenizer.selected_token
        print("original_sub= "+original_substring)
        modified_substring = self._get_modified_substring(filesystem_node, original_substring)
        print("modified_sub= "+modified_substring)
        new_name = (tokenizer.first_token + modified_substring + tokenizer.last_token)
        print("new_name="+new_name)
        if (self._target is Targets.extension):
            filesystem_node.modified_path.extension += new_name
        else:
            filesystem_node.modified_path.basename += new_name


class OriginalNameAction(Action):
    def __init__(self, target, string_range=StringRange(0, None)):
        """Keeps the original name. This action does not do anything.

        Args:
           target (Targets): Specifies what filesystem entity must be modified.
        """
        super().__init__(target, string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        return original_substring


class FindAndReplaceAction(Action):
    def __init__(self,
                 old_value,
                 new_value,
                 is_regex=False,
                 target=Targets.filename,
                 string_range=StringRange(0, None)):
        """Finds a value and replaces it with the given value.

        Args:
            old_value (string): The string to change.
            new_value (string): The new string that will replace the old_value.
            is_regex (bool): Specifies whether the old_value uses a regex.
            target (Targets, optional): Specifies what filesystem entity must be
                modified.
            string_range (StringRange, optional): A portion of the name
                upon which the action is applied.
        """
        super().__init__(target, string_range)
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
                 target=Targets.filename,
                 string_range=StringRange(0, None)):
        """Return a titlecased version of the name, i.e. words start with uppercase characters, all remaining cased characters have lowercase.

        Args:
            is_first_letter_uppercase (bool):
                Specifies whether the first letter should be uppercase
                or lowercase.
            special_characters: list of symbols after which the letters are
                capitalized.
            target (Targets, optional): Specifies what filesystem entity must be
                modified.
            string_range (StringRange, optional): A portion of the name
                upon which the action is applied.
        """
        super().__init__(target, string_range)
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
                decomposed_name[special_character_index + 1] = decomposed_name[
                    special_character_index + 1].upper()
        if self._is_first_letter_uppercase:
            decomposed_name[0] = decomposed_name[0].upper()
            modified_sliced_name = ''.join(decomposed_name)
        return modified_sliced_name


class UpperCaseAction(Action):
    def __init__(self, target=Targets.filename, string_range=StringRange(0, None)):
        """Uppercases the original name.

        Args:
            target (Targets, optional): Specifies what filesystem entity must be
                modified.
            string_range (StringRange, optional): A portion of the name
                upon which the action is applied.
        """
        super().__init__(target, string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        return original_substring.upper()


class LowerCaseAction(Action):
    def __init__(self, target=Targets.filename, string_range=StringRange(0, None)):
        """Lowercases the original name.

        Args:
            target (Targets, optional): Specifies what filesystem entity must be
                modified.
            string_range (StringRange, optional): A portion of the name
                upon which the action is applied.
        """
        super().__init__(target, string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        return original_substring.lower()


class OverwriteAction(Action):
    def __init__(self, custom_name, target=Targets.filename, string_range=StringRange(0, None)):
        """Replace the given portion of the filesystem node with a custom name.

        Args:
            custom_name (string): The new name to be given.
            target (Targets, optional): Specifies what filesystem entity must be
                modified.
            string_range (StringRange, optional): A portion of the name
                upon which the action is applied.
        """
        super().__init__(target, string_range)
        self._custom_name = custom_name

    def _get_modified_substring(self, filesystem_node, original_substring):
        return self._custom_name


class DeleteAction(Action):
    def __init__(self, string_range, target=Targets.filename):
        """Deletes n-character(s) specified by the given string range.

        Args:
            string_range (StringRange): A portion of the name
                upon which the action is applied.
            target (Targets, optional): Specifies what filesystem entity must be
                modified.
        """
        super().__init__("", target, string_range)


class FolderNameAction(Action):
    def __init__(self, target=Targets.filename, string_range=StringRange(0, None)):
        """Uses the parent foldername as the new name.

        Args:
            target (Targets, optional): Specifies what filesystem entity must be
                modified.
            string_range (StringRange): A portion of the name
                upon which the action is applied.
        """
        super().__init__(target, string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        folder_name = self._file_system_tree_node.parent.basename
        return folder_name


class DateAction(Action):
    def __init__(self,
                 is_modified_date=True,
                 time_format='%Y',
                 target=Targets.filename,
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
            target (Targets, optional): Specifies what filesystem entity can be
                modified.
            string_range (StringRange, optional): A portion of the name
                upon which the action is applied.
        """
        super().__init__(target, string_range)
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
                 target=Targets.filename,
                 string_range=StringRange(0, None)):
        """A counter that is incremented for each files that uses it.

        Args:
            start_index (int): The index at which the counter starts.
            increment (int): Specifies the incrementation of the counter
                for each iteration.
            digit_number (int): The length of the zero-padded numbers.
            target (Targets, optional): Specifies what filesystem entity can be
                modified.
            string_range (StringRange, optional): A portion of the name
                upon which the action is applied.
        """
        super().__init__(target, string_range)
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
        super().__init__(Targets.filename, string_range)
        self._metadata = metadata
        self._target = Targets.filename

    def _get_exif_tag(self, filesystem_node):
        file_path = filesystem_node.original_path.absolute
        with open(file_path, 'rb') as f:
            tags = process_file(f, details=False, stop_tag=self.metadata)
            exif_tag = tags[self.metadata].values
            return exif_tag


class ImageDateAction(GenericImageAction):
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


class ImageFNumberAction(GenericImageAction):
    def __init__(self, string_range=StringRange(0, None)):
        """ Uses the image exif F number metadata.

        Args:
            string_range (StringRange, optional): A portion of the name
                upon which the action is applied.
        """
        super().__init__('EXIF FNumber', string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            exif_tag = self._get_exif_tag(filesystem_node)
            return str(exif_tag[0].num / exif_tag[0].den)
        except:
            return original_substring


class ImageExposureTime(GenericImageAction):
    def __init__(self, string_range=StringRange(0, None)):
        """ Uses the image exposure time metadata.

        Args:
            string_range (StringRange, optional): A portion of the name
                upon which the action is applied.
        """
        super().__init__('EXIF ExposureTime', string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            exif_tag = self._get_exif_tag(filesystem_node)
            return str(exif_tag[0].num / exif_tag[0].den)
        except:
            return original_substring


class ImageISO(GenericImageAction):
    def __init__(self, string_range=StringRange(0, None)):
        """ Uses the image ISO metadata.

        Args:
            string_range (StringRange, optional): A portion of the name
                upon which the action is applied.
        """
        super().__init__('EXIF ISOSpeedRatings', string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            exif_tag = self._get_exif_tag(filesystem_node)
            return str(exif_tag[0])
        except:
            return original_substring


class ImageCameraModel(GenericImageAction):
    def __init__(self, string_range=StringRange(0, None)):
        """ Uses the image camera model metadata.

        Args:
            string_range (StringRange, optional): A portion of the name
                upon which the action is applied.
        """

        super().__init__('Image Model', string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            exif_tag = self._get_exif_tag(filesystem_node)
            return exif_tag
        except:
            return original_substring


class ImageXDimension(GenericImageAction):
    def __init__(self, string_range=StringRange(0, None)):
        """ Uses the image width metadata.

        Args:
            string_range (StringRange, optional): A portion of the name
                upon which the action is applied.
        """

        super().__init__('EXIF ExifImageWidth', string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            exif_tag = self._get_exif_tag(filesystem_node)
            return str(exif_tag[0])
        except:
            return original_substring


class ImageYDimension(GenericImageAction):
    def __init__(self, string_range=StringRange(0, None)):
        """ Uses the image length metadata.

        Args:
            string_range (StringRange, optional): A portion of the name
                upon which the action is applied.
        """

        super().__init__('EXIF ExifImageLength', string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            exif_tag = self._get_exif_tag(filesystem_node)
            return str(exif_tag[0])
        except:
            return original_substring


class ImageFocalLength(GenericImageAction):
    def __init__(self, string_range=StringRange(0, None)):
        """ Uses the image focal length metadata.

        Args:
            string_range (StringRange, optional): A portion of the name
                upon which the action is applied.
        """

        super().__init__('EXIF FocalLength', string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            exif_tag = self._get_exif_tag(filesystem_node)
            return str(exif_tag[0].num / exif_tag[0].den)
        except:
            return original_substring


class ImageArtist(GenericImageAction):
    def __init__(self, string_range=StringRange(0, None)):
        """ Uses the image artist metadata.

        Args:
            string_range (StringRange, optional): A portion of the name
                upon which the action is applied.
        """

        super().__init__('Image Artist', string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            exif_tag = self._get_exif_tag(filesystem_node)
            return exif_tag
        except:
            return original_substring


class GenericMusicAction(Action):
    def __init__(self, metadata, string_range=StringRange(0, None)):
        """An abstract action using the music metadata as new name.

        Args:
            metadata (string): The metadata that must be extracted.
            string_range (StringRange, optional): A portion of the name
                upon which the action is applied.
        """
        super().__init__(Targets.filename, string_range)
        self.metadata = metadata
        self._target = Targets.filename

    def _get_metadata_tag(self, filesystem_node):
        file_path = filesystem_node.original_path.absolute
        audio = EasyID3(file_path)
        return ', '.join(audio[self.metadata])


class MusicArtist(GenericMusicAction):
    def __init__(self, string_range=StringRange(0, None)):
        """ Uses the music artist metadata.

        Args:
            string_range (StringRange, optional): A portion of the name
                upon which the action is applied.
        """

        super().__init__('artist', string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            metadata_tag = self._get_metadata_tag(filesystem_node)
            return metadata_tag
        except:
            return original_substring


class MusicTitle(GenericMusicAction):
    def __init__(self, string_range=StringRange(0, None)):
        """ Uses the music title metadata.

        Args:
            string_range (StringRange, optional): A portion of the name
                upon which the action is applied.
        """

        super().__init__('title', string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            metadata_tag = self._get_metadata_tag(filesystem_node)
            return metadata_tag
        except:
            return original_substring


class MusicYear(GenericMusicAction):
    def __init__(self, string_range=StringRange(0, None)):
        """ Uses the music year metadata.

        Args:
            string_range (StringRange, optional): A portion of the name
                upon which the action is applied.
        """

        super().__init__('date', string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            metadata_tag = self._get_metadata_tag(filesystem_node)
            return metadata_tag
        except:
            return original_substring


class MusicAlbum(GenericMusicAction):
    def __init__(self, string_range=StringRange(0, None)):
        """ Uses the music album metadata.

        Args:
            string_range (StringRange, optional): A portion of the name
                upon which the action is applied.
        """

        super().__init__('album', string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            metadata_tag = self._get_metadata_tag(filesystem_node)
            return metadata_tag
        except:
            return original_substring


class MusicTrack(GenericMusicAction):
    def __init__(self, string_range=StringRange(0, None)):
        """ Uses the music track metadata.

        Args:
            string_range (StringRange, optional): A portion of the name
                upon which the action is applied.
        """

        super().__init__('tracknumber', string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            metadata_tag = self._get_metadata_tag(filesystem_node)
            return metadata_tag
        except:
            return original_substring


class MusicGenre(GenericMusicAction):
    def __init__(self, string_range=StringRange(0, None)):
        """ Uses the music genre metadata.

        Args:
            string_range (StringRange, optional): A portion of the name
                upon which the action is applied.
        """

        super().__init__('genre', string_range)

    def _get_modified_substring(self, filesystem_node, original_substring):
        try:
            metadata_tag = self._get_metadata_tag(filesystem_node)
            return metadata_tag
        except:
            return original_substring
