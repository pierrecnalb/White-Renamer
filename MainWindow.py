#author : pierrecnalb
#copyright pierrecnalb
#v.1.0.10
import os
import time
import shutil
import sys
from os import walk
import operator
import PySide
from PySide.QtCore import *
from PySide.QtGui  import *
from PySide.QtSvg  import *
import Renamer
import copy
import pdb
import resource_rc
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
    translator = QTranslator()
    translator.load('Translation/tr_fr', os.path.dirname(__file__))
    app.installTranslator(translator)
    win = MainWindow()
    win.show()
    app.exec_()

class MainWidget(QWidget):
    #QMainWindow does not allow any self.main_layout or boxes layout. Therefore we use a QWidget instance

    def __init__(self):
        QWidget.__init__(self)
        self.files_collection = None
        self.all_action_descriptors = []
        self.limited_action_descriptors = []
        self.frame_space = 20
        self.frame_width = 180
        self.frame_height = 200
        self.button_width = 30
        #----------------------------------INIT UI---------------------------------------
        #---INPUTS DEFINITION---
        original_name_inputs = []
        original_name_inputs.append(Renamer.ActionInput('untouched', self.tr('Unchanged'), bool, True))
        original_name_inputs.append(Renamer.ActionInput('uppercase', self.tr('Uppercase'), bool, False))
        original_name_inputs.append(Renamer.ActionInput('lowercase', self.tr('Lowercase'), bool, False))
        original_name_inputs.append(Renamer.ActionInput('titlecase', self.tr('Titlecase'), bool, False))
        character_replacement_inputs = []
        character_replacement_inputs.append(Renamer.ActionInput('old_char', self.tr('Replace'), str, ""))
        character_replacement_inputs.append(Renamer.ActionInput('new_char', self.tr('With'), str, ""))
        character_replacement_inputs.append(Renamer.ActionInput('regex', self.tr('Regex'), "boolean", False))
        character_insertion_inputs = []
        character_insertion_inputs.append(Renamer.ActionInput('new_char', self.tr('Insert'), str, ""))
        character_insertion_inputs.append(Renamer.ActionInput('index', self.tr('At Position'), int, 0))
        character_deletion_inputs = []
        character_deletion_inputs.append(Renamer.ActionInput('starting_position', self.tr('From'), int, 0))
        character_deletion_inputs.append(Renamer.ActionInput('ending_position', self.tr('To'), int, 1))
        custom_name_inputs = []
        custom_name_inputs.append(Renamer.ActionInput('new_name', self.tr('New Name'), str, ""))
        counter_inputs = []
        counter_inputs.append(Renamer.ActionInput('start_index', self.tr('Start At'), int, 0))
        counter_inputs.append(Renamer.ActionInput('increment', self.tr('Increment'), int, 1))
        counter_inputs.append(Renamer.ActionInput('restart', self.tr('Restart'), "boolean", True)) #The type "boolean" is to make the difference between checkbox and radiobutton that are both bool.
        date_inputs = []
        date_inputs.append(Renamer.ActionInput('is_modified_date', self.tr('Modified'), bool, False))
        date_inputs.append(Renamer.ActionInput('is_created_date', self.tr('Created'), bool, True))
        date_inputs.append(Renamer.ActionInput('format_display', self.tr('Format'), str, "%Y %d %B %A %H:%M:%S"))
        foldername_inputs = []
        foldername_inputs.append(Renamer.ActionInput('untouched', self.tr('Untouched'), bool, True))
        foldername_inputs.append(Renamer.ActionInput('uppercase', self.tr('Uppercase'), bool, False))
        foldername_inputs.append(Renamer.ActionInput('lowercase', self.tr('Lowercase'), bool, False))
        foldername_inputs.append(Renamer.ActionInput('titlecase', self.tr('Titlecase'), bool, False))
        #ALL ACTION DESCRIPTOR
        self.all_action_descriptors.append(Renamer.ActionDescriptor(self.tr("Case"), original_name_inputs, Renamer.OriginalName))
        self.all_action_descriptors.append(Renamer.ActionDescriptor(self.tr("Custom Name"), custom_name_inputs, Renamer.CustomNameAction))
        self.all_action_descriptors.append(Renamer.ActionDescriptor(self.tr("Folder Name"), foldername_inputs, Renamer.FolderNameUsageAction))
        self.all_action_descriptors.append(Renamer.ActionDescriptor(self.tr("Find And Replace"), character_replacement_inputs, Renamer.CharacterReplacementAction))
        self.all_action_descriptors.append(Renamer.ActionDescriptor(self.tr("Insert Characters"), character_insertion_inputs, Renamer.CharacterInsertionAction))
        self.all_action_descriptors.append(Renamer.ActionDescriptor(self.tr("Delete Characters"), character_deletion_inputs, Renamer.CharacterDeletionAction))
        self.all_action_descriptors.append(Renamer.ActionDescriptor(self.tr("Counter"), counter_inputs, Renamer.Counter))
        self.all_action_descriptors.append(Renamer.ActionDescriptor(self.tr("Date"), date_inputs, Renamer.DateAction))
        #LIMITED ACTION DESCRIPTOR
        self.limited_action_descriptors.append(Renamer.ActionDescriptor(self.tr("Custom Name"), custom_name_inputs, Renamer.CustomNameAction))
        self.limited_action_descriptors.append(Renamer.ActionDescriptor(self.tr("Folder Name"), foldername_inputs, Renamer.FolderNameUsageAction))
        self.limited_action_descriptors.append(Renamer.ActionDescriptor(self.tr("Counter"), counter_inputs, Renamer.Counter))
        self.limited_action_descriptors.append(Renamer.ActionDescriptor(self.tr("Date"), date_inputs, Renamer.DateAction))
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
        self.treeView.setSortingEnabled(False)
        #self.treeView.setDragDropMode(QAbstractItemView.DropOnly)
        self.model = QStandardItemModel()
        self.model.setObjectName("model")
        self.model.setHorizontalHeaderLabels([self.tr("Original Files"),self.tr("Modified Files")])
        self.treeView.setModel(self.model)
        self.treeView.setColumnWidth(0, (self.treeView.columnWidth(0)+self.treeView.columnWidth(1))/2)
        self.main_grid.addWidget(self.treeView, 1, 0)
               #---FOLDER GROUP---
        self.folder_box = ActionButtonGroup(self.tr("Folder"), self.all_action_descriptors, self.frame_width, self.frame_height)
        self.folder_box.setGeometry(QRect(self.frame_space, self.frame_space, self.frame_width, self.frame_height))
        self.folder_box.setParent(self.scroll_area_widget_contents)
        self.folder_box.changed.connect(self.apply_action)
        #---PREFIX GROUP--
        self.add_prefix_btn = QPushButton('+')
        #self.add_prefix_btn.setStyleSheet("QPushButton {border: 1px solid #8f8f91}")
        self.add_prefix_btn.setObjectName("add_prefix_btn")
        #self.add_prefix_btn.setStyleSheet("QPushButton#add_prefix_btn{background-color: rgb(200, 25, 20); border-style:outset; border-radius:15px};")
        x_coord = self.init_position(self.folder_box)
        self.add_prefix_btn.setGeometry(QRect(x_coord, 80, self.button_width, self.button_width))
        self.add_prefix_btn.setParent(self.scroll_area_widget_contents)
        self.add_prefix_btn.clicked.connect(self.add_prefix)
        self.remove_prefix_btn = QPushButton('-')
        self.remove_prefix_btn.setObjectName("remove_prefix_btn")
        self.remove_prefix_btn.clicked.connect(self.remove_prefix)
        self.remove_prefix_btn.setGeometry(QRect(x_coord, 120,self.button_width, self.button_width))
        self.remove_prefix_btn.setParent(self.scroll_area_widget_contents)
        #---FILE GROUP---
        self.file_box = ActionButtonGroup(self.tr("File"), self.all_action_descriptors, self.frame_width, self.frame_height)
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
        self.extension_box = ActionButtonGroup(self.tr("Extension"), self.all_action_descriptors, self.frame_width, self.frame_height)
        x_coord = self.init_position(self.add_suffix_btn)
        self.extension_box.setGeometry(QRect(x_coord, self.frame_space, self.frame_width, self.frame_height))
        self.extension_box.setParent(self.scroll_area_widget_contents)
        self.extension_box.changed.connect(self.apply_action)
        self.scroll_area_widget_contents.setMinimumSize(self.extension_box.geometry().x()+self.frame_width+self.frame_space,self.frame_height+self.frame_space)
        #---SCROLL AREA----
        self.scroll_area.setMinimumSize(self.extension_box.geometry().x()+self.frame_width+self.frame_space,self.frame_height+2.5*self.frame_space)
        self.scroll_area.setMaximumSize(10000,self.frame_height+2.5*self.frame_space)
        self.scroll_area.setWidget(self.scroll_area_widget_contents)
        self.main_grid.addWidget(self.scroll_area,0,0)
        self.folder_icon = QIcon(":/folder_icon.svg")
        self.file_icon = QIcon(":/file_icon.svg")
        
    def update_x_frame(self):
        self.x_frame += self.frame_width + self.frame_space

    def input_directory(self, directory, recursion, show_hidden_files, sorting_criteria, reverse_order):
        """Process the selected directory to create the tree and modify the files"""
        tree = self.main_grid.itemAtPosition(1,0)
        self.model.clear()
        self.model.setHorizontalHeaderLabels([self.tr("Original Files"),self.tr("Modified Files")])
        self.files_collection = Renamer.FilesCollection(directory, recursion, show_hidden_files, sorting_criteria, reverse_order)
        self.root_tree_node = self.files_collection.get_file_system_tree_node()
        self.populate_tree(self.model, self.root_tree_node, True)
        self.treeView.setColumnWidth(0, (self.treeView.columnWidth(0)+self.treeView.columnWidth(1))/2)

    def populate_tree(self, parent, tree_node, reset_view):
        """Populate the tree with the selected directory. If reset_view is False, only the modified_files are updated."""
        children = tree_node.get_children()
        for i, child in enumerate(children):
            if child.original_filedescriptor.is_folder:
                icon = self.folder_icon
            else:
                icon = self.file_icon
            original_file = QStandardItem(icon, child.original_filedescriptor.basename)
            original_file.setEditable(False)
            modified_file = QStandardItem(child.modified_filedescriptor.basename)
            if isinstance(parent, QStandardItemModel):
                parent.itemChanged[QStandardItem].connect(self.tree_item_changed)
                if reset_view:
                    parent.setItem(i,0,original_file)
                parent.setItem(i,1,modified_file)
                self.populate_tree(parent.item(i,0), child, reset_view)
            else:
                if reset_view:
                    parent.setChild(i,0,original_file)
                parent.setChild(i,1,modified_file)
                self.populate_tree(parent.child(i,0), child, reset_view)
    @Slot()            
    def tree_item_changed(self, selected_item):
        pass
        #print(selected_item.row())

    def init_position(self, action_button_group):
        """Initialize the position and the size of the ActionButtonGroup in the frame."""
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
        self.prefix_box = ActionButtonGroup(self.tr("Prefix ") + str(self.prefix_number), self.limited_action_descriptors, self.frame_width, self.frame_height)
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
            QMessageBox.information(self, "Information", self.tr("There is no prefix to remove."))
            raise Exception("There is no prefix to remove.")

    def add_suffix(self):
        self.suffix_number += 1
        self.move_action_button_group(self.add_suffix_btn, True)
        self.move_action_button_group(self.remove_suffix_btn, True)
        self.move_action_button_group(self.extension_box, True)
        self.suffix_box = ActionButtonGroup(self.tr("Suffix ") + str(self.suffix_number), self.limited_action_descriptors, self.frame_width, self.frame_height)
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
            QMessageBox.information(self, "Information", self.tr("There is no suffix to remove."))
            raise Exception("There is no suffix to remove.")

    def rename(self):
        """Rename all the files and folders."""
        self.files_collection.batch_rename()
        self.populate_tree(self.model, self.root_tree_node, True)

    def undo(self):
        """Undo the previous renaming action."""
        self.files_collection.batch_undo()
        self.populate_tree(self.model, self.root_tree_node, True)

    def apply_action(self):
        if self.files_collection is None:
            QMessageBox.information(self, "Information", "Please select a directory.")
            return
        self.actions = []
        self.populate_actions(self.folder_box, "folder")
        for prefix in self.prefix_boxes:
            self.populate_actions(prefix, "prefix")
        self.populate_actions(self.file_box, "file")
        for suffix in self.suffix_boxes:
            self.populate_actions(suffix, "suffix")
        self.populate_actions(self.extension_box, "extension")
        self.files_collection.process_file_system_tree_node(self.actions)

        #refresh tree
        self.populate_tree(self.model, self.root_tree_node, False)

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
            form.rowWrapPolicy =QFormLayout.WrapLongRows
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
                    sub_button.setText(str(arguments.argument_caption))
                    label.setText("")
                    sub_button.setChecked(arguments.default_value)
                    sub_button.toggled.connect(self.radio_button_clicked)
                elif arguments.argument_type == int:
                    sub_button = QSpinBox()
                    sub_button.setValue(arguments.default_value)
                    sub_button.valueChanged[int].connect(self.get_integer_changed)
                sub_button.setObjectName(str(arguments.argument_name))
                form.addRow(label, sub_button)
                self.button_inputs_dict[arguments.argument_name] = arguments.default_value
            self.grid.addLayout(form,2,0,1,1)
        self.grid.addItem(self.spacerItem,3,0,1,1)

    def radio_button_clicked(self, enabled):
        if enabled:
            self.button_inputs_dict[self.sender().objectName()] = True
            self.change()
        else:
            self.button_inputs_dict[self.sender().objectName()] = False

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
            self.button_inputs_dict[self.sender().objectName()] = value
        except ValueError:
            self.on_show_information(self.tr("Please enter an integer."))
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
        self.directory = None
        self.use_subfolder = False
        self.show_hidden_files = False
        self.sorting_criteria = "name"
        self.reverse_order = False
        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(200,200,800,600)
        
        self.tab = QWidget()
        self.plainTextEdit = QPlainTextEdit(self.tab)

        #CREATE THE ACTIONS
        self.action_open = QAction(self.tr('&Open'), self)
        self.action_open = self.edit_action(self.action_open, self.open_directory_dialog_click, None, 'ctrl+o', "new_icon.svg" ,self.tr('Exit program.'))
        self.action_exit = QAction(self.tr('&Exit'), self)
        self.action_exit = self.edit_action(self.action_exit, self.close, None,'ctrl+q', None,self.tr('Open directory dialog.'))
        self.action_help = QAction(self.tr('&Help'), self)
        self.action_help = self.edit_action(self.action_help, self.help_click, None, 'ctrl+h', 'help_icon.svg', self.tr('Show help page.'))
        self.action_about = QAction(self.tr('&About'), self)
        self.action_about = self.edit_action(self.action_about, self.about_box_click, None, None, None,self.tr('Pop About Box.'))
        self.action_recursion = QAction(self.tr('Recursion'), self)
        self.action_recursion = self.edit_action(self.action_recursion, self.recursion_click, bool, 'alt+r', "subdirectory_icon.svg",self.tr('Rename subdirectories recursively.'))
        self.action_recursion.setCheckable(True)
        self.action_hide = QAction(self.tr('Show Hidden Files'), self)
        self.action_hide = self.edit_action(self.action_hide, self.hide_files_click, bool, 'alt+h', "hidden_icon.svg",self.tr('Show hidden files.'))
        self.action_hide.setCheckable(True)
        self.action_add_prefix = QAction(self.tr('Add Prefix'), self)
        self.action_add_prefix = self.edit_action(self.action_add_prefix, self.add_prefix_click, None, None, None,self.tr('Add prefix.'))
        self.action_add_suffix = QAction(self.tr('Add Suffix'), self)
        self.action_add_suffix = self.edit_action(self.action_add_suffix, self.add_suffix_click, None, None, None,self.tr('Add suffix.'))
        self.action_remove_prefix = QAction(self.tr('Remove Prefix'), self)
        self.action_remove_prefix = self.edit_action(self.action_remove_prefix, self.remove_prefix_click, None, None, None,self.tr('Remove prefix.'))
        self.action_remove_suffix = QAction(self.tr('Remove Suffix'), self)
        self.action_remove_suffix = self.edit_action(self.action_remove_suffix, self.remove_suffix_click, None, None, None,self.tr('Remove suffix.'))
        self.action_rename = QAction(self.tr('Run'), self)
        self.action_rename = self.edit_action(self.action_rename, self.rename_click, None, 'ctrl+enter', "run_icon.svg",self.tr('Rename the files/folders.'))
        self.action_undo = QAction(self.tr('Undo'), self)
        self.action_undo = self.edit_action(self.action_undo, self.undo_click, None, 'ctrl+z', "undo_icon.svg",self.tr('Undo the previous renaming.'))
        self.action_reverse_sorting = QAction(self.tr('Reverse'), self)
        self.action_reverse_sorting.setCheckable(True)
        self.action_reverse_sorting = self.edit_action(self.action_reverse_sorting, self.reverse_sorting_click, bool, None, "order_icon.svg",self.tr('Reverse the sorting order.'))
        self.action_name_sorting = QAction(self.tr('By Name'), self)
        self.action_name_sorting.setCheckable(True)
        self.action_name_sorting = self.edit_action(self.action_name_sorting, self.name_sorting_click, None, None, None,self.tr('Sort the files/folders by name.'))
        self.action_size_sorting = QAction(self.tr('By Size'), self)
        self.action_size_sorting.setCheckable(True)
        self.action_size_sorting = self.edit_action(self.action_size_sorting, self.size_sorting_click, None, None, None,self.tr('Sort the files/folders by size.'))
        self.action_modified_date_sorting = QAction(self.tr('By Modified Date'), self)
        self.action_modified_date_sorting.setCheckable(True)
        self.action_modified_date_sorting = self.edit_action(self.action_modified_date_sorting, self.modified_date_sorting_click, None, None, None,self.tr('Sort the files/folders by modified date.'))
        self.action_creation_date_sorting = QAction(self.tr('By Creation Date'), self)
        self.action_creation_date_sorting.setCheckable(True)
        self.action_creation_date_sorting = self.edit_action(self.action_creation_date_sorting, self.creation_date_sorting_click, None, None, None,self.tr('Sort the files/folders by creation date.'))
        # CREATE THE MENU BAR
        menubar = self.menuBar()
        #FILE
        menu_file = menubar.addMenu(self.tr('&File'))
        menu_file.addAction(self.action_open)
        menu_file.addSeparator()
        menu_file.addAction(self.action_hide)
        menu_file.addAction(self.action_recursion)
        menu_file.addSeparator()
        menu_file.addAction(self.action_exit)
        #EDIT
        menu_edit = menubar.addMenu(self.tr('&Sort'))
        menu_edit.addAction(self.action_name_sorting)
        menu_edit.addAction(self.action_size_sorting)
        menu_edit.addAction(self.action_creation_date_sorting)
        menu_edit.addAction(self.action_modified_date_sorting)
        menu_edit.addSeparator()
        menu_edit.addAction(self.action_reverse_sorting)
        #menu_edit.addAction(self.action_add_prefix)
        #menu_edit.addAction(self.action_add_suffix)
        #menu_edit.addAction(self.action_remove_prefix)
        #menu_edit.addAction(self.action_remove_suffix)
        #TOOL
        menu_tool = menubar.addMenu(self.tr('&Tool'))
        menu_tool.addAction(self.action_rename)
        menu_tool.addAction(self.action_undo)
        #HELP
        menu_help = menubar.addMenu(self.tr('&Help'))
        menu_help.addAction(self.action_help)
        menu_help.addAction(self.action_about)

        self.main_toolbar = self.addToolBar('main_toolbar')
        self.main_toolbar.addAction(self.action_open)
        self.main_toolbar.addSeparator()
        self.main_toolbar.addAction(self.action_hide)
        self.main_toolbar.addAction(self.action_recursion)
        self.main_toolbar.addSeparator()
        self.main_toolbar.addAction(self.action_rename)
        self.main_toolbar.addAction(self.action_undo)
        self.main_toolbar.addSeparator()
        self.main_toolbar.addAction(self.action_help)

        # create the status bar
        self.statusBar()
        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)

    def edit_action(self, action, slot=None, type=None, shortcut=None, icon=None,
                     tip=None):
        '''This method adds to action: icon, shortcut, ToolTip,\
        StatusTip and can connect triggered action to slot '''
        if icon is not None:
            action.setIcon(QIcon(":/%s" % (icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered[type].connect(slot)
        return action

    def help_click(self):
        '''Read and display a help file- currently the README.txt.'''
        self.plainTextEdit.setPlainText(open('README.md').read())

    def about_box_click(self):
        '''Popup a box with about message.'''
        QMessageBox.about(self, "About PySide, Platform and the like",
                """<b>Part of Structural Analysis.</b> v %s
                <p>Copyright &copy; 2015 Pierre BLANC. 
                All rights reserved in accordance with
                Creative Commons Attribution Licence (CCPL) v3
                or later - NO WARRANTIES!
                <p>This progam """ )
    @Slot()
    def recursion_click(self, value):
        self.use_subfolder = value
        if self.directory is None:
            return
        self.update_directory()

    @Slot()
    def hide_files_click(self, value):
        if value == False:
            self.show_hidden_files = False
        elif value == True:
            self.show_hidden_files = True
        if self.directory is None:
            return
        self.update_directory()

    @Slot()
    def open_directory_dialog_click(self):
        """Opens a dialog to allow user to choose a directory """
        flags = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        #self.directory = QFileDialog.getExistingDirectory(self,"Open Directory", os.getcwd(), flags)
        self.directory = os.path.join(os.path.dirname(__file__),"test","Test Directory")
        #self.directory = r"C:\Users\pblanc\Desktop\test"
        self.main_widget.input_directory(self.directory, self.use_subfolder, self.show_hidden_files, self.sorting_criteria, self.reverse_order)

    @Slot()
    def add_prefix_click(self):
        self.main_widget.add_prefix()
    @Slot()
    def add_suffix_click(self):
        self.main_widget.add_suffix()
    @Slot()
    def remove_prefix_click(self):
        self.main_widget.remove_prefix()
    @Slot()
    def remove_suffix_click(self):
        self.main_widget.remove_suffix()

    @Slot()
    def reverse_sorting_click(self, value):
        self.reverse_order = value
        self.update_directory()

    @Slot()
    def name_sorting_click(self):
        self.action_name_sorting.setChecked(True)
        self.action_creation_date_sorting.setChecked(False)
        self.action_modified_date_sorting.setChecked(False)
        self.action_size_sorting.setChecked(False)
        self.sorting_criteria = "name"
        self.update_directory()
    @Slot()
    def size_sorting_click(self):
        self.action_size_sorting.setChecked(True)
        self.action_name_sorting.setChecked(False)
        self.action_creation_date_sorting.setChecked(False)
        self.action_modified_date_sorting.setChecked(False)
        self.sorting_criteria = "size"
        self.update_directory()
    @Slot()
    def creation_date_sorting_click(self):
        self.action_creation_date_sorting.setChecked(True)
        self.action_name_sorting.setChecked(False)
        self.action_modified_date_sorting.setChecked(False)
        self.action_size_sorting.setChecked(False)
        self.sorting_criteria = "creation_date"
        self.update_directory()
    @Slot()
    def modified_date_sorting_click(self):
        self.action_modified_date_sorting.setChecked(True)
        self.action_name_sorting.setChecked(False)
        self.action_creation_date_sorting.setChecked(False)
        self.action_size_sorting.setChecked(False)
        self.sorting_criteria = "modified_date"
        self.update_directory()

    def update_directory(self):
            self.main_widget.input_directory(self.directory, self.use_subfolder, self.show_hidden_files, self.sorting_criteria, self.reverse_order)
            self.main_widget.apply_action()

    @Slot()
    def rename_click(self):
        self.main_widget.rename()

    @Slot()
    def undo_click(self):
        self.main_widget.undo()


if __name__ == '__main__':
    main()
