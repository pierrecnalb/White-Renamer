#!/usr/bin/python3

import os
from .folder import Folder
from .file import File


class Model(object):
    def __init__(self, root_path, is_recursive=False,
                 file_filter=Filter()):
    """ Represents a part or the full filesystem structure, starting from the given root node.

    Args:
        root_path (string): The full path of the root node.
        is_recursive (bool): Specifies whether the model uses the subdirectories recursively or not.
        file_filter (Filter, optional): An optional filter to discard some specific files.
    """
        self._current_id = 0
        self._nodes_by_id = dict()
        self._root_folder = Folder(self._current_id, root_path, None)
        self._nodes_by_id[self._current_id] = self._root_folder
        self._is_recursive = is_recursive
        self._file_filter = file_filter
        self._build_tree_model()

    @property
    def filter(self):
        """ The Filter used in this model to discard some files."""
        return self._file_filter

    @property
    def is_recursive(self):
        """ Specifies whether the model uses the subdirectories recursively or not."""
        return self._is_recursive

    @is_recursive.setter
    def is_recursive(self, value):
        """ Specifies whether the model uses the subdirectories recursively or not."""
        self._is_recursive = value
        self._build_tree_model()

    @property
    def root_folder(self):
        """ The Folder that is the root of the model."""
        return self._root_folder


    @property
    def nodes(self):
        """ Returns a flat list of all nodes in the filesystem model (filtered nodes excluded)."""
        node_list = list()
        for node_id_map in self._nodes_by_id:
            current_node = self._nodes_by_id[node_id_map]
            if current_node.is_filtered(self._file_filter):
                node_list.append(current_node)
        return node_list

    @property
    def _all_nodes(self):
        """ Returns a flat list of all nodes in the filesystem model (included filtered nodes)."""
        node_list = list()
        for node_id_map in self._nodes_by_id:
            node_list.append(self._nodes_by_id[node_id_map])
        return node_list

    def _new_id(self):
        return ++self._current_id

    def _build_tree_model(self):
        self._scan_file_system(self._root_folder)

    def _scan_file_system(self, tree_node):
        """Creates the files system hierarchy without any filters, except recursion."""
        path = tree_node.path
        children = os.listdir(path)
        for child in children:
            child_path = os.path.join(path, child)
            if os.path.isdir(child_path):
                # add folder
                folder_node = Folder(self._new_id(), child_path, tree_node)
                self._nodes_by_id[self._current_id] = folder_node
                if (not self.is_recursive):
                    continue
                else:
                    self._scan_file_system(folder_node)
            else:
                # add file
                file_node = File(self._new_id(), child_path, tree_node)
                self._nodes_by_id[self._current_id] = file_node

    # def natural_sort(self, tree_node):
    #     """ Sorts the given iterable in the way that is expected.
    #     """
    #     filename = tree_node.original_filedescriptor.basename
    #     convert = lambda text: int(text) if text.isdigit() else text
    #     alphanum_key = [convert(c) for c in re.split('([0-9]+)', filename)]
    #     return alphanum_key

    # def get_sorting_key(self, tree_node):
    #     """
    #     Criteria to sort the files.
    #     Parameters:
    #         --tree_node: path to the specified file/folder.
    #         --sorting_criteria: string that specifies the sorting criteria. Default is 'name'. Possible values are : name, size, creation_date and modified_date.
    #     """
    #     if self.sorting_criteria == "size":
    #         return tree_node.size
    #     elif self.sorting_criteria == "modified_date":
    #         return tree_node.modified_date
    #     elif self.sorting_criteria == "creation_date":
    #         return tree_node.created_date
    #     elif self.sorting_criteria == "name":
    #         return self.natural_sort(tree_node)
    #     else:
    #         return None

    # def generate_files_system_view(self, discard_hidden_files, files_type,
    #                                name_filter, sorting_criteria,
    #                                reverse_order):
    #     files_system_view = FileSystemView(
    #         self.root_tree_node, discard_hidden_files, files_type, name_filter,
    #         sorting_criteria, reverse_order)
    #     return files_system_view


class Filter(object):
    def __init__(self):
        """ A filter that allows a filesystem model to discard specific files based on its properties."""
        self._discard_hidden_files = True
        self._node_type = NodeType.all
        self._file_type = Types.all
        self._search_pattern = ""

    @property
    def discard_hidden_files(self):
        """ Specifies whether the hidden files must be used or not."""
        return self._discard_hidden_files

    @discard_hidden_files.setter
    def discard_hidden_files(self, value):
        self._discard_hidden_files = value

    @property
    def node_type(self):
        return self._node_type

    @node_type.setter
    def node_type(self, value):
        self._node_type = value

    @property
    def file_type(self):
        self._file_type

    @file_type.setter
    def file_type(self, value):
        self._file_type = value

    @property
    def search_pattern(self):
        """ The pattern used to search only specific file nodes."""
        self._search_pattern

    @search_pattern.setter
    def search_pattern(self, value):
        """ Specify a pattern used to select only specific file nodes."""
        self._search_pattern = value
