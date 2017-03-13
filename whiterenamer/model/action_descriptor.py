#!/usr/bin/python3


from action_input import ActionInput
from string_range import StringRange
from renaming_actions import *


class ActionDescriptor(object):
    """
    Describes the actions by names, inputs and classes.
    Parameters:
        --name: string that represents the name of the action.
        --inputs: list of ActionInput that represents the inputs properties of the acion.
        --action_class: string that represents the name of the class used for the action.
    """

    def __init__(self, name, inputs, action_class, string_range=None):
        self._name = name
        self._inputs = inputs
        self._class = action_class
        self._input_value_by_name = {_input.name: _input.value for _input in self._inputs}
        if string_range is None:
            self._range = StringRange(0, None)
        else:
            self._range = string_range

    def __repr__(self, string_range=None):
        """override string representation of the class"""
        return self._name

    @property
    def action_range(self, string_range=None):
        return self._range

    @action_range.setter
    def action_range(self, value):
        self.action_range = value

    def create_action(self, string_range=None):
        return self._class(**self._input_value_by_name, string_range=self._range)


class OriginalName(ActionDescriptor):

    def __init__(self):
        name = "Original Name"
        inputs = []
        cls = OriginalNameAction
        super().__init__(name, inputs, cls)


class FindAndReplace(ActionDescriptor):
    """
    Replace old_char by new_char in the section of the path.
    action_range can be 'folder', 'file', 'prefix', 'suffix' or 'extension'.
    """

    def __init__(self, old_char, new_char, is_regex, string_range=None):
        name = "Find And Replace"
        inputs = []
        old_char_input = ActionInput("old_char", "Replace", str, old_char)
        new_char_input = ActionInput("new_char", "With", str, new_char)
        is_regex_input = ActionInput("is_regex", "Regex", "checkable", is_regex)
        inputs.append(old_char_input)
        inputs.append(new_char_input)
        inputs.append(is_regex_input)
        cls = FindAndReplaceAction
        super().__init__(name, inputs, cls, string_range)


class CharacterInsertion(ActionDescriptor):
    """Insert new_char at index position."""

    def __init__(self, index):
        name = "Insert Characters"
        inputs = []
        new_char_input = ActionInput("custom_char", "Insert", str, "")
        inputs.append(new_char_input)
        cls = CustomNameAction
        string_range = StringRange(index, index)
        super().__init__(name, inputs, cls, string_range)
        super().action_range = StringRange(index, index)


class CharacterDeletion(ActionDescriptor):
    """Delete n-character from starting_position to ending_position."""

    def __init__(self):
        name = "Delete Characters"
        inputs = []
        start_index_input = ActionInput("start_range", "From", int, 0)
        end_index_input = ActionInput("end_range", "To", int, 1)
        inputs.append(start_index_input)
        inputs.append(end_index_input)
        cls = CustomNameAction
        string_range = StringRange(index, index)
        super().__init__(name, inputs, cls, string_range)


class TitleCase(ActionDescriptor):
    """
    Return the original name with a chosen casing option.
    Parameters:
        --case_choise: option to specify the case : 'uppercase', 'lowercase', 'titlecase'.
        --is_first_letter_uppercase: boolean making first letter uppercase or lowercase.
        --special_characters: list of symbols after which the letters are capitalized.
    """

    def __init__(self, string_range=None):
        name = "Titlecase"
        inputs = []
        is_first_letter_uppercase_input = ActionInput("is_first_letter_uppercase", "First Letter", "checkable", True)
        special_characters_input = ActionInput("special_characters", "And After", str, "- _")
        inputs.append(is_first_letter_uppercase_input)
        inputs.append(special_characters_input)
        cls = TitleCaseAction
        super().__init__(name, inputs, cls, string_range)


class UpperCase(ActionDescriptor):
    """
    Return the original name with a chosen casing option.
    Parameters:
        --case_choise: option to specify the case : 'uppercase', 'lowercase', 'titlecase'.
        --is_first_letter_uppercase: boolean making first letter uppercase or lowercase.
        --special_characters: list of symbols after which the letters are capitalized.
    """

    def __init__(self, string_range=None):
        name = "Uppercase"
        inputs = []
        cls = UpperCaseAction
        super().__init__(name, inputs, cls, string_range)


class LowerCase(ActionDescriptor):
    """
    Return the original name with a chosen casing option.
    Parameters:
        --case_choise: option to specify the case : 'uppercase', 'lowercase', 'titlecase'.
        --is_first_letter_uppercase: boolean making first letter uppercase or lowercase.
        --special_characters: list of symbols after which the letters are capitalized.
    """

    def __init__(self, string_range=None):
        name = "Lowercase"
        inputs = []
        cls = LowerCaseAction
        super().__init__(name, inputs, cls, string_range=None)


