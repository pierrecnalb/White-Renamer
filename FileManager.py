#author : pierrecnalb
#copyright pierrecnalb
import os
import shutil
import copy
import pdb
import io
import ActionManager
import re

class FileDescriptor(object):
    """
    Group information related to the input files.
    Parameters:
        --basename: string that represents the name of the file or folder.
        --is_folder: boolean that tells if the current FileDescriptor is a directory or a file.
    """
    def __init__(self, basename, is_folder):
        self._basename = basename
        self.is_folder = is_folder
        if (self.is_folder is False):
            (self._filename, self._extension) = os.path.splitext(self._basename)
            self._extension = self._extension[1:] #remove dot
            self._foldername = ""
        else:
            self._filename = ""
            self._foldername = self._basename
            self._extension = ""
        self._prefix = ""
        self._suffix = ""

    def __repr__(self):
        """override string representation of the class"""
        return self._basename

    def is_folder(self):
        return self.is_folder

    @property
    def basename(self):
        self.update_basename()
        return self._basename

    @basename.setter
    def basename(self, value):
        self._basename = value

    @property
    def foldername(self):
        return self._foldername

    @foldername.setter
    def foldername(self, value):
        self._foldername = value
        self.update_basename()

    @property
    def suffix(self):
        return self._suffix

    @suffix.setter
    def suffix(self, value):
        self._suffix = value
        self.update_basename()

    @property
    def prefix(self):
        return self._prefix

    @prefix.setter
    def prefix(self, value):
        self._prefix = value
        self.update_basename()

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value
        self.update_basename()

    @property
    def extension(self):
        return self._extension

    @extension.setter
    def extension(self, value):
        self._extension = value
        self.update_basename()

    def update_basename(self):
        if self.is_folder is True:
            self._basename = self._prefix + self._foldername + self._suffix
        else:
            self._basename = self._prefix + self._filename + self._suffix + "." + self._extension

class FileSystemTreeNode(object):
    """
    Contains the original, modified and backup FileDescriptor for a given node of the specified directory.
    The structure of the system tree node is reproduced by adding children for each subdirectory.

    Parameters:
        --root_path: string that represents the whole path of the current file or directory.
        --parent: the FileSystemTreeNode parent of the current FileSystemTreeNode.
        --original_filedescriptor: represents the current file or directory basename.
        --is_folder: boolean that tells if the current FileSystemTreeNode is a directory or a file.
        --rank: integer that represents the position of the current file/folder in the list of FileSystemTreeNode children.
    """
    def __init__(self, root_path, parent, original_filedescriptor, is_folder, rank):
        self.children = []
        self._root_path = root_path
        self._original_filedescriptor = original_filedescriptor
        self._modified_filedescriptor = self._original_filedescriptor
        self._parent = parent
        self._backup_filedescriptor = self._original_filedescriptor
        self.is_folder = is_folder
        self._rank = rank

    def add_children(self, file_system_tree_node):
        self.children.append(file_system_tree_node)
        return file_system_tree_node

    def get_children(self):
        return self.children

    def get_parent(self):
        return self._parent

    def get_original_relative_path(self):
        if self._parent != None:
            return os.path.join(self._parent.get_original_relative_path(), self._original_filedescriptor.basename)
        else:
            return self._original_filedescriptor.basename

    def get_modified_relative_path(self):
        if self._parent != None:
            return os.path.join(self._parent.get_modified_relative_path(), self._modified_filedescriptor.basename)
        else:
            return self._modified_filedescriptor.basename

    def get_backup_relative_path(self):
        if self._parent != None:
            return os.path.join(self._parent.get_backup_relative_path(), self._backup_filedescriptor.basename)
        else:
            return self._backup_filedescriptor.basename

    def get_original_path(self):
        return os.path.join(self._root_path, self.get_original_relative_path())

    def get_modified_path(self):
        return os.path.join(self._root_path, self.get_modified_relative_path())

    def get_backup_path(self):
        return os.path.join(self._root_path, self.get_backup_relative_path())

    @property
    def original_filedescriptor(self):
        return self._original_filedescriptor

    @original_filedescriptor.setter
    def original_filedescriptor(self, value):
        self._original_filedescriptor = value

    @property
    def modified_filedescriptor(self):
        return self._modified_filedescriptor

    @modified_filedescriptor.setter
    def modified_filedescriptor(self, value):
        self._modified_filedescriptor = value

    @property
    def backup_filedescriptor(self):
        return self._backup_filedescriptor

    @backup_filedescriptor.setter
    def backup_filedescriptor(self, value):
        self._backup_filedescriptor = value

    @property
    def rank(self):
        """Give the position of the file according to the sorting criteria."""
        return self._rank

    @rank.setter
    def rank(self, value):
        self._rank = value

