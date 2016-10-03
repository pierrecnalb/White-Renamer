#!/usr/bin/python3

# Copyright (C) 2015-2016 Pierre Blanc
#
# This file is part of WhiteRenamer.
#
# WhiteRenamer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WhiteRenamer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WhiteRenamer. If not, see <http://www.gnu.org/licenses/>.
from time import strftime, strptime, localtime
from re import sub
from exifread import process_file
from mutagen.easyid3 import EasyID3
import abs

class RenamingAction(object):
    """
    Describes how the action is applied on the FileSystemTreeNodes. This class
    is inherited by all the specific actions.
    Parameters:
        --name: string that represents where the action will be applied.
    name can be 'folder', 'file', 'prefix', 'suffix' or 'extension'.
        --file_or_folder: specifies where to apply the actions : to the files or the folders.
    """
    __metaclass__ = abs.ABCMeta

    def __init__(self):
        self._location = location.Over

    @abc.abstractmethod
    def _get_new_name(self, file_system_tree_node):
        return

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    def action_type(self):
        self._action_type

    def execute(self, file_system_tree_node, location):
        new_name = _get_new_name(file_system_tree_node)
        file_system_tree_node.modified_name = new_name

    def _get_old_name(self):
        return file_system_tree_node.original_name



class CharacterReplacementAction(RenamingAction):
    """
    Replace old_char by new_char in the section of the path.
    location can be 'folder', 'file', 'prefix', 'suffix' or 'extension'.
    """

    def __init__(self, old_char, new_char, regex):
        RenamingAction.__init__(self)
        self.old_char = old_char
        self.new_char = new_char
        self.regex = regex

    def _get_new_name(self, file_system_tree_node):
        if not self.regex:
            return file_system_tree_node.modified_name.replace(self.old_char, self.new_char)
        else:
            return re.sub(self.old_char, self.new_char, location)


class OriginalNameAction(RenamingAction):
    """Gets the original name."""

    def __init__(self):
        RenamingAction.__init__(self)

    def _get_new_name(self, file_system_tree_node, location):
        return RenamingAction._get_old_name()


class CaseChangeAction(RenamingAction):
    """
    Return the original name with a chosen casing option.
    Parameters:
        --case_choise: option to specify the case : 'uppercase', 'lowercase', 'titlecase'.
        --is_first_letter_uppercase: boolean making first letter uppercase or lowercase.
        --after_symbols: list of symbols after which the letters are capitalized.
    """

    def __init__(self):
        RenamingAction.__init__(self)

    def _get_new_name(self, file_system_tree_node, location):
        return 


class TitleCaseAction(CaseChangeAction):
    """
    Return the original name with a chosen casing option.
    Parameters:
        --case_choise: option to specify the case : 'uppercase', 'lowercase', 'titlecase'.
        --is_first_letter_uppercase: boolean making first letter uppercase or lowercase.
        --after_symbols: list of symbols after which the letters are capitalized.
    """

    def __init__(self, is_first_letter_uppercase=True, after_symbols=""):
        CaseChangeAction.__init__(self)
        self._is_first_letter_uppercase = is_first_letter_uppercase
        self._after_symbols = after_symbols

    def make_upper_first_letters(self, string):

    def _get_new_name(self, file_system_tree_node, location):
        special_char_position = []
        stringlist = list(RenamingAction.original_name)
        for i, char in enumerate(stringlist):
            if char in self.after_symbols:
                special_char_position.append(i + 1)
        for position in special_char_position:
            if position < len(stringlist):
                stringlist[position] = stringlist[position].upper()
        return ''.join(stringlist)
        preview_name = self.make_upper_first_letters(file_system_tree_node.modified_name)
        if self.is_first_letter_uppercase:
            location = location[0].upper() + location[1:]
        return location


class UpperCaseAction(CaseChangeAction):
    """
    Return the original name with a chosen casing option.
    Parameters:
        --case_choise: option to specify the case : 'uppercase', 'lowercase', 'titlecase'.
        --is_first_letter_uppercase: boolean making first letter uppercase or lowercase.
        --after_symbols: list of symbols after which the letters are capitalized.
    """

    def __init__(self, name):
        CaseChangeAction.__init__(self, name)

    def _get_new_name(self, file_system_tree_node, location):
        return location.upper()


