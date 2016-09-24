#!/usr/bin/python3

# Copyright (C) 2015-2016 Pierre Blanc
#
# This file is part of WhiteRenamer.
#
# WhiteRenamer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WhiteRenamer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WhiteRenamer. If not, see <http://www.gnu.org/licenses/>.
import FileSystemTreeNode


class FileSystemTreeModel(object):
    """
    Represents a portion of the FileSystemTreeNode depending on filters chosen by the users.
    Parameters:
        --file_system_tree_node: original filesystemtreenode
        --rank: integer that represents the position of the current file/folder in the list of FileSystemTreeNode children.
    """
    """
    Contains all the FileSystemTreeNodes representing the files system structure with or without the subdirectories, starting from the input path.
    Parameters:
        --input_path: string that represents the root directory to start the files collection from.
        --use_subdirectory: boolean that tells to look over the subdirectories recursively or not.
    """

    def __init__(self, root_node, is_recursive):
        self._root_node = root_node
        self._is_recursive = is_recursive
        self.update()

    # @property
    # def filter(self):
    #     return self._filter

    # @filter.setter
    # def filter(self, value):
    #     self._filter = value
    #     self.update()

    @property
    def is_recursive(self):
        return self._is_recursive

    @is_recursive.setter
    def is_recursive(self, value):
        self._is_recursive = value
        self.regenerate_tree()

    @property
    def root_node(self):
        return self._root_node

    def regenerate_tree(self):
        self.scan_file_system(self._root_node)

    def scan_file_system(self, tree_node):
        """Creates the files system hierarchy without any filters, except recursion."""
        path = tree_node.full_path
        children = listdir(path)
        for child in children:
            child_path = os.path.join(path, child)
            if isdir(os.path.join(path, child)):
                #add folder
                folder_node = FolderNode(child_path)
                tree_node.add_children(folder_node)
                if (not self.is_recursive):
                    continue
                else:
                    self.scan_file_system(node)
            else:
                #add file
                file_node = FileNode(child_path)
                tree_node.add_children(file_node)



    # def filter_tree_view(self, tree_node):
    #     rank_file = -1
    #     rank_folder = -1
    #     for child_node in tree_node.children:
    #         if self.is_filtered_tree_node(tree_node) is True:
    #             continue
            

    #     for tree_node_child in sorted(tree_node.get_children(), key=lambda node: self.get_sorting_key(node), reverse=self.reverse_order):
    #         if (self.is_filtered_tree_node(tree_node_child) is True):
    #             continue
    #         if (tree_node_child.is_folder):
    #             rank_folder += 1
    #             rank = rank_folder
    #         else:
    #             rank_file += 1
    #             rank = rank_file
    #         tree_node_child_view = FileSystemTreeNodeView(tree_node_child,
    #                                                       rank)
    #         tree_node_view.add_children(tree_node_child_view)
    #         if (tree_node_child.is_folder):
    #             self.filter_files(tree_node_child, tree_node_child_view)


    # def is_filtered_tree_node(self, tree_node):
    #     """Specifies whether tree_node is filtered or not (i.e. not seen in the model)."""
    #     if (not self.filter.show_hidden_files and tree_node.is_hidden):
    #         return True
    #     if (self.filter.files_only and tree_node.is_folder):
    #         return True
    #     if (not self.filter.music_files_only and tree_node.type.music):
    #         return True

        # if (tree_node.has_children is False and tree_node.is_folder is True and
        #         self.files_type != ["folders"]):
        #     return True
        # if (tree_node.is_folder and tree_node.has_children):
        #     return False
        # if (not tree_node.match_files_type(self.files_type)):
        #     return True
        # if (not tree_node.match_name_filter(self.name_filter)):
        #     return True
    #     return False

    # def get_file_system_tree_node(self):
    #     return self.root_tree_node_view

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
