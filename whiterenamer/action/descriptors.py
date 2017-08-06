#!/usr/bin/python3

from enum import Enum

from .actions import *
from .scope import StringRange, Targets


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
        self._parameters = dict()
        targets_parameter = ActionParameterDescriptor("targets", ParameterType.enum)
        targets_parameter.default_value = Targets.filename | Targets.foldername | Targets.extension
        targets_parameter.is_visible = False
        targets_parameter.documentation = """ Specifies what kind of filesystem entity
            (file, folder, extension) the action should be applied."""
        self._parameters["targets"] = targets_parameter
        range_parameter = ActionParameterDescriptor("string_range", ParameterType.range)
        range_parameter.default_value = StringRange(0, None)
        range_parameter.is_visible = False
        range_parameter.documentation = """Defines the portion of the name upon which the action will be perfomed.
        The range is defined with a start and a end index.
        0 being the beginning of the string,
        None being the end of the string,
        Negative numbers can be used to start from the end.
        """
        self._parameters["string_range"] = range_parameter
        self._allowed_targets = Targets.filename | Targets.foldername | Targets.extension
        self._group = None
        self._documentation = ""

    def __repr__(self):
        """override string representation of the class"""
        return self._name

    @property
    def parameters(self):
        """ A dictionary mapping the action parameters with the corresponding parameter names."""
        return self._parameters

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

    def allowed_targets(self):
        return self._allowed_targets

    @group.setter
    def group(self, value):
        self._group = value

    @property
    def documentation(self):
        """Gets the documentation of the action.
        (It is fetched automatically from the docstring of the action class.)
        """
        return self._documentation

    @documentation.setter
    def documentation(self, value):
        self._documentation = value

    def _add_parameter(self, action_parameter):
        self.parameters[action_parameter.name] = action_parameter

    def _verify_arguments(self, keyword_arguments):
        """Verify if the keyword_arguments passed to create the action are allowed.
        """
        for key, value in keyword_arguments.items():
            try:
                parameter_ = self._parameters[key]
                if parameter_.is_readonly:
                    raise Exception(
                        "The argument {0} is readonly and cannot be changed.".format(key))
            except KeyError:
                raise KeyError(
                    "The action {0} does not contain a {1} argument.".format(self._class.name, key))
            # Verify if the given target is in the target flags.
            if key is "targets":
                if value not in self._allowed_targets:
                    raise Exception("Invalid targets: \
                    it cannot be applied to the given filesystem node.")

    def _find_default_values(self):
        return filter(lambda value: value.default_value is not None, self._parameters.values())

    def _assign_parameter_default_values(self, keyword_arguments):
        for parameter in self._find_default_values():
            if keyword_arguments.get(parameter.name) is None:
                keyword_arguments[parameter.name] = parameter.default_value

    def create_action(self, **keyword_arguments):
        self._assign_parameter_default_values(keyword_arguments)
        self._verify_arguments(keyword_arguments)
        action_instance = self._class(**keyword_arguments)
        return action_instance


class OriginalName(ActionDescriptor):
    def __init__(self):
        super().__init__("OriginalName", OriginalNameAction)
        self.caption = "Original Name"
        self.documentation = """Keeps the original name. This action does not do anything."""


class FindAndReplace(ActionDescriptor):
    def __init__(self):
        super().__init__("FindAndReplace", FindAndReplaceAction)
        old_value_parameter = ActionParameterDescriptor("old_value", ParameterType.string)
        old_value_parameter.caption = "Replace"
        old_value_parameter.documentation = "The string to find."
        self._add_parameter(old_value_parameter)
        new_value_parameter = ActionParameterDescriptor("new_value", ParameterType.string)
        new_value_parameter.caption = "With"
        new_value_parameter.documentation = "The new string that will replace the old value."
        self._add_parameter(new_value_parameter)
        is_regex_parameter = ActionParameterDescriptor("is_regex", ParameterType.boolean)
        is_regex_parameter.caption = "Regex"
        is_regex_parameter.documentation = "Specifies whether regex are used to find the value that will be replaced."
        self._add_parameter(is_regex_parameter)
        self.caption = "Find And Replace"
        self.documentation = """Finds a string and replaces it yith the given value."""


