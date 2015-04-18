
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
    def __init__(self, input_path):
        self.path = input_path
        self.is_folder = os.path.isdir(self.path)
        (self.parents, basename)=os.path.split(self.path)
        if (self.is_folder is False):
            (self.basename, self.extension) = os.path.splitext(basename)
            self.filename = self.basename
            self.foldername = ""
        else:
            self.filename = ""
            self.basename = basename
            self.foldername = self.basename
            self.extension = ""

    def is_folder(self):
        return self.is_folder

    def _get_path(self):
        self.update_path()
        return self.path

    def _set_path(self, new_path):
        self.path = new_path
        return self.path

    def _get_parents(self):
        self.update_path()
        return self.parents

    def _set_parents(self, new_parents):
        self.parents = new_parents
        self.update_path()
        return self.parents

    def _get_foldername(self):
        self.update_path()
        return self.foldername

    def _set_foldername(self, new_foldername):
        self.foldername = new_foldername
        self.update_path()
        return self.foldername

    def _get_filename(self):
        self.update_path()
        return self.filename

    def _set_filename(self, new_filename):
        self.filename = new_filename
        self.update_path()
        return self.filename

    def _get_extension(self):
        self.update_path()
        return self.extension

    def _set_extension(self, new_extension):
        self.extension = new_extension
        self.update_path()
        return self.extension

    def _get_basename(self):
        self.update_path()
        return self.basename

    def update_path(self):
        self.path = os.path.join(self.parents, self.foldername, self.filename) + self.extension

    def _set_basename(self, new_basename):
        self.basename = new_basename
        self.update_path()
        return self.basename

    #list of properties
    entire_path = property(_get_path, _set_path)
    parents = property(_get_parents, _set_parents)
    basename = property(_get_basename, _set_basename)
    extension = property(_get_extension, _set_extension)
    filename = property(_get_filename, _set_filename)
    foldername = property(_get_foldername, _set_foldername)

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
        self.basename_tree = []
        self.basename_tree = self.parselist(self.modified_tree, path_section = lambda file_descriptor:file_descriptor.basename)
        return self.basename_tree

    def reset(self):
        self.modified_tree = copy.deepcopy(self.original_tree)
        return self.modified_tree

    def parselist(self, tree, path_section):
        """"""
        for item in tree:
            item[0] = path_section(item[0])
            if item[1] != []:
                self.parselist(item[1], path_section)
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
        parents = file_descriptor.parents
        basename = file_descriptor.basename
        extension = file_descriptor.extension
        prefix = ""
        suffix = ""
        if(self.path_type == "file"):
            file_descriptor.filename = self.call_on_path_part(file_descriptor, file_descriptor.filename)
            return file_descriptor
        elif(self.path_type == "folder"):
            file_descriptor.foldername = self.call_on_path_part(file_descriptor, file_descriptor.foldername)
            return file_descriptor
        elif(self.path_type == "prefix"):
            file_descriptor.filename = file_descriptor.filename + self.call_on_path_part(file_descriptor, prefix)
            return file_descriptor
        elif(self.path_type == "suffix"):
            file_descriptor.filename = self.call_on_path_part(file_descriptor, suffix) + file_descriptor.filename
            return file_descriptor
        elif(self.path_type == "extension"):
            file_descriptor.extension = self.call_on_path_part(file_descriptor, file_descriptor.extension)
            return file_descriptor
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

    def call_on_path_part(self, file_descriptor, path_part):
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

