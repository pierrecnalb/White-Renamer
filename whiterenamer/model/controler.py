
class Controller(object):
    def __init__(self, files_system_view):
        self.files_system_view = files_system_view
        self.root_tree_node_view = self.files_system_view.get_file_system_tree_node(
        )
        self.actions = []

    def populate_actions(self, action_button_group):
        (action_descriptor, action_args) = actiongroup.get_inputs()
        action_class = action_descriptor.action_class
        action_instance = action_class(path_part, **action_args)
        self.actions.append(action_instance)

    def execute_method_on_nodes(self, tree_node, method, *optional_argument):
        """Execute a method on a given FileSystemTreeNode with zero or more optional arguments."""
        if tree_node.get_original_relative_path(
        ) != self.root_tree_node_view.get_original_relative_path():
            #Do not apply the actions to the selected directory.
            method(tree_node, *optional_argument)
        for child in tree_node.get_children():
            self.execute_method_on_nodes(child, method, *optional_argument)

    def batch_update(self, actions, file_or_folder):
        self.execute_method_on_nodes(self.root_tree_node_view, self.update,
                                     actions, file_or_folder)

    def call_actions(self, tree_node, actions, file_or_folder):
        for action in actions:
            tree_node = action.call(tree_node, file_or_folder)

    def update(self, tree_node, actions, file_or_folder):
        self.reset(tree_node)
        self.call_actions(tree_node, actions, file_or_folder)

    def reset(self, tree_node):
        """Reset the modified filedescriptor with the original one."""
        tree_node.modified_filedescriptor = deepcopy(
            tree_node.original_filedescriptor)
        return tree_node

    def rename(self, tree_node):
        try:
            self.has_duplicates(tree_node)
            if exists(tree_node.get_modified_path()):
                conflicting_tree_node = tree_node.get_parent(
                ).find_child_by_path(tree_node.get_modified_path())
                if (conflicting_tree_node is not None and
                        tree_node.get_file_system_tree_node() !=
                        conflicting_tree_node):  #check if it is the same file
                    old_conflicting_file_descriptor = conflicting_tree_node.modified_filedescriptor
                    conflicting_tree_node.modified_filedescriptor = FileDescriptor(
                        str(uuid4()) + "." +
                        tree_node.original_filedescriptor.extension,
                        tree_node.is_folder)
                    self.rename(conflicting_tree_node)
                    conflicting_tree_node.modified_filedescriptor = old_conflicting_file_descriptor
            move(tree_node.get_original_path(), tree_node.get_modified_path())
            tree_node.original_filedescriptor = deepcopy(
                tree_node.modified_filedescriptor)
            # self.reset(tree_node)
        except IOError as e:
            raise Exception(str(e))

    def undo(self, tree_node):
        move(tree_node.get_original_path(), tree_node.get_backup_path())
        tree_node.original_filedescriptor = tree_node.backup_filedescriptor

    def has_duplicates(self, tree_node):
        """Finds if there are duplicate files/folders. If there are some duplicates, appends a counter to differenciate them."""
        children_names = []
        if tree_node.get_parent() is not None:
            for same_level_tree_node in tree_node.get_parent().get_children():
                if (same_level_tree_node.modified_filedescriptor.basename in
                        children_names):
                    raise Exception(
                        "Names conflict: several items have the same name. Please choose new options to avoid duplicates.")
                else:
                    children_names.append(
                        same_level_tree_node.modified_filedescriptor.basename)

    def batch_rename(self):
        self.execute_method_on_nodes(self.root_tree_node_view, self.rename)

    def batch_undo(self):
        self.execute_method_on_nodes(self.root_tree_node_view, self.undo)

    def convert_tree_to_list(self):
        flat_tree_list = []
        self.execute_method_on_nodes(self.root_tree_node_view,
                                     flat_tree_list.append)
        for tree_node in flat_tree_list:
            self.flat_tree_list.append(tree_node.get_modified_path())
        return self.flat_tree_list

    def save_result_to_file(self, name, input_list):
        directory = join(
            dirname(__file__), "UnitTest", "TestCase1_Models", name)
        file = open(directory, 'w+')
        for line in input_list:
            file.writelines(line + '\n')
        file.close()

    def parse_renamed_files(self, input_path, sorting_criteria, reverse_order):
        input_path = abspath(input_path)
        directory_files = sorted(listdir(input_path), key = lambda file : self.get_file_sorting_criteria(join(input_path, file), sorting_criteria), reverse=reverse_order)
        for filename in directory_files:
            filepath = join(input_path, filename)
            if filename[0] == '.' and not self.show_hidden_files:
                continue
            if isdir(filepath):
                self.renamed_files_list.append(relpath(filepath,
                                                       self.root_folder))
                if (not self.use_subdirectory):
                    continue
                else:
                    self.parse_renamed_files(filepath, sorting_criteria,
                                             reverse_order)
            else:
                self.renamed_files_list.append(relpath(filepath,
                                                       self.root_folder))

    def get_renamed_files(self):
        self.save_result_to_file("hooh", self.renamed_files_list)