class Overwrite(ActionDescriptor):
    def __init__(self):
        super().__init__("Overwrite", OverwriteAction)
        character_parameter = ActionParameterDescriptor("value", ParameterType.string)
        character_parameter.documentation = "The new string to use."
        self._add_parameter(character_parameter)
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
        is_first_letter_uppercase_parameter = ActionParameterDescriptor("is_first_letter_uppercase",
                                                                        ParameterType.boolean)
        is_first_letter_uppercase_parameter.caption = "First Letter"
        is_first_letter_uppercase_parameter.documentation = "Specifies whether the first letter should be capitalized or not."
        self._add_parameter(is_first_letter_uppercase_parameter)
        special_characters_parameter = ActionParameterDescriptor("special_characters",
                                                                 ParameterType.string)
        special_characters_parameter.caption = "And After"
        special_characters_parameter.documentation = "A list of symbols after which the letters are capitalized."
        self._add_parameter(special_characters_parameter)
        self.caption = "Title Case"
        self.documentation = "Return a titlecased version of the name, i.e. words start with uppercase characters, all remaining cased characters have lowercase."
        #self.group = ActionDescriptorGroup("Change Case")


class UpperCase(ActionDescriptor):
    def __init__(self):
        super().__init__("Uppercase", UpperCaseAction)
        self.caption = "UPPERCASE"
        self.documentation = "Uppercases the original name."
        #self.group = ActionDescriptorGroup("Change Case")


class LowerCase(ActionDescriptor):
    def __init__(self):
        super().__init__("Lowercase", LowerCaseAction)
        self.caption = "lowercase"
        self.documentation = "Lowercases the original name."
        #self.group = ActionDescriptorGroup("Change Case")


class FolderName(ActionDescriptor):
    """Use the parent foldername as the filename."""

    def __init__(self):
        super().__init__("FolderName", FolderNameAction)
        self.caption = "Folder Name"
        self.documentation = "Uses the parent foldername as the new name."


class FileDate(ActionDescriptor):
    def __init__(self):
        super().__init__("Date", DateAction)
        is_modified_date_parameter = ActionParameterDescriptor("is_modified_date",
                                                               ParameterType.boolean)
        is_modified_date_parameter.caption = "Modified"
        is_modified_date_parameter.documentation = "Specifies whether the modified or the created date is used."

        self._add_parameter(is_modified_date_parameter)
        time_format_parameter = ActionParameterDescriptor("time_format", ParameterType.string)
        time_format_parameter.caption = "Format"
        time_format_parameter.documentation = """The format to display the date.
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
        self._add_parameter(time_format_parameter)
        self.caption = "Date"
        self.documentation = "Uses the created or modified date metadata as the new name."


class Counter(ActionDescriptor):
    def __init__(self):
        super().__init__("Counter", CounterAction)
        start_index_parameter = ActionParameterDescriptor("start_index", ParameterType.number)
        start_index_parameter.caption = "Start numbers at"
        start_index_parameter.documentation = "The starting number of the sequence."
        self._add_parameter(start_index_parameter)
        increment_parameter = ActionParameterDescriptor("increment", ParameterType.number)
        increment_parameter.caption = "Increment"
        increment_parameter.documentation = "TODO"
        self._add_parameter(increment_parameter)
        digit_number_parameter = ActionParameterDescriptor("digit_number", ParameterType.number)
        digit_number_parameter.caption = "Number of Digit"
        digit_number_parameter.documentation = "TODO"
        self._add_parameter(digit_number_parameter)
        self.caption = "Counter"
        self.documentation = "Counts each files/folders in the same directory."


class ImageOriginalDate(ActionDescriptor):
    def __init__(self):
        super().__init__("ImageDate", ImageDateAction)
        self.caption = "Original Date"
        time_format_parameter = ActionParameterDescriptor("time_format", ParameterType.string)
        time_format_parameter.caption = "Format"
        time_format_parameter.documentation = """The format to display the date.


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
        self._add_parameter(time_format_parameter)
        #self.group = ActionDescriptorGroup("Image")
        self.documentation = "Uses the original date from the image metadata."
        self._allowed_targets = Targets.filename


class ImageFNumber(ActionDescriptor):
    def __init__(self):
        super().__init__("FNumber", ImageFNumber)
        self.caption = "F Number"
        #self.group = ActionDescriptorGroup("Image")
        self.documentation = "Uses the F Number from the image EXIF metadata."
        self._allowed_targets = Targets.filename


class ImageExposure(ActionDescriptor):
    def __init__(self):
        super().__init__("Exposure", ImageExposureTime)
        self.caption = "Exposure"
        #self.group = ActionDescriptorGroup("Image")
        self.documentation = "Uses the exposure time from the image EXIF metadata."
        self._allowed_targets = Targets.filename


class ImageISO(ActionDescriptor):
    def __init__(self):
        super().__init__("ImageISO", ImageISO)
        self.caption = "ISO"
        #self.group = ActionDescriptorGroup("Image")
        self.documentation = "Uses the ISO from the image EXIF metadata."
        self._allowed_targets = Targets.filename


