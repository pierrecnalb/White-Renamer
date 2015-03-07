#author : pierrecnalb
#copyright pierrecnalb
#v.1.0.1
import os
import time
import shutil
import sys
from os import walk
import operator
import PySide
from PySide.QtCore import *
from PySide.QtGui  import *
language = "english"
class MainWidget(QWidget):
    #QMainWindow does not allow any self.main_grid or boxes layout. Therefore we use a QWidget instance
    def __init__(self):
        QWidget.__init__(self)
        #Create Button and Layout
        header = ['Original Files','test']
        data_list = [('test',10)]
        self.prefix_number = 0
        self.suffix_number = 0
        self.main_grid = QGridLayout()
        self.filename_index = 3
        self.extension_index = 5
        self.add_widgets()
        #table_model = MyTableModel(self, data_list, header)
        #table_view = QTableView(self)
        #table_view.setModel(table_model)
        ## set column width to fit contents (set font first!)
        ##table_view.resizeColumnsToContents()
        ## enable sorting
        ##table_view.setSortingEnabled(True)
        #table_view.setColumnWidth(0,440)
        #table_view.setColumnWidth(1,440)
        #table_view.setGeometry(10, 350, 880, 300)
        #self.action_dict = action_dict
        #self.setGeometry(300,300,300,150)
        #self.actions = []
        #self.files = FilesCollection(directory, False)
        #for i, file_modified in enumerate(self.files.get_files_list()['new']):
         #   data_list.append([self.files.get_files_list()['old'][i], file_modified])
        # addWidget(QWidget, row, column, rowSpan, columnSpan)
    def add_widgets(self):
        #add combobox to the grid depending on the number of prefixes and suffixes
        filename_box = QComboBox(self)
        filename_box.setObjectName('filename_box')
        filename_lbl = QLabel('Filename')
        extension_box = QComboBox(self)
        extension_box.setObjectName('extension_box')
        extension_lbl = QLabel('Extension')
        path_box = QComboBox(self)
        path_box.setObjectName('path_box')
        path_lbl = QLabel('Path')
        add_prefix_btn = QPushButton('+')
        add_suffix_btn = QPushButton('+')
        #populate the combobox
        combo_list = ['Original Name', 'Insert Characters', 'Delete Characters', 'Find And Replace', 'Custom Name', 'Folder Name', 'Counter']
        filename_box.addItems(combo_list)
        extension_box.addItems(combo_list)
        path_box.addItems(combo_list)
        self.action_dict = {'Original Name' : OriginalName, 'Insert Characters' : CharacterInsertionAction, 'Delete Characters' : CharacterDeletionAction, 'Find And Replace' : CharacterReplacementAction, 'Custom Name' : CustomNameAction, 'Folder Name' : FolderNameUsageAction, 'Counter' : Counter}
        #connect selection to an action
        filename_box.activated[str].connect(self.add_sub_button)
        extension_box.activated[str].connect(self.add_sub_button)
        path_box.activated[str].connect(self.add_sub_button)
        add_prefix_btn.clicked.connect(self.add_prefix)
        add_suffix_btn.clicked.connect(self.add_suffix)
        self.main_grid.addWidget(path_box, 1, 0, 1, 1)
        self.main_grid.addWidget(path_lbl, 0, 0, 1, 1)
        self.main_grid.addWidget(add_prefix_btn, 1, 1, 1, 1)
        for i in range(self.prefix_number):
            prefix_box = QComboBox(self)
            prefix_box.setObjectName("prefix_box|" + str(i + 1))
            prefix_lbl = QLabel('Prefix')
            prefix_box.addItems(combo_list)
            prefix_box.activated[str].connect(self.add_sub_button)
            self.main_grid.addWidget(prefix_lbl, 0, (2 + i), 1, 1)
            self.main_grid.addWidget(prefix_box, 1, (2 + i), 1, 1)
        self.main_grid.addWidget(filename_box, 1, (self.filename_index), 1, 1)
        self.main_grid.addWidget(filename_lbl, 0, (self.filename_index), 1, 1)
        self.main_grid.addWidget(add_suffix_btn, 1, (self.filename_index + 1), 1, 1)
        for i in range(self.suffix_number):
            suffix_box = QComboBox(self)
            suffix_box.setObjectName("suffix_box|" + str(i + 1))
            suffix_lbl = QLabel('Suffix')
            suffix_box.addItems(combo_list)
            suffix_box.activated[str].connect(self.add_sub_button)
            self.main_grid.addWidget(suffix_lbl, 0, (self.filename_index + i + 2), 1, 1)
            self.main_grid.addWidget(suffix_box, 1, (self.filename_index + i + 2), 1, 1)
        self.main_grid.addWidget(extension_box, 1, (self.extension_index), 1, 1)
        self.main_grid.addWidget(extension_lbl, 0, (self.extension_index), 1, 1)
        #self.self.main_grid.addWidget(table_view, 2, 0, 3, 3)
        self.setLayout(self.main_grid)

    def add_suffix(self):
        self.suffix_number += 1
        self.extension_index += 1
        self.clearLayout(self.main_grid)
        self.add_widgets()

    def add_prefix(self):
        self.prefix_number += 1
        self.filename_index += 1
        self.extension_index += 1
        self.clearLayout(self.main_grid)
        self.add_widgets()

    def add_sub_button(self, value):
        selected_action = self.action_dict[value]
        button_pressed = self.sender()
        if button_pressed.objectName() == "filename_box":
            grid_index = self.filename_index
        elif button_pressed.objectName() == "extension_box":
            grid_index = self.extension_index
        elif button_pressed.objectName() == "path_box":
            grid_index = 0
        elif button_pressed.objectName().split("|")[0] == "prefix_box":
            grid_index = int(button_pressed.objectName().split("|")[1]) + 1
        elif button_pressed.objectName().split("|")[0] == "suffix_box":
            grid_index = int(button_pressed.objectName().split("|")[1]) + self.filename_index + 1

        else:
            raise Exception("not implemented")
        sub_buttons = self.main_grid.itemAtPosition(2,grid_index)
        if sub_buttons is not None:
            self.clearLayout(sub_buttons)
            sub_buttons.deleteLater()
        hbox = QHBoxLayout()
        for arguments in (selected_action.INPUTS):
            vbox = QVBoxLayout()
            label = QLabel(self)
            label.setText(str(arguments.argumentCaption))
            textbox = QLineEdit(self)
            vbox.addWidget(label)
            vbox.addWidget(textbox)
            hbox.addLayout(vbox)
            self.setLayout(hbox)
        self.main_grid.addLayout(hbox,2,grid_index,1,1)


    def clearLayout(self, layout):
        """delete all children of the specified layout"""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clearLayout(child.layout())

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.setWindowTitle('Renamer')
        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(200,200,900,600)
        # exit option for the menu bar File menu
        self.exit = QAction('Exit', self)
        # message for the status bar if mouse is over Exit
        self.exit.setStatusTip('Exit program')
        # newer connect style (PySide/PyQT 4.5 and higher)
        self.exit.triggered.connect(app.quit)
        # create the menu bar
        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        # now add self.exit
        file.addAction(self.exit)
        # create the status bar
        self.statusBar()
        # QWidget or its instance needed for box layout
        self.widget = MainWidget()
        self.setCentralWidget(self.widget)
        #self.actions.append(self.action_dict[value])
        #renamedFiles = self.files.call_actions(self.actions)
        #print(renamedFiles)
        #actionClass = CharacterInsertionAction
        #value_searched_in_UI = {'new_char':"test", 'index' : 0}
        #actionArgs = {}
        #for input in actionClass.INPUTS:
        #    actionArgs[input.argumentName] = value_searched_in_UI[input.argumentName]#valeurquejevaischercherqqpartdanslui
        #actionInstance = actionClass('shortname', **actionArgs)
        #actions.append(actionInstance)

    @Slot()
    def openFileDialog(self):
        """
        Opens a file dialog and sets the label to the chosen path
        """
        import os
        path, _ = QFileDialog.getOpenFileNames(self, "Open File", os.getcwd())

    @Slot()
    def openDirectoryDialog(self):
        """Opens a dialog to allow user to choose a directory """
        flags = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        d = directory = QFileDialog.getExistingDirectory(self,"Open Directory", os.getcwd(), flags)

