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


class ActionDescriptor(object):
    """
    Describes the actions by names, inputs and classes.
    Parameters:
        --action_name: string that represents the name of the action.
        --action_inputs: list of ActionInput that represents the inputs properties of the acion.
        --action_class: string that represents the name of the class used for the action.
    """

    def __init__(self, action_name, action_inputs, action_class):
        self.action_name = action_name
        self.action_inputs = action_inputs
        self.action_class = action_class

    def __repr__(self):
        """override string representation of the class"""
        return self.action_name


class ActionInput(object):
    """
    Describes the inputs properties of the action.
    Parameters:
        --arg_name: string that represents the name of the given parameter.
        --arg_caption: string that represents the caption of the given parameter.
        --arg_type: specifies which type is the given parameter.
        --default_value: specifies the default value of the given parameter.
        --optional_argument: gives the possibility to add an optional argument for storing data.
    """

    def __init__(self,
                 arg_name,
                 arg_caption,
                 arg_type,
                 default_value,
                 optional_argument=None):
        self._name = arg_name
        self._caption = arg_caption
        self._type = arg_type
        self.default_value = default_value
        self.optional_argument = optional_argument

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self, value):
        self._caption = value

    @property
    def input_type(self):
        return self._type

    @input_type.setter
    def input_type(self, value):
        self._type = value

    @property
    def default_value(self):
        return self._default_value

    @default_value.setter
    def default_value(self, value):
        self._default_value = value


class FindAndReplaceActionDescriptor(ActionDescriptor):
    """
    Replace old_char by new_char in the section of the path.
    action_range can be 'folder', 'file', 'prefix', 'suffix' or 'extension'.
    """

    def __init__(self):
        super().__init__(self, )
        self._old_char = old_char
        self._new_char = new_char
        self._is_regex = is_regex

    def _get_modified_sliced_name(self, file_system_tree_node, action_range=ActionRange()):
        unmodified_sliced_name = self._get_unmodified_sliced_name(file_system_tree_node, action_range)
        if not self._is_regex:
            return unmodified_sliced_name.replace(self._old_char, self._new_char)
        else:
            return re.sub(self._old_char, self._new_char, unmodified_sliced_name)

# class CharacterInsertionAction(RenamingAction):
#     """Insert new_char at index position."""

#     def __init__(self, name, new_char, index):
#         RenamingAction.__init__(self, name)
#         self.new_char = new_char
#         self.index = index

#     def _get_modified_sliced_name(self, file_system_tree_node, action_range):
#         return action_range[:self.index] + self.new_char + action_range[self.index:]


# class CharacterDeletionAction(RenamingAction):
#     """Delete n-character from starting_position to ending_position."""

#     def __init__(self, name, starting_position, ending_position):
#         RenamingAction.__init__(self, name)
#         self.starting_position = starting_position
#         self.ending_position = ending_position

#     def _get_modified_sliced_name(self, file_system_tree_node, action_range):
#         if self.starting_position > self.ending_position:
#             raise Exception("Starting position cannot be higher than ending position.")
#         return action_range[:self.starting_position] + action_range[self.ending_position:]


# class OriginalNameAction(RenamingAction):
#     """Gets the original name."""

#     def __init__(self, file_system_tree_node, action_range):
#         RenamingAction.__init__(self, file_system_tree_node, action_range)

#     def _get_modified_sliced_name(self, file_system_tree_node, action_range):
#         return RenamingAction.file_system_tree_node.modified_name


class CaseChangeAction(RenamingAction):
    """
    Return the original name with a chosen casing option.
    Parameters:
        --case_choise: option to specify the case : 'uppercase', 'lowercase', 'titlecase'.
        --is_first_letter_uppercase: boolean making first letter uppercase or lowercase.
        --special_characters: list of symbols after which the letters are capitalized.
    """

    def __init__(self, file_system_tree_node, action_range):
        RenamingAction.__init__(self, file_system_tree_node, action_range)

    def _get_modified_sliced_name(self, file_system_tree_node, action_range):
        return