class ImageCameraModel(ActionDescriptor):
    def __init__(self):
        super().__init__("ImageCameraModel", ImageCameraModel)
        self.caption = "Camera Model"
        #self.group = ActionDescriptorGroup("Image")
        self.documentation = "Uses the camera model from the image EXIF metadata."
        self._allowed_targets = Targets.filename


class ImageXDimension(ActionDescriptor):
    def __init__(self):
        super().__init__("ImageX", ImageXDimension)
        self.caption = "X Dimension"
        #self.group = ActionDescriptorGroup("Image")
        self.documentation = "Uses the width of the image from the EXIF metadata."
        self._allowed_targets = Targets.filename


class ImageYDimension(ActionDescriptor):
    def __init__(self):
        super().__init__("ImageY", ImageYDimension)
        self.caption = "Y Dimension"
        #self.group = ActionDescriptorGroup("Image")
        self.documentation = "Uses the height of the image from the EXIF metadata."
        self._allowed_targets = Targets.filename


class ImageFocalLength(ActionDescriptor):
    def __init__(self):
        super().__init__("ImageFocal", ImageFocalLength)
        self.caption = "Focal Length"
        #self.group = ActionDescriptorGroup("Image")
        self.documentation = "Uses the focal length from the image EXIF metadata."
        self._allowed_targets = Targets.filename


class ImageArtist(ActionDescriptor):
    def __init__(self):
        super().__init__("ImageArtist", ImageArtist)
        self.caption = "Artist"
        #self.group = ActionDescriptorGroup("Image")
        self.documentation = "Uses the artist from the image EXIF metadata."
        self._allowed_targets = Targets.filename


class MusicArtist(ActionDescriptor):
    def __init__(self):
        super().__init__("MusicArtist", MusicArtist)
        self.caption = "Artist"
        #self.group = ActionDescriptorGroup("Music")
        self.documentation = "Uses the artist from the metadata."
        self._allowed_targets = Targets.filename


class MusicTitle(ActionDescriptor):
    def __init__(self):
        super().__init__("MusicTitle", MusicTitle)
        self.caption = "Title"
        #self.group = ActionDescriptorGroup("Music")
        self.documentation = "Uses the title from the metadata."
        self._allowed_targets = Targets.filename


class MusicYear(ActionDescriptor):
    def __init__(self):
        super().__init__("MusicYear", MusicYear)
        self.caption = "Year"
        #self.group = ActionDescriptorGroup("Music")
        self.documentation = "Uses the album year from the metadata."
        self._allowed_targets = Targets.filename


class MusicAlbum(ActionDescriptor):
    def __init__(self):
        super().__init__("MusicAlbum", MusicAlbum)
        self.caption = "Album"
        #self.group = ActionDescriptorGroup("Music")
        self.documentation = "Uses the album name from the metadata."
        self._allowed_targets = Targets.filename


class MusicTrack(ActionDescriptor):
    def __init__(self):
        super().__init__("MusicTrack", MusicTrack)
        self.caption = "Track Number"
        #self.group = ActionDescriptorGroup("Music")
        self.documentation = "Uses the track name from the metadata."
        self._allowed_targets = Targets.filename


class MusicGenre(ActionDescriptor):
    def __init__(self):
        super().__init__("MusicGenre", MusicGenre)
        self.caption = "Genre"
        #self.group = ActionDescriptorGroup("Music")
        self.documentation = "Uses the music genre from the metadata."
        self._allowed_targets = Targets.filename


class ActionDescriptorGroup(object):
    """
    Contains a collection of ActionDescriptor.

    Args:
        caption (string): The caption of the group.
    """

    def __init__(self, caption):
        self._caption = caption

    @property
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self, value):
        self._caption = value

    def __repr__(self):
        """override string representation of the class"""
        return self.caption


class ParameterType(Enum):
    boolean = 0
    string = 1
    number = 2
    range = 3
    enum = 4


class ActionParameterDescriptor(object):
    """ Describes a parameter from an action.

    Args:
        name (string): A string that is the name given to the parameter from the action.
        parameter_type (ParameterType): Specifies the type of the given parameter.
    """

    def __init__(self, name, parameter_type):
        self._name = name
        self._parameter_type = parameter_type
        # Set the parameter name as default to caption.
        self._caption = name
        self._is_readonly = False
        self._is_visible = True
        self._documentation = ""
        self._default_value = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def parameter_type(self):
        return self._parameter_type

    @parameter_type.setter
    def parameter_type(self, value):
        self._parameter_type = value

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

    @property
    def default_value(self):
        return self._default_value

    @default_value.setter
    def default_value(self, value):
        self._default_value = value
