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
import Renamer
language = "english"

def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec_()

class MainWidget(QWidget):
    #QMainWindow does not allow any self.main_grid or boxes layout. Therefore we use a QWidget instance
    def __init__(self):
        QWidget.__init__(self)
        self.all_action_descriptors = []
        character_replacement_inputs = []
        character_replacement_inputs.append(Renamer.ActionInput('old_char', 'replace', str))
        character_replacement_inputs.append(Renamer.ActionInput('new_char', 'with', str))

        character_insertion_inputs = []
        character_insertion_inputs.append(Renamer.ActionInput('new_char', 'insert', str))
        character_insertion_inputs.append(Renamer.ActionInput('index', 'at position', int))

        character_deletion_inputs = []
        character_deletion_inputs.append(Renamer.ActionInput('number_of_char', 'number of character', int))
        character_deletion_inputs.append(Renamer.ActionInput('index', 'from position', int))

        custom_name_inputs = []
        custom_name_inputs.append(Renamer.ActionInput('new_name', 'new name', str))

        counter_inputs = []
        counter_inputs.append(Renamer.ActionInput('start_index', 'start at', int))
        counter_inputs.append(Renamer.ActionInput('increment', 'increment by', int))
        counter_inputs.append(Renamer.ActionInput('restart', 'restart', bool))

        self.all_action_descriptors.append(Renamer.ActionDescriptor("Original Name", None, type(Renamer.OriginalName)))
        self.all_action_descriptors.append(Renamer.ActionDescriptor("Find and replace", character_replacement_inputs, type(Renamer.CharacterReplacementAction)))
        self.all_action_descriptors.append(Renamer.ActionDescriptor("Insert characters", character_insertion_inputs, type(Renamer.CharacterInsertionAction)))
        self.all_action_descriptors.append(Renamer.ActionDescriptor("Delete characters", character_deletion_inputs, type(Renamer.CharacterDeletionAction)))
        self.all_action_descriptors.append(Renamer.ActionDescriptor("Custom name", custom_name_inputs, type(Renamer.CustomNameAction)))
        self.all_action_descriptors.append(Renamer.ActionDescriptor("Folder name", None, type(Renamer.FolderNameUsageAction)))
        self.all_action_descriptors.append(Renamer.ActionDescriptor("Counter", counter_inputs, type(Renamer.Counter)))

        self.actions = []
        #Create Button and Layout
        header = ['Original Files','test']
        data_list = [('test',10)]
        self.prefix_number = 0
        self.suffix_number = 0
        self.main_grid = QGridLayout()
        self.filename_index = 3
        self.extension_index = 5
        self.add_widgets()
        self.action_button_link = {}
        self.subaction_button_link = {}
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
        preview_btn = QPushButton('Preview')
        preview_btn.clicked.connect(self.apply_action)
        self.path_box = ActionButtonGroup("path_box")
        self.path_box.set_action_descriptors(self.all_action_descriptors)
        self.path_box.setObjectName('path_box')
        self.filename_box = ActionButtonGroup("filename_box")
        self.filename_box.set_action_descriptors(self.all_action_descriptors)
        self.filename_box.setObjectName('filename_box')
        #print('after')
        #filename_lbl = QLabel('Filename')
        #extension_box = QComboBox(self)
        #extension_box.setObjectName('extension_box')
        #extension_lbl = QLabel('Extension')
        #path_box = QComboBox(self)
        #path_box.setObjectName('path_box')
        #path_lbl = QLabel('Path')
        #add_prefix_btn = QPushButton('+')
        #add_suffix_btn = QPushButton('+')
        ##populate the combobox
        #combo_list = ['Original Name', 'Insert Characters', 'Delete Characters', 'Find And Replace', 'Custom Name', 'Folder Name', 'Counter']
        #extension_box.addItems(combo_list)
        #path_box.addItems(combo_list)
        #self.action_dict = {'Original Name' : Renamer.OriginalName, 'Insert Characters' : Renamer.CharacterInsertionAction, 'Delete Characters' : Renamer.CharacterDeletionAction, 'Find And Replace' : Renamer.CharacterReplacementAction, 'Custom Name' : Renamer.CustomNameAction, 'Folder Name' : Renamer.FolderNameUsageAction, 'Counter' : Renamer.Counter}
        #connect selection to an action
        #self.filename_box.activated[str].connect(self.activated)
        #extension_box.activated[str].connect(self.add_sub_button)
        #path_box.activated[str].connect(self.add_sub_button)
        #add_prefix_btn.clicked.connect(self.add_prefix)
        #add_suffix_btn.clicked.connect(self.add_suffix)
        #self.main_grid.addWidget(self.path_box, 1, 0, 1, 1)
        self.main_grid.addWidget(preview_btn, 0, 0, 1, 1)
        #self.main_grid.addWidget(add_prefix_btn, 1, 1, 1, 1)
        #for i in range(self.prefix_number):
        #    prefix_box = QComboBox(self)
        #    prefix_box.setObjectName("prefix_box|" + str(i + 1))
        #    prefix_lbl = QLabel('Prefix')
        #    prefix_box.addItems(combo_list)
        #    prefix_box.activated[str].connect(self.add_sub_button)
        #    self.main_grid.addWidget(prefix_lbl, 0, (2 + i), 1, 1)
        #    self.main_grid.addWidget(prefix_box, 1, (2 + i), 1, 1)
        self.main_grid.addWidget(self.filename_box, 1, 1, 1, 1)
        self.main_grid.addWidget(self.path_box, 1, 0, 1, 1)
        #self.main_grid.addWidget(filename_lbl, 0, (self.filename_index), 1, 1)
        #self.main_grid.addWidget(add_suffix_btn, 1, (self.filename_index + 1), 1, 1)
        #for i in range(self.suffix_number):
        #    suffix_box = QComboBox(self)
        #    suffix_box.setObjectName("suffix_box|" + str(i + 1))
        #    suffix_lbl = QLabel('Suffix')
        #    suffix_box.addItems(combo_list)
        #    suffix_box.activated[str].connect(self.add_sub_button)
        #    self.main_grid.addWidget(suffix_lbl, 0, (self.filename_index + i + 2), 1, 1)
        #    self.main_grid.addWidget(suffix_box, 1, (self.filename_index + i + 2), 1, 1)
        #self.main_grid.addWidget(extension_box, 1, (self.extension_index), 1, 1)
        #self.main_grid.addWidget(extension_lbl, 0, (self.extension_index), 1, 1)
        #self.self.main_grid.addWidget(table_view, 2, 0, 3, 3)
        self.path_box.grid_placement(self.main_grid,0)
        self.filename_box.grid_placement(self.main_grid,1)
        self.setLayout(self.main_grid)
        #self.setCentralWidget(self.filename_box)

    def activated(self, value):
        self.add_sub_button(value)
        #Create or update dictionary containing the name of the combobox pressed and the tied action.
        self.action_button_link.update({self.sender().objectName() : self.action_dict[value]})

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

    #def add_sub_button(self, value):
    #    selected_action = self.action_dict[value]
    #    combobox_activated = self.sender()
    #    #specify where should the subbuttons go
    #    if combobox_activated == self.filename_box:
    #        grid_index = self.filename_index
    #    elif combobox_activated == self.extension_box:
    #        grid_index = self.extension_index
    #    elif combobox_activated == self.path_box:
    #        grid_index = 0
    #    elif combobox_activated.objectName().split("|")[0] == "prefix_box":
    #        grid_index = int(combobox_activated.objectName().split("|")[1]) + 1
    #    elif combobox_activated.objectName().split("|")[0] == "suffix_box":
    #        grid_index = int(combobox_activated.objectName().split("|")[1]) + self.filename_index + 1

    #    else:
    #        raise Exception("not implemented")
    #    sub_buttons = self.main_grid.itemAtPosition(2,grid_index)
    #    if sub_buttons is not None:
    #        self.clearLayout(sub_buttons)
    #        sub_buttons.deleteLater()
    #    hbox = QHBoxLayout()
    #    for arguments in (selected_action.INPUTS):
    #        vbox = QVBoxLayout()
    #        label = QLabel(self)
    #        label.setText(str(arguments.argumentCaption))
    #        textbox = QLineEdit(self)
    #        textbox.setObjectName(combobox_activated.objectName() + '|' + str(arguments.argumentName))
    #        textbox.textChanged[str].connect(self.get_subactions)
    #        vbox.addWidget(label)
    #        vbox.addWidget(textbox)
    #        hbox.addLayout(vbox)
    #        self.setLayout(hbox)
    #    self.main_grid.addLayout(hbox,2,grid_index,1,1)

    def get_subactions(self, value):
        #Update the dictionary containing the combobox pressed and the related arguments, each time an argument is updated.
        arg_called = self.sender().objectName()
        (combobox_name, subaction_name) = arg_called.split("|")
        self.subaction_button_link.update({combobox_name : subaction_name})
        #print(self.subaction_button_link[combobox_name])

    def apply_action(self):
        directory = "/home/pierre/Desktop/test"
        files = FilesCollection(directory, False)
        actionClass = self.action_button_link["filename_box"][0]
        #renamedFiles = files.call_actions(self.actions)
        value_searched_in_UI = {'new_char':"test", 'index' : 0}
        actionArgs = {}
        for input in actionClass.INPUTS:
            actionArgs[input.argumentName] = value_searched_in_UI[input.argumentName]#valeurquejevaischercherqqpartdanslui
        actionInstance = actionClass('shortname', **actionArgs)
        self.actions.append(actionInstance)
        #print(files.call_actions(self.actions))

