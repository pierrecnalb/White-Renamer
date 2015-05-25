#author : pierrecnalb
#copyright pierrecnalb
#v.1.0.7
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
import pdb
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
        self.main_grid.setObjectName("main_grid")
        self.main_layout = QHBoxLayout()
        self.main_layout.setObjectName("main_layout")
        self.prefix_layout = QVBoxLayout()
        self.prefix_layout.setObjectName("prefix_layout")
        self.suffix_layout = QVBoxLayout()
        self.suffix_layout.setObjectName("suffix_layout")
        self.spacer_prefix = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.spacer_suffix = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.setLayout(self.main_grid)
        self.main_grid.addLayout(self.main_layout,0,0)
        #---TREE VIEW---
        self.treeView = QTreeView()
        self.treeView.setObjectName("treeView")
        self.treeView.setAlternatingRowColors(True)
        self.model = QStandardItemModel()
        self.model.setObjectName("model")
        self.model.setHorizontalHeaderLabels(["Original Files","Modified Files"])
        self.treeView.setModel(self.model)
        self.main_grid.addWidget(self.treeView, 1, 0)
        #---FOLDER GROUP---
        self.folder_box = ActionButtonGroup("Folder", self.all_action_descriptors)
        self.main_layout.addWidget(self.folder_box)
        self.folder_box.changed.connect(self.apply_action)
        #---PREFIX GROUP---
        self.add_prefix_btn = QToolButton()
        self.add_prefix_btn.setObjectName("add_prefix_btn")
        self.add_prefix_btn.setText('+')
        self.add_prefix_btn.clicked.connect(self.add_prefix)
        self.remove_prefix_btn = QToolButton()
        self.remove_prefix_btn.setObjectName("remove_prefix_btn")
        self.remove_prefix_btn.setText('-')
        self.remove_prefix_btn.clicked.connect(self.remove_prefix)
        self.prefix_layout.addWidget(QLabel())
        self.prefix_layout.addWidget(self.add_prefix_btn)
        self.prefix_layout.addWidget(self.remove_prefix_btn)
        self.prefix_layout.addItem(self.spacer_prefix)
        #self.main_layout.addLayout(self.prefix_layout)
        #---FILE GROUP---
        self.file_box = ActionButtonGroup("File", self.all_action_descriptors)
        self.main_layout.addWidget(self.file_box)
        self.file_box.changed.connect(self.apply_action)
        #---SUFFIX GROUP---
        self.add_suffix_btn = QToolButton()
        self.add_suffix_btn.setObjectName("add_suffix_btn")
        self.add_suffix_btn.setText('+')
        self.add_suffix_btn.clicked.connect(self.add_suffix)
        self.remove_suffix_btn = QToolButton()
        self.remove_suffix_btn.setObjectName("remove_suffix_btn")
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
        self.preview_btn = QPushButton()
        self.preview_btn.setObjectName("preview_btn")
        self.preview_btn.clicked.connect(self.apply_action)
        self.main_grid.addWidget(self.preview_btn, 2, 0)
        self.scroll_area_content= QWidget()
        vlayout = QVBoxLayout(self.scroll_area_content)
        fil_box = ActionButtonGroup("File", self.all_action_descriptors)
        fil_box.setGeometry(10,10,100,100)
        #vlayout.addWidget(QComboBox())
        vlayout.addLayout(self.prefix_layout)
        vlayout.insertWidget(0,fil_box)
        vlayout.addWidget(QComboBox())
        scrollArea = QScrollArea()
        scrollArea.setBackgroundRole(QPalette.Dark)
        scrollArea.setWidget(self.scroll_area_content)
        #fil_box.setLayout(self.scroll_area_content)
        self.main_grid.addWidget(scrollArea,3,0)
        self.folder_icon = QIcon("/home/pierre/Documents/Programs/White-Renamer/Icons/folder_icon.svg")
        self.file_icon = QIcon("/home/pierre/Documents/Programs/White-Renamer/Icons/file_icon.svg")

    def input_directory(self, directory, recursion, show_hidden_files):
        """Process the selected directory to create the tree and modify the files"""
        tree = self.main_grid.itemAtPosition(1,0)
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Original Files","Modified Files"])
        self.files = Renamer.FilesCollection(directory, recursion, show_hidden_files)
        self.preview_data = self.files.get_files()
        self.addItems(self.model, self.preview_data)
        self.treeView.resizeColumnToContents(0)


    def addItems(self, parent, original_elements):
        """Populate the tree with the selected directory"""
        for i in range(len(original_elements)):
            if original_elements[i][0].is_folder:
                icon = self.folder_icon
            else:
                icon = self.file_icon
            original_files = QStandardItem(icon , original_elements[i][0].basename)
            modified_files = QStandardItem(original_elements[i][0].basename)
            parent.appendRow([original_files, modified_files])
            original_children = original_elements[i][1]
            if original_children:
                self.addItems(original_files, original_children)

    def modifyItems(self, parent, modified_elements):
        """Modify the tree with the selected directory"""
        for i in range(len(modified_elements)):
            modified_file = QStandardItem(modified_elements[i][0].basename)
            if isinstance(parent, QStandardItemModel):
                parent.setItem(i,1,modified_file)
                modified_children = modified_elements[i][1]
                self.modifyItems(parent.item(i,0), modified_children)
            else:
                parent.setChild(i,1,modified_file)
                modified_children = modified_elements[i][1]
                self.modifyItems(parent.child(i,0), modified_children)

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
        self.main_layout.insertWidget(self.prefix_number + self.suffix_number + 2, self.suffix_box)
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
        self.preview_data = self.files.get_files()
        #print(self.model.rowCount())
        self.modifyItems(self.model, self.preview_data)

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
        self.frame = QFrame(self)
        self.frame.setObjectName("frame")
        #self.frame.setStyleSheet("background-color: rgb(210, 210, 210);")
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Plain)
        self.frame.setLineWidth(2)
        self.frame.setGeometry(QRect(0, 0, 150, 200))
        self.frame_grid = QGridLayout(self.frame) #this is a hidden grid to handle the objects in the frame as if it was a grid.
        self.frame_grid.setObjectName("frame_grid")
        self.frame_name = frame_name
        self.combobox = QComboBox()
        self.combobox.setObjectName("combobox")
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
        self.grid.setObjectName("grid")
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
            form.setObjectName("form")
            self.button_inputs_dict = {}
            for arguments in (self.selected_action.action_inputs):
                label = QLabel()
                label.setObjectName("label")
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
        self.frame_grid.addLayout(self.grid,0,0,1,1)
        #self.setLayout(self.frame_grid)

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
        self.use_subfolder = False
        self.show_hidden_files = False
        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(200,200,800,600)
        # open option for the menu bar File menu
        self.openAction = QAction(QIcon("/home/pierre/Documents/Programs/White-Renamer/Icons/folder_icon.svg"),'&Open', self)
        self.openAction.setShortcut('Ctrl+o')
        self.openAction.triggered.connect(self.openDirectoryDialog)
        self.recursionAction = QAction('Modify Subfolders Recursively', self)
        self.recursionAction.setShortcut('Ctrl+u')
        self.recursionAction.triggered.connect(self.recursion)
        self.hiddenFilesAction = QAction('Show Hidden Files', self)
        self.hiddenFilesAction.setShortcut('Ctrl+h')
        self.hiddenFilesAction.triggered.connect(self.hide_files)

        self.exit = QAction('Exit', self)
        # message for the status bar if mouse is over Exit
        self.exit.setStatusTip('Exit program')
        #self.exit.triggered.connect(app.quit)
        # create the menu bar
        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        # now add self.exit
        file.addAction(self.exit)
        # create the status bar
        self.statusBar()
        self.main_toolbar = self.addToolBar('main_toolbar')
        self.main_toolbar.addAction(self.openAction)
        self.hide_files_btn = QCheckBox("Show Hidden Files")
        self.hide_files_btn.setObjectName('hide_files_btn')
        self.hide_files_btn.stateChanged[int].connect(self.hide_files)
        
        self.recursion_btn = QCheckBox("Show Subdirectories")
        self.recursion_btn.setObjectName('recursion_btn')
        self.recursion_btn.stateChanged[int].connect(self.recursion)

        #self.folder_icon = QIcon()
        #self.folder_icon.addPixmap(QPixmap(":/icons/Icons/folder.png"), QIcon.Normal, QIcon.On)
    #def addActions(self, target, actions):
    #    '''Actions are added to Tool Bar.'''
    #    for action in actions:
    #        if action is None:
    #            target.addSeparator()
    #        else:
    #            target.addAction(action)
    #
    #def editAction(self, action, slot=None, shortcut=None, icon=None,
    #                 tip=None):
    #    '''This method adds to action: icon, shortcut, ToolTip,\
    #    StatusTip and can connect triggered action to slot '''
    #    if icon is not None:
    #        action.setIcon(QIcon(":/%s.png" % (icon)))
    #    if shortcut is not None:
    #        action.setShortcut(shortcut)
    #    if tip is not None:
    #        action.setToolTip(tip)
    #        action.setStatusTip(tip)
    #    if slot is not None:
    #        action.triggered.connect(slot)                        
    #    return action

        self.main_toolbar.addWidget(self.hide_files_btn)
        self.main_toolbar.addWidget(self.recursion_btn)
        #self.recursion_toolbar = self.addToolBar('Recursion')
        #self.recursion_toolbar.addAction(self.recursionAction)
        #self.hidden_files_toolbar = self.addToolBar('Recursion')
        #self.hidden_files_toolbar.addAction(self.hiddenFilesAction)
        # QWidget or its instance needed for box layout
        self.widget = MainWidget()
        self.setCentralWidget(self.widget)

    @Slot()
    def recursion(self, value):
        if value == 0:
            self.use_subfolder = False
        elif value == 2:
            self.use_subfolder = True
        self.widget.input_directory(self.directory, self.use_subfolder, self.show_hidden_files)

    @Slot()
    def hide_files(self, value):
        if value == 0:
            self.show_hidden_files = False
        elif value == 2:
            self.show_hidden_files = True
        self.widget.input_directory(self.directory, self.use_subfolder, self.show_hidden_files)

    @Slot()
    def openFileDialog(self):
        """ Opens a file dialog and sets the label to the chosen path """
        import os
        path, _ = QFileDialog.getOpenFileNames(self, "Open File", os.getcwd())

    @Slot()
    def openDirectoryDialog(self):
        """Opens a dialog to allow user to choose a directory """
        flags = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        self.directory = QFileDialog.getExistingDirectory(self,"Open Directory", os.getcwd(), flags)
        self.widget.input_directory(self.directory, False, False)


if __name__ == '__main__':
    main()
