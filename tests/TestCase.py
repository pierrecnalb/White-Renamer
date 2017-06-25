#!/usr/bin/python3

import whiterenamer


class TestCases(unittest.TestCase):

    # def SetUp(self):



    def test_original_name(self):
        whiterenamer = WhiteRenamer(root)
        whiterenamer.filename_action_collection.append("OriginalName")

        # """Test to be sure that orginalnameaction is not doing anything."""
        # self.init("TestCase1", True, False, "name", False)
        # action_descriptor = action_manager.OriginalNameAction
        # files = self.files_collection
        # action_args = {}
        # self.apply_actions(action_descriptor, action_args, 'folder', 'folder')
        # self.apply_actions(action_descriptor, action_args, 'file', 'file')
        # self.apply_actions(action_descriptor, action_args, 'extension','file')
        # self.scan_directory(self.directory, self.sorting_criteria, self.reverse_order)
        # self.compare_with_model_file(TestCasesFileSystemModel.Main_OriginalName)

    def compare_with_model_file(self, model_file):
        self.assertCountEqual(self.files_list, model_file)
        shutil.rmtree(self.directory)

    def apply_actions(self, action_descriptor, action_args, path_type, file_or_folder):
        self.actions = []
        self.populate_actions(action_descriptor, action_args, path_type)
        self.controller.batch_update(self.actions, file_or_folder)
        self.controller.batch_rename()


    def scan_directory(self, input_path, sorting_criteria, reverse_order):
        input_path = os.path.abspath(input_path)
        directory_files = sorted(os.listdir(input_path), key = lambda file : self.get_sorting_key(os.path.join(input_path,file)), reverse=reverse_order)
        for filename in directory_files:
            filepath = os.path.join(input_path, filename)
            if filename[0] == '.' and not self.show_hidden_files:
                continue
            if os.path.isdir(filepath):
                self.files_list.append(os.path.relpath(filepath, self.root_folder))
                if (not self.recursion):
                    continue
                else:
                    self.scan_directory(filepath, sorting_criteria, reverse_order)
            else:
                self.files_list.append(os.path.relpath(filepath, self.root_folder ))
