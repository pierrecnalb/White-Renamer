#author : pierrecnalb
#copyright pierrecnalb
#v.1.0.9
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
    app.setStyle(QStyleFactory.create("fusion"))
    palette = QPalette()
    #palette.setColor(QPalette.Window, QColor(210,210,210));
    #palette.setColor(QPalette.WindowText, Qt.white);
    #palette.setColor(QPalette.Base, Qt.white);
    #palette.setColor(QPalette.AlternateBase, QColor(53,53,53));
    #palette.setColor(QPalette.ToolTipBase, Qt.white);
    #palette.setColor(QPalette.ToolTipText, Qt.white);
    #palette.setColor(QPalette.Text, Qt.red);
    #palette.setColor(QPalette.Button, QColor(53,53,53));
    #palette.setColor(QPalette.ButtonText, Qt.red);
    #palette.setColor(QPalette.BrightText, Qt.red);
    #palette.setColor(QPalette.Highlight, QColor(142,45,197).lighter());
    palette.setColor(QPalette.HighlightedText, Qt.green);
    app.setPalette(palette);
    win = MainWindow()
    win.show()
    app.exec_()

class MainWidget(QWidget):
    #QMainWindow does not allow any self.main_layout or boxes layout. Therefore we use a QWidget instance

    def __init__(self):
        QWidget.__init__(self)
        self.all_action_descriptors = []
        self.limited_action_descriptors = []
        self.frame_space = 20
        self.frame_width = 170
        self.frame_height = 200
        self.button_width = 30
        #----------------------------------INIT UI---------------------------------------
        #---INPUTS DEFINITION---
        original_name_inputs = []
        original_name_inputs.append(Renamer.ActionInput('untouched', 'Untouched', bool, True))
        original_name_inputs.append(Renamer.ActionInput('uppercase', 'Uppercase', bool, False))
        original_name_inputs.append(Renamer.ActionInput('lowercase', 'Lowercase', bool, False))
        original_name_inputs.append(Renamer.ActionInput('titlecase', 'Titlecase', bool, False))
        character_replacement_inputs = []
        character_replacement_inputs.append(Renamer.ActionInput('old_char', 'Replace', str, ""))
        character_replacement_inputs.append(Renamer.ActionInput('new_char', 'With', str, ""))
        character_insertion_inputs = []
        character_insertion_inputs.append(Renamer.ActionInput('new_char', 'Insert', str, ""))
        character_insertion_inputs.append(Renamer.ActionInput('index', 'at Position', int, 0))
        character_deletion_inputs = []
        character_deletion_inputs.append(Renamer.ActionInput('number_of_char', 'Number of Character', int, 0))
        character_deletion_inputs.append(Renamer.ActionInput('index', 'From Position', int, 0))
        custom_name_inputs = []
        custom_name_inputs.append(Renamer.ActionInput('new_name', 'New Name', str, ""))
        counter_inputs = []
        counter_inputs.append(Renamer.ActionInput('start_index', 'Start At', int, 0))
        counter_inputs.append(Renamer.ActionInput('increment', 'Increment By', int, 1))
        counter_inputs.append(Renamer.ActionInput('restart', 'Restart', "boolean", True)) #The type "boolean" is to make the difference between checkbox and radiobutton that are both bool.
        foldername_inputs = []
        foldername_inputs.append(Renamer.ActionInput('untouched', 'Untouched', bool, True))
        foldername_inputs.append(Renamer.ActionInput('uppercase', 'Uppercase', bool, False))
        foldername_inputs.append(Renamer.ActionInput('lowercase', 'Lowercase', bool, False))
        foldername_inputs.append(Renamer.ActionInput('titlecase', 'Titlecase', bool, False))
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
        self.setLayout(self.main_grid)
        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("scroll_area")
        self.scroll_area.setAutoFillBackground(False)
        self.scroll_area.setStyleSheet("QFrame#scroll_area{border:2px solid rgb(213, 213, 213); border-radius: 4px; padding:2px; background-color: rgb(220, 220, 220)};")
        self.scroll_area.setWidgetResizable(True)
        #self.scroll_area.setBackgroundRole(QPalette.Dark)
        self.scroll_area_widget_contents = QWidget()
        self.scroll_area_widget_contents.setObjectName("scroll_area_widget_contents")
        self.scroll_area_widget_contents.setStyleSheet("QWidget#scroll_area_widget_contents{background-color: rgb(250, 250, 250)};")
        #---TREE VIEW---
        self.treeView = QTreeView()
        self.treeView.setStyleSheet("QTreeView{border:2px solid rgb(213, 213, 213); border-radius: 4px};")
        self.treeView.setObjectName("treeView")
        self.treeView.setAlternatingRowColors(True)
        self.model = QStandardItemModel()
        self.model.setObjectName("model")
        self.model.setHorizontalHeaderLabels(["Original Files","Modified Files"])
        self.treeView.setModel(self.model)
        self.treeView.setColumnWidth(0, (self.treeView.columnWidth(0)+self.treeView.columnWidth(1))/2)
        self.treeView.setSortingEnabled(True)
        self.main_grid.addWidget(self.treeView, 1, 0)
               #---FOLDER GROUP---
        self.folder_box = ActionButtonGroup("Folder", self.all_action_descriptors, self.frame_width, self.frame_height)
        self.folder_box.setGeometry(QRect(self.frame_space, self.frame_space, self.frame_width, self.frame_height))
        self.folder_box.setParent(self.scroll_area_widget_contents)
        self.folder_box.changed.connect(self.apply_action)
        #---PREFIX GROUP--
        self.add_prefix_btn = QPushButton('+')
        #self.add_prefix_btn.setStyleSheet("QPushButton {border: 1px solid #8f8f91}")
        self.add_prefix_btn.setObjectName("add_prefix_btn")
        self.add_prefix_btn.setStyleSheet("QPushButton#add_prefix_btn{background-color: rgb(200, 25, 20); border-style:outset; border-radius:15px};")
        #self.add_prefix_btn.setStyleSheet("QPushButton#add_prefix_btn:pressed{background-color: rgb(20, 25, 20); border-style:inset};")
        x_coord = self.init_position(self.folder_box)
        self.add_prefix_btn.setGeometry(QRect(x_coord, 80, self.button_width, self.button_width))
        self.add_prefix_btn.setParent(self.scroll_area_widget_contents)
        self.add_prefix_btn.clicked.connect(self.add_prefix)
        self.remove_prefix_btn = QPushButton('-')
        self.remove_prefix_btn.setObjectName("remove_prefix_btn")
        self.remove_prefix_btn.clicked.connect(self.remove_prefix)
        self.remove_prefix_btn.setGeometry(QRect(x_coord, 120,self.button_width, self.button_width))
        self.remove_prefix_btn.setParent(self.scroll_area_widget_contents)
        #self.main_layout.addLayout(self.prefix_layout)
        #---FILE GROUP---
        self.file_box = ActionButtonGroup("File", self.all_action_descriptors, self.frame_width, self.frame_height)
        x_coord = self.init_position(self.add_prefix_btn)
        self.file_box.setGeometry(QRect(x_coord, self.frame_space, self.frame_width, self.frame_height))
        self.file_box.setParent(self.scroll_area_widget_contents)
        self.file_box.changed.connect(self.apply_action)
        #---SUFFIX GROUP---
        self.add_suffix_btn = QPushButton('+')
        self.add_suffix_btn.setObjectName("add_suffix_btn")
        x_coord = self.init_position(self.file_box)
        self.add_suffix_btn.setGeometry(QRect(x_coord, 80,self.button_width, self.button_width))
        self.add_suffix_btn.setParent(self.scroll_area_widget_contents)
        self.add_suffix_btn.clicked.connect(self.add_suffix)
        self.remove_suffix_btn = QPushButton('-')
        self.remove_suffix_btn.setObjectName("remove_suffix_btn")
        self.remove_suffix_btn.clicked.connect(self.remove_suffix)
        self.remove_suffix_btn.setGeometry(QRect(x_coord, 120,self.button_width, self.button_width))
        self.remove_suffix_btn.setParent(self.scroll_area_widget_contents)
        #---EXTENSION GROUP---
        self.extension_box = ActionButtonGroup("Extension", self.all_action_descriptors, self.frame_width, self.frame_height)
        x_coord = self.init_position(self.add_suffix_btn)
        self.extension_box.setGeometry(QRect(x_coord, self.frame_space, self.frame_width, self.frame_height))
        self.extension_box.setParent(self.scroll_area_widget_contents)
        self.extension_box.changed.connect(self.apply_action)
        self.scroll_area_widget_contents.setMinimumSize(self.extension_box.geometry().x()+self.frame_width+self.frame_space,self.frame_height+self.frame_space)
        #---SCROLL AREA----
        self.preview_btn = QPushButton()
        self.preview_btn.setObjectName("preview_btn")
        self.preview_btn.clicked.connect(self.test)
        self.scroll_area.setMinimumSize(self.extension_box.geometry().x()+self.frame_width+self.frame_space,self.frame_height+2.5*self.frame_space)
        self.scroll_area.setMaximumSize(10000,self.frame_height+2.5*self.frame_space)
        self.scroll_area.setWidget(self.scroll_area_widget_contents)
        self.main_grid.addWidget(self.scroll_area,0,0)
        self.main_grid.addWidget(self.preview_btn, 2, 0)
        self.folder_icon = QIcon("/home/pierre/Documents/Programs/White-Renamer/Icons/folder_icon.svg")
        self.file_icon = QIcon("/home/pierre/Documents/Programs/White-Renamer/Icons/file_icon.svg")
        
    def update_x_frame(self):
        self.x_frame += self.frame_width + self.frame_space

    def input_directory(self, directory, recursion, show_hidden_files):
        """Process the selected directory to create the tree and modify the files"""
        tree = self.main_grid.itemAtPosition(1,0)
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Original Files","Modified Files"])
        self.files = Renamer.FilesCollection(directory, recursion, show_hidden_files)
        self.preview_data = self.files.get_file_system_tree_node()
        self.addItems(self.model, self.preview_data)
        self.treeView.setColumnWidth(0, (self.treeView.columnWidth(0)+self.treeView.columnWidth(1))/2)

    def list_children(self, tree_node):
        children = tree_node.get_children()
        if children:
            for child in tree_node.get_children():
                print(child.original_filedescriptor.basename)
                self.list_children(child)
        else:
            print(tree_node.original_filedescriptor.basename)

    def addItems(self, parent, tree_node):
        """Populate the tree with the selected directory"""
        children = tree_node.get_children()
        original_files = QStandardItem(tree_node.original_filedescriptor.basename)
        modified_files = QStandardItem(tree_node.original_filedescriptor.basename)
        if children:
            for child in children:
                self.addItems(original_files, child)
        parent.appendRow([original_files, modified_files])

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

    def init_position(self, action_button_group):
        x_coord = action_button_group.geometry().x()
        x_coord += action_button_group.size().width() + self.frame_space
        return x_coord

    def move_action_button_group(self, action_button_group, is_added):
        x_coord = action_button_group.geometry().x()
        if(is_added):
            x_coord += self.frame_width + self.frame_space
        else:
            x_coord -= (self.frame_width + self.frame_space)
        action_button_group.move(x_coord, action_button_group.geometry().y())



    def add_prefix(self):
        self.prefix_number += 1
        if(self.prefix_number >= 1):
            for prefix in self.prefix_boxes:
                self.move_action_button_group(prefix, True)
        self.move_action_button_group(self.file_box, True)
        if(self.suffix_number >= 0):
            for suffix in self.suffix_boxes:
                self.move_action_button_group(suffix, True)
        self.move_action_button_group(self.add_suffix_btn, True)
        self.move_action_button_group(self.remove_suffix_btn, True)
        self.move_action_button_group(self.extension_box, True)
        self.prefix_box = ActionButtonGroup("Prefix " + str(self.prefix_number), self.limited_action_descriptors, self.frame_width, self.frame_height)
        x_left_prefix = self.add_prefix_btn.geometry().x() + self.button_width + self.frame_space
        self.prefix_box.setGeometry(QRect(x_left_prefix, self.frame_space, self.frame_width, self.frame_height))
        self.prefix_box.setParent(self.scroll_area_widget_contents)
        self.scroll_area_widget_contents.setMinimumSize(self.extension_box.geometry().x()+self.frame_width+self.frame_space,self.frame_height)
        self.prefix_box.show()
        self.prefix_boxes.append(self.prefix_box)
        self.prefix_box.changed.connect(self.apply_action)

    def remove_prefix(self):
        if self.prefix_number > 0:
            self.prefix_number -= 1
            self.prefix_boxes[self.prefix_number].destruct_layout()
            del self.prefix_boxes[self.prefix_number]
            for prefix in self.prefix_boxes:
                self.move_action_button_group(prefix, False)
            self.move_action_button_group(self.file_box, False)
            if(self.suffix_number >= 0):
                for suffix in self.suffix_boxes:
                    self.move_action_button_group(suffix, False)
            self.move_action_button_group(self.add_suffix_btn, False)
            self.move_action_button_group(self.remove_suffix_btn, False)
            self.move_action_button_group(self.extension_box, False)
            self.scroll_area_widget_contents.setMinimumSize(self.extension_box.geometry().x()+self.frame_width+self.frame_space,self.frame_height)
            self.apply_action()
        else:
            QMessageBox.information(self, "Information", "There is no prefix to remove.")
            raise Exception("There is no prefix to remove.")

    def add_suffix(self):
        self.suffix_number += 1
        self.move_action_button_group(self.add_suffix_btn, True)
        self.move_action_button_group(self.remove_suffix_btn, True)
        self.move_action_button_group(self.extension_box, True)
        self.suffix_box = ActionButtonGroup("Suffix " + str(self.suffix_number), self.limited_action_descriptors, self.frame_width, self.frame_height)
        if(self.suffix_number > 1):
            x_left_suffix = self.init_position(self.suffix_boxes[-1])
        else:
            x_left_suffix = self.file_box.geometry().x() + self.frame_width + self.frame_space
        self.suffix_box.setGeometry(QRect(x_left_suffix, self.frame_space, self.frame_width, self.frame_height))
        self.suffix_box.setParent(self.scroll_area_widget_contents)
        self.scroll_area_widget_contents.baseSize()
        self.suffix_box.show()
        self.suffix_boxes.append(self.suffix_box)
        self.suffix_box.changed.connect(self.apply_action)
        self.scroll_area_widget_contents.setMinimumSize(self.extension_box.geometry().x()+self.frame_width+self.frame_space,self.frame_height)

    def remove_suffix(self):
        if self.suffix_number > 0:
            self.suffix_number -= 1
            self.suffix_boxes[self.suffix_number].destruct_layout()
            del self.suffix_boxes[self.suffix_number]
            self.move_action_button_group(self.add_suffix_btn, False)
            self.move_action_button_group(self.remove_suffix_btn, False)
            self.move_action_button_group(self.extension_box, False)
            self.scroll_area_widget_contents.setMinimumSize(self.extension_box.geometry().x()+self.frame_width+self.frame_space,self.frame_height)
            self.apply_action()
        else:
            QMessageBox.information(self, "Information", "There is no suffix to remove.")
            raise Exception("There is no suffix to remove.")



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

    def test(self):
        self.files.rename(self.files.get_original_files(), self.files.get_file_system_tree_node())

    def apply_action(self):
        self.actions = []
        self.populate_actions(self.folder_box, "folder")
        for prefix in self.prefix_boxes:
            self.populate_actions(prefix, "prefix")
        self.populate_actions(self.file_box, "file")
        for suffix in self.suffix_boxes:
            self.populate_actions(suffix, "suffix")
        self.populate_actions(self.extension_box, "extension")
        #self.files.reset()
        self.files.execute_method_on_node(self.files.get_file_system_tree_node(),self.files.call_actions,self.actions)
        #refresh tree
        self.preview_data = self.files.get_file_system_tree_node()
        #self.modifyItems(self.model, self.preview_data)

    def populate_actions(self, actiongroup, path_part):
        """populate the list of actions depending on the parameters entered in the ActionButtonGroup"""
        (action_descriptor, action_args) = actiongroup.get_inputs()
        action_class = action_descriptor.action_class
        action_instance = action_class(path_part, **action_args)
        self.actions.append(action_instance)


