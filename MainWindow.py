#author : pierrecnalb
#copyright pierrecnalb
#v.1.0.6
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
import copy
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
        self.limited_action_descriptors = []
        self.directory = os.path.join(os.getcwd(),"Documents","Programs","White-Renamer","test","Test Directory")
        self.files = Renamer.FilesCollection(self.directory, True)
        self.untouched_files = Renamer.FilesCollection(self.directory, True)
        self.original_tree = self.untouched_files.get_basename_tree()
        self.preview_data = self.files.get_basename_tree()
        #----------------------------------INIT UI---------------------------------------
        #---INPUTS DEFINITION---
        original_name_inputs = []
        original_name_inputs.append(Renamer.ActionInput('untouched', 'Untouched', bool))
        original_name_inputs.append(Renamer.ActionInput('uppercase', 'Uppercase', bool))
        original_name_inputs.append(Renamer.ActionInput('lowercase', 'Lowercase', bool))
        original_name_inputs.append(Renamer.ActionInput('titlecase', 'Titlecase', bool))
        character_replacement_inputs = []
        character_replacement_inputs.append(Renamer.ActionInput('old_char', 'Replace', str))
        character_replacement_inputs.append(Renamer.ActionInput('new_char', 'With', str))
        character_insertion_inputs = []
        character_insertion_inputs.append(Renamer.ActionInput('new_char', 'Insert', str))
        character_insertion_inputs.append(Renamer.ActionInput('index', 'at Position', int))
        character_deletion_inputs = []
        character_deletion_inputs.append(Renamer.ActionInput('number_of_char', 'Number of Character', int))
        character_deletion_inputs.append(Renamer.ActionInput('index', 'From Position', int))
        custom_name_inputs = []
        custom_name_inputs.append(Renamer.ActionInput('new_name', 'New Name', str))
        counter_inputs = []
        counter_inputs.append(Renamer.ActionInput('start_index', 'Start At', int))
        counter_inputs.append(Renamer.ActionInput('increment', 'Increment By', int))
        counter_inputs.append(Renamer.ActionInput('restart', 'Restart', "boolean")) #The type "boolean" is to make the difference between checkbox and radiobutton that are both bool.
        foldername_inputs = []
        foldername_inputs.append(Renamer.ActionInput('untouched', 'Untouched', bool))
        foldername_inputs.append(Renamer.ActionInput('uppercase', 'Uppercase', bool))
        foldername_inputs.append(Renamer.ActionInput('lowercase', 'Lowercase', bool))
        foldername_inputs.append(Renamer.ActionInput('titlecase', 'Titlecase', bool))
        #ALL ACTION DESCRIPTOR
        self.all_action_descriptors.append(Renamer.ActionDescriptor("Original Name", original_name_inputs, Renamer.OriginalName))
        self.all_action_descriptors.append(Renamer.ActionDescriptor("Custom Name", custom_name_inputs, Renamer.CustomNameAction))
        self.all_action_descriptors.append(Renamer.ActionDescriptor("Folder Name", foldername_inputs, Renamer.FolderNameUsageAction))
        self.all_action_descriptors.append(Renamer.ActionDescriptor("Find And Replace", character_replacement_inputs, Renamer.CharacterReplacementAction))
        self.all_action_descriptors.append(Renamer.ActionDescriptor("Insert Characters", character_insertion_inputs, Renamer.CharacterInsertionAction))
        self.all_action_descriptors.append(Renamer.ActionDescriptor("Delete Characters", character_deletion_inputs, Renamer.CharacterDeletionAction))
        self.all_action_descriptors.append(Renamer.ActionDescriptor("Counter", counter_inputs, Renamer.Counter))
        #LIMITED ACTION DESCRIPTOR
        self.limited_action_descriptors.append(Renamer.ActionDescriptor("Custom Name", custom_name_inputs, Renamer.CustomNameAction))
        self.limited_action_descriptors.append(Renamer.ActionDescriptor("Folder Name", foldername_inputs, Renamer.FolderNameUsageAction))
        self.limited_action_descriptors.append(Renamer.ActionDescriptor("Counter", counter_inputs, Renamer.Counter))
        #Create Button and Layout
        self.prefix_number = 0
        self.suffix_number = 0
        self.suffix_boxes = []
        self.prefix_boxes = []
        #---LAYOUT---
        self.main_grid = QGridLayout(self)
        self.main_layout = QHBoxLayout()
        self.prefix_layout = QVBoxLayout()
        self.suffix_layout = QVBoxLayout()
        self.spacer_prefix = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.spacer_suffix = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.setLayout(self.main_grid)
        self.main_grid.addLayout(self.main_layout,0,0)
        #---TREE VIEW---
        self.treeView = QTreeView()
        self.treeView.setAlternatingRowColors(True)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([self.tr("Directories"),"test"])
        self.addItems(self.model, self.original_tree, self.preview_data)
        self.treeView.setModel(self.model)
        self.main_grid.addWidget(self.treeView, 1, 0)
        self.treeView.resizeColumnToContents(0)
        #---FOLDER GROUP---
        self.folder_box = ActionButtonGroup("Folder", self.all_action_descriptors)
        self.main_layout.addWidget(self.folder_box)
        self.folder_box.changed.connect(self.apply_action)
        #---PREFIX GROUP---
        self.add_prefix_btn = QToolButton()
        self.add_prefix_btn.setText('+')
        self.add_prefix_btn.clicked.connect(self.add_prefix)
        self.remove_prefix_btn = QToolButton()
        self.remove_prefix_btn.setText('-')
        self.remove_prefix_btn.clicked.connect(self.remove_prefix)
        self.prefix_layout.addWidget(QLabel())
        self.prefix_layout.addWidget(self.add_prefix_btn)
        self.prefix_layout.addWidget(self.remove_prefix_btn)
        self.prefix_layout.addItem(self.spacer_prefix)
        self.main_layout.addLayout(self.prefix_layout)
        #---FILE GROUP---
        self.file_box = ActionButtonGroup("File", self.all_action_descriptors)
        self.main_layout.addWidget(self.file_box)
        self.file_box.changed.connect(self.apply_action)
        #---SUFFIX GROUP---
        self.add_suffix_btn = QToolButton()
        self.add_suffix_btn.setText('+')
        self.add_suffix_btn.clicked.connect(self.add_suffix)
        self.remove_suffix_btn = QToolButton()
        self.remove_suffix_btn.setText('-')
        self.remove_suffix_btn.clicked.connect(self.remove_suffix)
        self.suffix_layout.addWidget(QLabel()) #This empty label is used to get the buttons at the same level as the combobox
        self.suffix_layout.addWidget(self.add_suffix_btn)
        self.suffix_layout.addWidget(self.remove_suffix_btn)
        self.suffix_layout.addItem(self.spacer_suffix)
        self.main_layout.addLayout(self.suffix_layout)
        #---EXTENSION GROUP---
        self.extension_box = ActionButtonGroup("Extension", self.all_action_descriptors)
        self.main_layout.addWidget(self.extension_box)
        self.extension_box.changed.connect(self.apply_action)
        #
        self.preview_btn = QPushButton('Preview')
        self.preview_btn.clicked.connect(self.apply_action)
        self.main_grid.addWidget(self.preview_btn, 2, 0)


    def addItems(self, parent, original_elements, modified_elements):
        """Populate the tree with the selected directory"""
        for i in range(len(original_elements)):
        #for text, children in elements:
            original_files = QStandardItem(original_elements[i][0])
            modified_files = QStandardItem(modified_elements[i][0])
            parent.appendRow([original_files,modified_files])
            original_children = original_elements[i][1]
            modified_children = modified_elements[i][1]
            if original_children:
                self.addItems(original_files, original_children, modified_children)

    def modifyItems(self, parent, modified_elements):
        """Modify the tree with the selected directory"""
        for i in range(len(modified_elements)):
        #for text, children in elements:
            modified_files = QStandardItem(modified_elements[i][0])
            parent.setItem(i,1, modified_files)
            modified_children = modified_elements[i][1]
            if modified_children:
                self.modifyItems(modified_files, modified_children)

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
        self.prefix_box = ActionButtonGroup("Prefix " + str(self.prefix_number), self.limited_action_descriptors)
        self.main_layout.insertWidget(2,self.prefix_box)
        self.prefix_boxes.append(self.prefix_box)
        self.prefix_box.changed.connect(self.apply_action)

    def add_suffix(self):
        self.suffix_number += 1
        self.suffix_box = ActionButtonGroup("Suffix " + str(self.suffix_number), self.limited_action_descriptors)
        self.main_layout.insertWidget(self.prefix_number + self.suffix_number + 3, self.suffix_box)
        self.suffix_boxes.append(self.suffix_box)
        self.suffix_box.changed.connect(self.apply_action)

    def remove_suffix(self):
        if self.suffix_number > 0:
            self.suffix_number -= 1
            self.suffix_boxes[self.suffix_number].destruct_layout()
            del self.suffix_boxes[self.suffix_number]
        else:
            raise Exception("There is no suffix to remove.")
        self.apply_action()

    def remove_prefix(self):
        if self.prefix_number > 0:
            self.prefix_number -= 1
            self.prefix_boxes[self.prefix_number].destruct_layout()
            del self.prefix_boxes[self.prefix_number]
        else:
            raise Exception("There is no prefix to remove.")
        self.apply_action()


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

    def apply_action(self):
        self.actions = []
        self.populate_actions(self.folder_box, "folder")
        for prefix in self.prefix_boxes:
            self.populate_actions(prefix, "prefix")
        self.populate_actions(self.file_box, "file")
        for suffix in self.suffix_boxes:
            self.populate_actions(suffix, "suffix")
        self.populate_actions(self.extension_box, "extension")
        self.files.reset()
        self.files.call_actions(self.actions, self.files.get_files())
        #refresh tree
        self.preview_data = self.files.get_basename_tree()
        #print(self.model.rowCount())
        print(self.modifyItems(self.model, self.preview_data))

    def populate_actions(self, actiongroup, path_part):
        """populate the list of actions depending on the parameters entered in the ActionButtonGroup"""
        (action_descriptor, action_args) = actiongroup.get_inputs()
        action_class = action_descriptor.action_class
        action_instance = action_class(path_part, **action_args)
        self.actions.append(action_instance)