class ActionButtonGroup(QWidget):
    """Group the combobox with the textboxes containing the subactions"""
    def __init__(self, frame_name):
        QWidget.__init__(self)
        self.frame_name = frame_name
        self.all_action_descriptors = None
        self.combobox = QComboBox(self)
        self.label = QLabel(frame_name)
        self.grid = QGridLayout()
        self.grid.addWidget(self.combobox, 0, 0, 1, 1)
        self.combobox.activated[int].connect(self.add_sub_button)

    def set_action_descriptors(self, action_descriptors):
        self.all_action_descriptors = action_descriptors
        for element in action_descriptors:
            self.combobox.addItem(str(element))

    def add_sub_button(self, value):
        selected_action = self.all_action_descriptors[value]
        #combobox_activated = self.sender()
        ##specify where should the subbuttons go
        #if combobox_activated == self.filename_box:
        #    grid_index = self.filename_index
        #elif combobox_activated == self.extension_box:
        #    grid_index = self.extension_index
        #elif combobox_activated == self.path_box:
        #    grid_index = 0
        #elif combobox_activated.objectName().split("|")[0] == "prefix_box":
        #    grid_index = int(combobox_activated.objectName().split("|")[1]) + 1
        #elif combobox_activated.objectName().split("|")[0] == "suffix_box":
        #    grid_index = int(combobox_activated.objectName().split("|")[1]) + self.filename_index + 1

        #else:
        #    raise Exception("not implemented")
        sub_buttons = self.grid.itemAtPosition(1,0)
        print(sub_buttons)
        if sub_buttons is not None:
            self.clearLayout(sub_buttons)
            sub_buttons.deleteLater()
        hbox = QHBoxLayout()
        hbox.setObjectName('test')
        for arguments in (selected_action.action_inputs):
            vbox = QVBoxLayout()
            label = QLabel(self)
            label.setText(str(arguments.argumentCaption))
            textbox = QLineEdit(self)
            #textbox.setObjectName(combobox_activated.objectName() + '|' + str(arguments.argumentName))
            #textbox.textChanged[str].connect(self.get_subactions)
            vbox.addWidget(label)
            vbox.addWidget(textbox)
            hbox.addLayout(vbox)
            #self.setLayout(hbox)
        self.grid.addLayout(hbox,1,0,1,1)
        MainWidget().add_widgets()
        #self.main_grid.addLayout(self.grid,1,self.index,1)
        #self.setLayout(self.main_grid)
    #dict = {.argName : QLineEdit}
    def clearLayout(self, layout):
        """delete all children of the specified layout"""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clearLayout(child.layout())

    def grid_placement(self, main_grid, index):
        self.main_grid = main_grid
        self.index = index




class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.setWindowTitle('Renamer')
        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(200,200,900,600)
        # exit option for the menu bar File menu
        self.exit = QAction('Exit', self)
        # message for the status bar if mouse is over Exit
        #self.exit.setStatusTip('Exit program')
        # newer connect style (PySide/PyQT 4.5 and higher)
        #self.exit.triggered.connect(app.quit)
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



if __name__ == '__main__':
    main()
