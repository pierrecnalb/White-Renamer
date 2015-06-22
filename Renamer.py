
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
        (self._parent, self._basename)=os.path.split(self._path)
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
    def parent(self):
        self.update_path()
        return self._parent

    @parent.setter
    def parent(self, value):
        self.update_path()
        self._parent = value

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
            self._path = os.path.join(self._parent, self._foldername)
        else:
            self._path = os.path.join(self._parent, self._foldername, (self._prefix + self._filename + self._suffix)) + self._extension

class FileSystemTreeNode(object):
    """Contains the original and modified FileDescriptor for a given node of the selected directory.
    The structure of the system tree node is reproduced by adding children for each subdirectory."""
    def __init__(self, original_path, is_dir, rank = 0, parent=None):
        self.children = []
        self.parent = parent
        self._original_path = FileDescriptor(original_path, is_dir)
        self._modified_path = copy.deepcopy(self._original_path)
        self._backup_path = copy.deepcopy(self._original_path)
        self.is_dir = is_dir
        self._rank = rank

    def add_children(self, file_system_tree_node):
        self.children.append(file_system_tree_node)
        self._rank = len(self.children) 
        return file_system_tree_node

    def get_children(self):
        return self.children
        
    def get_parent(self):
        return self.parent

    @property
    def original_filedescriptor(self):
        return self._original_path

    @original_filedescriptor.setter
    def original_filedescriptor(self, value):
        self._original_path = value

    @property
    def modified_filedescriptor(self):
        return self._modified_path

    @modified_filedescriptor.setter
    def modified_filedescriptor(self, value):
        self._modified_path = value

    @property
    def backup_filedescriptor(self):
        return self._backup_path

    @property
    def rank(self):
        """Give the position of the file according to the sorting criteria."""
        return self._rank
 
    @rank.setter
    def rank(self, value):
        self._rank = value

class FilesCollection(object):
    """Contains the files system structure with all subdirectories, starting from the input path."""
    def __init__(self, input_path, use_subdirectory, show_hidden_files, sorting_criteria="name", reverse_order=False):
        self.input_path = input_path
        self.use_subdirectory = use_subdirectory
        self.show_hidden_files = show_hidden_files
        self.root_tree_node = FileSystemTreeNode(self.input_path, True, 0 ,None)
        self.scan(self.root_tree_node, sorting_criteria, reverse_order)
        self.root_tree_node_backup = copy.deepcopy(self.root_tree_node)

    def scan(self, tree_node, sorting_criteria, reverse_order):
        """Build the files system structure with FileSystemTreeNode."""
        path = tree_node.original_filedescriptor.path
        children = sorted(os.listdir(path), key = lambda file : self.get_file_sorting_criteria(os.path.join(path, file), sorting_criteria), reverse=reverse_order)
        folder_rank = 0
        file_rank = 0
        for child in children:
            #Check for hidden files
            if child[0] == '.' and not self.show_hidden_files:
                continue
            if os.path.isdir(os.path.join(path,child)):
                folder_rank += 1
                file_system_child_node = FileSystemTreeNode(os.path.join(path,child), True, folder_rank, tree_node)
                tree_node.add_children(file_system_child_node)
                if (not self.use_subdirectory):
                    continue
                else:
                    self.scan(file_system_child_node, sorting_criteria, reverse_order)
            else:
                file_rank += 1
                file_system_child_node = FileSystemTreeNode(os.path.join(path,child), False, file_rank, tree_node)
                tree_node.add_children(file_system_child_node)

    def get_file_sorting_criteria(self, directory, sorting_criteria):
        """Criteria to sort the files."""
        (protection_bits, inode_number, device, hard_link, user_id, group_id, size, acessed_time, modification_time, creation_time) = os.stat(directory)
        if sorting_criteria == "size":
            return size
        elif sorting_criteria == "modified_date":
            return modification_time
        elif sorting_criteria ==  "creation_date":
            return creation_time
        elif sorting_criteria == "name":
            return directory.lower()
        else:
            return None


    def get_file_system_tree_node(self):
        return self.root_tree_node

    def reset(self, tree_node):
        """Reset the modified name with the original."""
        tree_node.modified_filedescriptor = copy.deepcopy(tree_node.original_filedescriptor)
        return tree_node
    
    def undo(self, tree_node):
        shutil.move(tree_node.original_filedescriptor.path, tree_node.backup_filedescriptor.path)
        tree_node.original_filedescriptor = copy.deepcopy(tree_node.backup_filedescriptor)

    def execute_method_on_nodes(self, tree_node, method, *optional_argument):
        """Execute a method on a given file of the tree node with zero or more optional arguments."""
        children_names = []
        duplicate_counter = 1
        if tree_node.original_filedescriptor.path != self.input_path:
            #Do not apply the actions to the selected directory.
            method(tree_node, *optional_argument)
        for child in tree_node.get_children():
            self.execute_method_on_nodes(child, method, *optional_argument)

    
    def call_actions(self, tree_node, actions):
        for action in actions:
            tree_node = action.call(tree_node)
        

    def rename(self, tree_node):
        try :
            shutil.move(tree_node.original_filedescriptor.path, tree_node.modified_filedescriptor.path)
            tree_node.original_filedescriptor = copy.deepcopy(tree_node.modified_filedescriptor)
        except (OSError, IOError, Error), e:
            print(sys.stderr, 'Error moving %s to %s: %s' % (sourcepath, destpath, e))

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

    def call(self, file_system_tree_node):
        """Apply action on the specified part."""
        prefix = ""
        suffix = ""
        if(self.path_type == "file"):
            file_system_tree_node.modified_filedescriptor.filename = self.call_on_path_part(file_system_tree_node, file_system_tree_node.modified_filedescriptor.filename)
            self.find_duplicates(file_system_tree_node)
            return file_system_tree_node
        elif(self.path_type == "folder"):
            file_system_tree_node.modified_filedescriptor.foldername = self.call_on_path_part(file_system_tree_node, file_system_tree_node.modified_filedescriptor.foldername)
            self.find_duplicates(file_system_tree_node)
            return file_system_tree_node
        elif(self.path_type == "suffix"):
            file_system_tree_node.modified_filedescriptor.suffix = file_system_tree_node.modified_filedescriptor.suffix + self.call_on_path_part(file_system_tree_node, file_system_tree_node.modified_filedescriptor.suffix)
            return file_system_tree_node
        elif(self.path_type == "prefix"):
            file_system_tree_node.modified_filedescriptor.prefix = self.call_on_path_part(file_system_tree_node, file_system_tree_node.modified_filedescriptor.prefix) + file_system_tree_node.modified_filedescriptor.prefix
            return file_system_tree_node
        elif(self.path_type == "extension"):
            file_system_tree_node.modified_filedescriptor.extension = self.call_on_path_part(file_system_tree_node, file_system_tree_node.modified_filedescriptor.extension)
            return file_system_tree_node
        else:
            raise Exception("path_part not valid")

    def call_on_path_part(self, file_system_tree_node, path_part):
        raise Exception("not implemented")

    def find_duplicates(self, file_system_tree_node):
        children_names = []
        duplicate_counter = 1
        for same_level_tree_node in file_system_tree_node.parent.get_children():
            if (same_level_tree_node.modified_filedescriptor.path in children_names):
                same_level_tree_node.modified_filedescriptor.path += ' (' + str(duplicate_counter) + ')'
                duplicate_counter += 1
            else:
                children_names.append(same_level_tree_node.modified_filedescriptor.path)


