#author : pierrecnalb
#copyright pierrecnalb
#v.1.0.4
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

        self.all_action_descriptors.append(Renamer.ActionDescriptor("Original Name", None, Renamer.OriginalName))
        self.all_action_descriptors.append(Renamer.ActionDescriptor("Find and replace", character_replacement_inputs, Renamer.CharacterReplacementAction))
        self.all_action_descriptors.append(Renamer.ActionDescriptor("Insert characters", character_insertion_inputs, Renamer.CharacterInsertionAction))
        self.all_action_descriptors.append(Renamer.ActionDescriptor("Delete characters", character_deletion_inputs, Renamer.CharacterDeletionAction))
        self.all_action_descriptors.append(Renamer.ActionDescriptor("Custom name", custom_name_inputs, Renamer.CustomNameAction))
        self.all_action_descriptors.append(Renamer.ActionDescriptor("Folder name", None, Renamer.FolderNameUsageAction))
        self.all_action_descriptors.append(Renamer.ActionDescriptor("Counter", counter_inputs, Renamer.Counter))

        #Create Button and Layout
        header = ['Original Files','test']
        data_list = [('test',10)]
        self.prefix_number = 0
        self.suffix_number = 0
        self.filename_index = 3
        self.extension_index = 5
        self.suffix_boxes = []
        self.prefix_boxes = []
        self.preview_btn = QPushButton('Preview')
        self.preview_btn.clicked.connect(self.apply_action)
        self.path_box = ActionButtonGroup("Path")
        self.path_box.set_action_descriptors(self.all_action_descriptors)
        self.path_box.setObjectName('path_box')
        self.path_box.reset_layout()
        self.filename_box = ActionButtonGroup("Filename")
        self.filename_box.set_action_descriptors(self.all_action_descriptors)
        self.filename_box.setObjectName('filename_box')
        self.filename_box.reset_layout()
        self.extension_box = ActionButtonGroup("Extension")
        self.extension_box.set_action_descriptors(self.all_action_descriptors)
        self.extension_box.setObjectName('extension_box')
        self.extension_box.reset_layout()
        self.path_lbl = QLabel('Path')
        self.filename_lbl = QLabel('Filename')
        self.extension_lbl = QLabel('Extension')
        self.add_prefix_btn = QPushButton('+')
        self.remove_prefix_btn = QPushButton('-')
        self.add_suffix_btn = QPushButton('+')
        self.add_prefix_btn.clicked.connect(self.add_prefix)
        self.prefix_layout = QVBoxLayout()
        self.prefix_layout.addWidget(self.add_prefix_btn)
        self.prefix_layout.addWidget(self.remove_prefix_btn)
        self.add_suffix_btn.clicked.connect(self.add_suffix)
        self.main_grid = None
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
        #for i, file_modified in enumerate(self.files.get_files_list()['new']):
         #   data_list.append([self.files.get_files_list()['old'][i], file_modified])
    def add_widgets(self):
        #add AciontButtonGroup to the grid depending on the number of prefixes and suffixes
        self.main_grid = QGridLayout()
        self.main_grid.addWidget(self.preview_btn, 2, 0, 1, 1)
        self.main_grid.addWidget(self.path_box, 1, 0, 1, 1)
        self.main_grid.addLayout(self.prefix_layout, 1, 1, 1, 1)
        if self.prefix_number != 0:
            for i in enumerate(self.prefix_boxes):
                #the last prefix should be added to the most left of the grid.
                self.main_grid.addWidget(self.prefix_boxes[len(self.prefix_boxes) - i -1], 1, (i + 2), 1, 1)
        self.main_grid.addWidget(self.filename_box, 1,(self.filename_index), 1, 1)
        self.main_grid.addWidget(self.add_suffix_btn, 1, (self.filename_index + 1), 1, 1)
        if self.suffix_number != 0:
            for i, suffix_box in enumerate(self.suffix_boxes):
                self.main_grid.addWidget(suffix_box, 1, (self.filename_index + i + 2), 1, 1)
        self.main_grid.addWidget(self.extension_box, 1, (self.extension_index), 1, 1)
        self.setLayout(self.main_grid)
        #self.self.main_grid.addWidget(table_view, 2, 0, 3, 3)

    def add_prefix(self):
        self.prefix_number += 1
        self.filename_index += 1
        self.extension_index += 1
        self.main_grid.deleteLater()
        prefix_box = ActionButtonGroup("Prefix " + str(self.prefix_number))
        prefix_box.set_action_descriptors(self.all_action_descriptors)
        prefix_box.reset_layout()
        self.prefix_boxes.append(prefix_box)
        self.add_widgets()

    def remove_prefix(self):
        self.prefix_number -= 1
        self.filename_index -= 1
        self.extension_index -= 1
        self.main_grid.deleteLater()
        prefix_box.reset_layout()
        del self.prefix_boxes[self.prefix_number]
        self.add_widgets()

    def add_suffix(self):
        self.suffix_number += 1
        self.extension_index += 1
        self.main_grid.deleteLater()
        suffix_box = ActionButtonGroup("Suffix " + str(self.suffix_number))
        suffix_box.set_action_descriptors(self.all_action_descriptors)
        suffix_box.reset_layout()
        self.suffix_boxes.append(suffix_box)
        self.add_widgets()


    def apply_action(self):
        self.add_widgets()
        directory = "/home/pierre/Desktop/test"
        files = Renamer.FilesCollection(directory, False)
        (path_action_descriptor, path_action_args) = self.path_box.get_inputs()
        (filename_action_descriptor, filename_action_args) = self.filename_box.get_inputs()
        (extension_action_descriptor, extension_action_args) = self.extension_box.get_inputs()
        path_action_class = path_action_descriptor.action_class
        filename_action_class = filename_action_descriptor.action_class
        extension_action_class = extension_action_descriptor.action_class
        path_action_instance = path_action_class('path', **path_action_args)
        filename_action_instance = filename_action_class('shortname', **filename_action_args)
        extension_action_instance = extension_action_class('extension', **extension_action_args)
        actions = []
        actions.append(path_action_instance)
        actions.append(filename_action_instance)
        actions.append(extension_action_instance)
        print(files.call_actions(actions))

