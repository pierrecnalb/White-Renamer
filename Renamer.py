#author : pierrecnalb
#copyright pierrecnalb
#v.1.0.1
import os
import time
import shutil
import sys
from os import walk
import operator
import PySide
from PySide.QtCore import *
from PySide.QtGui  import *
language = "english"

class FilesCollection:
    def __init__(self, input_path, use_subdirectory):
        self.input_path = input_path
        self.use_subdirectory = use_subdirectory
        self.original_files_paths = []
        self.modified_files_paths = []
        for(dirpath, dirnames, filenames) in walk(self.input_path):
            for filename in filenames:
                self.original_files_paths.append(os.path.join(dirpath,filename))
            if (not use_subdirectory):
                break

    def get_files_list(self):
        return {'old' : self.original_files_paths, 'new' : self.modified_files_paths}

    def call_actions(self, actions):
        for old_file_path in self.original_files_paths:
            new_file_path = old_file_path
            for action in actions:
                new_file_path = action.call(new_file_path)
            self.modified_files_paths.append(new_file_path)
        return self.modified_files_paths

class ActionDescriptor:
    def __init__(self, action_name, action_inputs, action_class):
        self.action_name = action_name
        self.action_inputs = action_inputs
        self.action_class = action_class

    def __repr__(self):
        """override string representation of the class"""
        return self.action_name

class ActionInput:
    def __init__(self, argName, arg_caption, argType):
        self.argumentName = argName
        self.argumentCaption = arg_caption
        self.argumentType = argType

class Action:
    def __init__(self, path_section):
        self.path_section = path_section

    def split_path(self, file_path):
        """Split the entire path into three part."""
        (self.path, self.filename)=os.path.split(file_path)
        (self.shortname, self.extension) = os.path.splitext(self.filename)
        return self.path, self.shortname, self.extension

    def call(self, file_path):
        """Apply action on the specified part."""
        path, shortname, extension = self.split_path(file_path)
        #mode = "path|shortname"
        #flags = mode.split("|")
        #if ("shortname" in flags):
        #    pass
        if(self.path_section == "shortname"):
            return os.path.join(path, self.call_on_path_part(file_path, shortname)) + extension
        elif(self.path_section == "path"):
            return os.path.join(self.call_on_path_part(file_path, path), shortname) + extension
        elif(self.path_section == "extension"):
            return os.path.join(path, shortname) + self.call_on_path_part(file_path, extension)
        else:
            raise Exception("path_section not valid")

    def call_on_path_part(self, file_path, path_part):
        raise Exception("not implemented")


class CharacterReplacementAction(Action):
    """Replace old_char by new_char in the section of the path."""
    """Path_section can be 'path', 'shortname' or 'extension'."""
    def __init__(self, path_section, old_char, new_char):
        Action.__init__(self, path_section)
        self.old_char = old_char
        self.new_char = new_char

    def call_on_path_part(self, file_path, path_part):
        return path_part.replace(self.old_char,self.new_char)

class OriginalName(Action):
    """Return the original name."""

    def call_on_path_part(self, file_path, path_part):
        return path_part

class CharacterInsertionAction(Action):
    """Insert new_char at index position."""
    def __init__(self, path_section, new_char, index):
        Action.__init__(self, path_section)
        self.new_char = new_char
        self.index = index

    def call_on_path_part(self, file_path, path_part):
        return path_part[:self.index] + self.new_char + path_part[self.index:]

class CharacterDeletionAction(Action):
    """Delete n-character starting from index position."""
    def __init__(self, path_section, number_of_char, index):
        Action.__init__(self, path_section)
        self.number_of_char = number_of_char
        self.index = index

    def call_on_path_part(self, file_path, path_part):
        return path_part[:self.index] + path_part[self.index + self.number_of_char :]

class UppercaseConversionAction(Action):
    """Convert the string to UPPERCASE."""
    INPUTS = []
    def call_on_path_part(self, file_path, path_part):
        return path_part.upper()

class LowercaseConversionAction(Action):
    """Convert the string to lowercase."""
    INPUTS = []
    def call_on_path_part(self, file_path, path_part):
        return path_part.lower()

class TitlecaseConversionAction(Action):
    """Convert the string to Title Case."""
    INPUTS = []
    def call_on_path_part(self, file_path, path_part):
        if language=="english":
            return ' '.join([name[0].upper()+name[1:] for name in path_part.split(' ')])
        elif language=="french":
            return path_part.title()

class CustomNameAction(Action):
    """Use a custom name in the filename."""
    def __init__(self, path_section, new_name):
        Action.__init__(self, path_section)
        self.new_name = new_name

    def call_on_path_part(self, file_path, path_part):
        return self.new_name

class FolderNameUsageAction(Action):
    """Use the parent foldername as the filename."""

    def call_on_path_part(self, file_path, path_part):
        (path, shortname, extension) = self.split_path(file_path)
        return path.rsplit(os.sep,1)[-1]

class ModifiedTimeUsageAction(Action):
    """Use the modified time metadata as the filename."""
    def call(self, file_path):
        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(self.filenames)
        return time.ctime(mtime)

class Counter(Action):
    """Count the number of files starting from start_index with the given increment."""
    """If restart==True, the counter is set to startindex at each subfolder."""
    COUNTER = 0
    PREVIOUS_PATH = ""

    def __init__(self, path_section, start_index, increment, restart):
        Action.__init__(self, path_section)
        self.start_index = start_index
        self.increment = increment
        self.restart = restart

    def call_on_path_part(self, file_path, path_part):
        path, shortname, extension = self.split_path(file_path)
        if (path!=Counter.PREVIOUS_PATH and self.restart is True):
            Counter.COUNTER = self.start_index
        else:
            if(Counter.COUNTER == 0):
                Counter.COUNTER = self.start_index
            else:
                Counter.COUNTER = Counter.COUNTER + (1 * self.increment)
        Counter.PREVIOUS_PATH=path
        return str(Counter.COUNTER)

class PipeAction(Action):
    """Execute actions inside another action."""
    def __init__(self, path_section, main_action, sub_action):
        Action.__init__(self, path_section)
        self.main_action = main_action
        self.sub_action = sub_action

    def call_on_path_part(self, file_path, path_part):
        # Execute all left hand side actions to get argument values for the
        # action to execute.
        argumentValues = {}
        for argument_name, argument_provider in self.sub_action.items():
            if isinstance(argument_provider, Action):
                argumentValues[argument_name] = argument_provider.call_on_path_part(file_path, path_part)
            else:
                argumentValues[argument_name] = argument_provider
        # Prepare right hand side for this file.
        action = self.main_action(self.path_section, **argumentValues)
        value = action.call_on_path_part(file_path, path_part)
        return value

    #directory = "/home/pierre/Desktop/test"
    #files = FilesCollection(directory, False)
    #actions=[]
   ## action_dict = {'UPPERCASE' : UppercaseConversionAction("shortname")}
    #actionClass = CharacterInsertionAction
    #value_searched_in_UI = {'new_char':"test", 'index' : 0}
    #actionArgs = {}
    #for input in actionClass.INPUTS:
    #    actionArgs[input.argumentName] = value_searched_in_UI[input.argumentName]#valeurquejevaischercherqqpartdanslui
    ##Action.createAction(actionClass, 'shortnmae', **actionArgs) methode statique a implementer
    #actionInstance = actionClass('shortname', **actionArgs)
    #actions.append(actionInstance)
    ##print(files.call_actions(actions))