class LowerCaseAction(CaseChangeAction):
    """
    Return the original name with a chosen casing option.
    Parameters:
        --case_choise: option to specify the case : 'uppercase', 'lowercase', 'titlecase'.
        --is_first_letter_uppercase: boolean making first letter uppercase or lowercase.
        --after_symbols: list of symbols after which the letters are capitalized.
    """

    def __init__(self, name):
        CaseChangeAction.__init__(self, name)

    def _get_new_name(self, file_system_tree_node, location):
        return location.lower()


class CharacterInsertionAction(RenamingAction):
    """Insert new_char at index position."""

    def __init__(self, name, new_char, index):
        RenamingAction.__init__(self, name)
        self.new_char = new_char
        self.index = index

    def _get_new_name(self, file_system_tree_node, location):
        return location[:self.index] + self.new_char + location[self.index:]


class CharacterDeletionAction(RenamingAction):
    """Delete n-character from starting_position to ending_position."""

    def __init__(self, name, starting_position, ending_position):
        RenamingAction.__init__(self, name)
        self.starting_position = starting_position
        self.ending_position = ending_position

    def _get_new_name(self, file_system_tree_node, location):
        if self.starting_position > self.ending_position:
            raise Exception(
                "Starting position cannot be higher than ending position.")
        return location[:self.starting_position] + location[
            self.ending_position:]


class CustomNameAction(RenamingAction):
    """Use a custom name in the filename."""

    def __init__(self, name, new_name):
        RenamingAction.__init__(self, name)
        self.new_name = new_name

    def _get_new_name(self, file_system_tree_node, location):
        return self.new_name


class FolderNameUsageAction(RenamingAction):
    """Use the parent foldername as the filename."""

    def __init__(self, name):
        RenamingAction.__init__(self, name)

    def _get_new_name(self, file_system_tree_node, location):
        folder = file_system_tree_node.get_parent(
        ).original_filedescriptor.basename
        return folder


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

    def __init__(self,
                 name,
                 is_modified_date=False,
                 is_created_date=True,
                 format_display='%Y'):
        RenamingAction.__init__(self, name)
        self.is_modified_date = is_modified_date
        self.is_created_date = is_created_date
        self.format_display = format_display

    def _get_new_name(self, file_system_tree_node, location):
        if self.is_modified_date:
            file_date = file_system_tree_node.modified_date
        elif self.is_created_date:
            file_date = file_system_tree_node.created_date
        return strftime(self.format_display, localtime(file_date))


class Counter(RenamingAction):
    """Count the number of files starting from start_index with the given increment."""

    def __init__(self, name, start_index, increment, digit_number):
        RenamingAction.__init__(self, name)
        self.start_index = start_index
        self.increment = increment
        self.digit_number = digit_number

    def _get_new_name(self, file_system_tree_node, location):
        counter = file_system_tree_node.rank
        counter *= self.increment
        counter += self.start_index
        counter = str(counter)
        number_length = len(str(counter))
        if (number_length < self.digit_number):
            for i in range(self.digit_number - number_length):
                counter = "0" + counter
        return counter


class GenericImageAction(RenamingAction):
    def __init__(self, name, metadata):
        RenamingAction.__init__(self, name)
        self.metadata = metadata

    def get_exif_tag(self, file):
        with open(file, 'rb') as f:
            tags = process_file(f, details=False, stop_tag=self.metadata)
            exif_tag = tags[self.metadata].values
            return exif_tag


class ImageDateTimeOriginal(GenericImageAction):
    def __init__(self, name, time_format):  #, time_format):
        #     self.time_format = time_format
        GenericImageAction.__init__(self, name, 'EXIF DateTimeOriginal')
        self.time_format = time_format

    def _get_new_name(self, file_system_tree_node, location):
        try:
            exif_tag = self.get_exif_tag(
                file_system_tree_node.get_original_path())
            localtime = strptime(exif_tag, "%Y:%m:%d %H:%M:%S")
            return strftime(self.time_format, localtime)
        except:
            return location


class ImageFNumber(GenericImageAction):
    def __init__(self, name):
        GenericImageAction.__init__(self, name, 'EXIF FNumber')

    def _get_new_name(self, file_system_tree_node, location):
        try:
            exif_tag = self.get_exif_tag(
                file_system_tree_node.get_original_path())
            return str(exif_tag[0].num / exif_tag[0].den)
        except:
            return location


class ImageExposureTime(GenericImageAction):
    def __init__(self, name):
        GenericImageAction.__init__(self, name, 'EXIF ExposureTime')

    def _get_new_name(self, file_system_tree_node, location):
        try:
            exif_tag = self.get_exif_tag(
                file_system_tree_node.get_original_path())
            return str(exif_tag[0].num / exif_tag[0].den)
        except:
            return location


