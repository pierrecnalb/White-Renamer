import sys
from renamer import Renamer
from string_range import StringRange

if __name__ is "__main__":
    arguments = sys.argv

path = r"/home/pierre/Documents/Programs/whiterenamer-1.0.0/whiterenamer/model/testcases.t"
# model = DataModel(path, False)
renamer = Renamer(path, False)
string_range = StringRange(1, 3)
renamer.append("CustomName", "foo", string_range)
renamer.append("TitleCase")
# action2 = CustomNameAction("bar")
# renamer.append(action)
# renamer.append(action2)
renamer.invoke_actions()
renamer.batch_rename()
