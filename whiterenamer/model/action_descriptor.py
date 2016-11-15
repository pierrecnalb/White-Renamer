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

from action_input import ActionInput
from renaming_actions import RenamingAction, CustomNameAction
from action_range import ActionRange


class ActionDescriptor(object):
    """
    Describes the actions by names, inputs and classes.
    Parameters:
        --action_name: string that represents the name of the action.
        --action_inputs: list of ActionInput that represents the inputs properties of the acion.
        --action_class: string that represents the name of the class used for the action.
    """

    def __init__(self, action_name, action_inputs, action_class):
        self._action_name = action_name
        self._action_inputs = action_inputs
        self._action_class = action_class
        self._caption_value_map = {action_input.name: action_input.value for action_input in self._action_inputs}
        self._action_range = ActionRange()
        self._modify_extension = False

    def __repr__(self):
        """override string representation of the class"""
        return self._action_name

    @property
    def action_range(self):
        return self._action_range

    @action_range.setter
    def action_range(self, value):
        self.action_range = value

    @property
    def modify_extension(self):
        return self._modify_extension

    @modify_extension.setter
    def modify_extension(self, value):
        self._modify_extension = value

    def invoke_action(self, tree_node_model):
        """Executes the action."""
        for tree_node in tree_node_model.root_node.children:
            action_instance = self._action_class(tree_node, self._action_range, **self._caption_value_map)
            action_instance.modify_extension = self._modify_extension
            action_instance.execute()


class OriginalNameActionDescriptor(ActionDescriptor):

    def __init__(self):
        name = "Original Name"
        inputs = []
        cls = RenamingAction.OriginalNameAction
        super().__init__(name, inputs, cls)


class FindAndReplaceActionDescriptor(ActionDescriptor):
    """
    Replace old_char by new_char in the section of the path.
    action_range can be 'folder', 'file', 'prefix', 'suffix' or 'extension'.
    """

    def __init__(self, old_char, new_char, is_regex):
        name = "Find And Replace"
        inputs = []
        old_char_input = ActionInput("old_char", "Replace", str, old_char)
        new_char_input = ActionInput("new_char", "With", str, new_char)
        is_regex_input = ActionInput("is_regex", "Regex", "checkable", is_regex)
        inputs.append(old_char_input)
        inputs.append(new_char_input)
        inputs.append(is_regex_input)
        cls = RenamingAction.FindAndReplaceAction
        super().__init__(name, inputs, cls)


class CharacterInsertionActionDescriptor(ActionDescriptor):
    """Insert new_char at index position."""

    def __init__(self):
        name = "Insert Characters"
        inputs = []
        new_char_input = ActionInput("custom_char", "Insert", str, "")
        inputs.append(new_char_input)
        cls = CustomNameAction
        super().__init__(name, inputs, cls)
        super().action_range.start = "index_input"


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
        super().__init__(name, inputs, cls)


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
        cls = RenamingAction.TitleCaseAction
        super().__init__(name, inputs, cls)


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
        cls = RenamingAction.UpperCaseAction
        super().__init__(name, inputs, cls)


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
        cls = RenamingAction.LowerCaseAction
        super().__init__(name, inputs, cls)


class CustomNameActionDescriptor(ActionDescriptor):
    """Use a custom name in the filename.
    Can be also used to remove character if en empty string is given.
    """

    def __init__(self, new_name):
        name = "Custom Name"
        inputs = []
        action_input = ActionInput("custom_name", "New Name", str, new_name)
        inputs.append(action_input)
        cls = CustomNameAction
        super().__init__(name, inputs, cls)


class FolderNameActionDescriptor(ActionDescriptor):
    """Use the parent foldername as the filename."""

    def __init__(self):
        name = "Folder Name"
        inputs = []
        cls = RenamingAction.FolderNameAction
        super().__init__(name, inputs, cls)


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
        cls = RenamingAction.DateAction
        super().__init__(name, inputs, cls)


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
        cls = RenamingAction.CounterAction
        super().__init__(name, inputs, cls)


class ImageDateTimeOriginalDescriptor(ActionDescriptor):

    def __init__(self):
        name = "Original Date"
        inputs = []
        time_format_input = ActionInput("time_format", "Format", str, "%Y-%m-%d %H:%M:%S")
        inputs.append(time_format_input)
        cls = RenamingAction.ImageDateTimeOriginal
        super().__init__(name, inputs, cls)


class ImageFNumberDescriptor(ActionDescriptor):
    def __init__(self):
        name = "F Number"
        inputs = []
        cls = RenamingAction.ImageFNumber
        super().__init__(name, inputs, cls)


class ImageExposureTimeDescriptor(ActionDescriptor):
    def __init__(self):
        name = "Exposure"
        inputs = []
        cls = RenamingAction.ImageExposureTime
        super().__init__(name, inputs, cls)


class ImageISODescriptor(ActionDescriptor):
    def __init__(self):
        name = "ISO"
        inputs = []
        cls = RenamingAction.ImageISO
        super().__init__(name, inputs, cls)


class ImageCameraModelDescriptor(ActionDescriptor):
    def __init__(self):
        name = "Camera Model"
        inputs = []
        cls = RenamingAction.ImageCameraModel
        super().__init__(name, inputs, cls)


class ImageXDimensionDescriptor(ActionDescriptor):
    def __init__(self):
        name = "X Dimension"
        inputs = []
        cls = RenamingAction.ImageXDimension
        super().__init__(name, inputs, cls)


class ImageYDimensionDescriptor(ActionDescriptor):
    def __init__(self):
        name = "Y Dimension"
        inputs = []
        cls = RenamingAction.ImageYDimension
        super().__init__(name, inputs, cls)


class ImageFocalLengthDescriptor(ActionDescriptor):
    def __init__(self):
        name = "Focal Length"
        inputs = []
        cls = RenamingAction.ImageFocalLength
        super().__init__(name, inputs, cls)


class ImageArtistDescriptor(ActionDescriptor):
    def __init__(self):
        name = "Artist"
        inputs = []
        cls = RenamingAction.ImageArtist
        super().__init__(name, inputs, cls)


class MusicArtistDescriptor(ActionDescriptor):
    def __init__(self):
        name = "Artist"
        inputs = []
        cls = RenamingAction.MusicArtist
        super().__init__(name, inputs, cls)


class MusicTitleDescriptor(ActionDescriptor):
    def __init__(self):
        name = "Title"
        inputs = []
        cls = RenamingAction.MusicTitle
        super().__init__(name, inputs, cls)


class MusicYearDescriptor(ActionDescriptor):
    def __init__(self):
        name = "Year"
        inputs = []
        cls = RenamingAction.MusicYear
        super().__init__(name, inputs, cls)


class MusicAlbumDescriptor(ActionDescriptor):
    def __init__(self):
        name = "Album"
        inputs = []
        cls = RenamingAction.MusicAlbum
        super().__init__(name, inputs, cls)


class MusicTrackDescriptor(ActionDescriptor):
    def __init__(self):
        name = "Track Number"
        inputs = []
        cls = RenamingAction.MusicTrack
        super().__init__(name, inputs, cls)


class MusicGenreDescriptor(ActionDescriptor):
    def __init__(self):
        name = "Genre"
        inputs = []
        cls = RenamingAction.MusicGenre
        super().__init__(name, inputs, cls)
