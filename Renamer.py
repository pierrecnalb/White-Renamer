
#author : pierrecnalb
#copyright pierrecnalb
#v.1.0.5
import os
import time
import shutil
import sys
from os import walk
import operator
import copy
import re
import shutil
import pdb
language = "english"

class FileDescriptor(object):
    """Group information related to the input files."""
    def __init__(self, input_path, is_dir):
        self._path = input_path
        self.is_folder = is_dir
        (self._parents, self._basename)=os.path.split(self._path)
        if (self.is_folder is False):
            (self._filename, self._extension) = os.path.splitext(self._basename)
            self._foldername = ""
        else:
            self._filename = ""
            self._foldername = self._basename
            self._extension = ""
        self._prefix = ""
        self._suffix = ""

    def is_folder(self):
        return self.is_folder

    @property
    def path(self):
        self.update_path()
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def parents(self):
        self.update_path()
        return self._parents

    @parents.setter
    def parents(self, value):
        self.update_path()
        self._parents = value

    @property
    def foldername(self):
        self.update_path()
        return self._foldername

    @foldername.setter
    def foldername(self, value):
        self._foldername = value
        self.update_path()

    @property
    def suffix(self):
        self.update_path()
        return self._suffix

    @suffix.setter
    def suffix(self, value):
        self.update_path()
        self._suffix = value

    @property
    def prefix(self):
        self.update_path()
        return self._prefix

    @prefix.setter
    def prefix(self, value):
        self.update_path()
        self._prefix = value

    @property
    def filename(self):
        self.update_path()
        return self._filename

    @filename.setter
    def filename(self, value):
        self.update_path()
        self._filename = value

    @property
    def extension(self):
        self.update_path()
        return self._extension

    @extension.setter
    def extension(self, value):
        self._extension = value
        self.update_path()

    @property
    def basename(self):
        if self.is_folder is True:
            self._basename = self._foldername
        else:
            self._basename = self._prefix + self._filename + self._suffix + self._extension
        return self._basename

    @basename.setter
    def basename(self, value):
        self._basename = value
        self.update_path()

    def update_path(self):
        if self.is_folder is True:
            self._path = os.path.join(self._parents, self._foldername)
        else:
            self._path = os.path.join(self._parents, self._foldername, (self._prefix + self._filename + self._prefix)) + self._extension

class FileSystemTree(object):
    def __init__(self, rootPath):
        self.root = FileSystemTreeNode()

class FileSystemTreeNode(object):
    """Contains the original and modified FileDescriptor for a given node of the selected directory.
    The structure of the system tree node is reproduced by adding children for each subdirectory."""
    def __init__(self, original_path, is_dir):
        self.children = []
        self._original_path = FileDescriptor(original_path, is_dir)
        self._modified_path = copy.deepcopy(self._original_path)
        self.is_dir = is_dir

    def add_children(self, file_system_tree_node):
        self.children.append(file_system_tree_node)
        return file_system_tree_node

    def get_children(self):
        return self.children
        
    @property
    def original_filedescriptor(self):
        return self._original_path

    @property
    def modified_filedescriptor(self):
        return self._modified_path

    @modified_filedescriptor.setter
    def modified_filedescriptor(self, value):
        self._modified_path = value
 
