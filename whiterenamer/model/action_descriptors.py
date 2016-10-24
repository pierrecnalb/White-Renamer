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
                 default_value):
        self._name = arg_name
        self._caption = arg_caption
        self._type = arg_type
        self.default_value = default_value

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
        name = "Find And Replace"
        inputs = []
        old_char_input = ActionInput("old_char", "Replace", str, "")
        new_char_input = ActionInput("new_char", "With", str, "")
        is_regex_input = ActionInput("is_regex", "Regex", "checkable", False)
        inputs.append(old_char_input)
        inputs.append(new_char_input)
        inputs.append(is_regex_input)
        cls = FindAndReplaceAction
        super().__init__(self, name, inputs, cls)


class CharacterInsertionActionDescriptor(ActionDescriptor):
    """Insert new_char at index position."""

    def __init__(self):
        name = "Insert Characters"
        inputs = []
        new_char_input = ActionInput("custom_char", "Insert", str, "")
        index_input = ActionInput("start_and_end_range", "At", int, 0)
        inputs.append(new_char_input)
        inputs.append(index_input)
        cls = CustomNameAction
        super().__init__(self, name, inputs, cls)


class CharacterDeletionActionDescriptor(ActionDescriptor):
    """Delete n-character from starting_position to ending_position."""

    def __init__(self):
        name = "Delete Characters"
        inputs = []
        start_index_input = ActionInput("start_range", "From", int, 0)
        end_index_input = ActionInput("end_range", "To", int, 1)
        inputs.append(start_index_input)
        inputs.append(end_index_input)
        cls = CustomNameAction
        super().__init__(self, name, inputs, cls)



class OriginalNameActionDescriptor(ActionDescriptor):
    """Gets the original name."""

    def __init__(self):
        name = "Original Name"
        inputs = []
        cls = OriginalNameAction
        super().__init__(self, name, inputs, cls)



class TitleCaseActionDescriptor(ActionDescriptor):
    """
    Return the original name with a chosen casing option.
    Parameters:
        --case_choise: option to specify the case : 'uppercase', 'lowercase', 'titlecase'.
        --is_first_letter_uppercase: boolean making first letter uppercase or lowercase.
        --special_characters: list of symbols after which the letters are capitalized.
    """

    def __init__(self):
        name = "Titlecase"
        inputs = []
        is_first_letter_uppercase_input = ActionInput("is_first_letter_uppercase", "First Letter", "checkable", True)
        special_characters_input = ActionInput("special_characters", "And After", str, "- _")
        inputs.append(is_first_letter_uppercase_input)
        inputs.append(special_characters_input)
        cls = TitleCaseAction
        super().__init__(self, name, inputs, cls)


class UpperCaseActionDescriptor(ActionDescriptor):
    """
    Return the original name with a chosen casing option.
    Parameters:
        --case_choise: option to specify the case : 'uppercase', 'lowercase', 'titlecase'.
        --is_first_letter_uppercase: boolean making first letter uppercase or lowercase.
        --special_characters: list of symbols after which the letters are capitalized.
    """

    def __init__(self):
        name = "Uppercase"
        inputs = []
        cls = UpperCaseAction
        super().__init__(self, name, inputs, cls)



class LowerCaseActionDescriptor(ActionDescriptor):
    """
    Return the original name with a chosen casing option.
    Parameters:
        --case_choise: option to specify the case : 'uppercase', 'lowercase', 'titlecase'.
        --is_first_letter_uppercase: boolean making first letter uppercase or lowercase.
        --special_characters: list of symbols after which the letters are capitalized.
    """

    def __init__(self):
        name = "Lowercase"
        inputs = []
        cls = LowerCaseAction
        super().__init__(self, name, inputs, cls)


class CustomNameActionDescriptor(ActionDescriptor):
    """Use a custom name in the filename.
    Can be also used to remove character if en empty string is given.
    """

    def __init__(self):
        name = "Custom Name"
        inputs = []
        action_input = ActionInput("custom_name", "New Name", str, "")
        inputs.append(action_input)
        cls = CustomNameAction
        super().__init__(self, name, inputs, cls)


class FolderNameActionDescriptor(ActionDescriptor):
    """Use the parent foldername as the filename."""

    def __init__(self):
        name = "Folder Name"
        inputs = []
        cls = FolderNameAction
        super().__init__(self, name, inputs, cls)


class DateActionDescriptor(ActionDescriptor):

    def __init__(self):
        name = "Date"
        inputs = []
        is_modified_date_input = ActionInput("is_modified_date", "Modified", bool, True)
        is_created_date_input = ActionInput("is_modified_date", "Created", bool, False)
        time_format_input_ = ActionInput("time_format", "Format", str, "%Y-%m-%d %H:%M:%S (%A %B)")
        inputs.append(is_modified_date_input)
        inputs.append(is_created_date_input)
        inputs.append(time_format_input_)
        cls = DateAction
        super().__init__(self, name, inputs, cls)


class CounterActionDescriptor(ActionDescriptor):
    """Count the number of files starting from start_index with the given increment."""
    def __init__(self):
        name = "Counter"
        inputs = []
        start_index_input = ActionInput("start_index", "Start At", int, 0)
        increment_input = ActionInput("increment", "Increment", int, 1)
        digit_number_input = ActionInput("digit_number", "Number of Digit", int, 1)
        inputs.append(start_index_input)
        inputs.append(increment_input)
        inputs.append(digit_number_input)
        cls = CounterAction
        super().__init__(self, name, inputs, cls)



class ImageDateTimeOriginalDescriptor(ActionDescriptor):

    def __init__(self):
        name = "Original Date"
        inputs = []
        time_format_input = ActionInput("time_format", "Format", str, "%Y-%m-%d %H:%M:%S")
        inputs.append(time_format_input)
        cls = ImageDateTimeOriginal
        super().__init__(self, name, inputs, cls)


class ImageFNumberDescriptor(ActionDescriptor):
    def __init__(self):
        name = "F Number"
        inputs = []
        cls = ImageFNumber
        super().__init__(self, name, inputs, cls)


class ImageExposureTimeDescriptor(ActionDescriptor):
    def __init__(self):
        name = "Exposure"
        inputs = []
        cls = ImageExposureTime
        super().__init__(self, name, inputs, cls)


class ImageISODescriptor(ActionDescriptor):
    def __init__(self):
        name = "ISO"
        inputs = []
        cls = ImageISO
        super().__init__(self, name, inputs, cls)


class ImageCameraModelDescriptor(ActionDescriptor):
    def __init__(self):
        name = "Camera Model"
        inputs = []
        cls = ImageCameraModel
        super().__init__(self, name, inputs, cls)


class ImageXDimensionDescriptor(ActionDescriptor):
    def __init__(self):
        name = "X Dimension"
        inputs = []
        cls = ImageXDimension
        super().__init__(self, name, inputs, cls)


class ImageYDimensionDescriptor(ActionDescriptor):
    def __init__(self):
        name = "Y Dimension"
        inputs = []
        cls = ImageYDimension
        super().__init__(self, name, inputs, cls)


class ImageFocalLengthDescriptor(ActionDescriptor):
    def __init__(self):
        name = "Focal Length"
        inputs = []
        cls = ImageFocalLength
        super().__init__(self, name, inputs, cls)


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
