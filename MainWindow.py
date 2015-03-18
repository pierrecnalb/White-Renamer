
#author : pierrecnalb
#copyright pierrecnalb
#v.1.0.5
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
    #QMainWindow does not allow any self.main_layout or boxes layout. Therefore we use a QWidget instance
    def __init__(self):
        QWidget.__init__(self)
        self.all_action_descriptors = []
        original_name_inputs = []
        original_name_inputs.append(Renamer.ActionInput('untouched', 'untouched', bool))
        original_name_inputs.append(Renamer.ActionInput('uppercase', 'UPPERCASE', bool))
        original_name_inputs.append(Renamer.ActionInput('lowercase', 'lowercase', bool))
        original_name_inputs.append(Renamer.ActionInput('titlecase', 'TitleCase', bool))
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
        #The type "boolean" is to make the difference between checkbox and radiobutton that are both bool.
        counter_inputs.append(Renamer.ActionInput('restart', 'restart', "boolean"))
        foldername_inputs = []
        foldername_inputs.append(Renamer.ActionInput('untouched', 'untouched', bool))
        foldername_inputs.append(Renamer.ActionInput('uppercase', 'UPPERCASE', bool))
        foldername_inputs.append(Renamer.ActionInput('lowercase', 'lowercase', bool))
        foldername_inputs.append(Renamer.ActionInput('titlecase', 'TitleCase', bool))

        self.all_action_descriptors.append(Renamer.ActionDescriptor("Original name", original_name_inputs, Renamer.OriginalName))
        self.all_action_descriptors.append(Renamer.ActionDescriptor("Find and replace", character_replacement_inputs, Renamer.CharacterReplacementAction))
        self.all_action_descriptors.append(Renamer.ActionDescriptor("Insert characters", character_insertion_inputs, Renamer.CharacterInsertionAction))
        self.all_action_descriptors.append(Renamer.ActionDescriptor("Delete characters", character_deletion_inputs, Renamer.CharacterDeletionAction))
        self.all_action_descriptors.append(Renamer.ActionDescriptor("Custom name", custom_name_inputs, Renamer.CustomNameAction))
        self.all_action_descriptors.append(Renamer.ActionDescriptor("Folder name", foldername_inputs, Renamer.FolderNameUsageAction))
        self.all_action_descriptors.append(Renamer.ActionDescriptor("Counter", counter_inputs, Renamer.Counter))

        #Create Button and Layout
        self.prefix_number = 0
        self.suffix_number = 0
        self.suffix_boxes = []
        self.prefix_boxes = []
        self.main_grid = QGridLayout(self)
        self.setLayout(self.main_grid)
        directory = "/home/pierre/Desktop/test"
        self.model = QFileSystemModel();
        self.model.setRootPath(directory)
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(directory))
        self.path_box = ActionButtonGroup("Path", self.all_action_descriptors)
        self.main_layout = QHBoxLayout()
        self.preview_btn = QPushButton('Preview')
        self.preview_btn.clicked.connect(self.apply_action)
        self.filename_box = ActionButtonGroup("Filename", self.all_action_descriptors)
        self.filename_box.setObjectName('filename_box')
        self.extension_box = ActionButtonGroup("Extension", self.all_action_descriptors)
        self.extension_box.setObjectName('extension_box')
        self.path_lbl = QLabel('Path')
        self.filename_lbl = QLabel('Filename')
        self.extension_lbl = QLabel('Extension')
        self.add_prefix_btn = QToolButton()
        self.add_prefix_btn.setText('+')
        self.remove_prefix_btn = QToolButton()
        self.remove_prefix_btn.setText('-')
        self.add_suffix_btn = QToolButton()
        self.add_suffix_btn.setText('+')
        self.remove_suffix_btn = QToolButton()
        self.remove_suffix_btn.setText('-')
        self.add_prefix_btn.clicked.connect(self.add_prefix)
        self.remove_prefix_btn.clicked.connect(self.remove_prefix)
        self.add_suffix_btn.clicked.connect(self.add_suffix)
        self.remove_suffix_btn.clicked.connect(self.remove_suffix)
        self.prefix_layout = QVBoxLayout()
        self.spacer_prefix = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.prefix_layout.addWidget(QLabel())
        self.prefix_layout.addWidget(self.add_prefix_btn)
        self.prefix_layout.addWidget(self.remove_prefix_btn)
        self.prefix_layout.addItem(self.spacer_prefix)
        self.suffix_layout = QVBoxLayout()
        self.spacer_suffix = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.suffix_layout.addWidget(QLabel())
        self.suffix_layout.addWidget(self.add_suffix_btn)
        self.suffix_layout.addWidget(self.remove_suffix_btn)
        self.suffix_layout.addItem(self.spacer_suffix)
        self.main_layout.addWidget(self.path_box)
        self.main_layout.addLayout(self.prefix_layout)
        self.main_layout.addWidget(self.filename_box)
        self.main_layout.addLayout(self.suffix_layout)
        self.main_layout.addWidget(self.extension_box)
        self.main_grid.addLayout(self.main_layout,0,0)
        self.main_grid.addWidget(self.tree, 1, 0)
        self.main_grid.addWidget(self.preview_btn, 2, 0)

    def clearLayout(self, layout):
        """delete all children of the specified layout"""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clearLayout(child.layout())

    def add_prefix(self):
        self.prefix_number += 1
        self.prefix_box = ActionButtonGroup("Prefix " + str(self.prefix_number), self.all_action_descriptors)
        self.main_layout.insertWidget(2,self.prefix_box)
        self.prefix_boxes.append(self.prefix_box)

    def add_suffix(self):
        self.suffix_number += 1
        self.suffix_box = ActionButtonGroup("Suffix " + str(self.suffix_number), self.all_action_descriptors)
        self.main_layout.insertWidget(self.prefix_number + self.suffix_number + 3, self.suffix_box)
        self.suffix_boxes.append(self.suffix_box)

    def remove_suffix(self):
        if self.suffix_number > 0:
            self.suffix_number -= 1
            self.suffix_boxes[self.suffix_number].destruct_layout()
            del self.suffix_boxes[self.suffix_number]
        else:
            raise Exception("There is no suffix to remove.")

    def remove_prefix(self):
        if self.prefix_number > 0:
            self.prefix_number -= 1
            self.prefix_boxes[self.prefix_number].destruct_layout()
            del self.prefix_boxes[self.prefix_number]
        else:
            raise Exception("There is no prefix to remove.")

    def apply_action(self):
        directory = "/home/pierre/Desktop/test"
        files = Renamer.FilesCollection(directory, False)
        self.actions = []
        #self.populate_actions(self.path_box, 'path')
        self.populate_actions(self.filename_box, 'shortname')
        #self.populate_actions(self.extension_box, 'extension')
        #(path_action_descriptor, path_action_args) = self.path_box.get_inputs()
        for prefix in self.prefix_boxes:
            print(prefix)
            self.populate_actions(prefix, "shortname")

        self.actions.append(Renamer.PipeAction("shortname", Renamer.CharacterInsertionAction, {'new_char' : "shortname", 'index' : 0}))
        #(filename_action_descriptor, filename_action_args) = self.filename_box.get_inputs()
        #(extension_action_descriptor, extension_action_args) = self.extension_box.get_inputs()
        #path_action_class = path_action_descriptor.action_class
        #filename_action_class = filename_action_descriptor.action_class
        #extension_action_class = extension_action_descriptor.action_class
        #path_action_instance = path_action_class('path', **path_action_args)
        #filename_action_instance = filename_action_class('shortname', **filename_action_args)
        #extension_action_instance = extension_action_class('extension', **extension_action_args)
        #actions.append(path_action_instance)
        #actions.append(filename_action_instance)
        #actions.append(extension_action_instance)
        print(files.call_actions(self.actions))

    def populate_actions(self, actiongroup, path_part):
        (action_descriptors, action_args) = actiongroup.get_inputs()
        action_class = action_descriptors.action_class
        action_instance = action_class(path_part, **action_args)
        self.actions.append(action_instance)


