#!/usr/bin/python3


from action_input import ActionInput
from string_range import StringRange
from scope import Scope
from renaming_actions import *


class ActionDescriptor(object):
    """
    Describes the actions by names, inputs and classes.
    Parameters:
        --name: string that represents the name of the action.
        --inputs: list of ActionInput that represents the inputs properties of the acion.
        --action_class: string that represents the name of the class used for the action.
    """

    def __init__(self, name, class_, inputs=[]):
        self._name = name
        self._class = class_
        self._inputs = inputs
        self._caption = ""

        self._input_value_by_name = {_input.name: _input.value for _input in self._inputs}
        self._scope_flags = Scope.filename | Scope.foldername | Scope.extension

    def __repr__(self):
        """override string representation of the class"""
        return self._name

    @property
    def name(self):
        return self._name

    @property
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self, value):
        self._caption = value

    @property
    def inputs(self):
        return self._inputs

    @property
    def scope_flags(self):
        return self._scope_flags

    @scope_flags.setter
    def scope_flags(self, value):
        self._scope_flags = value

    def create_action(self):
        action_instance = self._class(**self._input_value_by_name)
        action_instance.range = self.range
        action_instance.scope = self.scope
        return action_instance


class OriginalName(ActionDescriptor):

    def __init__(self):
        super().__init__("OriginalName", OriginalNameAction)
        self.caption = "Original Name"


class FindAndReplace(ActionDescriptor):
    """
    Replace old_value by new_value in the section of the path.
    action_range can be 'folder', 'file', 'prefix', 'suffix' or 'extension'.
    """
    def __init__(self):
        inputs = []
        old_value_input = ActionInput("old_value", InputType.string)
        old_value_input.caption = "Replace"
        new_value_input = ActionInput("new_value", InputType.string)
        old_value_input.caption = "With"
        is_regex_input = ActionInput("is_regex", InputType.boolean)
        is_regex_input.caption = "Regex"
        inputs.append(old_value_input)
        inputs.append(new_value_input)
        inputs.append(is_regex_input)
        super().__init__("FindAndReplace", FindAndReplaceAction, inputs)
        self.caption = "Find And Replace"


class CharacterInsertion(ActionDescriptor):
    """Insert new_value at index position."""

    def __init__(self):
        inputs = []
        custom_name_input = ActionInput("custom_name", InputType.string)
        custom_name_input.is_readonly = True
        custom_name_input.is_visible = False
        inputs.append(custom_name_input)
        range_input = ActionInput("string_range", InputType.range)
        range_input.caption = "Range"
        inputs.append(range_input)
        super().__init__("Insert", CustomNameAction, inputs)
        self.caption = "Insert Characters"
        self._is_range_readonly = True


class CharacterDeletion(ActionDescriptor):
    """Delete n-character from starting_position to ending_position."""
    def __init__(self):
        inputs = []
        custom_name_input = ActionInput("custom_name", InputType.string)
        custom_name_input.is_readonly = True
        custom_name_input.is_visible = False
        inputs.append(custom_name_input)
        super().__init__("Delete", CustomNameAction, inputs)
        self.caption = "Delete Characters"


class TitleCase(ActionDescriptor):
    """
    Return the original name with a chosen casing option.
    Parameters:
        --case_choise: option to specify the case : 'uppercase', 'lowercase', 'titlecase'.
        --is_first_letter_uppercase: boolean making first letter uppercase or lowercase.
        --special_characters: list of symbols after which the letters are capitalized.
    """
    def __init__(self):
        inputs = []
        is_first_letter_uppercase_input = ActionInput("is_first_letter_uppercase", InputType.boolean)
        is_first_letter_uppercase_input.caption = "First Letter"
        inputs.append(is_first_letter_uppercase_input)
        special_characters_input = ActionInput("special_characters", InputType.string)
        special_characters_input.caption = "And After"
        inputs.append(special_characters_input)
        super().__init__("Titlecase", TitleCaseAction, inputs)
        self.caption = "Titlecase"


class UpperCase(ActionDescriptor):
    """
    Return the original name with a chosen casing option.
    Parameters:
        --case_choise: option to specify the case : 'uppercase', 'lowercase', 'titlecase'.
        --is_first_letter_uppercase: boolean making first letter uppercase or lowercase.
        --special_characters: list of symbols after which the letters are capitalized.
    """

    def __init__(self):
        super().__init__("Uppercase", UppercaseAction)
        self.caption = "Uppercase"


