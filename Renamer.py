
#author : pierrecnalb
#copyright pierrecnalb
#v.1.0.2
import os
import time
import shutil
import sys
from os import walk
import operator
language = "english"

class FilesCollection:
    def __init__(self, input_path, use_subdirectory):
        self.input_path = input_path
        self.use_subdirectory = use_subdirectory
        self.original_tree = self.scan(self.input_path)
        self.modified_tree = list(self.original_tree)

    def scan(self, path):
        tree = []
        children = os.listdir(path)
        for child in children:
            if os.path.isdir(os.path.join(path,child)):
                #if (not use_subdirectory):
                #    break
                tree.append([os.path.join(path,child), self.scan(os.path.join(path,child))])
            else:
                tree.append([os.path.join(path,child), []])
        return tree

    def get_files(self):
        return self.modified_tree

    def reset(self):
        self.modified_tree = list(self.original_tree)
        return self.original_tree

    def parselist(self, elements):
        for item in elements:
            if item[1] != []:
                self.data.append(item[0])
                self.parselist(item[1])
            else:
                self.data.append(item[0])
        return self.data

    #def call_actions(self, actions, tree):
    #    for item in tree:
    #        if item[1] != []:
    #            for action in actions:
    #                item[0] = action.call(item[0])
    #            self.call_actions(actions, item[1])
    #        else:
    #            for action in actions:
    #                item[0] = action.call(item[0])
    #    return tree
    def call_actions(self, actions, tree):
        for i in range(len(tree)):
            if tree[i][1] != []:
                for action in actions:
                    tree[i][0] = action.call(tree[i][0])
                self.call_actions(actions, tree[i][1])
            else:
                for action in actions:
                    tree[i][0] = action.call(tree[i][0])
        return tree

class ActionDescriptor:
    def __init__(self, action_name, action_inputs, action_class):
        self.action_name = action_name
        self.action_inputs = action_inputs
        self.action_class = action_class

    def __repr__(self):
        """override string representation of the class"""
        return self.action_name

class ActionInput:
    def __init__(self, arg_name, arg_caption, arg_type):
        self.argument_name = arg_name
        self.argument_caption = arg_caption
        self.argument_type = arg_type

class Action:
    def __init__(self, path_type):
        self.path_type = path_type

    def split_path(self, file_path):
        """Split the entire path into three part."""
        if (os.path.isdir(file_path) is False):
            (self.path, self.filename)=os.path.split(file_path)
            (self.file, self.extension) = os.path.splitext(self.filename)
        else:
            self.path = file_path
            self.file = ""
            self.extension = ""
        return self.path, self.file, self.extension

    def call(self, file_path):
        """Apply action on the specified part."""
        entire_path, file, extension = self.split_path(file_path)
        prefix = ""
        suffix = ""
        path, folder = entire_path.rsplit(os.sep,1)
        #mode = "path|file"
        #flags = mode.split("|")
        #if ("file" in flags):
        #    pass
        if(self.path_type == "file"):
            return os.path.join(entire_path, self.call_on_path_part(file_path, file)) + extension
        elif(self.path_type == "folder"):
            return os.path.join(path, self.call_on_path_part(file_path, folder), file) + extension
        elif(self.path_type == "prefix"):
            return os.path.join(entire_path, self.call_on_path_part(file_path, prefix) + file) + extension
        elif(self.path_type == "suffix"):
            return os.path.join(entire_path, file + self.call_on_path_part(file_path, suffix)) + extension
        elif(self.path_type == "extension"):
            return os.path.join(entire_path, file) + self.call_on_path_part(file_path, extension)
        else:
            raise Exception("path_part not valid")

    def call_on_path_part(self, file_path, path_part):
        raise Exception("not implemented")


class CharacterReplacementAction(Action):
    """Replace old_char by new_char in the section of the path."""
    """path_part can be 'folder', 'file', 'prefix', 'suffix' or 'extension'."""
    def __init__(self, path_type, old_char, new_char):
        Action.__init__(self, path_type)
        self.old_char = old_char
        self.new_char = new_char

    def call_on_path_part(self, file_path, path_part):
        return path_part.replace(self.old_char,self.new_char)

class OriginalName(Action):
    """Return the original name."""
    def __init__(self, path_type, untouched = False, uppercase = False, lowercase = False, titlecase = False):
        Action.__init__(self, path_type)
        self.untouched = untouched
        self.uppercase = uppercase
        self.lowercase = lowercase
        self.titlecase = titlecase

    def call_on_path_part(self, file_path, path_part):
        if self.uppercase is True:
            return path_part.upper()
        elif self.lowercase is True:
            return path_part.lower()
        elif self.titlecase is True:
            return ' '.join([name[0].upper() + name[1:] for name in path_part.split(' ')])
        else:
            return path_part

class CharacterInsertionAction(Action):
    """Insert new_char at index position."""
    def __init__(self, path_type, new_char, index):
        Action.__init__(self, path_type)
        self.new_char = new_char
        self.index = index

    def call_on_path_part(self, file_path, path_part):
        return path_part[:self.index] + self.new_char + path_part[self.index:]

