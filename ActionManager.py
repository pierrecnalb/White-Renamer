#author : pierrecnalb
#copyright pierrecnalb
import os
import time
import re
import pdb
import exifread
from mutagen.easyid3 import EasyID3

class ActionDescriptorGroup(object):
    """
    Contains a collectino of ActionDescriptor.
    Parameters:
        --action_descriptors: a list of ActionDescriptor.
    """
    def __init__(self, action_name, action_descriptors, action_class):
        self.action_name = action_name
        self.action_descriptors = action_descriptors
        self.action_class = action_class

    def __repr__(self):
        """override string representation of the class"""
        return self.action_name

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
    def __init__(self, arg_name, arg_caption, arg_type, default_value, optional_argument = None):
        self.argument_name = arg_name
        self.argument_caption = arg_caption
        self.argument_type = arg_type
        self.default_value = default_value
        self.optional_argument = optional_argument

class Action(object):
    """
    Describes how the action is applied on the FileSystemTreeNodes. This class is inherited by all the specific actions.
    Parameters:
        --path_type: string that represents where the action will be applied. path_type can be 'folder', 'file', 'prefix', 'suffix' or 'extension'.
        --file_or_folder: specifies where to apply the actions : to the files or the folders.
    """
    def __init__(self, path_type):
        self.path_type = path_type

    def call(self, file_system_tree_node, file_or_folder):
        """Apply action on the specified part."""
        prefix = ""
        suffix = ""
        if (file_or_folder == "folder"):
            if (file_system_tree_node.is_folder):
                if(self.path_type == "folder"):
                        file_system_tree_node.modified_filedescriptor.foldername = self.call_on_path_part(file_system_tree_node, file_system_tree_node.modified_filedescriptor.foldername)
                elif(self.path_type == "suffix"):
                        file_system_tree_node.modified_filedescriptor.suffix = file_system_tree_node.modified_filedescriptor.suffix + self.call_on_path_part(file_system_tree_node, file_system_tree_node.modified_filedescriptor.suffix)
                elif(self.path_type == "prefix"):
                        file_system_tree_node.modified_filedescriptor.prefix = file_system_tree_node.modified_filedescriptor.prefix + self.call_on_path_part(file_system_tree_node, file_system_tree_node.modified_filedescriptor.prefix)
                elif(self.path_type == "extension"):
                    return file_system_tree_node
                else:
                    raise Exception("path_type not valid")

        elif (file_or_folder == "file"):
            if (file_system_tree_node.is_folder is False):
                if(self.path_type == "file"):
                        file_system_tree_node.modified_filedescriptor.filename = self.call_on_path_part(file_system_tree_node, file_system_tree_node.modified_filedescriptor.filename)
                elif(self.path_type == "suffix"):
                        file_system_tree_node.modified_filedescriptor.suffix = file_system_tree_node.modified_filedescriptor.suffix + self.call_on_path_part(file_system_tree_node, file_system_tree_node.modified_filedescriptor.suffix)
                elif(self.path_type == "prefix"):
                        file_system_tree_node.modified_filedescriptor.prefix = file_system_tree_node.modified_filedescriptor.prefix + self.call_on_path_part(file_system_tree_node, file_system_tree_node.modified_filedescriptor.prefix)
                elif(self.path_type == "extension"):
                    file_system_tree_node.modified_filedescriptor.extension = self.call_on_path_part(file_system_tree_node, file_system_tree_node.modified_filedescriptor.extension)
                else:
                    raise Exception("path_type not valid")
        return file_system_tree_node

    def call_on_path_part(self, file_system_tree_node, path_part):
        raise Exception("not implemented")



class CharacterReplacementAction(Action):
    """
    Replace old_char by new_char in the section of the path.
    path_part can be 'folder', 'file', 'prefix', 'suffix' or 'extension'.
    """
    def __init__(self, path_type, old_char, new_char, regex):
        Action.__init__(self, path_type)
        self.old_char = old_char
        self.new_char = new_char
        self.regex = regex

    def call_on_path_part(self, file_system_tree_node, path_part):
        if not self.regex:
            return path_part.replace(self.old_char,self.new_char)
        else:
            return re.sub(self.old_char, self.new_char, path_part)

class OriginalNameAction(Action):
    """Gets the original name."""
    def __init__(self, path_type):
        Action.__init__(self, path_type)

    def call_on_path_part(self, file_system_tree_node, path_part):
        return path_part

class CaseChangeAction(Action):
    """
    Return the original name with a chosen casing option.
    Parameters:
        --case_choise: option to specify the case : 'uppercase', 'lowercase', 'titlecase'.
        --first_letter: boolean making first letter uppercase or lowercase.
        --after_symbols: list of symbols after which the letters are capitalized.
    """
    def __init__(self, path_type):
        Action.__init__(self, path_type)

    def call_on_path_part(self, file_system_tree_node, path_part):
        return path_part

