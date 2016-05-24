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
import re 


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

    def get_file_system_tree_node(self):
        return self.files_system_tree_node

    def add_children(self, file_system_tree_node_view):
        self.children.append(file_system_tree_node_view)

    def get_children(self):
        return self.children

    def find_child_by_path(self, path):
        return self.files_system_tree_node.find_child_by_path(path)

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
        self.files_system_tree_node.rank = value

    def match_files_type(self, files_type):
        self.files_system_tree_node.match_files_type(files_type)

    def match_name_filter(self, name_filter):
        self.files_system_tree_node.match_name_filter(name_filter)

    @property
    def is_hidden(self):
        self.files_system_tree_node.is_hidden

    @property
    def has_children(self):
        return self.files_system_tree_node.has_children


class FileSystemView(object):
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
        self.reverse_order = reverse_order
        self.root_tree_node_view = FileSystemTreeNodeView(root_tree_node, 0)
        self.filter_files(root_tree_node, self.root_tree_node_view)

    def filter_files(self, tree_node, tree_node_view):
        rank_file = -1
        rank_folder = -1
        for tree_node_child in sorted(tree_node.get_children(), key = lambda node: self.get_sorting_key(node), reverse=self.reverse_order):
            if (self.is_filtered_tree_node(tree_node_child) is True):
                continue
            if (tree_node_child.is_folder):
                rank_folder += 1
                rank = rank_folder
            else:
                rank_file +=1
                rank = rank_file
            tree_node_child_view = FileSystemTreeNodeView(tree_node_child, rank)
            tree_node_view.add_children(tree_node_child_view)
            if (tree_node_child.is_folder):
                self.filter_files(tree_node_child, tree_node_child_view)

    def is_filtered_tree_node(self, tree_node):
        if (not self.show_hidden_files and tree_node.is_hidden):
            return True
        if(tree_node.has_children is False and tree_node.is_folder is True and self.files_type != ["folders"]):
            return True
        if (tree_node.is_folder and tree_node.has_children):
            return False
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
