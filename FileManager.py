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
        --size: size of the file in bytes.
        --modified_date: time of last modification.
        --created_date: time of creation.
    """
    def __init__(self, root_path, parent, original_filedescriptor, is_folder, is_hidden, size, modified_date, created_date):
        self.children = []
        self._root_path = root_path
        self._original_filedescriptor = original_filedescriptor
        self._modified_filedescriptor = self._original_filedescriptor
        self._parent = parent
        self._backup_filedescriptor = self._original_filedescriptor
        self._is_folder = is_folder
        self._is_hidden = is_hidden
        self._size = size
        self._modified_date = modified_date
        self._created_date = created_date
        
    def __repr__(self):
        return self.get_original_relative_path()
    
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
    def size(self):
        return self._size
    @property
    def modified_date(self):
        return self._modified_date
    @property
    def created_date(self):
        return self._created_date

    @property
    def is_folder(self):
        return self._is_folder

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
    def is_hidden(self):
        return self._is_hidden

    def match_files_type(self, files_type):
        if (files_type == ['*.*']):
            return True
        if(self.is_folder and files_type == ["folders"]):
            return True
        elif(self.is_folder is False):
            name = self.original_filedescriptor.extension.lower()
            for ext in files_type:
                if (name in ext):
                    return True
        return False

    def match_name_filter(self, name_filter):
        if(self.is_folder is False):
            name = str(self.original_filedescriptor.filename).lower()
            if (name_filter in name):
                return True
        if(name_filter == ""):
            return True
        return False


class FileSystemTreeNodeView(object):
    """
    Represents a portion of the FileSystemTreeNode depending on filters chosen by the users.
    Parameters:
        --file_system_tree_node: original filesystemtreenode
        --rank: integer that represents the position of the current file/folder in the list of FileSystemTreeNode children.
    """
    def __init__(self, file_system_tree_node, rank):
        self._rank = rank
        self.children = []
        self.files_system_tree_node = file_system_tree_node

    def __repr__(self):
        return self.files_system_tree_node.__repr__()

    def add_children(self, file_system_tree_node_view):
        self.children.append(file_system_tree_node_view)

    def get_children(self):
        return self.children

    def get_parent(self):
        return self.files_system_tree_node.get_parent()

    def get_original_relative_path(self):
        return self.files_system_tree_node.get_original_relative_path()

    def get_modified_relative_path(self):
        return self.files_system_tree_node.get_modified_relative_path()

    def get_backup_relative_path(self):
        return self.files_system_tree_node.get_backup_relative_path()

    def get_original_path(self):
        return self.files_system_tree_node.get_original_path()

    def get_modified_path(self):
        return self.files_system_tree_node.get_modified_path()

    def get_backup_path(self):
        return self.files_system_tree_node.get_backup_path()
    @property
    def size(self):
        return self.files_system_tree_node.size
    @property
    def modified_date(self):
        return self.files_system_tree_node.modified_date
    @property
    def created_date(self):
        return self.files_system_tree_node.created_date

    @property
    def is_folder(self):
        return self.files_system_tree_node.is_folder

    @property
    def original_filedescriptor(self):
        return self.files_system_tree_node.original_filedescriptor

    @original_filedescriptor.setter
    def original_filedescriptor(self, value):
        self.files_system_tree_node.original_filedescriptor = value

    @property
    def modified_filedescriptor(self):
        return self.files_system_tree_node.modified_filedescriptor

    @modified_filedescriptor.setter
    def modified_filedescriptor(self, value):
        self.files_system_tree_node.modified_filedescriptor = value

    @property
    def backup_filedescriptor(self):
        return self.files_system_tree_node.backup_filedescriptor

    @backup_filedescriptor.setter
    def backup_filedescriptor(self, value):
        self.files_system_tree_node.backup_filedescriptor = value

    @property
    def rank(self):
        """Give the position of the file according to the sorting criteria."""
        return self._rank

    @rank.setter
    def rank(self, value):
        self._rank = value

    def match_files_type(self, files_type):
        self.files_system_tree_node.match_files_type(files_type)

    def match_name_filter(self, name_filter):
        self.files_system_tree_node.match_name_filter(name_filter)

    @property
    def is_hidden(self):
        self.files_system_tree_node.is_hidden()


class FilesSystemView(object):
    """
    Represents a portion of the FilesSystem. This portion depends on the following filters:
    Parameters:
        --show_hidden_files: whether or not to show the hidden files.
    """

    def __init__(self, root_tree_node, show_hidden_files, files_type, name_filter, sorting_criteria, reverse_order):
        self.show_hidden_files = show_hidden_files
        self.files_type = files_type
        self.name_filter = name_filter
        self.sorting_criteria = sorting_criteria
        print(sorting_criteria)
        self.reverse_order = reverse_order
        self.root_tree_node_view = FileSystemTreeNodeView(root_tree_node, 0)
        self.filter_files(root_tree_node, self.root_tree_node_view)

    def filter_files(self, tree_node, tree_node_view):
        rank = -1
        for tree_node_child in sorted(tree_node.get_children(), key = lambda node: self.get_sorting_key(node), reverse=self.reverse_order):
            if (self.is_filtered_tree_node(tree_node_child) is True):
                continue
            rank += 1
            tree_node_child_view = FileSystemTreeNodeView(tree_node_child, rank)
            tree_node_view.add_children(tree_node_child_view)
            if (tree_node_child.is_folder):
                self.filter_files(tree_node_child, tree_node_child_view)

    def is_filtered_tree_node(self, tree_node):
        if (not self.show_hidden_files and tree_node.is_hidden):
            return True
        if (not tree_node.match_files_type(self.files_type)):
            return True
        if (not tree_node.match_name_filter(self.name_filter)):
            return True
        return False

    def get_file_system_tree_node(self):
        return self.root_tree_node_view
 
    def natural_sort(self, tree_node):
        """ Sorts the given iterable in the way that is expected.
        """
        filename = tree_node.original_filedescriptor.basename
        convert = lambda text: int(text) if text.isdigit() else text
        alphanum_key = [convert(c) for c in re.split('([0-9]+)', filename)]
        return alphanum_key

    def get_sorting_key(self, tree_node):
        """
        Criteria to sort the files.
        Parameters:
            --tree_node: path to the specified file/folder.
            --sorting_criteria: string that specifies the sorting criteria. Default is 'name'. Possible values are : name, size, creation_date and modified_date.
        """
        if self.sorting_criteria == "size":
            return tree_node.size
        elif self.sorting_criteria == "modified_date":
            return tree_node.modified_date
        elif self.sorting_criteria ==  "creation_date":
            return tree_node.created_date
        elif self.sorting_criteria == "name":
            return self.natural_sort(tree_node)
        else:
            return None

class FilesSystem(object):
    """
    Contains all the FilesSystemTreeNodes representing the files system structure with or without the subdirectories, starting from the input path.
    Parameters:
        --input_path: string that represents the root directory to start the files collection from.
        --use_subdirectory: boolean that tells to look over the subdirectories recursively or not.
    """

    def __init__(self, input_path, use_subdirectory):
        self.input_path = input_path
        (self.root_folder, basename)=os.path.split(self.input_path)
        self.use_subdirectory = use_subdirectory
        root_filedescriptor = FileDescriptor(basename, True)
        self.root_tree_node = FileSystemTreeNode(self.root_folder, None, root_filedescriptor, True, False,0,0,0 )
        self.scan(self.root_tree_node)
        self.renamed_files_list = []

    def scan(self, tree_node):
        """Creates the files system structure with FileSystemTreeNode."""
        path = self.get_full_path(tree_node.get_original_relative_path())
        children = os.listdir(path)
        for child in children:
            print(child)
            size = os.path.getsize(os.path.join(path,child))#return 0 when folders.
            modified_date = os.path.getmtime(os.path.join(path,child))
            created_date = os.path.getctime(os.path.join(path,child))
            if os.path.isdir(os.path.join(path,child)):
                file_system_child_node = self.add_folder(tree_node, child, size, modified_date, created_date)
                if (not self.use_subdirectory):
                    continue
                else:
                    self.scan(file_system_child_node)
            else:
                self.add_file(tree_node, child, size, modified_date, created_date)

    def add_file(self, tree_node, child, size, modified_date, created_date):
        file_system_child_node = FileSystemTreeNode(self.root_folder,tree_node, FileDescriptor(child, False), False, child.startswith('.'), size, modified_date, created_date)
        tree_node.add_children(file_system_child_node)

    def add_folder(self, tree_node, child, size, modified_date, created_date):
        file_system_child_node = FileSystemTreeNode(self.root_folder,tree_node, FileDescriptor(child, True), True, child.startswith('.'), size, modified_date, created_date)
        tree_node.add_children(file_system_child_node)
        return file_system_child_node

    def get_full_path(self, *children):
        return os.path.join(self.root_folder, *children)

    def generate_files_system_view(self, show_hidden_files, files_type, name_filter, sorting_criteria, reverse_order):
        files_system_view = FilesSystemView(self.root_tree_node, show_hidden_files, files_type, name_filter, sorting_criteria, reverse_order )
        return files_system_view


class Controller(object):
    def __init__(self, files_system_view):
        self.files_system_view = files_system_view
        self.root_tree_node_view = self.files_system_view.get_file_system_tree_node()
        self.actions = []

    def populate_actions(self, action_button_group):
        (action_descriptor, action_args) = actiongroup.get_inputs()
        action_class = action_descriptor.action_class
        action_instance = action_class(path_part, **action_args)
        self.actions.append(action_instance)


    def execute_method_on_nodes(self, tree_node, method, *optional_argument):
        """Execute a method on a given FileSystemTreeNode with zero or more optional arguments."""
        if tree_node.get_original_relative_path() != self.root_tree_node_view.get_original_relative_path():
            #Do not apply the actions to the selected directory.
            method(tree_node, *optional_argument)
        for child in tree_node.get_children():
            self.execute_method_on_nodes(child, method, *optional_argument)

    def reset(self, tree_node):
        """Reset the modified filedescriptor with the original one."""
        tree_node.modified_filedescriptor = copy.deepcopy(tree_node.original_filedescriptor)
        return tree_node


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
        # methods = {}
        # methods[self.reset] = []
        # methods[self.call_actions] = [actions, file_or_folder]
        # self.execute_method_on_nodes(self.root_tree_node_view, self.call_actions, actions, file_or_folder)
        self.execute_method_on_nodes(self.root_tree_node_view, self.reset)
        self.execute_method_on_nodes(self.root_tree_node_view, self.call_actions, actions, file_or_folder)
    
        

    def call_actions(self, tree_node, actions, file_or_folder):
        for action in actions:
            tree_node = action.call(tree_node, file_or_folder)

    def rename(self, tree_node):
        # self.execute_method_on_nodes(self.root_tree_node, {self.find_duplicates : []})
        try:
            shutil.move(tree_node.get_original_path(), tree_node.get_modified_path())
            tree_node.original_filedescriptor = tree_node.modified_filedescriptor
        except IOError as e:
            raise Exception(str(e))

    def undo(self, tree_node):
        shutil.move(tree_node.get_original_path(), tree_node.get_backup_path())
        tree_node.original_filedescriptor = tree_node.backup_filedescriptor

    def batch_rename(self):
        self.execute_method_on_nodes(self.root_tree_node, FileSystemTreeNodeView.rename)

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