class TitleCaseAction(RenamingAction):
    """
    Return the original name with a chosen casing option.
    Parameters:
        --case_choise: option to specify the case : 'uppercase', 'lowercase', 'titlecase'.
        --is_first_letter_uppercase: boolean making first letter uppercase or lowercase.
        --special_characters: list of symbols after which the letters are capitalized.
    """

    def __init__(self, file_system_tree_node, action_range, is_first_letter_uppercase=True, special_characters=""):
        RenamingAction.__init__(self, file_system_tree_node, action_range)
        self._is_first_letter_uppercase = is_first_letter_uppercase
        self._special_characters = special_characters

    def _get_decomposed_name(self):
        unmodified_sliced_name = self._get_unmodified_sliced_name()
        decomposed_name = list(unmodified_sliced_name)
        return decomposed_name

    def _get_special_character_indices(self):
        decomposed_name = self._get_decomposed_name
        special_character_indices = []
        for index, character in enumerate(decomposed_name):
            if character in self._special_characters:
                special_character_indices.append(index)
        return special_character_indices

    def _get_modified_sliced_name(self):
        decomposed_name = self._get_decomposed_name
        for special_character_index in self._get_special_character_indices:
            if special_character_index < len(decomposed_name):
                decomposed_name[special_character_index + 1] = decomposed_name[special_character_index + 1].upper()
        if self._is_first_letter_uppercase:
            decomposed_name[0] = decomposed_name[0].upper()
        modified_sliced_name = ''.join(decomposed_name)
        return modified_sliced_name


class UpperCaseAction(CaseChangeAction):
    """
    Return the original name with a chosen casing option.
    Parameters:
        --case_choise: option to specify the case : 'uppercase', 'lowercase', 'titlecase'.
        --is_first_letter_uppercase: boolean making first letter uppercase or lowercase.
        --special_characters: list of symbols after which the letters are capitalized.
    """

    def __init__(self, file_system_tree_node, action_range):
        RenamingAction.__init__(self, file_system_tree_node, action_range)

    def _get_modified_sliced_name(self):
        unmodified_sliced_name = self._get_unmodified_sliced_name()
        modified_sliced_name = unmodified_sliced_name.upper()
        return modified_sliced_name


class LowerCaseAction(CaseChangeAction):
    """
    Return the original name with a chosen casing option.
    Parameters:
        --case_choise: option to specify the case : 'uppercase', 'lowercase', 'titlecase'.
        --is_first_letter_uppercase: boolean making first letter uppercase or lowercase.
        --special_characters: list of symbols after which the letters are capitalized.
    """

    def __init__(self, file_system_tree_node, action_range):
        RenamingAction.__init__(self, file_system_tree_node, action_range)

    def _get_modified_sliced_name(self):
        unmodified_sliced_name = self._get_unmodified_sliced_name()
        modified_sliced_name = unmodified_sliced_name.upper()
        return modified_sliced_name



class CustomNameAction(RenamingAction):
    """Use a custom name in the filename.
    Can be also used to remove character if en empty string is given.
    """

    def __init__(self, file_system_tree_node, action_range, custom_name):
        RenamingAction.__init__(self, file_system_tree_node, action_range)
        self._custom_name = custom_name

    def _get_modified_sliced_name(self):
        return self._custom_name


class FolderNameUsageAction(RenamingAction):
    """Use the parent foldername as the filename."""

    def __init__(self, file_system_tree_node, action_range):
        RenamingAction.__init__(self, file_system_tree_node, action_range)

    def _get_modified_sliced_name(self):
        folder_name = self.file_system_tree_node.parent.modified_name
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

    def __init__(self, file_system_tree_node, action_range, is_modified_date=True, time_format='%Y'):
        self._is_modified_date = is_modified_date
        self._display_format = time_format

    def _get_modified_sliced_name(self):
        if self.is_modified_date:
            file_date = self.file_system_tree_node.modified_date
        else:
            # created date
            file_date = self.file_system_tree_node.created_date
        return time.strftime(self.format_display, time.localtime(file_date))


