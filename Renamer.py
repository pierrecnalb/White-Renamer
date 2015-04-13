
#author : pierrecnalb
#copyright pierrecnalb
#v.1.0.2
import os
import time
import shutil
import sys
from os import walk
import operator
import copy
language = "english"

class FileDescriptor:
    """Group information related to the input files."""
    def __init__(self, path):
        self.path = path
        self.isfolder = True
        self.folder = None
        self.parents = None
        self.filename = None
        self.extension = None

    def is_folder(self):
        return os.path.isdir(self.path)

    def get_path(self):
        return self.path

    def get_parents(self):
        self.parents = os.path.dirname(self.path)
        return self.parents

    def get_basename(self):
        if (self.isfolder is False):
            (self.basename, self.extension) = os.path.splitext(self.basename)[0]
        else:
            self.basename = os.path.basename(self.path)
            self.extension = ""
        return self.basename, self.extension

class FilesCollection:
    def __init__(self, input_path, use_subdirectory):
        self.input_path = input_path
        self.use_subdirectory = use_subdirectory
        self.original_tree = self.scan(self.input_path)
        self.modified_tree = copy.deepcopy(self.original_tree)
        self.basename_tree = []

    def scan(self, path):
        """Create a nested list of FileDescriptor contained in the input directory."""
        """Example of list : [["FileDescriptor1,["SubFileDescriptor1,[]"]],["FileDescriptor2",[]]]."""
        tree = []
        children = os.listdir(path)
        for child in children:
            if os.path.isdir(os.path.join(path,child)):
                if (not self.use_subdirectory):
                    break
                tree.append([FileDescriptor(os.path.join(path,child)), self.scan(os.path.join(path,child))])
            else:
                tree.append([FileDescriptor(os.path.join(path,child)), []])
        return tree

    def get_files(self):
        return self.original_tree

    def get_basename_tree(self):
        self.basename_tree = self.parselist(self.modified_tree)
        return self.basename_tree

    def reset(self):
        self.modified_tree = copy.deepcopy(self.original_tree)
        return self.modified_tree

    def parselist(self, tree, dirpath = lambda filedescriptor:filedescriptor.get_basename()[0]):
        """"""
        for item in tree:
            item[0] = dirpath(item[0])
            if item[1] != []:
                self.parselist(item[1])
        return tree

    def call_actions(self, actions, tree):
        """"""
        for item in tree:
            if item[1] != []:
                self.call_actions(actions, item[1])
            for action in actions:
                item[0] = action.call(item[0])
        return tree

class ActionDescriptor:

    def __init__(self, action_name, action_inputs, action_class):
        self.action_name = action_name
        self.action_inputs = action_inputs
        self.action_class = action_class

    def __repr__(self):
        """override string representation of the class"""
        return self.action_name

class ActionInput:
    def __init__(self, arg_name, arg_caption, arg_type):
        self.argument_name = arg_name
        self.argument_caption = arg_caption
        self.argument_type = arg_type

class Action:
    def __init__(self, path_type):
        self.path_type = path_type

    def split_path(self, file_path):
        """Split the entire path into three part."""
        if (os.path.isdir(file_path) is False):
            (self.path, self.filename)=os.path.split(file_path)
            (self.file, self.extension) = os.path.splitext(self.filename)
        else:
            self.path = file_path
            self.file = ""
            self.extension = ""
        return self.path, self.file, self.extension

    def call(self, file_descriptor):
        """Apply action on the specified part."""
        file_path = file_descriptor.get_path()
        parents = file_descriptor.get_parents()
        (basename, extension) = file_descriptor.get_basename()
        prefix = ""
        suffix = ""
        if(self.path_type == "file"):
            return os.path.join(parents, self.call_on_path_part(file_path, basename)) + extension
        elif(self.path_type == "folder"):
            return os.path.join(parents, self.call_on_path_part(file_path, basename)) + extension
        elif(self.path_type == "prefix"):
            return os.path.join(parents, self.call_on_path_part(file_path, prefix)) + extension
        elif(self.path_type == "suffix"):
            return os.path.join(parents, basename + self.call_on_path_part(file_path, suffix)) + extension
        elif(self.path_type == "extension"):
            return os.path.join(parents, basename) + self.call_on_path_part(file_path, extension)
        else:
            raise Exception("path_part not valid")

    def call_on_path_part(self, file_path, path_part):
        raise Exception("not implemented")