class ImageISO(GenericImageAction):
    def __init__(self, name):
        GenericImageAction.__init__(self, name, 'EXIF ISOSpeedRatings')

    def _get_new_name(self, file_system_tree_node, location):
        try:
            exif_tag = self.get_exif_tag(
                file_system_tree_node.get_original_path())
            return str(exif_tag[0])
        except:
            return location


class ImageCameraModel(GenericImageAction):
    def __init__(self, name):
        GenericImageAction.__init__(self, name, 'Image Model')

    def _get_new_name(self, file_system_tree_node, location):
        try:
            exif_tag = self.get_exif_tag(
                file_system_tree_node.get_original_path())
            return exif_tag
        except:
            return location


class ImageXDimension(GenericImageAction):
    def __init__(self, name):
        GenericImageAction.__init__(self, name, 'EXIF ExifImageWidth')

    def _get_new_name(self, file_system_tree_node, location):
        try:
            exif_tag = self.get_exif_tag(
                file_system_tree_node.get_original_path())
            return str(exif_tag[0])
        except:
            return location


class ImageYDimension(GenericImageAction):
    def __init__(self, name):
        GenericImageAction.__init__(self, name, 'EXIF ExifImageLength')

    def _get_new_name(self, file_system_tree_node, location):
        try:
            exif_tag = self.get_exif_tag(
                file_system_tree_node.get_original_path())
            return str(exif_tag[0])
        except:
            return location


class ImageFocalLength(GenericImageAction):
    def __init__(self, name):
        GenericImageAction.__init__(self, name, 'EXIF FocalLength')

    def _get_new_name(self, file_system_tree_node, location):
        try:
            exif_tag = self.get_exif_tag(
                file_system_tree_node.get_original_path())
            return str(exif_tag[0].num / exif_tag[0].den)
        except:
            return location


class ImageArtist(GenericImageAction):
    def __init__(self, name):
        GenericImageAction.__init__(self, name, 'Image Artist')

    def _get_new_name(self, file_system_tree_node, location):
        try:
            exif_tag = self.get_exif_tag(
                file_system_tree_node.get_original_path())
            return exif_tag
        except:
            return location


class GenericMusicAction(RenamingAction):
    def __init__(self, name, metadata):
        RenamingAction.__init__(self, name)
        self.metadata = metadata

    def get_metadata_tag(self, file):
        audio = EasyID3(file)
        return ', '.join(audio[self.metadata])


class MusicArtist(GenericMusicAction):
    def __init__(self, name):
        GenericImageAction.__init__(self, name, 'artist')

    def _get_new_name(self, file_system_tree_node, location):
        try:
            metadata_tag = self.get_metadata_tag(
                file_system_tree_node.get_original_path())
            return metadata_tag
        except:
            return location


class MusicTitle(GenericMusicAction):
    def __init__(self, name):
        GenericImageAction.__init__(self, name, 'title')

    def _get_new_name(self, file_system_tree_node, location):
        try:
            metadata_tag = self.get_metadata_tag(
                file_system_tree_node.get_original_path())
            return metadata_tag
        except:
            return location


class MusicYear(GenericMusicAction):
    def __init__(self, name):
        GenericImageAction.__init__(self, name, 'date')

    def _get_new_name(self, file_system_tree_node, location):
        try:
            metadata_tag = self.get_metadata_tag(
                file_system_tree_node.get_original_path())
            return metadata_tag
        except:
            return location


class MusicAlbum(GenericMusicAction):
    def __init__(self, name):
        GenericImageAction.__init__(self, name, 'album')

    def _get_new_name(self, file_system_tree_node, location):
        try:
            metadata_tag = self.get_metadata_tag(
                file_system_tree_node.get_original_path())
            return metadata_tag
        except:
            return location


class MusicTrack(GenericMusicAction):
    def __init__(self, name):
        GenericImageAction.__init__(self, name, 'tracknumber')

    def _get_new_name(self, file_system_tree_node, location):
        try:
            metadata_tag = self.get_metadata_tag(
                file_system_tree_node.get_original_path())
            return metadata_tag
        except:
            return location


class MusicGenre(GenericMusicAction):
    def __init__(self, name):
        GenericImageAction.__init__(self, name, 'genre')

    def _get_new_name(self, file_system_tree_node, location):
        try:
            metadata_tag = self.get_metadata_tag(
                file_system_tree_node.get_original_path())
            return metadata_tag
        except:
            return location
