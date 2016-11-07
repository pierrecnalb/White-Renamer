from file_system_tree_model import FileSystemTreeModel
from action_descriptor import CustomNameActionDescriptor


path = r"/home/pierre/Documents/Programs/whiterenamer-1.0.0/whiterenamer/model/testcases.t"
model = FileSystemTreeModel(path, False)
custom_name_action_descriptor = CustomNameActionDescriptor()
custom_name_action_descriptor.invoke_action(model)

