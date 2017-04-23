#!/usr/bin/python3

from action_input import ActionInput
from scope import Scope
from renaming_actions import *
from input_type import InputType
import inspect


class InputType(Enum):
    boolean = 0
    string = 1
    number = 2
    range = 3


class ActionInput(object):
    """ Describes a parameter from an action.
    Parameters:
        --parameter_name: string that represents the name given to the parameter described by this action input.
        --caption: string that represents the caption of the given parameter.
        --arg_type: specifies which type is the given parameter.
        --default_value: specifies the default value of the given parameter.
        --optional_argument: gives the possibility to add an optional argument for storing data.
    """

    def __init__(self, parameter_name, input_type):
        self._parameter_name = parameter_name
        self._input_type = input_type
        # Set the parameter name as default to caption.
        self._caption = parameter_name
        self._is_readonly = False
        self._is_visible = True

    @property
    def parameter_name(self):
        return self._parameter_name

    @parameter_name.setter
    def parameter_name(self, value):
        self._parameter_name = value

    @property
    def input_type(self):
        return self._input_type

    @input_type.setter
    def input_type(self, value):
        self._input_type = value

    @property
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self, value):
        self._caption = value

    @property
    def is_readonly(self):
        return self._is_readonly

    @is_readonly.setter
    def is_readonly(self, value):
        self._is_readonly = value

    @property
    def is_visible(self):
        return self._is_visible

    @is_visible.setter
    def is_visible(self, value):
        self._is_visible = value


class ActionDescriptor(object):
    """
    Describes the actions by names, inputs and classes.
    Parameters:
        --name: string that represents the name of the action.
        --inputs: list of ActionInput that represents the inputs properties of the acion.
        --action_class: string that represents the name of the class used for the action.
    """

    def __init__(self, name, class_):
        self._name = name
        self._class = class_
        self._caption = ""
        self._inputs = dict()
        scope_input = ActionInput("scope", InputType.scope)
        scope_input.is_visible = False
        self._inputs["scope"] = scope_input
        range_input = ActionInput("string_range", InputType.range)
        range_input.is_visible = False
        self._inputs["string_range"] = range_input
        self._scope_flags = Scope.filename | Scope.foldername | Scope.extension
        self._group = None
        self._documentation = inspect.getdoc(class_)

    def __repr__(self):
        """override string representation of the class"""
        return self._name

    @property
    def inputs(self):
        """ A dictionary mapping the action inputs with the corresponding parameter names."""
        return self._inputs

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
    def scope_flags(self):
        return self._scope_flags

    @scope_flags.setter
    def scope_flags(self, value):
        self._scope_flags = value

    @property
    def group(self):
        return self._group

    @property
    def documentation(self):
        """Gets the documentation of the action.
        (It is fetched automatically from the docstring of the action class.)
        """
        return self._documentation

    def _add_input(self, action_input):
        self.inputs[action_input.name] = action_input

    def _verify_arguments(self, **keyword_arguments):
        """Verify if the keyword_arguments passed to create the action are allowed.
        """
        # Verify if the given scope is in the scope flags.
        scope = self._inputs.get("scope")
        if scope is not None:
            scope = self._inputs["scope"]
            if scope not in self.scope_flags:
                raise Exception("Invalid scope: \
                it cannot be applied to the given filesystem node.")
        for keyword_argument in keyword_arguments:
            try:
                input_ = self._inputs[keyword_argument]
                if input_.is_readonly:
                    raise Exception(
                        "The argument {0} is readonly and cannot be changed.".
                        format(keyword_argument))
            except KeyError:
                raise KeyError(
                    "The action {0} does not contain a {1} argument.".format(
                        self._class.name, keyword_argument))

    def create_action(self, **keyword_arguments):
        self._verify_arguments(**keyword_arguments)
        action_instance = self._class(**keyword_arguments)
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
        super().__init__("FindAndReplace", FindAndReplaceAction)
        old_value_input = ActionInput("old_value", InputType.string)
        old_value_input.caption = "Replace"
        self._add_input(old_value_input)
        new_value_input = ActionInput("new_value", InputType.string)
        new_value_input.caption = "With"
        self._add_input(new_value_input)
        is_regex_input = ActionInput("is_regex", InputType.boolean)
        is_regex_input.caption = "Regex"
        self._add_input(is_regex_input)
        self.caption = "Find And Replace"


class CharacterInsertion(ActionDescriptor):
    """Insert new_value at index position."""

    def __init__(self):
        super().__init__("Insert", CharacterInsertionAction)
        character_input = ActionInput("value", InputType.string)
        self._add_input(character_input)
        index_input = ActionInput("index", InputType.integer)
        self._add_input(index_input)
        self.caption = "Insert Characters"


class CharacterDeletion(ActionDescriptor):
    """Delete n-character from starting_position to ending_position."""

    def __init__(self):
        super().__init__("Delete", CustomNameAction)
        range_input = ActionInput("string_range", InputType.range)
        self._add_input(range_input)
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
        super().__init__("Titlecase", TitleCaseAction)
        is_first_letter_uppercase_input = ActionInput(
            "is_first_letter_uppercase", InputType.boolean)
        is_first_letter_uppercase_input.caption = "First Letter"
        self._add_input(is_first_letter_uppercase_input)
        special_characters_input = ActionInput("special_characters",
                                               InputType.string)
        special_characters_input.caption = "And After"
        self._add_input(special_characters_input)
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
        super().__init__("CustomName", CustomNameAction)
        custom_name_input = ActionInput("custom_name", InputType.string)
        self._add_input(custom_name_input)
        self.caption = "Custom Name"