class TitleCaseAction(CaseChangeAction):
    """
    Return the original name with a chosen casing option.
    Parameters:
        --case_choise: option to specify the case : 'uppercase', 'lowercase', 'titlecase'.
        --first_letter: boolean making first letter uppercase or lowercase.
        --after_symbols: list of symbols after which the letters are capitalized.
    """
    def __init__(self, path_type, first_letter = True, after_symbols = ""):
        CaseChangeAction.__init__(self, path_type)
        self.first_letter = first_letter
        self.after_symbols = after_symbols

    def make_upper_first_letters(self, string):
        special_char_position = []
        stringlist = list(string)
        for i, char in enumerate(stringlist):
            if char in self.after_symbols:
                special_char_position.append(i+1)
        for position in special_char_position:
            if position < len(stringlist):
                stringlist[position] = stringlist[position].upper()
        return ''.join(stringlist)

    def call_on_path_part(self, file_system_tree_node, path_part):
       path_part = self.make_upper_first_letters(path_part)
       if self.first_letter:
           path_part = path_part[0].upper() + path_part[1:]
       return path_part

class UpperCaseAction(CaseChangeAction):
    """
    Return the original name with a chosen casing option.
    Parameters:
        --case_choise: option to specify the case : 'uppercase', 'lowercase', 'titlecase'.
        --first_letter: boolean making first letter uppercase or lowercase.
        --after_symbols: list of symbols after which the letters are capitalized.
    """
    def __init__(self, path_type, first_letter = True, after_symbols = ""):
        CaseChangeAction.__init__(self, path_type)

    def call_on_path_part(self, file_system_tree_node, path_part):
       return path_part.upper()

class LowerCaseAction(CaseChangeAction):
    """
    Return the original name with a chosen casing option.
    Parameters:
        --case_choise: option to specify the case : 'uppercase', 'lowercase', 'titlecase'.
        --first_letter: boolean making first letter uppercase or lowercase.
        --after_symbols: list of symbols after which the letters are capitalized.
    """
    def __init__(self, path_type, first_letter = True, after_symbols = ""):
        CaseChangeAction.__init__(self, path_type)

    def call_on_path_part(self, file_system_tree_node, path_part):
        return path_part.lower()

class CharacterInsertionAction(Action):
    """Insert new_char at index position."""
    def __init__(self, path_type, new_char, index):
        Action.__init__(self, path_type)
        self.new_char = new_char
        self.index = index

    def call_on_path_part(self, file_system_tree_node, path_part):
        return path_part[:self.index] + self.new_char + path_part[self.index:]

class CharacterDeletionAction(Action):
    """Delete n-character from starting_position to ending_position."""
    def __init__(self, path_type, starting_position, ending_position):
        Action.__init__(self, path_type)
        self.starting_position = starting_position
        self.ending_position = ending_position

    def call_on_path_part(self, file_system_tree_node, path_part):
        if self.starting_position > self.ending_position:
            raise Exception("Starting position cannot be higher than ending position.")
        return path_part[:self.starting_position] + path_part[self.ending_position:]

class CustomNameAction(Action):
    """Use a custom name in the filename."""
    def __init__(self, path_type, new_name):
        Action.__init__(self, path_type)
        self.new_name = new_name

    def call_on_path_part(self, file_system_tree_node, path_part):
        return self.new_name

class FolderNameUsageAction(Action):
    """Use the parent foldername as the filename."""
    def __init__(self, path_type):
        Action.__init__(self, path_type)

    def call_on_path_part(self, file_system_tree_node, path_part):
        folder = file_system_tree_node.get_parent().original_filedescriptor.basename
        return folder

class DateAction(Action):
    """
    Use the created or modified date metadata as the filename.
    If is_modified_time = True, the modified date from the file metadata is taken. Otherwise, it is the created date.
    Commonly used format_display are :
    %Y  Year with century as a decimal number.
    %m  Month as a decimal number [01,12].
    %d  Day of the month as a decimal number [01,31].
    %H  Hour (24-hour clock) as a decimal number [00,23].
    %M  Minute as a decimal number [00,59].
    %S  Second as a decimal number [00,61].
    %z  Time zone offset from UTC.
    %a  Locale's abbreviated weekday name.
    %A  Locale's full weekday name.
    %b  Locale's abbreviated month name.
    %B  Locale's full month name.
    %c  Locale's appropriate date and time representation.
    %I  Hour (12-hour clock) as a decimal number [01,12].
    %p  Locale's equivalent of either AM or PM.
    """
    def __init__(self, path_type, is_modified_date = False, is_created_date = True, format_display = '%Y'):
        Action.__init__(self, path_type)
        self.is_modified_date = is_modified_date
        self.is_created_date = is_created_date
        self.format_display = format_display

    def call_on_path_part(self, file_system_tree_node, path_part):
        if self.is_modified_date:
            file_date = os.path.getmtime(file_system_tree_node.get_original_path())
        elif self.is_created_date:
            file_date = os.path.getctime(file_system_tree_node.get_original_path())
        return time.strftime(self.format_display, time.localtime(file_date))

