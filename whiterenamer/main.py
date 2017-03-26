import sys
from renamer import Renamer
from string_range import StringRange

if __name__ is "__main__":
    arguments = sys.argv

path = r"/home/pierre/Documents/Programs/whiterenamer-1.0.0/whiterenamer/model/testcases.t"
# model = FileSystemTreeModel(path, False)
renamer = Renamer(path, False)
string_range = StringRange(1, 3)
renamer.append_action("CustomName", "foo", string_range)
renamer.append_action("TitleCase")
# action2 = CustomNameAction("bar")
# renamer.append_action(action)
# renamer.append_action(action2)
renamer.invoke_actions()
renamer.batch_rename()