class FilesCollection(object):
    def __init__(self, input_path, use_subdirectory, show_hidden_files):
        self.input_path = input_path
        self.use_subdirectory = use_subdirectory
        self.show_hidden_files = show_hidden_files
        self.file_system_tree_node = FileSystemTreeNode(self.input_path, True)
        self.scan(self.file_system_tree_node)

    def scan(self, file_system_tree_node):
        """Create a nested list of FileSystemTreeNode containing original and modified FileDescriptor."""
        #pdb.set_trace()
        path = file_system_tree_node.original_filedescriptor.path
        children = sorted(os.listdir(path))
        for child in children:
            #Check for hidden files
            if child[0] == '.' and not self.show_hidden_files:
                continue
            if os.path.isdir(os.path.join(path,child)):
                file_system_child_node = FileSystemTreeNode(os.path.join(path,child), True)
                file_system_tree_node.add_children(file_system_child_node)
                if (not self.use_subdirectory):
                    continue
                else:
                    self.scan(file_system_child_node)
            else:
                file_system_child_node = FileSystemTreeNode(os.path.join(path,child), False)
                file_system_tree_node.add_children(file_system_child_node)

    def get_file_system_tree_node(self):
        return self.file_system_tree_node

    def get_original_files(self):
        return self.original_tree

    def list_children(self, tree_node):
        children = tree_node.get_children()
        if children:
            for child in tree_node.get_children():
                print(child.original_filedescriptor.basename)
                self.list_children(child)
        else:
            print(tree_node.original_filedescriptor.basename)
            
    def reset(self, tree_node):
        tree_node.modified_filedescriptor = copy.deepcopy(tree_node.original_filedescriptor)
        return self.tree_node

    def execute_method_on_node(self, tree_node, method, *optional_argument):
        method(tree_node, *optional_argument)
        for child in tree_node.get_children():
            self.execute_method_on_node(child, method, *optional_argument)
    
    def call_actions(self, tree_node, actions):
        #self.execute_method_on_node(tree_node, self.reset)
        for action in actions:
            tree_node.modified_filedescriptor = action.call(tree_node.modified_filedescriptor)
        print(tree_node.modified_filedescriptor.basename)
    #def parselist(self, tree, path_section):
    #    """"""
    #    for item in tree:
    #        if item[1] != []:
    #            self.parselist(item[1], path_section)
    #        item[0] = path_section(item[0])
    #    return tree

    #def call_actions(self, actions, tree):
    #    """"""
    #    for item in tree:
    #        if item[1] != []:
    #            self.call_actions(actions, item[1])
    #        for action in actions:
    #            item[0] = action.call(item[0])
    #    return tree

    def rename(self, original_tree, modified_tree):
        for i in range(len(modified_tree)):
            if modified_tree[i][1] != []:
                self.rename(original_tree[i][1], modified_tree[i][1])
            shutil.move(original_tree[i][0].path,modified_tree[i][0].path)
            original_tree[i][0] = copy.deepcopy(modified_tree[i][0])

class ActionDescriptor:

    def __init__(self, action_name, action_inputs, action_class):
        self.action_name = action_name
        self.action_inputs = action_inputs
        self.action_class = action_class

    def __repr__(self):
        """override string representation of the class"""
        return self.action_name

class ActionInput:
    def __init__(self, arg_name, arg_caption, arg_type, default_value):
        self.argument_name = arg_name
        self.argument_caption = arg_caption
        self.argument_type = arg_type
        self.default_value = default_value

class Action:
    def __init__(self, path_type):
        self.path_type = path_type

    def call(self, file_descriptor):
        """Apply action on the specified part."""
        prefix = ""
        suffix = ""
        if(self.path_type == "file"):
            file_descriptor.filename = self.call_on_path_part(file_descriptor, file_descriptor.filename)
            return file_descriptor
        elif(self.path_type == "folder"):
            file_descriptor.foldername = self.call_on_path_part(file_descriptor, file_descriptor.foldername)
            return file_descriptor
        elif(self.path_type == "suffix"):
            file_descriptor.suffix = file_descriptor.suffix + self.call_on_path_part(file_descriptor, file_descriptor.suffix)
            return file_descriptor
        elif(self.path_type == "prefix"):
            file_descriptor.prefix = self.call_on_path_part(file_descriptor, file_descriptor.prefix) + file_descriptor.prefix
            return file_descriptor
        elif(self.path_type == "extension"):
            file_descriptor.extension = self.call_on_path_part(file_descriptor, file_descriptor.extension)
            return file_descriptor
        else:
            raise Exception("path_part not valid")

    def call_on_path_part(self, file_descriptor, path_part):
        raise Exception("not implemented")


class CharacterReplacementAction(Action):
    """Replace old_char by new_char in the section of the path."""
    """path_part can be 'folder', 'file', 'prefix', 'suffix' or 'extension'."""
    def __init__(self, path_type, old_char, new_char):
        Action.__init__(self, path_type)
        self.old_char = old_char
        self.new_char = new_char

    def call_on_path_part(self, file_descriptor, path_part):
        return path_part.replace(self.old_char,self.new_char)

