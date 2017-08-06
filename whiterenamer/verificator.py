#!/usr/bin/python3

import os


class ModelVerificator(object):
    def __init__(self, filesystem_model):
        self._filesystem_model = filesystem_model

    def run_tests(self):
        self.check_user_inputs()
        self._verify_files_integrity()

    def _verify_files_integrity(self):
        """ Performs various tests to be sure that the renaming operations are safe."""
        unchecked_folders = list(self._original_model.root_folder)
        while len(unchecked_folders) > 0:
            folder = unchecked_folders.pop()
            folder._check_user_inputs()
            unchecked_folders.append(folder.get_folder_children())

    def check_user_inputs(self):
        """ Specifies whether the user inputs does not lead to files with same names.
        """
        unique_names = set()
        for node in self._filesystem_model.nodes:
            if (node.modified_path not in unique_names):
                unique_names.add(node.modified_path)
            else:
                raise Exception("""Naming conflict error.
                {0} cannot be renamed {1} since an item with the same name already exists.
                """.format(node.original_path, node.modified_path))

    def check_conflicting_node(self):
        for child in self.filtered_nodes:
            if os.path.exists(child.modified_path):
                conflicting_node = self._filtered_model.find_node_by_path(child.modified_path)
                if conflicting_node is None:
                    continue
                else:
                    # If there is a conflicting node that must be renamed later,
                    # name it with a unique name to solve the issue.
                    # It will be renamed later anyway.
                    if conflicting_node.modified_name is "":
                        # This node is not intended to be renamed,
                        # so we'd better raise an exception
                        raise Exception(
                            """The file/folder {0} cannot be renamed {1} since this path already exists.""".
                            format(child.original_path, child.modified_path))
                    else:
                        conflicting_node = conflicting_node.original_name
                        temporary_name = uuid.uuid4()
                        conflicting_node.original_name.fullname = temporary_name
                        shutil.move(conflicting_node.original_path, conflicting_node.modified_path)