class ActionButtonGroup(QWidget):
    """Group the combobox with the textboxes containing the subactions"""
    def __init__(self, frame_name, action_descriptors):
        QWidget.__init__(self)
        self.frame_name = frame_name
        self.combobox = QComboBox()
        self.action_descriptors = action_descriptors
        for element in action_descriptors:
            self.combobox.addItem(str(element))
        self.selected_action = self.action_descriptors[0]
        self.label = QLabel(self.frame_name)
        font = QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.combobox.currentIndexChanged[int].connect(self.on_selected_action_changed)
        self.spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.button_inputs_dict = {}
        self.grid.addWidget(self.label, 0, 0, 1, 1)
        self.grid.addWidget(self.combobox, 1, 0, 1, 1)
        self.add_sub_button()

    def on_selected_action_changed(self, index):
        self.selected_action = self.action_descriptors[index]
        self.button_inputs_dict = {}
        self.add_sub_button()

    def add_sub_button(self):
        sub_buttons = self.grid.itemAtPosition(2,0)
        if sub_buttons is not None:
            self.clearLayout(sub_buttons)
            sub_buttons.deleteLater()
        if self.selected_action and self.selected_action.action_inputs is not None:
            form = QFormLayout()
            self.button_inputs_dict = {}
            for arguments in (self.selected_action.action_inputs):
                label = QLabel()
                label.setText(str(arguments.argument_caption))
                if arguments.argument_type == str:
                    sub_button = QLineEdit()
                    sub_button.textChanged[str].connect(self.get_text_changed)
                elif arguments.argument_type == "boolean":
                    sub_button = QCheckBox()
                    sub_button.stateChanged[int].connect(self.get_state_changed)
                elif arguments.argument_type == bool:
                    sub_button = QRadioButton()
                    sub_button.toggled.connect(self.radio_button_clicked)
                elif arguments.argument_type == int:
                    sub_button = QLineEdit()
                    sub_button.textChanged[str].connect(self.get_integer_changed)
                sub_button.setObjectName(str(arguments.argument_name))
                form.addRow(label, sub_button)
                self.button_inputs_dict[arguments.argument_name] = ""
            self.grid.addLayout(form,2,0,1,1)
        self.grid.addItem(self.spacerItem,3,0,1,1)

    def radio_button_clicked(self, enabled):
        if enabled:
            self.button_inputs_dict[self.sender().objectName()] = True
        else:
            self.button_inputs_dict[self.sender().objectName()] = False

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

    def destruct_layout(self):
        """delete all children of the specified layout"""
        while self.grid.count():
            child = self.grid.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clearLayout(child.layout())
        self.deleteLater()

    def get_inputs(self):
        return self.selected_action, self.button_inputs_dict

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.setWindowTitle('Renamer')
        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(200,200,300,400)
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

if __name__ == '__main__':
    main()
