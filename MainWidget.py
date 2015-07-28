#author : pierrecnalb
#copyright pierrecnalb
#v.1.0.11
import os
import sys
import PySide
from PySide.QtCore import *
from PySide.QtGui  import *
from PySide.QtSvg  import *
import Renamer
import resource_rc
import io
import ActionButtonGroup
class MainWidget(QWidget):
    #QMainWindow does not allow any self.main_layout or boxes layout. Therefore we use a QWidget instance

    def __init__(self):
        QWidget.__init__(self)
        self.files_collection = None
        self.all_action_descriptors = []
        self.limited_action_descriptors = []
        if sys.platform == 'linux':
            self.frame_space = 20
            self.frame_width = 211
            self.frame_height = 240
            self.button_width = 30
        elif sys.platform == 'win32' or sys.platform == 'win64':
            self.frame_space = 20
            self.frame_width = 174
            self.frame_height = 182
            self.button_width = 30
        #----------------------------------INIT UI---------------------------------------
        #---INPUTS DEFINITION---
        original_name_inputs = []
        case_change_inputs = []
        case_change_inputs.append(Renamer.ActionInput('case_choice', "", "combo", "titlecase", [('titlecase', self.tr('Titlecase')), ('uppercase',self.tr('Uppercase')), ('lowercase',self.tr('Lowercase')),]))
        case_change_inputs.append(Renamer.ActionInput('first_letter', self.tr('First Letter'), "checkable", True))
        case_change_inputs.append(Renamer.ActionInput('after_symbols', self.tr('And After'), str, "- _" ))
        #case_change_inputs.append(Renamer.ActionInput('titlecase', self.tr('Titlecase'), "combo", False))
        character_replacement_inputs = []
        character_replacement_inputs.append(Renamer.ActionInput('old_char', self.tr('Replace'), str, ""))
        character_replacement_inputs.append(Renamer.ActionInput('new_char', self.tr('With'), str, ""))
        character_replacement_inputs.append(Renamer.ActionInput('regex', self.tr('Regex'), "checkable", False))
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
        date_inputs = []
        date_inputs.append(Renamer.ActionInput('is_modified_date', self.tr('Modified'), bool, False))
        date_inputs.append(Renamer.ActionInput('is_created_date', self.tr('Created'), bool, True))
        date_inputs.append(Renamer.ActionInput('format_display', self.tr('Format'), str, "%Y/%m/%d %H:%M:%S (%A %B)"))
        foldername_inputs = []
        #foldername_inputs.append(Renamer.ActionInput())
        #ALL ACTION DESCRIPTOR
        self.all_action_descriptors.append(Renamer.ActionDescriptor(self.tr("Original Name"), original_name_inputs, Renamer.OriginalNameAction))
        self.all_action_descriptors.append(Renamer.ActionDescriptor(self.tr("Case"), case_change_inputs, Renamer.CaseChangeAction))
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
        self.folder_box = ActionButtonGroup.ActionButtonGroup(self.tr("Folder"), self.all_action_descriptors, self.frame_width, self.frame_height)
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
        self.file_box = ActionButtonGroup.ActionButtonGroup(self.tr("File"), self.all_action_descriptors, self.frame_width, self.frame_height)
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
        self.extension_box = ActionButtonGroup.ActionButtonGroup(self.tr("Extension"), self.all_action_descriptors, self.frame_width, self.frame_height)
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
        #generatefile
        self.directory = os.path.join(os.path.dirname(__file__),"UnitTest")
        #self.create_folder("TestCase2")
        #self.directory = os.path.join(os.path.dirname(__file__),"UnitTest", "TestCase2")
        #self.create_folder("FOLDER1")
        #self.create_folder(os.path.join("FOLDER1","sub fOlder_1"))
        #self.create_folder(os.path.join("FOLDER1","sub.FOLDER 2"))
        #self.create_folder("folder 2")
        #self.create_file("file.with.dots.txt")
        #self.create_file("file with é è.txt")
        #self.create_file("file_with_underscore.txt")
        #self.create_file("l'appostrophe.txt")
        #self.create_file(os.path.join("FOLDER1","folder1-file1.txt"))
        #self.create_file(os.path.join("FOLDER1","folder1-sub file #2.txt"))
        #self.create_file(os.path.join("FOLDER1","sub fOlder_1","sub file 1.txt"))
        #self.create_file(os.path.join("FOLDER1","sub fOlder_1","sub file 2.txt"))

    def get_action_button_group(self):
        return self.file_box

    def create_file(self, name):
        file = io.open(os.path.join(self.directory, name), 'w')
        file.write(name)
        file.close()

    def create_folder(self, name):
        os.makedirs(os.path.join(self.directory, name))
        
    def update_x_frame(self):
        self.x_frame += self.frame_width + self.frame_space

    def input_directory(self, directory, recursion, show_hidden_files, sorting_criteria, reverse_order):
        """Process the selected directory to create the tree and modify the files"""
        self.recursion = recursion
        self.show_hidden_files = show_hidden_files
        self.sorting_criteria = sorting_criteria
        self.reverse_order = reverse_order
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
        self.prefix_box = ActionButtonGroup.ActionButtonGroup(self.tr("Prefix ") + str(self.prefix_number), self.limited_action_descriptors, self.frame_width, self.frame_height)
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

    def add_suffix(self):
        self.suffix_number += 1
        self.move_action_button_group(self.add_suffix_btn, True)
        self.move_action_button_group(self.remove_suffix_btn, True)
        self.move_action_button_group(self.extension_box, True)
        self.suffix_box = ActionButtonGroup.ActionButtonGroup(self.tr("Suffix ") + str(self.suffix_number), self.limited_action_descriptors, self.frame_width, self.frame_height)
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

    def rename(self):
        """Rename all the files and folders."""
        try:
            self.files_collection.batch_rename()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        self.populate_tree(self.model, self.root_tree_node, True)
        #self.files_collection.parse_renamed_files(self.directory, self.sorting_criteria, self.reverse_order)
        #self.files_collection.get_renamed_files()
        #shutil.rmtree(self.directory)


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
        try:
            self.files_collection.process_file_system_tree_node(self.actions)
        except Exception as e:
            QMessageBox.warning(self, "Warning", str(e))
        #refresh tree
        self.populate_tree(self.model, self.root_tree_node, False)

    def populate_actions(self, actiongroup, path_part):
        """populate the list of actions depending on the parameters entered in the ActionButtonGroup"""
        (action_descriptor, action_args) = actiongroup.get_inputs()
        action_class = action_descriptor.action_class
        action_instance = action_class(path_part, **action_args)
        self.actions.append(action_instance)

class SizeCalculator(object):
    def __init__(self, main_window):
        self.main_window = main_window
        main_widget = main_window.get_main_widget()
        action_button_group = main_widget.get_action_button_group()
        for i in range(len(action_button_group.get_action_descriptors())):
            action_button_group.on_selected_action_changed(i)
            self.max_height = action_button_group.get_maximum_height()
            self.max_width = action_button_group.get_maximum_width()
        return(self.max_height, self.max_width)


