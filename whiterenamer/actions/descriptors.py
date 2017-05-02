#!/usr/bin/python3

from action_input import ActionInput
from target import Target
from actions import *
from input_type import InputType
import inspect

class ActionDescriptor(object):
    """
    An abstract base class of all action descriptors,
    that defines all the specification, documentation of a given action.

    Args:
        name (string): The string used to instanciate the action specified by the class parameter.
        action_class (string): A string that represents the name of the Action class.
    """

    def __init__(self, name, action_class):
        self._name = name
        self._class = action_class
        self._caption = ""
        self._inputs = dict()
        target_input = ActionInput("target", InputType.target)
        target_input.is_visible = False
        target_input.documentation = """Specifies what kind of filesystem entity (file, folder, extension) the action should be applied."""
        self._inputs["target"] = target_input
        range_input = ActionInput("string_range", InputType.range)
        range_input.is_visible = False
        range_input.documentation = """Defines the portion of the name upon which the action will be perfomed.
        The range is defined with a start and a end index.
        0 being the beginning of the string,
        None being the end of the string,
        Negative numbers can be used to start from the end.
        """
        self._inputs["string_range"] = range_input
        self._target_flags = Target.filename | Target.foldername | Target.extension
        self._group = None
        self._documentation = ""

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
        # Verify if the given target is in the target flags.
        target = self._inputs.get("target")
        if target is not None:
            if target not in self.target_flags:
                raise Exception("Invalid target: \
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
        self.documentation.summary = """Keeps the original name. This action does not do anything."""


class FindAndReplace(ActionDescriptor):
    def __init__(self):
        super().__init__("FindAndReplace", FindAndReplaceAction)
        old_value_input = ActionInput("old_value", InputType.string)
        old_value_input.caption = "Replace"
        old_value.documetation = "The string to find."
        self._add_input(old_value_input)
        new_value_input = ActionInput("new_value", InputType.string)
        new_value_input.caption = "With"
        new_value.documetation = "The new string that will replace the old value."
        self._add_input(new_value_input)
        is_regex_input = ActionInput("is_regex", InputType.boolean)
        is_regex_input.caption = "Regex"
        is_regex.documentation = "Specifies whether regex are used to find the value that will be replaced."
        self._add_input(is_regex_input)
        self.caption = "Find And Replace"
        self.documentation = """Finds a string and replaces it yith the given value."""


class Overwrite(ActionDescriptor):
    def __init__(self):
        super().__init__("Overwrite", OverwriteAction)
        character_input = ActionInput("value", InputType.string)
        character_input.documentation = "The new string to use."
        self._add_input(character_input)
        self.caption = "Overwrite"
        self.documentation = """Overwrites a portion of the name with the given string."""


class Delete(ActionDescriptor):
    def __init__(self):
        super().__init__("Delete", DeleteAction)
        self.caption = "Delete"
        self.documentation = "Deletes n-character(s) specified by the given range."


class TitleCase(ActionDescriptor):
    def __init__(self):
        super().__init__("Titlecase", TitleCaseAction)
        is_first_letter_uppercase_input = ActionInput(
            "is_first_letter_uppercase", InputType.boolean)
        is_first_letter_uppercase_input.caption = "First Letter"
        is_first_letter_uppercase_input.documentation = "Specifies whether the first letter should be capitalized or not."
        self._add_input(is_first_letter_uppercase_input)
        special_characters_input = ActionInput("special_characters",
                                               InputType.string)
        special_characters_input.caption = "And After"
        special_characters_input.documentation = "A list of symbols after which the letters are capitalized."
        self._add_input(special_characters_input)
        self.caption = "Titlecase"
        self.documetation = "Return a titlecased version of the name, i.e. words start with uppercase characters, all remaining cased characters have lowercase."


class UpperCase(ActionDescriptor):
    def __init__(self):
        super().__init__("Uppercase", UppercaseAction)
        self.caption = "Uppercase"
        self.documetation = "Uppercases the original name."


class LowerCase(ActionDescriptor):
    def __init__(self):
        super().__init__("Lowercase", LowerCaseAction)
        self.caption = "Lowercase"
        self.documetation = "Lowercases the original name."


class FolderName(ActionDescriptor):
    """Use the parent foldername as the filename."""

    def __init__(self):
        super().__init__("FolderName", FolderNameAction)
        self.caption = "Folder Name"
        self.documentation = "Uses the parent foldername as the new name."


class FileDate(ActionDescriptor):
    def __init__(self):
        super().__init__("Date", DateAction)
        is_modified_date_input = ActionInput("is_modified_date",
                                             InputType.boolean)
        is_modified_date_input.caption = "Modified"
        is_modified_date_input.documentation = "Specifies whether the modified or the created date is used."

        self._add_input(is_modified_date_input)
        time_format_input = ActionInput("time_format", InputType.string)
        time_format_input.caption = "Format"
        time_format_input.documentation = """The format to display the date.
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
        self._add_input(time_format_input)
        self.caption = "Date"
        self.documentation = "Uses the created or modified date metadata as the new name."


class Counter(ActionDescriptor):
    def __init__(self):
        super().__init__("Counter", CounterAction)
        start_index_input = ActionInput("start_index", InputType.number)
        start_index_input.caption = "Start At"
        start_index_input.documentation = "The index at which the counter starts."
        self._add_input(start_index_input)
        increment_input = ActionInput("increment", InputType.number)
        increment_input.caption = "Increment"
        increment_input.documentation = "TODO"
        self._add_input(increment_input)
        digit_number_input = ActionInput("digit_number", InputType.number)
        digit_number_input.caption = "Number of Digit"
        digit_number_input.documentation = "TODO"
        self._add_input(digit_number_input)
        self.caption = "Counter"
        self.documentation = "Counts each files/folders in the same directory."


class ImageOriginalDate(ActionDescriptor):
    def __init__(self):
        super().__init__("ImageDate", ImageDateTimeOriginal)
        self.caption = "Original Date"
        time_format_input = ActionInput("time_format", InputType.string)
        time_format_input.caption = "Format"
        time_format_input.documentation = """The format to display the date.
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
        self._add_input(time_format_input)
        self.group = ActionDescriptorGroup("Image")
        self.documentation = "Uses the original date from the image metadata."


class ImageFNumber(ActionDescriptor):
    def __init__(self):
        super().__init__("FNumber", ImageFNumber)
        self.caption = "F Number"
        self.group = ActionDescriptorGroup("Image")
        self.documentation = "Uses the F Number from the image EXIF metadata."


class ImageExposure(ActionDescriptor):
    def __init__(self):
        super().__init__("Exposure", ImageExposureTime)
        self.caption = "Exposure"
        self.group = ActionDescriptorGroup("Image")
        self.documentation = "Uses the exposure time from the image EXIF metadata."


class ImageISO(ActionDescriptor):
    def __init__(self):
        super().__init__("ImageISO", ImageISO)
        self.caption = "ISO"
        self.group = ActionDescriptorGroup("Image")
        self.documentation = "Uses the ISO from the image EXIF metadata."


class ImageCameraModel(ActionDescriptor):
    def __init__(self):
        super().__init__("ImageCameraModel", ImageCameraModel)
        self.caption = "Camera Model"
        self.group = ActionDescriptorGroup("Image")
        self.documentation = "Uses the camera model from the image EXIF metadata."


class ImageXDimension(ActionDescriptor):
    def __init__(self):
        super().__init__("ImageX", ImageXDimension)
        self.caption = "X Dimension"
        self.group = ActionDescriptorGroup("Image")
        self.documentation = "Uses the width of the image from the EXIF metadata."


class ImageYDimension(ActionDescriptor):
    def __init__(self):
        super().__init__("ImageY", ImageYDimension)
        self.caption = "Y Dimension"
        self.group = ActionDescriptorGroup("Image")
        self.documentation = "Uses the height of the image from the EXIF metadata."


class ImageFocalLength(ActionDescriptor):
    def __init__(self):
        super().__init__("ImageFocal", ImageFocalLength)
        self.caption = "Focal Length"
        self.group = ActionDescriptorGroup("Image")
        self.documentation = "Uses the focal length from the image EXIF metadata."


class ImageArtist(ActionDescriptor):
    def __init__(self):
        super().__init__("ImageArtist", ImageArtist)
        self.caption = "Artist"
        self.group = ActionDescriptorGroup("Image")
        self.documentation = "Uses the artist from the image EXIF metadata."


class MusicArtist(ActionDescriptor):
    def __init__(self):
        super().__init__("MusicArtist", MusicArtist)
        self.caption = "Artist"
        self.group = ActionDescriptorGroup("Music")
        self.documentation = "Uses the artist from the metadata."


class MusicTitle(ActionDescriptor):
    def __init__(self):
        super().__init__("MusicTitle", MusicTitle)
        self.caption = "Title"
        self.group = ActionDescriptorGroup("Music")
        self.documentation = "Uses the title from the metadata."


class MusicYear(ActionDescriptor):
    def __init__(self):
        super().__init__("MusicYear", MusicYear)
        self.caption = "Year"
        self.group = ActionDescriptorGroup("Music")
        self.documentation = "Uses the album year from the metadata."


class MusicAlbum(ActionDescriptor):
    def __init__(self):
        super().__init__("MusicAlbum", MusicAlbum)
        self.caption = "Album"
        self.group = ActionDescriptorGroup("Music")
        self.documentation = "Uses the album name from the metadata."


class MusicTrack(ActionDescriptor):
    def __init__(self):
        super().__init__("MusicTrack", MusicTrack)
        self.caption = "Track Number"
        self.group = ActionDescriptorGroup("Music")
        self.documentation = "Uses the track name from the metadata."


class MusicGenre(ActionDescriptor):
    def __init__(self):
        super().__init__("MusicGenre", MusicGenre)
        self.caption = "Genre"
        self.group = ActionDescriptorGroup("Music")
        self.documentation = "Uses the music genre from the metadata."


class ActionDescriptorGroup(object):
    """
    Contains a collection of ActionDescriptor.

    Args:
        caption (string): The caption of the group.
    """

    def __init__(self, caption):
        self._caption = name

    @property
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self, value):
        self._caption = value

    def __repr__(self):
        """override string representation of the class"""
        return self.name

class InputType(Enum):
    boolean = 0
    string = 1
    number = 2
    range = 3


class ActionInput(object):
    """ Describes a parameter from an action.

    Args:
        parameter_name (string): A string that is the name given to the parameter from the action.
        input_type (InputType): Specifies the type of the given parameter.
    """

    def __init__(self, parameter_name, input_type):
        self._parameter_name = parameter_name
        self._input_type = input_type
        # Set the parameter name as default to caption.
        self._caption = parameter_name
        self._is_readonly = False
        self._is_visible = True
        self._documentation = ""

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

    @property
    def documentation(self):
        return self._documentation

    @documentation.setter
    def documentation(self, value):
        self._documentation = value

