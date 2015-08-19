#author : pierrecnalb
#copyright pierrecnalb
import os
import sys
import PySide
from PySide.QtCore import *
from PySide.QtGui  import *
from PySide.QtSvg  import *
import ActionManager
import ActionButtonGroup
import FileManager
import resource_rc
import io
class MainWidget(QWidget):
    #QMainWindow does not allow any self.main_layout or boxes layout. Therefore we use a QWidget instance

    def __init__(self):
        QWidget.__init__(self)
        self.files_collection = None
        self.all_action_descriptors = []
        self.prefix_action_descriptors = []
        self.extension_action_descriptors = []
        self.file_or_folder = "file"
        if sys.platform == 'linux':
            self.frame_space = 20
            self.frame_width = 211
            self.frame_height = 240
            self.button_width = 25
        elif sys.platform == 'win32' or sys.platform == 'win64':
            self.frame_space = 20
            self.frame_width = 174
            self.frame_height = 182
            self.button_width = 25
        elif sys.platform == 'darwin':
            self.frame_space = 20
            self.frame_width = 211
            self.frame_height = 230
            self.button_width = 25
        #----------------------------------INIT UI---------------------------------------
        #---INPUTS DEFINITION---
        original_name_inputs = []
        case_change_inputs = []
        case_change_inputs.append(ActionManager.ActionInput('case_choice', "", "combo", "titlecase", [('titlecase', self.tr('Titlecase')), ('uppercase',self.tr('Uppercase')), ('lowercase',self.tr('Lowercase'))]))
        case_change_inputs.append(ActionManager.ActionInput('first_letter', self.tr('First Letter'), "checkable", True))
        case_change_inputs.append(ActionManager.ActionInput('after_symbols', self.tr('And After'), str, "- _" ))
        extension_case_change_inputs = []
        extension_case_change_inputs.append(ActionManager.ActionInput('case_choice', "", "combo", "uppercase" ,[('uppercase',self.tr('Uppercase')), ('lowercase',self.tr('Lowercase'))]))
        #case_change_inputs.append(ActionManager.ActionInput('titlecase', self.tr('Titlecase'), "combo", False))
        character_replacement_inputs = []
        character_replacement_inputs.append(ActionManager.ActionInput('old_char', self.tr('Replace'), str, ""))
        character_replacement_inputs.append(ActionManager.ActionInput('new_char', self.tr('With'), str, ""))
        character_replacement_inputs.append(ActionManager.ActionInput('regex', self.tr('Regex'), "checkable", False))
        character_insertion_inputs = []
        character_insertion_inputs.append(ActionManager.ActionInput('new_char', self.tr('Insert'), str, ""))
        character_insertion_inputs.append(ActionManager.ActionInput('index', self.tr('At Position'), int, 0))
        character_deletion_inputs = []
        character_deletion_inputs.append(ActionManager.ActionInput('starting_position', self.tr('From'), int, 0))
        character_deletion_inputs.append(ActionManager.ActionInput('ending_position', self.tr('To'), int, 1))
        custom_name_inputs = []
        custom_name_inputs.append(ActionManager.ActionInput('new_name', self.tr('New Name'), str, ""))
        counter_inputs = []
        counter_inputs.append(ActionManager.ActionInput('start_index', self.tr('Start At'), int, 0))
        counter_inputs.append(ActionManager.ActionInput('increment', self.tr('Increment'), int, 1))
        date_inputs = []
        date_inputs.append(ActionManager.ActionInput('is_modified_date', self.tr('Modified'), bool, False))
        date_inputs.append(ActionManager.ActionInput('is_created_date', self.tr('Created'), bool, True))
        date_inputs.append(ActionManager.ActionInput('format_display', self.tr('Format'), str, "%Y-%m-%d %H:%M:%S (%A %B)"))
        foldername_inputs = []
        #foldername_inputs.append(ActionManager.ActionInput())
        #ALL ACTION DESCRIPTOR
        self.all_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Original Name"), original_name_inputs, ActionManager.OriginalNameAction))
        self.all_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Case"), case_change_inputs, ActionManager.CaseChangeAction))
        self.all_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Custom Name"), custom_name_inputs, ActionManager.CustomNameAction))
        self.all_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Folder Name"), foldername_inputs, ActionManager.FolderNameUsageAction))
        self.all_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Find And Replace"), character_replacement_inputs, ActionManager.CharacterReplacementAction))
        self.all_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Insert Characters"), character_insertion_inputs, ActionManager.CharacterInsertionAction))
        self.all_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Delete Characters"), character_deletion_inputs, ActionManager.CharacterDeletionAction))
        self.all_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Counter"), counter_inputs, ActionManager.Counter))
        self.all_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Date"), date_inputs, ActionManager.DateAction))
        #PREFIX ACTION DESCRIPTOR
        self.prefix_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Custom Name"), custom_name_inputs, ActionManager.CustomNameAction))
        self.prefix_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Folder Name"), foldername_inputs, ActionManager.FolderNameUsageAction))
        self.prefix_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Counter"), counter_inputs, ActionManager.Counter))
        self.prefix_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Date"), date_inputs, ActionManager.DateAction))
        #EXTENSION ACTION DESCRIPTOR
        self.extension_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Original Name"), original_name_inputs, ActionManager.OriginalNameAction))
        self.extension_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Case"), extension_case_change_inputs, ActionManager.CaseChangeAction))
        self.extension_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Custom Name"), custom_name_inputs, ActionManager.CustomNameAction))
        self.extension_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Find And Replace"), character_replacement_inputs, ActionManager.CharacterReplacementAction))
        self.extension_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Insert Characters"), character_insertion_inputs, ActionManager.CharacterInsertionAction))
        self.extension_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Delete Characters"), character_deletion_inputs, ActionManager.CharacterDeletionAction))
        #Create Button and Layout
        self.prefix_number = 0
        self.suffix_number = 0
        self.suffix_boxes = []
        self.prefix_boxes = []
        #---LAYOUT---
        self.main_grid = QGridLayout(self)
        self.main_grid.setObjectName("main_grid")
        self.setLayout(self.main_grid)
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
        # self.hbox = QHBoxLayout()
        # self.scroll_area_widget_contents.setLayout(self.hbox)
        #---PREFIX GROUP--
        self.add_prefix_btn = QPushButton('+')
        #self.add_prefix_btn.setStyleSheet("QPushButton {border: 1px solid #8f8f91}")
        self.add_prefix_btn.setObjectName("add_prefix_btn")
        #self.add_prefix_btn.setStyleSheet("QPushButton#add_prefix_btn{background-color: rgb(200, 25, 20); border-style:outset; border-radius:15px};")
        #x_coord = self.init_position(self.folder_box)
        x_coord = 10
        #self.add_prefix_btn.setGeometry(QRect(x_coord, 80, self.button_width, self.button_width))
        # self.hbox.addSpacerItem(self.left_spacerItem)
        # self.hbox.addStretch()
        # self.hbox.addWidget(self.add_prefix_btn)
        self.add_prefix_btn.setMaximumSize(20,20)
        self.add_prefix_btn.setSizePolicy( QSizePolicy.Fixed, QSizePolicy.Fixed );
        # self.add_prefix_btn.setParent(self.scroll_area_widget_contents)
        self.add_prefix_btn.clicked.connect(self.add_prefix)
        self.remove_prefix_btn = QPushButton('-')
        self.remove_prefix_btn.setObjectName("remove_prefix_btn")
        self.remove_prefix_btn.clicked.connect(self.remove_prefix)
        self.remove_prefix_btn.setGeometry(QRect(x_coord, 120,self.button_width, self.button_width))
        # self.remove_prefix_btn.setParent(self.scroll_area_widget_contents)
        #---FILE GROUP---
        self.file_box = ActionButtonGroup.ActionButtonGroup(self.tr("File"), self.all_action_descriptors, self.frame_width, self.frame_height)
        x_coord = self.init_position(self.add_prefix_btn)
        # self.file_box.setGeometry(QRect(x_coord, self.frame_space, self.frame_width, self.frame_height))
        self.file_box.setSizePolicy( QSizePolicy.Fixed, QSizePolicy.Fixed );
        self.file_box.setMinimumSize(self.frame_width, self.frame_height)
        # self.hbox.addWidget(self.file_box)
        # self.file_box.setParent(self.scroll_area_widget_contents)
        self.file_box.changed.connect(self.apply_action)
        x_coord = self.init_position(self.file_box)
        #---SUFFIX GROUP---
        self.add_suffix_btn = QPushButton('+')
        self.add_suffix_btn.setObjectName("add_suffix_btn")
        # self.add_suffix_btn.setGeometry(QRect(x_coord, 80,self.button_width, self.button_width))
        # self.add_suffix_btn.setParent(self.scroll_area_widget_contents)
        self.add_suffix_btn.clicked.connect(self.add_suffix)
        self.add_suffix_btn.setMaximumSize(20,20)
        self.add_suffix_btn.setSizePolicy( QSizePolicy.Fixed, QSizePolicy.Fixed );
        # self.hbox.addWidget(self.add_suffix_btn)
        self.remove_suffix_btn = QPushButton('-')
        self.remove_suffix_btn.setObjectName("remove_suffix_btn")
        self.remove_suffix_btn.clicked.connect(self.remove_suffix)
        self.remove_suffix_btn.setGeometry(QRect(x_coord, 120,self.button_width, self.button_width))
        # self.remove_suffix_btn.setParent(self.scroll_area_widget_contents)
            #---EXTENSION GROUP---
        self.extension_box = ActionButtonGroup.ActionButtonGroup(self.tr("Extension"), self.extension_action_descriptors, self.frame_width, self.frame_height)
        self.extension_box.setSizePolicy( QSizePolicy.Fixed, QSizePolicy.Fixed );
        self.extension_box.setMinimumSize(self.frame_width, self.frame_height)
        x_coord = self.init_position(self.add_suffix_btn)
        # self.extension_box.setGeometry(QRect(x_coord, self.frame_space, self.frame_width, self.frame_height))
        # self.extension_box.setParent(self.scroll_area_widget_contents)
        self.extension_box.changed.connect(self.apply_action)
        # self.hbox.addWidget(self.extension_box)
        # self.hbox.addStretch()
        # self.hbox.addSpacerItem(self.right_spacerItem)
        # self.scroll_area_widget_contents.setMinimumSize(self.extension_box.geometry().x()+self.frame_width+self.frame_space,self.frame_height+self.frame_space)
        # self.scroll_area.setMinimumSize(self.extension_box.geometry().x()+self.frame_width+self.frame_space,self.frame_height+2.5*self.frame_space)
        # self.scroll_area.setMaximumSize(10000,self.frame_height+2.5*self.frame_space)




        #Container Widget        
        widget_container = QWidget()
        #Layout of Container Widget
        layout_container = QHBoxLayout()
        layout_container.addWidget(self.add_prefix_btn)
        layout_container.addWidget(self.file_box)
        layout_container.addWidget(self.extension_box)
        widget_container.setLayout(layout_container)
        widget_container.setStyleSheet("QWidget#widget_container{background-color: rgb(213, 213, 213)};")
        #Scroll Area Properties
        scroll = QScrollArea()
        scroll.setObjectName("scroll_area")
        scroll.setAutoFillBackground(False)
        scroll.setStyleSheet("QFrame#scroll_area{border:1px solid rgb(213, 213, 213); border-radius: 4px; padding:2px; background-color: rgb(213, 213, 213)};")
        scroll.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Fixed);
        scroll.setMinimumSize(self.frame_width + 20, self.frame_height + 20)
        scroll.setWidgetResizable(True)
        # scroll_widget_contents = QWidget()
        # scroll_widget_contents.setObjectName("scroll_area_widget_contents")
        scroll.setStyleSheet("QWidget#scroll_area{background-color: rgb(213, 213, 213)};")
        scroll.setWidgetResizable(False)
        scroll.setWidget(widget_container)
        #Scroll Area Layer add 
        hLayout = QHBoxLayout()
        hLayout.addWidget(scroll)
        self.main_grid.addLayout(hLayout,0,0)

        #generatefile
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
        # self.scroll_area.setWidget(self.scroll_area_widget_contents)
        # self.hLayout = QHBoxLayout()
        # self.hLayout.addWidget(self.scroll_area)
        self.folder_icon = QIcon(":/folder_icon.svg")
        self.file_icon = QIcon(":/file_icon.svg")
        self.directory = os.path.join(os.path.dirname(__file__),"UnitTest")

    def remove_action_button_group(self):
        print("pass")

    def on_selector_changed(self, index):
        if index == 0:
            self.file_or_folder = "file"
            self.file_box.set_label(self.tr("File"))
            #---EXTENSION GROUP---
            self.extension_box = ActionButtonGroup.ActionButtonGroup(self.tr("Extension"), self.extension_action_descriptors, self.frame_width, self.frame_height)
            x_coord = self.init_position(self.add_suffix_btn)
            self.extension_box.setGeometry(QRect(x_coord, self.frame_space, self.frame_width, self.frame_height))
            self.extension_box.setParent(self.scroll_area_widget_contents)
            self.extension_box.changed.connect(self.apply_action)
            self.extension_box.show()
            self.scroll_area_widget_contents.setMinimumSize(self.extension_box.geometry().x()+self.frame_width+self.frame_space,self.frame_height)
        elif index == 1:
            self.file_or_folder = "folder"
            self.extension_box.destruct_layout()
            self.file_box.set_label(self.tr("Folder"))
            self.scroll_area_widget_contents.setMinimumSize(self.add_suffix_btn.geometry().x()+self.frame_width+self.frame_space,self.frame_height)
        #---SCROLL AREA----
        self.apply_action()

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

    def input_directory(self, directory, recursion, show_hidden_files, sorting_criteria, reverse_order, filters):
        """Process the selected directory to create the tree and modify the files"""
        self.recursion = recursion
        self.show_hidden_files = show_hidden_files
        self.sorting_criteria = sorting_criteria
        self.reverse_order = reverse_order
        tree = self.main_grid.itemAtPosition(1,0)
        self.model.clear()
        self.model.setHorizontalHeaderLabels([self.tr("Original Files"),self.tr("Modified Files")])
        self.files_collection = FileManager.FilesCollection(directory, recursion, show_hidden_files, sorting_criteria, reverse_order, filters)
        self.root_tree_node = self.files_collection.get_file_system_tree_node()
        self.populate_tree(self.model, self.root_tree_node, True)
        self.treeView.setColumnWidth(0, (self.treeView.columnWidth(0)+self.treeView.columnWidth(1))/2)
        self.apply_action()

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
            modified_file.setEditable(False)
            if isinstance(parent, QStandardItemModel):
                    #parent.itemChanged[QStandardItem].connect(self.tree_item_changed)
                if reset_view:
                    parent.setItem(i,0,original_file)
                parent.setItem(i,1,modified_file)
                self.populate_tree(parent.item(i,0), child, reset_view)
            else:
                if reset_view:
                    parent.setChild(i,0,original_file)
                parent.setChild(i,1,modified_file)
                self.populate_tree(parent.child(i,0), child, reset_view)
    #@Slot()            
    #def tree_item_changed(self, selected_item):
    #    pass
    #    #print(selected_item.row())

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
        if self.file_or_folder == "file":
            self.move_action_button_group(self.extension_box, True)
        self.prefix_box = ActionButtonGroup.ActionButtonGroup(self.tr("Prefix ") + str(self.prefix_number), self.prefix_action_descriptors, self.frame_width, self.frame_height)
        x_left_prefix = self.add_prefix_btn.geometry().x() + self.button_width + self.frame_space
        self.prefix_box.setGeometry(QRect(x_left_prefix, self.frame_space, self.frame_width, self.frame_height))
        self.prefix_box.setParent(self.scroll_area_widget_contents)
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
            if self.file_or_folder == "file":
                self.move_action_button_group(self.extension_box, False)
            #self.scroll_area_widget_contents.setMinimumSize(self.extension_box.geometry().x()+self.frame_width+self.frame_space,self.frame_height)
            self.apply_action()
        else:
            QMessageBox.information(self, "Information", self.tr("There is no prefix to remove."))

    def add_suffix(self):
        self.suffix_number += 1
        self.move_action_button_group(self.add_suffix_btn, True)
        self.move_action_button_group(self.remove_suffix_btn, True)
        if self.file_or_folder == "file":
            self.move_action_button_group(self.extension_box, True)
        self.suffix_box = ActionButtonGroup.ActionButtonGroup(self.tr("Suffix ") + str(self.suffix_number), self.prefix_action_descriptors, self.frame_width, self.frame_height)
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

    def remove_suffix(self):
        if self.suffix_number > 0:
            self.suffix_number -= 1
            self.suffix_boxes[self.suffix_number].destruct_layout()
            del self.suffix_boxes[self.suffix_number]
            self.move_action_button_group(self.add_suffix_btn, False)
            self.move_action_button_group(self.remove_suffix_btn, False)
            if self.file_or_folder == "file":
                self.move_action_button_group(self.extension_box, False)
            # self.scroll_area_widget_contents.setMinimumSize(self.extension_box.geometry().x()+self.frame_width+self.frame_space,self.frame_height)
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
        self.actions = []
        for prefix in self.prefix_boxes:
            self.populate_actions(prefix, "prefix")
        self.populate_actions(self.file_box, self.file_or_folder)
        for suffix in self.suffix_boxes:
            self.populate_actions(suffix, "suffix")
        if self.file_or_folder == "file":
            self.populate_actions(self.extension_box, "extension")
        try:
            self.files_collection.process_file_system_tree_node(self.actions, self.file_or_folder)
        except Exception as e:
            pass
            #QMessageBox.warning(self, "Warning", str(e))
        #refresh tree
        if self.files_collection is not None:
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