class OriginalName(Action):
    """Return the original name."""
    def __init__(self, path_type, untouched = True, uppercase = False, lowercase = False, titlecase = False):
        Action.__init__(self, path_type)
        self.untouched = untouched
        self.uppercase = uppercase
        self.lowercase = lowercase
        self.titlecase = titlecase

    def titlecase_converter(self, string, exceptions):
       words = re.split(' ', string)
       words_converted = [words[0].capitalize()]
       exceptions = ['a', 'an', 'of', 'the', 'is']
       for word in words[1:]:
          words_converted.append(word in exceptions and word or word.capitalize())
       return " ".join(words_converted)

    def call_on_path_part(self, file_descriptor, path_part):
        if self.uppercase is True:
            return path_part.upper()
        elif self.lowercase is True:
            return path_part.lower()
        elif self.titlecase is True:
            return self.titlecase_converter(path_part, "exceptions")
        else:
            return path_part

class CharacterInsertionAction(Action):
    """Insert new_char at index position."""
    def __init__(self, path_type, new_char, index):
        Action.__init__(self, path_type)
        self.new_char = new_char
        self.index = index

    def call_on_path_part(self, file_descriptor, path_part):
        return path_part[:self.index] + self.new_char + path_part[self.index:]

class CharacterDeletionAction(Action):
    """Delete n-character starting from index position."""
    def __init__(self, path_type, number_of_char, index):
        Action.__init__(self, path_type)
        self.number_of_char = number_of_char
        self.index = index

    def call_on_path_part(self, file_descriptor, path_part):
        return path_part[:self.index] + path_part[self.index + self.number_of_char :]

class CustomNameAction(Action):
    """Use a custom name in the filename."""
    def __init__(self, path_type, new_name):
        Action.__init__(self, path_type)
        self.new_name = new_name

    def call_on_path_part(self, file_descriptor, path_part):
        return self.new_name

class FolderNameUsageAction(Action):
    """Use the parent foldername as the filename."""
    def __init__(self, path_type, untouched = False, uppercase = False, lowercase = False, titlecase = False):
        Action.__init__(self, path_type)
        self.untouched = untouched
        self.uppercase = uppercase
        self.lowercase = lowercase
        self.titlecase = titlecase

    def call_on_path_part(self, file_descriptor, path_part):
        (path, folder) = os.path.split(file_descriptor.parents)
        if self.uppercase is True:
            return folder.upper()
        elif self.lowercase is True:
            return folder.lower()
        elif self.titlecase is True:
            return ' '.join([name[0].upper() + name[1:] for name in folder.split(' ')])
        else:
            return folder

class ModifiedTimeUsageAction(Action):
    """Use the modified time metadata as the filename."""
    def call(self, file_descriptor):
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
        self.previous_parents = ""

    def call_on_path_part(self, file_descriptor, path_part):
        if (file_descriptor.parents!=self.previous_parents and self.restart is True):
            self.counter = self.start_index
        else:
            if(self.counter == 0):
                self.counter = self.start_index
            else:
                self.counter = self.counter + (1 * self.increment)
        self.previous_parents=file_descriptor.parents
        return str(self.counter)

class PipeAction(Action):
    """Execute actions inside another action."""
    def __init__(self, path_type, main_action, sub_action):
        Action.__init__(self, path_type)
        self.main_action = main_action
        self.sub_action = sub_action

    def call_on_path_part(self, file_descriptor, path_part):
        # Execute all left hand side actions to get argument values for the
        # action to execute.
        argumentValues = {}
        for argument_name, argument_provider in self.sub_action.items():
            if isinstance(argument_provider, Action):
                argumentValues[argument_name] = argument_provider.call_on_path_part(file_descriptor, path_part)
            else:
                argumentValues[argument_name] = argument_provider
        # Prepare right hand side for this file.
        action = self.main_action(self.path_part, **argumentValues)
        value = action.call_on_path_part(file_descriptor, path_part)
        return value
##def method(arg):
#    print(arg)
#filesystem = FilesCollection("/home/pierre/Documents/Programs/White-Renamer/test/Test Directory", True, False)
#files = filesystem.get_file_system_tree_node()
#filesystem.execute_method_on_node(files , filesystem.call_actions)