class CharacterDeletionAction(Action):
    """Delete n-character starting from index position."""
    def __init__(self, path_type, number_of_char, index):
        Action.__init__(self, path_type)
        self.number_of_char = number_of_char
        self.index = index

    def call_on_path_part(self, file_path, path_part):
        return path_part[:self.index] + path_part[self.index + self.number_of_char :]

class CustomNameAction(Action):
    """Use a custom name in the filename."""
    def __init__(self, path_type, new_name):
        Action.__init__(self, path_type)
        self.new_name = new_name

    def call_on_path_part(self, file_path, path_part):
        return self.new_name

class FolderNameUsageAction(Action):
    """Use the parent foldername as the filename."""
    def __init__(self, path_type, untouched = False, uppercase = False, lowercase = False, titlecase = False):
        Action.__init__(self, path_type)
        self.untouched = untouched
        self.uppercase = uppercase
        self.lowercase = lowercase
        self.titlecase = titlecase

    def call_on_path_part(self, file_path, path_part):
        (path, file, extension) = self.split_path(file_path)
        foldername = path.rsplit(os.sep,1)[-1]
        if self.uppercase is True:
            return foldername.upper()
        elif self.lowercase is True:
            return foldername.lower()
        elif self.titlecase is True:
            return ' '.join([name[0].upper() + name[1:] for name in foldername.split(' ')])
        else:
            return foldername

class ModifiedTimeUsageAction(Action):
    """Use the modified time metadata as the filename."""
    def call(self, file_path):
        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(self.filenames)
        return time.ctime(mtime)

class Counter(Action):
    """Count the number of files starting from start_index with the given increment."""
    """If restart==True, the counter is set to startindex at each subfolder."""

    def __init__(self, path_type, start_index, increment, restart):
        Action.__init__(self, path_type)
        self.start_index = start_index
        self.increment = increment
        self.restart = restart
        self.counter = 0
        self.previous_path = ""

    def call_on_path_part(self, file_path, path_part):
        path, file, extension = self.split_path(file_path)
        if (path!=self.previous_path and self.restart is True):
            self.counter = self.start_index
        else:
            if(self.counter == 0):
                self.counter = self.start_index
            else:
                self.counter = self.counter + (1 * self.increment)
        self.previous_path=path
        return str(self.counter)

class PipeAction(Action):
    """Execute actions inside another action."""
    def __init__(self, path_type, main_action, sub_action):
        Action.__init__(self, path_type)
        self.main_action = main_action
        self.sub_action = sub_action

    def call_on_path_part(self, file_path, path_part):
        # Execute all left hand side actions to get argument values for the
        # action to execute.
        argumentValues = {}
        for argument_name, argument_provider in self.sub_action.items():
            if isinstance(argument_provider, Action):
                argumentValues[argument_name] = argument_provider.call_on_path_part(file_path, path_part)
            else:
                argumentValues[argument_name] = argument_provider
        # Prepare right hand side for this file.
        action = self.main_action(self.path_part, **argumentValues)
        value = action.call_on_path_part(file_path, path_part)
        return value

class FileDescriptor:
    def __init__(self, path):
        self.path = path
        self.isfile = True # True
        self.name = 'file1' # 'file1'
        self.parentName = 'home/truc' # '/home/truc'

    def is_file(self):
        return os.path.isdir(self.path)

    def get_path(self):
        return self.path

    def get_name(self):
        return os.path.split(self.path)[-1]

#def scan(path):
#    tree = []
#    children = os.listdir(path)
#    for child in children:
#        if os.path.isdir(os.path.join(path,child)):
#            tree.append([FileDescriptor(os.path.join(path,child)), scan(os.path.join(path,child))])
#        else:
#            tree.append([FileDescriptor(os.path.join(path,child)), []])
#    return tree


#    def addItems(self, parent, elements):
#        for text, children in elements:
#            item = QStandardItem(text)
#            parent.appendRow(item)
#            if children:
#                self.addItems(item, children)
#
#mylist=[]
#def parselist(elements):
#    for item in elements:
#        if item[1] != []:
#            mylist.append(item[0].get_name())
#            parselist(item[1])
#        else:
#            mylist.append(item[0].get_name())

directory = "/home/pierre/Desktop/test"
FilesCollection(directory, True)
#data = []
#folders = []
#files = []
#for i, (dirpath, dirnames, filenames) in enumerate(walk(directory)):
#    for filename in filenames:
#        print(filename)
#        files.append((filename,[]))
#    for dirname in dirnames:
#        folders.append((dirname,[]))
#    data[i]
#    data.append(folders)
#    data.append(files)

    #if i == 1:
    #    break
        #print(os.path.split(new_list[i]))
#print(data)
    #actions=[]
    #actions.append(UppercaseConversionAction("file"))
    #print(files.call_actions(actions))
   ### action_dict = {'UPPERCASE' : UppercaseConversionAction("file")}
    #actionClass = CharacterInsertionAction
    #value_searched_in_UI = {'new_char':"test", 'index' : 0}
    #actionArgs = {}
    #for input in actionClass.argument_inputs:
    #    actionArgs[input.argumentName] = value_searched_in_UI[input.argumentName]#valeurquejevaischercherqqpartdanslui
    ###Action.createAction(actionClass, 'shortnmae', **actionArgs) methode statique a implementer
    #actionInstance = actionClass('file', **actionArgs)
    #actions.append(actionInstance)
    #print(files.call_actions(actions))