class ActionButtonGroup(QWidget):
    """Group the combobox with the textboxes containing the subactions"""
    changed = Signal() # get changes in order to refresh the preview
    def __init__(self, frame_name, action_descriptors, frame_width, frame_height):
        QWidget.__init__(self)
        self.frame = QFrame(self)
        self.frame.setObjectName("frame")
        if ("Prefix" in frame_name or "Suffix" in frame_name):
            self.frame.setStyleSheet("QFrame#frame{border:1px solid rgb(190, 190, 190); border-radius: 4px; padding:2px; background-color: rgb(230, 230, 230)};")
        else:
            self.frame.setStyleSheet("QFrame#frame{border:2px solid rgb(203, 203, 203); border-radius: 10px; padding:2px; background-color: rgb(244, 244, 244)};")
        self.frame.setGeometry(QRect(0, 0, frame_width, frame_height))
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
        self.frame_grid.addLayout(self.grid,0,0,1,1)

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
                    sub_button.setText(arguments.default_value)
                    sub_button.textChanged[str].connect(self.get_text_changed)
                elif arguments.argument_type == "boolean":
                    sub_button = QCheckBox()
                    sub_button.setChecked(arguments.default_value)
                    sub_button.stateChanged[int].connect(self.get_state_changed)
                elif arguments.argument_type == bool:
                    sub_button = QRadioButton()
                    sub_button.setChecked(arguments.default_value)
                    sub_button.toggled.connect(self.radio_button_clicked)
                elif arguments.argument_type == int:
                    sub_button = QLineEdit()
                    sub_button.setText(str(arguments.default_value))
                    sub_button.textChanged[str].connect(self.get_integer_changed)
                sub_button.setObjectName(str(arguments.argument_name))
                form.addRow(label, sub_button)
                self.button_inputs_dict[arguments.argument_name] = arguments.default_value
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
        if value=="":
            value = 0
        try:
            self.button_inputs_dict[self.sender().objectName()] = int(value)
        except ValueError:
            self.on_show_information("Please enter an integer.")
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
        
    def on_show_information(self, warning_message):
        """Show the information message"""
        QMessageBox.information(self, "Information", warning_message)

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
        #path, _ = QFileDialog.getOpenFileNames(self, "Open File", os.getcwd())
        path = "/home/pierre/Documents/Programs/White-Renamer/test/Test Directory"

    @Slot()
    def openDirectoryDialog(self):
        """Opens a dialog to allow user to choose a directory """
        flags = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        #self.directory = QFileDialog.getExistingDirectory(self,"Open Directory", os.getcwd(), flags)
        self.directory = "/home/pierre/Documents/Programs/White-Renamer/test/Test Directory"
        self.widget.input_directory(self.directory, False, False)


if __name__ == '__main__':
    main()
