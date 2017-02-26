#!/usr/bin/python3

import action_descriptor


class ActionFactory(object):

    def CreateAction(name):
        action_descriptor.OriginalNameActionDescriptor()

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