class ActionButtonGroup(QWidget):
    """Group the combobox with the textboxes containing the subactions"""
    changed = Signal() # get changes in order to refresh the preview
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
        #self.selected_action.sub_button.setChecked(True)

    def change(self):
        ''' Change occurs on the layout. '''
        self.changed.emit()

    def on_selected_action_changed(self, index):
        self.selected_action = self.action_descriptors[index]
        self.button_inputs_dict = {}
        self.add_sub_button()
        self.change()

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
        self.change()

    def get_text_changed(self, value):
        self.button_inputs_dict[self.sender().objectName()] = value
        self.change()

    def get_state_changed(self, value):
        state = None
        if value == 0:
            state = False
        elif value == 2:
            state = True
        self.button_inputs_dict[self.sender().objectName()] = state
        self.change()

    def get_integer_changed(self, value):
        try:
            self.button_inputs_dict[self.sender().objectName()] = int(value)
        except:
            raise Exception("Please enter an integer.")
        self.change()

    def clearLayout(self, layout):
        """delete all children of the specified layout"""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clearLayout(child.layout())

    def destruct_layout(self):
        """Delete entire layout."""
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
        """ Opens a file dialog and sets the label to the chosen path """
        import os
        path, _ = QFileDialog.getOpenFileNames(self, "Open File", os.getcwd())

    @Slot()
    def openDirectoryDialog(self):
        """Opens a dialog to allow user to choose a directory """
        flags = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        d = directory = QFileDialog.getExistingDirectory(self,"Open Directory", os.getcwd(), flags)

if __name__ == '__main__':
    main()