class Counter(RenamingAction):
    """Count the number of files starting from start_index with the given increment."""

    def __init__(self, file_system_tree_node, action_range, start_index, increment, digit_number):
        RenamingAction.__init__(self, file_system_tree_node, action_range)
        self._start_index = start_index
        self._increment = increment
        self._digit_number = digit_number

    def _get_modified_sliced_name(self):
        counter = self.file_system_tree_node.rank
        counter *= self.increment
        counter += self.start_index
        counter = str(counter)
        number_length = len(str(counter))
        if (number_length < self.digit_number):
            for i in range(self.digit_number - number_length):
                counter = "0" + counter
        return counter


class GenericImageAction(RenamingAction):
    def __init__(self, file_system_tree_node, action_range, metadata):
        RenamingAction.__init__(self, file_system_tree_node, action_range)
        self._metadata = metadata

    def _get_exif_tag(self):
        file_path = self._file_system_tree_node.original_path
        with open(file_path, 'rb') as f:
            tags = process_file(f, details=False, stop_tag=self.metadata)
            exif_tag = tags[self.metadata].values
            return exif_tag


class ImageDateTimeOriginal(GenericImageAction):
    def __init__(self, file_system_tree_node, action_range, time_format):
        GenericImageAction.__init__(self, file_system_tree_node, action_range, 'EXIF DateTimeOriginal')
        self._time_format = time_format

    def _get_modified_sliced_name(self):
        try:
            exif_tag = self._get_exif_tag()
            localtime = time.strptime(exif_tag, "%Y:%m:%d %H:%M:%S")
            return time.strftime(self._time_format, localtime)
        except:
            return self._get_unmodified_sliced_name()


class ImageFNumber(GenericImageAction):
    def __init__(self, file_system_tree_node, action_range):
        GenericImageAction.__init__(self, file_system_tree_node, action_range, 'EXIF FNumber')

    def _get_modified_sliced_name(self):
        try:
            exif_tag = self._get_exif_tag()
            return str(exif_tag[0].num / exif_tag[0].den)
        except:
            return self._get_unmodified_sliced_name()


class ImageExposureTime(GenericImageAction):
    def __init__(self, file_system_tree_node, action_range):
        GenericImageAction.__init__(self, file_system_tree_node, action_range, 'EXIF ExposureTime')

    def _get_modified_sliced_name(self):
        try:
            exif_tag = self._get_exif_tag()
            return str(exif_tag[0].num / exif_tag[0].den)
        except:
            return self._get_unmodified_sliced_name()


class ImageISO(GenericImageAction):
    def __init__(self, file_system_tree_node, action_range):
        GenericImageAction.__init__(self, file_system_tree_node, action_range, 'EXIF ISOSpeedRatings')

    def _get_modified_sliced_name(self):
        try:
            exif_tag = self._get_exif_tag()
            return str(exif_tag[0])
        except:
            return self._get_unmodified_sliced_name()


class ImageCameraModel(GenericImageAction):
    def __init__(self, file_system_tree_node, action_range):
        GenericImageAction.__init__(self, file_system_tree_node, action_range, 'Image Model')

    def _get_modified_sliced_name(self):
        try:
            exif_tag = self._get_exif_tag()
            return exif_tag
        except:
            return self._get_unmodified_sliced_name()


class ImageXDimension(GenericImageAction):
    def __init__(self, file_system_tree_node, action_range):
        GenericImageAction.__init__(self, file_system_tree_node, action_range, 'EXIF ExifImageWidth')

    def _get_modified_sliced_name(self, file_system_tree_node, action_range):
        try:
            exif_tag = self._get_exif_tag()
            return str(exif_tag[0])
        except:
            return self._get_unmodified_sliced_name()