class ActionButtonGroup(QWidget):
    """Group the combobox with the textboxes containing the subactions"""
    def __init__(self, frame_name):
        QWidget.__init__(self)
        self.frame_name = frame_name
        self.all_action_descriptors = None
        self.combobox = QComboBox()
        self.label = QLabel(frame_name)
        self.combobox.currentIndexChanged[int].connect(self.on_selected_action_changed)
        self.grid = QGridLayout()
        self.button_inputs_dict = {}

    def set_action_descriptors(self, action_descriptors):
        self.all_action_descriptors = action_descriptors
        for element in action_descriptors:
            self.combobox.addItem(str(element))

    def reset_layout(self):
        self.grid.addWidget(self.label, 0, 0, 1, 1)
        self.grid.addWidget(self.combobox, 1, 0, 1, 1)
        self.button_inputs_dict = {}
        self.add_sub_button()
        self.setLayout(self.grid)

    def on_selected_action_changed(self, index):
        self.selected_action = self.all_action_descriptors[index]
        self.reset_layout()
        #self.add_sub_button()

    def add_sub_button(self):
        sub_buttons = self.grid.itemAtPosition(2,0)
        if sub_buttons is not None:
            self.clearLayout(sub_buttons)
            sub_buttons.deleteLater()
        if self.selected_action.action_inputs is not None:
            hbox = QHBoxLayout()
            self.button_inputs_dict = {}
            for arguments in (self.selected_action.action_inputs):
                vbox = QVBoxLayout()
                label = QLabel()
                label.setText(str(arguments.argument_caption))
                if arguments.argument_type == str:
                    sub_button = QLineEdit()
                    sub_button.textChanged[str].connect(self.get_text_changed)
                elif arguments.argument_type == bool:
                    sub_button = QCheckBox()
                    sub_button.stateChanged[int].connect(self.get_state_changed)
                elif arguments.argument_type == int:
                    sub_button = QLineEdit()
                    sub_button.textChanged[str].connect(self.get_integer_changed)
                sub_button.setObjectName(str(arguments.argument_name))
                vbox.addWidget(label)
                vbox.addWidget(sub_button)
                hbox.addLayout(vbox)
                self.button_inputs_dict[arguments.argument_name] = ""
            self.grid.addLayout(hbox,2,0,1,1)

    def get_text_changed(self, value):
        self.button_inputs_dict[self.sender().objectName()] = value

    def get_state_changed(self, value):
        state = None
        if value == 0:
            state = False
        elif value == 2:
            state = True
        self.button_inputs_dict[self.sender().objectName()] = state

    def get_integer_changed(self, value):
        try:
            self.button_inputs_dict[self.sender().objectName()] = int(value)
        except:
            raise Exception("Please enter an integer.")

    def clearLayout(self, layout):
        """delete all children of the specified layout"""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clearLayout(child.layout())

    def get_inputs(self):
        return self.selected_action, self.button_inputs_dict



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
