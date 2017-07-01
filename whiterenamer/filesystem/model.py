#!/usr/bin/python3

import os
from .folder import Folder
from .file import File
import copy


class FileSystemModel(object):
    def __init__(self, root_path, is_recursive=False):
        """ Represents a part or the full filesystem structure, starting from the given root node.

        Args:
            root_path (string): The full path of the root node.
            is_recursive (bool): Specifies whether the model uses the subdirectories recursively.
            file_filter (Filter, optional): An optional filter to discard some specific files.
        """
        self._current_id = 0
        self._is_recursive = is_recursive
        self._nodes_by_id = dict()
        self._node_list = []
        self._path_to_root = os.path.split(root_path)
        self._root_folder = Folder(root_path, None, self)
        self._register_node(self._root_folder)
        self._build_tree_model()
        self._file_filter = None

    @property
    def root_folder(self):
        """ The Folder that is the root of the model."""
        return self._root_folder

    @property
    def is_recursive(self):
        """ Specifies whether the model uses the subdirectories recursively or not."""
        return self._is_recursive

    @property
    def nodes(self):
        """ Returns a flat list of all nodes in the filesystem model (both filtered and unfiltered)."""
        return list(self._nodes_by_id.values())

    def find_node_by_path(self, path):
        for node in self.nodes:
            if node._backup_path is path:
                return node
        return None

    def remove(self, node):
        """ Remove node from the model."""
        del self._nodes_by_id[node.id]

    @property
    def file_filter(self):
        """ The Filter used in this model to discard some files."""
        return self._file_filter

    def _new_id(self):
        return ++self._current_id

    def _register_node(self, node):
        self._nodes_by_id[self._current_id] = self._root_folder
        self._node_list.append(self._root_folder)

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
                folder_node = Folder(child_path, tree_node, self)
                self._register_node(folder_node)
                if (not self.is_recursive):
                    continue
                else:
                    self._scan_file_system(folder_node)
            else:
                # add file
                file_node = File(child_path, tree_node, self)
                self._register_node(file_node)

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


class FilteredModel(FileSystemModel):
    def __init__(self, filesystem_model, file_filter):
        super().__init__(filesystem_model.root_path, filesystem_model.is_recursive)
        model = copy.deepcopy(filesystem_model)
        for node in model.nodes:
            if not node.is_filtered(file_filter):
                node.remove()

    @property
    def file_filter(self):
        """ The Filter used in this model to discard some files."""
        return self._file_filter
