#!/usr/bin/python3

from folder_node import FolderNode
from file_node import FileNode
from file_filter import FileFilter
import os


class Model(object):
    """
    Represents a portion of the FilesystemNode depending on filters chosen by the users.
    Parameters:
        --file_system_tree_node: original filesystemtreenode
        --rank: integer that represents the position of the current file/folder in the list of FilesystemNode children.
    """
    """
    Contains all the FilesystemNodes representing the files system structure with or without the subdirectories, starting from the input path.
    Parameters:
        --input_path: string that represents the root directory to start the files collection from.
        --use_subdirectory: boolean that tells to look over the subdirectories recursively or not.
    """

    def __init__(self, root_path, is_recursive=False, file_filter=FileFilter()):
        self._current_id = 0
        self._nodes_by_id = dict()
        self._root_node = FolderNode(self._current_id, root_path, None)
        self._nodes_by_id[self._current_id] = self._root_node
        self._is_recursive = is_recursive
        self._file_filter = file_filter
        self._build_tree_model()

    @property
    def file_filter(self):
        return self._file_filter

    @property
    def is_recursive(self):
        return self._is_recursive

    @is_recursive.setter
    def is_recursive(self, value):
        self._is_recursive = value
        self._build_tree_model()

    @property
    def root_node(self):
        return self._root_node

    @property
    def all_nodes(self):
        node_list = list()
        for node_id_map in self._nodes_by_id:
            node_list.append(self._nodes_by_id[node_id_map])
        return node_list

    @property
    def filtered_nodes(self):
        node_list = list()
        for node_id_map in self._nodes_by_id:
            current_node = self._nodes_by_id[node_id_map]
            if current_node.is_filtered(self._file_filter):
                node_list.append(current_node)
        return node_list

    def _new_id(self):
        return ++self._current_id

    def _build_tree_model(self):
        self._scan_file_system(self._root_node)

    def _scan_file_system(self, tree_node):
        """Creates the files system hierarchy without any filters, except recursion."""
        path = tree_node.path
        children = os.listdir(path)
        for child in children:
            child_path = os.path.join(path, child)
            if os.path.isdir(child_path):
                # add folder
                folder_node = FolderNode(self._new_id(), child_path, tree_node)
                self._nodes_by_id[self._current_id] = folder_node
                if (not self.is_recursive):
                    continue
                else:
                    self._scan_file_system(folder_node)
            else:
                # add file
                file_node = FileNode(self._new_id(), child_path, tree_node)
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

    # def generate_files_system_view(self, show_hidden_files, files_type,
    #                                name_filter, sorting_criteria,
    #                                reverse_order):
    #     files_system_view = FileSystemView(
    #         self.root_tree_node, show_hidden_files, files_type, name_filter,
    #         sorting_criteria, reverse_order)
    #     return files_system_view