class ImageYDimension(GenericImageAction):
    def __init__(self, file_system_tree_node, action_range):
        GenericImageAction.__init__(self, file_system_tree_node, action_range, 'EXIF ExifImageLength')

    def _get_modified_sliced_name(self):
        try:
            exif_tag = self._get_exif_tag()
            return str(exif_tag[0])
        except:
            return self._get_unmodified_sliced_name()


class ImageFocalLength(GenericImageAction):
    def __init__(self, file_system_tree_node, action_range):
        GenericImageAction.__init__(self, file_system_tree_node, action_range, 'EXIF FocalLength')

    def _get_modified_sliced_name(self):
        try:
            exif_tag = self._get_exif_tag()
            return str(exif_tag[0].num / exif_tag[0].den)
        except:
            return self._get_unmodified_sliced_name()


class ImageArtist(GenericImageAction):
    def __init__(self, file_system_tree_node, action_range):
        GenericImageAction.__init__(self, file_system_tree_node, action_range, 'Image Artist')

    def _get_modified_sliced_name(self):
        try:
            exif_tag = self._get_exif_tag()
            return exif_tag
        except:
            return self._get_unmodified_sliced_name()


class GenericMusicAction(RenamingAction):
    def __init__(self, file_system_tree_node, action_range, metadata):
        RenamingAction.__init__(self, file_system_tree_node, action_range)
        self.metadata = metadata

    def _get_metadata_tag(self):
        file_path = self.file_system_tree_node.original_path
        audio = EasyID3(file_path)
        return ', '.join(audio[self.metadata])


class MusicArtist(GenericMusicAction):
    def __init__(self, file_system_tree_node, action_range):
        GenericImageAction.__init__(self, file_system_tree_node, action_range, 'artist')

    def _get_modified_sliced_name(self):
        try:
            metadata_tag = self._get_metadata_tag()
            return metadata_tag
        except:
            return self._get_unmodified_sliced_name()


class MusicTitle(GenericMusicAction):
    def __init__(self, file_system_tree_node, action_range):
        GenericImageAction.__init__(self, file_system_tree_node, action_range, 'title')

    def _get_modified_sliced_name(self):
        try:
            metadata_tag = self._get_metadata_tag()
            return metadata_tag
        except:
            return self._get_unmodified_sliced_name()


class MusicYear(GenericMusicAction):
    def __init__(self, file_system_tree_node, action_range):
        GenericImageAction.__init__(self, file_system_tree_node, action_range, 'date')

    def _get_modified_sliced_name(self):
        try:
            metadata_tag = self._get_metadata_tag()
            return metadata_tag
        except:
            return self._get_unmodified_sliced_name()


class MusicAlbum(GenericMusicAction):
    def __init__(self, file_system_tree_node, action_range):
        GenericImageAction.__init__(self, file_system_tree_node, action_range, 'album')

    def _get_modified_sliced_name(self):
        try:
            metadata_tag = self._get_metadata_tag()
            return metadata_tag
        except:
            return self._get_unmodified_sliced_name()


class MusicTrack(GenericMusicAction):
    def __init__(self, file_system_tree_node, action_range):
        GenericImageAction.__init__(self, file_system_tree_node, action_range, 'tracknumber')

    def _get_modified_sliced_name(self):
        try:
            metadata_tag = self._get_metadata_tag()
            return metadata_tag
        except:
            return self._get_unmodified_sliced_name()


class MusicGenre(GenericMusicAction):
    def __init__(self, file_system_tree_node, action_range):
        GenericImageAction.__init__(self, file_system_tree_node, action_range, 'genre')

    def _get_modified_sliced_name(self):
        try:
            metadata_tag = self._get_metadata_tag()
            return metadata_tag
        except:
            return self._get_unmodified_sliced_name()