class FolderName(ActionDescriptor):
    """Use the parent foldername as the filename."""

    def __init__(self):
        super().__init__("FolderName", FolderNameAction)
        self.caption = "Folder Name"


class FileDate(ActionDescriptor):
    def __init__(self):
        super().__init__("Date", DateAction)
        is_modified_date_input = ActionInput("is_modified_date",
                                             InputType.boolean)
        is_modified_date_input.caption = "Modified"
        time_format_input = ActionInput("time_format", InputType.string)
        time_format_input.caption = "Format"
        self._add_input(time_format_input)
        self.caption = "Date"


class Counter(ActionDescriptor):
    """Count the number of files starting from start_index with the given increment."""

    def __init__(self):
        super().__init__("Counter", CounterAction)
        start_index_input = ActionInput("start_index", InputType.number)
        start_index_input.caption = "Start At"
        self._add_input(start_index_input)
        increment_input = ActionInput("increment", InputType.number)
        increment_input.caption = "Increment"
        self._add_input(increment_input)
        digit_number_input = ActionInput("digit_number", InputType.number)
        digit_number_input.caption = "Number of Digit"
        self._add_input(digit_number_input)
        self.caption = "Counter"


class ImageOriginalDate(ActionDescriptor):
    def __init__(self):
        super().__init__("ImageDate", ImageDateTimeOriginal)
        self.caption = "Original Date"
        time_format_input = ActionInput("time_format", InputType.string)
        time_format_input.caption = "Format"
        self._add_input(time_format_input)
        self._scope_flags = Scope.filename
        self.group = ActionDescriptorGroup("Image")


class ImageFNumber(ActionDescriptor):
    def __init__(self):
        super().__init__("FNumber", ImageFNumber)
        self.caption = "F Number"
        self._scope_flags = Scope.filename
        self.group = ActionDescriptorGroup("Image")


class ImageExposure(ActionDescriptor):
    def __init__(self):
        super().__init__("Exposure", ImageExposureTime)
        self.caption = "Exposure"
        self._scope_flags = Scope.filename
        self.group = ActionDescriptorGroup("Image")


class ImageISO(ActionDescriptor):
    def __init__(self):
        super().__init__("ImageISO", ImageISO)
        self.caption = "ISO"
        self._scope_flags = Scope.filename
        self.group = ActionDescriptorGroup("Image")


class ImageCameraModel(ActionDescriptor):
    def __init__(self):
        super().__init__("ImageCameraModel", ImageCameraModel)
        self.caption = "Camera Model"
        self._scope_flags = Scope.filename
        self.group = ActionDescriptorGroup("Image")


class ImageXDimension(ActionDescriptor):
    def __init__(self):
        super().__init__("ImageX", ImageXDimension)
        self.caption = "X Dimension"
        self._scope_flags = Scope.filename
        self.group = ActionDescriptorGroup("Image")


class ImageYDimension(ActionDescriptor):
    def __init__(self):
        super().__init__("ImageY", ImageYDimension)
        self.caption = "Y Dimension"
        self._scope_flags = Scope.filename
        self.group = ActionDescriptorGroup("Image")


class ImageFocalLength(ActionDescriptor):
    def __init__(self):
        super().__init__("ImageFocal", ImageFocalLength)
        self.caption = "Focal Length"
        self._scope_flags = Scope.filename
        self.group = ActionDescriptorGroup("Image")


class ImageArtist(ActionDescriptor):
    def __init__(self):
        super().__init__("ImageArtist", ImageArtist)
        self.caption = "Artist"
        self._scope_flags = Scope.filename
        self.group = ActionDescriptorGroup("Image")


class MusicArtist(ActionDescriptor):
    def __init__(self):
        super().__init__("MusicArtist", MusicArtist)
        self.caption = "Artist"
        self._scope_flags = Scope.filename
        self.group = ActionDescriptorGroup("Music")


class MusicTitle(ActionDescriptor):
    def __init__(self):
        super().__init__("MusicTitle", MusicTitle)
        self.caption = "Title"
        self._scope_flags = Scope.filename
        self.group = ActionDescriptorGroup("Music")


class MusicYear(ActionDescriptor):
    def __init__(self):
        super().__init__("MusicYear", MusicYear)
        self.caption = "Year"
        self._scope_flags = Scope.filename
        self.group = ActionDescriptorGroup("Music")


class MusicAlbum(ActionDescriptor):
    def __init__(self):
        super().__init__("MusicAlbum", MusicAlbum)
        self.caption = "Album"
        self._scope_flags = Scope.filename
        self.group = ActionDescriptorGroup("Music")


class MusicTrack(ActionDescriptor):
    def __init__(self):
        super().__init__("MusicTrack", MusicTrack)
        self.caption = "Track Number"
        self._scope_flags = Scope.filename
        self.group = ActionDescriptorGroup("Music")


class MusicGenre(ActionDescriptor):
    def __init__(self):
        super().__init__("MusicGenre", MusicGenre)
        self.caption = "Genre"
        self._scope_flags = Scope.filename
        self.group = ActionDescriptorGroup("Music")


class ActionDescriptorGroup(object):
    """
    Contains a collectino of ActionDescriptor.
    Parameters:
        --action_descriptors: a list of ActionDescriptor.
    """

    def __init__(self, name):
        self._name = name
        self._caption = name

    @property
    def name(self):
        return self._name

    @property
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self, value):
        self._caption = value

    def __repr__(self):
        """override string representation of the class"""
        return self.name
