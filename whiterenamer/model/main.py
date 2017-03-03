from renaming_actions import CustomNameAction
from renamer import Renamer
from string_range import StringRange


path = r"/home/pierre/Documents/Programs/whiterenamer-1.0.0/whiterenamer/model/testcases.t"
# model = FileSystemTreeModel(path, False)
renamer = Renamer(path, False)
string_range = StringRange(-1, 0)
action = renamer.appen_action("CustomName", "FOO")
# action2 = CustomNameAction("bar")
renamer.append_action(action)
# renamer.append_action(action2)
renamer.invoke_actions()
renamer.batch_rename()