class FilesCollection(object):
    """
    Contains all the FilesSystemTreeNodes representing the files system structure with all subdirectories, starting from the input path.
    Parameters:
        --input_path: string that represents the root directory to start the files collection from.
        --use_subdirectory: boolean that tells to look over the subdirectories recursively or not.
        --show_hidden_files: boolean that tells to look at hidden files or not.
        --sorting_criteria: string that specifies the sorting criteria. Default is 'name'. Possible values are : name, size, creation_date and modified_date.
        --reverse_order: boolean that specifies the sorting order. Default is 'False'.
    """

    def __init__(self, input_path, use_subdirectory, show_hidden_files, sorting_criteria="name", reverse_order=False, filters = [], type_filters = []):
        self.input_path = input_path
        (self.root_folder, basename)=os.path.split(self.input_path)
        self.use_subdirectory = use_subdirectory
        self.show_hidden_files = show_hidden_files
        root_filedescriptor = FileDescriptor(basename, True)
        self.root_tree_node = FileSystemTreeNode(self.root_folder, None, root_filedescriptor, True, 0)
        self.scan(self.root_tree_node, sorting_criteria, reverse_order, filters, type_filters)
        self.root_tree_node_backup = copy.deepcopy(self.root_tree_node)
        self.flat_tree_list = []
        self.renamed_files_list = []

    def scan(self, tree_node, sorting_criteria, reverse_order, filters, type_filters):
        """Creates the files system structure with FileSystemTreeNode."""
        path = self.get_full_path(tree_node.get_original_relative_path())
        children = sorted(os.listdir(path), key = lambda file : self.get_file_sorting_criteria(os.path.join(path, file), sorting_criteria), reverse=reverse_order)
        folder_rank = -1
        file_rank = -1
        for child in children:
            #Check for hidden files
            if child[0] == '.' and not self.show_hidden_files:
                continue
            if os.path.isdir(os.path.join(path,child)):
                folder_rank += 1
                file_system_child_node = FileSystemTreeNode(self.root_folder,tree_node, FileDescriptor(child, True), True, folder_rank)
                tree_node.add_children(file_system_child_node)
                if (not self.use_subdirectory):
                    continue
                else:
                    self.scan(file_system_child_node, sorting_criteria, reverse_order, filters, type_filters)
            else:
                if type_filters == "folders":
                    continue
                if type_filters != []:
                    for type_filter in type_filters:
                        if type_filter in os.path.splitext(child)[1].lower():
                            if filters != ['']:
                                for filter in filters:
                                    if filter in child:
                                        file_rank += 1
                                        file_system_child_node = FileSystemTreeNode(self.root_folder,tree_node, FileDescriptor(child, False), False, file_rank)
                                        tree_node.add_children(file_system_child_node)
                                        break
                            elif filters == ['']:
                                file_rank += 1
                                file_system_child_node = FileSystemTreeNode(self.root_folder,tree_node, FileDescriptor(child, False), False, file_rank)
                                tree_node.add_children(file_system_child_node)
                                break
                elif type_filters == []:
                    file_rank += 1
                    file_system_child_node = FileSystemTreeNode(self.root_folder,tree_node, FileDescriptor(child, False), False, file_rank)
                    tree_node.add_children(file_system_child_node)

    def get_full_path(self, *children):
        return os.path.join(self.root_folder, *children)

    def get_file_sorting_criteria(self, directory, sorting_criteria):
        """
        Criteria to sort the files.
        Parameters:
            --directory: path to the specified file/folder.
            --sorting_criteria: string that specifies the sorting criteria. Default is 'name'. Possible values are : name, size, creation_date and modified_date.
        """
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
        """Reset the modified filedescriptor with the original one."""
        tree_node.modified_filedescriptor = copy.deepcopy(tree_node.original_filedescriptor)
        return tree_node

    def execute_method_on_nodes(self, tree_node, method, *optional_argument):
        """Execute a method on a given FileSystemTreeNode with zero or more optional arguments."""
        children_names = []
        duplicate_counter = 1
        if tree_node.get_original_relative_path() != os.path.split(self.input_path)[-1]:
            #Do not apply the actions to the selected directory.
            method(tree_node, *optional_argument)
        for child in tree_node.get_children():
            self.execute_method_on_nodes(child, method, *optional_argument)

    def find_duplicates(self, tree_node):
        """Finds if there are duplicate files/folders. If there are some duplicates, appends a counter to differenciate them."""
        children_names = []
        files_duplicate_counter = 1
        folders_duplicate_counter = 1
        if tree_node.get_parent() is not None:
            for same_level_tree_node in tree_node.get_parent().get_children():
                if (same_level_tree_node.modified_filedescriptor.basename in children_names):
                    if same_level_tree_node.modified_filedescriptor.is_folder:
                        same_level_tree_node.modified_filedescriptor.foldername += ' (' + str(folders_duplicate_counter) + ')'
                        folders_duplicate_counter += 1
                    else:
                        same_level_tree_node.modified_filedescriptor.suffix += ' (' + str(files_duplicate_counter) + ')'
                        files_duplicate_counter += 1
                else:
                    children_names.append(same_level_tree_node.modified_filedescriptor.basename)

    def process_file_system_tree_node(self, actions, file_or_folder):
        self.execute_method_on_nodes(self.root_tree_node, self.reset)
        self.execute_method_on_nodes(self.root_tree_node, self.call_actions, actions, file_or_folder)
        self.execute_method_on_nodes(self.root_tree_node, self.find_duplicates)

    def call_actions(self, tree_node, actions, file_or_folder):
        for action in actions:
            tree_node = action.call(tree_node, file_or_folder)

    def rename(self, tree_node):
        try:
            shutil.move(tree_node.get_original_path(), tree_node.get_modified_path())
            tree_node.original_filedescriptor = tree_node.modified_filedescriptor
        except IOError as e:
            raise Exception(str(e))

    def undo(self, tree_node):
        shutil.move(tree_node.get_original_path(), tree_node.get_backup_path())
        tree_node.original_filedescriptor = tree_node.backup_filedescriptor

    def batch_rename(self):
        self.execute_method_on_nodes(self.root_tree_node, self.rename)

    def batch_undo(self):
        self.execute_method_on_nodes(self.root_tree_node, self.undo)

    def convert_tree_to_list(self):
        flat_tree_list = []
        self.execute_method_on_nodes(self.root_tree_node, flat_tree_list.append)
        for tree_node in flat_tree_list:
            self.flat_tree_list.append(tree_node.get_modified_path())
        return self.flat_tree_list

    def save_result_to_file(self, name, input_list):
        directory = os.path.join(os.path.dirname(__file__),"UnitTest", "TestCase1_Models", name)
        file = io.open(directory, 'w+')
        for line in input_list:
            file.writelines(line + '\n')
        file.close()

    def parse_renamed_files(self, input_path, sorting_criteria, reverse_order):
        input_path = os.path.abspath(input_path)
        directory_files = sorted(os.listdir(input_path), key = lambda file : self.get_file_sorting_criteria(os.path.join(input_path, file), sorting_criteria), reverse=reverse_order)
        for filename in directory_files:
            filepath = os.path.join(input_path, filename)
            if filename[0] == '.' and not self.show_hidden_files:
                continue
            if os.path.isdir(filepath):
                self.renamed_files_list.append(os.path.relpath(filepath, self.root_folder))
                if (not self.use_subdirectory):
                    continue
                else:
                    self.parse_renamed_files(filepath, sorting_criteria, reverse_order)
            else:
                self.renamed_files_list.append(os.path.relpath(filepath, self.root_folder))

    def get_renamed_files(self):
        self.save_result_to_file("hooh", self.renamed_files_list)