class CharacterReplacementAction(Action):
    """Replace old_char by new_char in the section of the path."""
    """path_part can be 'folder', 'file', 'prefix', 'suffix' or 'extension'."""
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

    def call_on_path_part(self, file_system_tree_node, path_part):
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
            raise Exception("starting_position cannot be higher than ending_position.")
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
    def __init__(self, path_type, untouched = False, uppercase = False, lowercase = False, titlecase = False):
        Action.__init__(self, path_type)
        self.untouched = untouched
        self.uppercase = uppercase
        self.lowercase = lowercase
        self.titlecase = titlecase

    def call_on_path_part(self, file_system_tree_node, path_part):
        (path, folder) = os.path.split(file_system_tree_node.original_filedescriptor.parent)
        if self.uppercase is True:
            return folder.upper()
        elif self.lowercase is True:
            return folder.lower()
        elif self.titlecase is True:
            return ' '.join([name[0].upper() + name[1:] for name in folder.split(' ')])
        else:
            return folder

class DateAction(Action):
    """Use the created or modified date metadata as the filename."""
    """If is_modified_time = True, the modified date from the file metadata is taken. Otherwise, it is the created date."""
    def __init__(self, path_type, is_modified_date = False, is_created_date = True, format_display = '%Y'):
        Action.__init__(self, path_type)
        self.is_modified_date = is_modified_date
        self.is_created_date = is_created_date
        self.format_display = format_display

    def call_on_path_part(self, file_system_tree_node, path_part):
        if self.is_modified_date:
            file_date = os.path.getmtime(file_system_tree_node.original_filedescriptor.path)
        elif self.is_created_date:
            file_date = os.path.getctime(file_system_tree_node.original_filedescriptor.path)
        return time.strftime(self.format_display, time.localtime(file_date))

class Counter(Action):
    """Count the number of files starting from start_index with the given increment."""
    """If restart==True, the counter is set to startindex at each subfolder."""

    def __init__(self, path_type, start_index, increment, restart):
        Action.__init__(self, path_type)
        self.start_index = start_index
        self.increment = increment
        self.restart = restart

    def call_on_path_part(self, file_system_tree_node, path_part):
        counter = file_system_tree_node.rank
        counter *= self.increment
        counter += self.start_index
        return str(counter)

class PipeAction(Action):
    """Execute actions inside another action."""
    def __init__(self, path_type, main_action, sub_action):
        Action.__init__(self, path_type)
        self.main_action = main_action
        self.sub_action = sub_action

    def call_on_path_part(self, file_system_tree_node, path_part):
        # Execute all left hand side actions to get argument values for the  action to execute.
        argumentValues = {}
        for argument_name, argument_provider in self.sub_action.items():
            if isinstance(argument_provider, Action):
                argumentValues[argument_name] = argument_provider.call_on_path_part(file_system_tree_node.modified_filedescriptor, path_part)
            else:
                argumentValues[argument_name] = argument_provider
        # Prepare right hand side for this file.
        action = self.main_action(self.path_part, **argumentValues)
        value = action.call_on_path_part(file_system_tree_node.modified_filedescriptor, path_part)
        return value