class Counter(Action):
    """Count the number of files starting from start_index with the given increment."""
    def __init__(self, path_type, start_index, increment):
        Action.__init__(self, path_type)
        self.start_index = start_index
        self.increment = increment

    def call_on_path_part(self, file_system_tree_node, path_part):
        counter = file_system_tree_node.rank
        counter *= self.increment
        counter += self.start_index
        return str(counter)

class GenericImageAction(Action):
    def __init__(self, path_type, metadata):
        Action.__init__(self, path_type)
        self.metadata = metadata

    def format_output(self, output):
            return output

    def call_on_path_part(self, file_system_tree_node, path_part):
        try:
            f = open(file_system_tree_node.get_original_path(), 'rb')
            tags = exifread.process_file(f, details=False, stop_tag=self.metadata)
            path_part = tags[self.metadata].values
            return format_output(path_part)
        except:
            return path_part
        
class ImageDateTimeOriginal(GenericImageAction):
    def __init__(self, path_type):#, time_format):
   #     self.time_format = time_format
        GenericImageAction.__init__(self, path_type, 'EXIF DateTimeOriginal')

##    def format_output(path_part)
##        time.strftime(self.time_format, time.localtime(path_part))

class ImageFNumber(GenericImageAction):
    def __init__(self, path_type):
        GenericImageAction.__init__(self, path_type, 'EXIF FNumber')
        
    def format_output(path_part):
        return path_part[0].num/path_part[0].den

class ImageExposureTime(GenericImageAction):
    def __init__(self, path_type):
        GenericImageAction.__init__(self, path_type, 'EXIF ExposureTime')

    def format_output(path_part):
        return path_part[0].num/path_part[0].den

class ImageISO(GenericImageAction):
    def __init__(self, path_type):
        GenericImageAction.__init__(self, path_type, 'EXIF ISOSpeedRatings')

    def format_output(path_part):
        return path_part[0]

class ImageCameraModel(GenericImageAction):
    def __init__(self, path_type):
        GenericImageAction.__init__(self, path_type, 'Image Model')

class ImageXDimension(GenericImageAction):
    def __init__(self, path_type):
        GenericImageAction.__init__(self, path_type, 'EXIF ExifImageWidth')
    def format_output(path_part):
        return path_part[0]

class ImageYDimension(GenericImageAction):
    def __init__(self, path_type):
        GenericImageAction.__init__(self, path_type, 'EXIF Exif ExifImageLength')
    def format_output(path_part):
        return path_part[0]

class ImageFocalLength(GenericImageAction):
    def __init__(self, path_type):
        GenericImageAction.__init__(self, path_type, 'EXIF FocalLength')
    def format_output(path_part):
        return path_part[0]

class ImageArtist(GenericImageAction):
    def __init__(self, path_type):
        GenericImageAction.__init__(self, path_type, 'Image Artist')





class GenericMusicAction(Action):
    def __init__(self, path_type, metadata):
        Action.__init__(self, path_type)
        self.metadata = metadata

    def call_on_path_part(self, file_system_tree_node, path_part):
        try:
            audio = EasyID3(file_system_tree_node.get_original_path())
            return ', '.join(audio[self.metadata])
        except:
            return path_part

class MusicArtist(GenericMusicAction):
    def __init__(self, path_type):
        GenericImageAction.__init__(self, path_type, 'artist')
class MusicTitle(GenericMusicAction):
    def __init__(self, path_type):
        GenericImageAction.__init__(self, path_type, 'title')
class MusicYear(GenericMusicAction):
    def __init__(self, path_type):
        GenericImageAction.__init__(self, path_type, 'date')
class MusicAlbum(GenericMusicAction):
    def __init__(self, path_type):
        GenericImageAction.__init__(self, path_type, 'album')
class MusicTrack(GenericMusicAction):
    def __init__(self, path_type):
        GenericImageAction.__init__(self, path_type, 'tracknumber')
class MusicGenre(GenericMusicAction):
    def __init__(self, path_type):
        GenericImageAction.__init__(self, path_type, 'genre')