class CharacterReplacementAction(Action):
    """Replace old_char by new_char in the section of the path."""
    """path_part can be 'folder', 'file', 'prefix', 'suffix' or 'extension'."""
    def __init__(self, path_type, old_char, new_char):
        Action.__init__(self, path_type)
        self.old_char = old_char
        self.new_char = new_char

    def call_on_path_part(self, file_path, path_part):
        return path_part.replace(self.old_char,self.new_char)

class OriginalName(Action):
    """Return the original name."""
    def __init__(self, path_type, untouched = False, uppercase = False, lowercase = False, titlecase = False):
        Action.__init__(self, path_type)
        self.untouched = untouched
        self.uppercase = uppercase
        self.lowercase = lowercase
        self.titlecase = titlecase

    def call_on_path_part(self, file_path, path_part):
        if self.uppercase is True:
            return path_part.upper()
        elif self.lowercase is True:
            return path_part.lower()
        elif self.titlecase is True:
            return ' '.join([name[0].upper() + name[1:] for name in path_part.split(' ')])
        else:
            return path_part

class CharacterInsertionAction(Action):
    """Insert new_char at index position."""
    def __init__(self, path_type, new_char, index):
        Action.__init__(self, path_type)
        self.new_char = new_char
        self.index = index

    def call_on_path_part(self, file_path, path_part):
        return path_part[:self.index] + self.new_char + path_part[self.index:]

class CharacterDeletionAction(Action):
    """Delete n-character starting from index position."""
    def __init__(self, path_type, number_of_char, index):
        Action.__init__(self, path_type)
        self.number_of_char = number_of_char
        self.index = index

    def call_on_path_part(self, file_path, path_part):
        return path_part[:self.index] + path_part[self.index + self.number_of_char :]

class CustomNameAction(Action):
    """Use a custom name in the filename."""
    def __init__(self, path_type, new_name):
        Action.__init__(self, path_type)
        self.new_name = new_name

    def call_on_path_part(self, file_path, path_part):
        return self.new_name

class FolderNameUsageAction(Action):
    """Use the parent foldername as the filename."""
    def __init__(self, path_type, untouched = False, uppercase = False, lowercase = False, titlecase = False):
        Action.__init__(self, path_type)
        self.untouched = untouched
        self.uppercase = uppercase
        self.lowercase = lowercase
        self.titlecase = titlecase

    def call_on_path_part(self, file_path, path_part):
        (path, file, extension) = self.split_path(file_path)
        foldername = path.rsplit(os.sep,1)[-1]
        if self.uppercase is True:
            return foldername.upper()
        elif self.lowercase is True:
            return foldername.lower()
        elif self.titlecase is True:
            return ' '.join([name[0].upper() + name[1:] for name in foldername.split(' ')])
        else:
            return foldername

class ModifiedTimeUsageAction(Action):
    """Use the modified time metadata as the filename."""
    def call(self, file_path):
        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(self.filenames)
        return time.ctime(mtime)

class Counter(Action):
    """Count the number of files starting from start_index with the given increment."""
    """If restart==True, the counter is set to startindex at each subfolder."""

    def __init__(self, path_type, start_index, increment, restart):
        Action.__init__(self, path_type)
        self.start_index = start_index
        self.increment = increment
        self.restart = restart
        self.counter = 0
        self.previous_path = ""

    def call_on_path_part(self, file_path, path_part):
        path, file, extension = self.split_path(file_path)
        if (path!=self.previous_path and self.restart is True):
            self.counter = self.start_index
        else:
            if(self.counter == 0):
                self.counter = self.start_index
            else:
                self.counter = self.counter + (1 * self.increment)
        self.previous_path=path
        return str(self.counter)

class PipeAction(Action):
    """Execute actions inside another action."""
    def __init__(self, path_type, main_action, sub_action):
        Action.__init__(self, path_type)
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
        action = self.main_action(self.path_part, **argumentValues)
        value = action.call_on_path_part(file_path, path_part)
        return value