class CustomName(ActionDescriptor):
    """Use a custom name in the filename.
    Can be also used to remove character if en empty string is given.
    """

    def __init__(self, new_name, string_range=None):
        name = "Custom Name"
        inputs = []
        _input = ActionInput("custom_name", "New Name", str, new_name)
        inputs.append(_input)
        cls = CustomNameAction
        super().__init__(name, inputs, cls, string_range)


class FolderName(ActionDescriptor):
    """Use the parent foldername as the filename."""

    def __init__(self, string_range=None):
        name = "Folder Name"
        inputs = []
        cls = FolderNameAction
        super().__init__(name, inputs, cls, string_range)


class FileDate(ActionDescriptor):

    def __init__(self, string_range=None):
        name = "Date"
        inputs = []
        is_modified_date_input = ActionInput("is_modified_date", "Modified", bool, True)
        is_created_date_input = ActionInput("is_modified_date", "Created", bool, False)
        time_format_input_ = ActionInput("time_format", "Format", str, "%Y-%m-%d %H:%M:%S (%A %B)")
        inputs.append(is_modified_date_input)
        inputs.append(is_created_date_input)
        inputs.append(time_format_input_)
        cls = DateAction
        super().__init__(name, inputs, cls, string_range)


class Counter(ActionDescriptor):
    """Count the number of files starting from start_index with the given increment."""
    def __init__(self, string_range=None):
        name = "Counter"
        inputs = []
        start_index_input = ActionInput("start_index", "Start At", int, 0)
        increment_input = ActionInput("increment", "Increment", int, 1)
        digit_number_input = ActionInput("digit_number", "Number of Digit", int, 1)
        inputs.append(start_index_input)
        inputs.append(increment_input)
        inputs.append(digit_number_input)
        cls = CounterAction
        super().__init__(name, inputs, cls, string_range)


class ImageOriginalDate(ActionDescriptor):

    def __init__(self, string_range=None):
        name = "Original Date"
        inputs = []
        time_format_input = ActionInput("time_format", "Format", str, "%Y-%m-%d %H:%M:%S")
        inputs.append(time_format_input)
        cls = ImageDateTimeOriginal
        super().__init__(name, inputs, cls, string_range)


class ImageFNumber(ActionDescriptor):
    def __init__(self, string_range=None):
        name = "F Number"
        inputs = []
        cls = ImageFNumber
        super().__init__(name, inputs, cls, string_range)


class ImageExposure(ActionDescriptor):
    def __init__(self, string_range=None):
        name = "Exposure"
        inputs = []
        cls = ImageExposureTime
        super().__init__(name, inputs, cls, string_range)


class ImageISO(ActionDescriptor):
    def __init__(self, string_range=None):
        name = "ISO"
        inputs = []
        cls = ImageISO
        super().__init__(name, inputs, cls, string_range)


class ImageCameraModel(ActionDescriptor):
    def __init__(self, string_range=None):
        name = "Camera Model"
        inputs = []
        cls = ImageCameraModel
        super().__init__(name, inputs, cls, string_range)


class ImageXDimension(ActionDescriptor):
    def __init__(self, string_range=None):
        name = "X Dimension"
        inputs = []
        cls = ImageXDimension
        super().__init__(name, inputs, cls, string_range)


class ImageYDimension(ActionDescriptor):
    def __init__(self, string_range=None):
        name = "Y Dimension"
        inputs = []
        cls = ImageYDimension
        super().__init__(name, inputs, cls, string_range)


class ImageFocalLength(ActionDescriptor):
    def __init__(self, string_range=None):
        name = "Focal Length"
        inputs = []
        cls = ImageFocalLength
        super().__init__(name, inputs, cls, string_range)


class ImageArtist(ActionDescriptor):
    def __init__(self, string_range=None):
        name = "Artist"
        inputs = []
        cls = ImageArtist
        super().__init__(name, inputs, cls, string_range)


class MusicArtist(ActionDescriptor):
    def __init__(self, string_range=None):
        name = "Artist"
        inputs = []
        cls = MusicArtist
        super().__init__(name, inputs, cls, string_range)


class MusicTitle(ActionDescriptor):
    def __init__(self, string_range=None):
        name = "Title"
        inputs = []
        cls = MusicTitle
        super().__init__(name, inputs, cls, string_range)


class MusicYear(ActionDescriptor):
    def __init__(self, string_range=None):
        name = "Year"
        inputs = []
        cls = MusicYear
        super().__init__(name, inputs, cls, string_range)


class MusicAlbum(ActionDescriptor):
    def __init__(self, string_range=None):
        name = "Album"
        inputs = []
        cls = MusicAlbum
        super().__init__(name, inputs, cls, string_range)


class MusicTrack(ActionDescriptor):
    def __init__(self, string_range=None):
        name = "Track Number"
        inputs = []
        cls = MusicTrack
        super().__init__(name, inputs, cls, string_range)


class MusicGenre(ActionDescriptor):
    def __init__(self, string_range=None):
        name = "Genre"
        inputs = []
        cls = MusicGenre
        super().__init__(name, inputs, cls, string_range)