class LowerCase(ActionDescriptor):
    """
    Return the original name with a chosen casing option.
    Parameters:
        --case_choise: option to specify the case : 'uppercase', 'lowercase', 'titlecase'.
        --is_first_letter_uppercase: boolean making first letter uppercase or lowercase.
        --special_characters: list of symbols after which the letters are capitalized.
    """
    def __init__(self):
        super().__init__("Lowercase", LowerCaseAction)
        self.caption = "Lowercase"


class CustomName(ActionDescriptor):
    """Use a custom name in the filename.
    Can be also used to remove character if en empty string is given.
    """

    def __init__(self):
        custom_name_input = ActionInput("custom_name", InputType.string)
        inputs.append(custom_name_input)
        super().__init__("CustomName", CustomNameAction)
        self.caption = "Custom Name"


class FolderName(ActionDescriptor):
    """Use the parent foldername as the filename."""

    def __init__(self):
        name = "Folder Name"
        inputs = []
        _input = ActionInput("custom_name", "New Name", str, new_name)
        inputs.append(_input)
        cls = FolderNameAction
        super().__init__(name, inputs, cls)


class FileDate(ActionDescriptor):

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
        super().__init__(name, inputs, cls)


class Counter(ActionDescriptor):
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
        super().__init__(name, inputs, cls)


class ImageOriginalDate(ActionDescriptor):

    def __init__(self):
        name = "Original Date"
        inputs = []
        time_format_input = ActionInput("time_format", "Format", str, "%Y-%m-%d %H:%M:%S")
        inputs.append(time_format_input)
        cls = ImageDateTimeOriginal
        super().__init__(name, inputs, cls)
        self._scope_flags = Scope.filename


class ImageFNumber(ActionDescriptor):
    def __init__(self):
        name = "F Number"
        inputs = []
        cls = ImageFNumber
        super().__init__(name, inputs, cls)
        self._scope_flags = Scope.filename


class ImageExposure(ActionDescriptor):
    def __init__(self):
        name = "Exposure"
        inputs = []
        cls = ImageExposureTime
        super().__init__(name, inputs, cls)
        self._scope_flags = Scope.filename


class ImageISO(ActionDescriptor):
    def __init__(self):
        name = "ISO"
        inputs = []
        cls = ImageISO
        super().__init__(name, inputs, cls)
        self._scope_flags = Scope.filename


class ImageCameraModel(ActionDescriptor):
    def __init__(self):
        name = "Camera Model"
        inputs = []
        cls = ImageCameraModel
        super().__init__(name, inputs, cls)
        self._scope_flags = Scope.filename


class ImageXDimension(ActionDescriptor):
    def __init__(self):
        name = "X Dimension"
        inputs = []
        cls = ImageXDimension
        super().__init__(name, inputs, cls)
        self._scope_flags = Scope.filename


class ImageYDimension(ActionDescriptor):
    def __init__(self):
        name = "Y Dimension"
        inputs = []
        cls = ImageYDimension
        super().__init__(name, inputs, cls)
        self._scope_flags = Scope.filename


class ImageFocalLength(ActionDescriptor):
    def __init__(self):
        name = "Focal Length"
        inputs = []
        cls = ImageFocalLength
        super().__init__(name, inputs, cls)
        self._scope_flags = Scope.filename


class ImageArtist(ActionDescriptor):
    def __init__(self):
        name = "Artist"
        inputs = []
        cls = ImageArtist
        super().__init__(name, inputs, cls)
        self._scope_flags = Scope.filename


class MusicArtist(ActionDescriptor):
    def __init__(self):
        name = "Artist"
        inputs = []
        cls = MusicArtist
        super().__init__(name, inputs, cls)
        self._scope_flags = Scope.filename


class MusicTitle(ActionDescriptor):
    def __init__(self):
        name = "Title"
        inputs = []
        cls = MusicTitle
        super().__init__(name, inputs, cls)
        self._scope_flags = Scope.filename


class MusicYear(ActionDescriptor):
    def __init__(self):
        name = "Year"
        inputs = []
        cls = MusicYear
        super().__init__(name, inputs, cls)
        self._scope_flags = Scope.filename


class MusicAlbum(ActionDescriptor):
    def __init__(self):
        name = "Album"
        inputs = []
        cls = MusicAlbum
        super().__init__(name, inputs, cls)
        self._scope_flags = Scope.filename


class MusicTrack(ActionDescriptor):
    def __init__(self):
        name = "Track Number"
        inputs = []
        cls = MusicTrack
        super().__init__(name, inputs, cls)
        self._scope_flags = Scope.filename


class MusicGenre(ActionDescriptor):
    def __init__(self):
        name = "Genre"
        inputs = []
        cls = MusicGenre
        super().__init__(name, inputs, cls)
        self._scope_flags = Scope.filename