class MyTableModel(QAbstractTableModel):
    def __init__(self, parent, mylist, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.mylist = mylist
        self.header = header
    def rowCount(self, parent):
        return len(self.mylist)
    def columnCount(self, parent):
        return len(self.mylist[0])
    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.mylist[index.row()][index.column()]
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None
    def sort(self, col, order):
        """sort table by given column number col"""
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.mylist = sorted(self.mylist,
            key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self.mylist.reverse()
        self.emit(SIGNAL("layoutChanged()"))

class FilesCollection:
    def __init__(self, input_path, use_subdirectory):
        self.input_path = input_path
        self.use_subdirectory = use_subdirectory
        self.original_files_paths = []
        self.modified_files_paths = []
        for(dirpath, dirnames, filenames) in walk(self.input_path):
            for filename in filenames:
                self.original_files_paths.append(os.path.join(dirpath,filename))
            if (not use_subdirectory):
                break

    def get_files_list(self):
        return {'old' : self.original_files_paths, 'new' : self.modified_files_paths}

    def call_actions(self, actions):
        for old_file_path in self.original_files_paths:
            new_file_path = old_file_path
            for action in actions:
                new_file_path = action.call(new_file_path)
            self.modified_files_paths.append(new_file_path)
        return self.modified_files_paths

class ActionInput(object):
    def __init__(self, argName, arg_caption, argType):
        self.argumentName = argName
        self.argumentCaption = arg_caption
        self.argumentType = argType

class Action:
    def __init__(self, path_section):
        self.path_section = path_section

    def split_path(self, file_path):
        """Split the entire path into three part."""
        (self.path, self.filename)=os.path.split(file_path)
        (self.shortname, self.extension) = os.path.splitext(self.filename)
        return self.path, self.shortname, self.extension

    def call(self, file_path):
        """Apply action on the specified part."""
        path, shortname, extension = self.split_path(file_path)
        #mode = "path|shortname"
        #flags = mode.split("|")
        #if ("shortname" in flags):
        #    pass
        if(self.path_section == "shortname"):
            return os.path.join(path, self.call_on_path_part(file_path, shortname)) + extension
        elif(self.path_section == "path"):
            return os.path.join(self.call_on_path_part(file_path, path), shortname) + extension
        elif(self.path_section == "extension"):
            return os.path.join(path, shortname) + self.call_on_path_part(file_path, extension)
        else:
            raise Exception("path_section not valid")

    def call_on_path_part(self, file_path, path_part):
        raise Exception("not implemented")


class CharacterReplacementAction(Action):
    """Replace old_char by new_char in the section of the path."""
    """Path_section can be 'path', 'shortname' or 'extension'."""
    INPUTS = []
    def __init__(self, path_section, old_char, new_char):
        Action.__init__(self, path_section)
        self.old_char = old_char
        self.new_char = new_char

    def call_on_path_part(self, file_path, path_part):
        return path_part.replace(self.old_char,self.new_char)

CharacterReplacementAction.INPUTS.append(ActionInput('old_char', 'replace', str))
CharacterReplacementAction.INPUTS.append(ActionInput('new_char', 'with', str))

class OriginalName(Action):
    """Return the original name."""
    INPUTS = []

    def call_on_path_part(self, file_path, path_part):
        return path_part

class CharacterInsertionAction(Action):
    """Insert new_char at index position."""
    INPUTS = []

    def __init__(self, path_section, new_char, index):
        Action.__init__(self, path_section)
        self.new_char = new_char
        self.index = index

    def call_on_path_part(self, file_path, path_part):
        return path_part[:self.index] + self.new_char + path_part[self.index:]

CharacterInsertionAction.INPUTS.append(ActionInput('new_char','insert',  str))
CharacterInsertionAction.INPUTS.append(ActionInput('index', 'position', int))

class CharacterDeletionAction(Action):
    """Delete n-character starting from index position."""
    INPUTS = []
    def __init__(self, path_section, number_of_char, index):
        Action.__init__(self, path_section)
        self.number_of_char = number_of_char
        self.index = index

    def call_on_path_part(self, file_path, path_part):
        return path_part[:self.index] + path_part[self.index + self.number_of_char :]

CharacterDeletionAction.INPUTS.append(ActionInput('number_of_char', 'number of character', int))
CharacterDeletionAction.INPUTS.append(ActionInput('index', 'from', int))

class UppercaseConversionAction(Action):
    """Convert the string to UPPERCASE."""
    INPUTS = []
    def call_on_path_part(self, file_path, path_part):
        return path_part.upper()

class LowercaseConversionAction(Action):
    """Convert the string to lowercase."""
    INPUTS = []
    def call_on_path_part(self, file_path, path_part):
        return path_part.lower()

class TitlecaseConversionAction(Action):
    """Convert the string to Title Case."""
    INPUTS = []
    def call_on_path_part(self, file_path, path_part):
        if language=="english":
            return ' '.join([name[0].upper()+name[1:] for name in path_part.split(' ')])
        elif language=="french":
            return path_part.title()

class CustomNameAction(Action):
    """Use a custom name in the filename."""
    INPUTS = []
    def __init__(self, path_section, new_name):
        Action.__init__(self, path_section)
        self.new_name = new_name

    def call_on_path_part(self, file_path, path_part):
        return self.new_name
CustomNameAction.INPUTS.append(ActionInput('new_name', 'new name', str))

class FolderNameUsageAction(Action):
    """Use the parent foldername as the filename."""
    INPUTS = []

    def call_on_path_part(self, file_path, path_part):
        (path, shortname, extension) = self.split_path(file_path)
        return path.rsplit(os.sep,1)[-1]

class ModifiedTimeUsageAction(Action):
    """Use the modified time metadata as the filename."""
    INPUTS = []
    def call(self, file_path):
        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(self.filenames)
        return time.ctime(mtime)

class Counter(Action):
    """Count the number of files starting from start_index with the given increment."""
    """If restart==True, the counter is set to startindex at each subfolder."""
    INPUTS = []
    COUNTER = 0
    PREVIOUS_PATH = ""

    def __init__(self, path_section, start_index, increment, restart):
        Action.__init__(self, path_section)
        self.start_index = start_index
        self.increment = increment
        self.restart = restart

    def call_on_path_part(self, file_path, path_part):
        path, shortname, extension = self.split_path(file_path)
        if (path!=Counter.PREVIOUS_PATH and self.restart is True):
            Counter.COUNTER = self.start_index
        else:
            if(Counter.COUNTER == 0):
                Counter.COUNTER = self.start_index
            else:
                Counter.COUNTER = Counter.COUNTER + (1 * self.increment)
        Counter.PREVIOUS_PATH=path
        return str(Counter.COUNTER)

Counter.INPUTS.append(ActionInput('start_index', 'start at', int))
Counter.INPUTS.append(ActionInput('increment', 'increment by',  int))
Counter.INPUTS.append(ActionInput('restart', 'restart', bool))

class PipeAction(Action):
    """Execute actions inside another action."""
    INPUTS = []
    def __init__(self, path_section, main_action, sub_action):
        Action.__init__(self, path_section)
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
        action = self.main_action(self.path_section, **argumentValues)
        value = action.call_on_path_part(file_path, path_part)
        return value

PipeAction.INPUTS.append(ActionInput('main_action','main_action', type))
PipeAction.INPUTS.append(ActionInput('sub_action','main_action', type))


if __name__ == '__main__':
    directory = "/home/pierre/Desktop/test"
    files = FilesCollection(directory, False)
    actions=[]
   # action_dict = {'UPPERCASE' : UppercaseConversionAction("shortname")}
    actionClass = CharacterInsertionAction
    value_searched_in_UI = {'new_char':"test", 'index' : 0}
    actionArgs = {}
    for input in actionClass.INPUTS:
        actionArgs[input.argumentName] = value_searched_in_UI[input.argumentName]#valeurquejevaischercherqqpartdanslui
    #Action.createAction(actionClass, 'shortnmae', **actionArgs) methode statique a implementer
    actionInstance = actionClass('shortname', **actionArgs)
    actions.append(actionInstance)
    #print(files.call_actions(actions))

app = QApplication(sys.argv)
win = MainWindow()
win.show()
app.exec_()
