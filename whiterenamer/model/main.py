from file_system_tree_model import FileSystemTreeModel
from action_descriptor import CustomNameActionDescriptor
from action_descriptor_stack import ActionDescriptorStack


path = r"/home/pierre/Documents/Programs/whiterenamer-1.0.0/whiterenamer/model/testcases.t"
model = FileSystemTreeModel(path, False)
action_descriptor_stack = ActionDescriptorStack()
action1 = CustomNameActionDescriptor("foo")
action2 = CustomNameActionDescriptor("bar")
action_descriptor_stack.append_action(action1)
action_descriptor_stack.append_action(action2)
action_descriptor_stack.execute_all_actions(model)
action_descriptor_stack.rename_all(model)
