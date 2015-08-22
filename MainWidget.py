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
        self.init_actions()
        self.init_UI()
        #----------------------------------INIT UI---------------------------------------
        #---INPUTS DEFINITION---
    def init_actions(self):
        original_name_inputs = []
        case_change_inputs = []
        case_change_inputs.append(ActionManager.ActionInput('case_choice', "", "combo", "titlecase", [('titlecase', self.tr('Titlecase')), ('uppercase',self.tr('Uppercase')), ('lowercase',self.tr('Lowercase'))]))
        case_change_inputs.append(ActionManager.ActionInput('first_letter', self.tr('First Letter'), "checkable", True))
        case_change_inputs.append(ActionManager.ActionInput('after_symbols', self.tr('And After'), str, "- _" ))
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
        self.extension_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Case"), case_change_inputs, ActionManager.CaseChangeAction))
        self.extension_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Custom Name"), custom_name_inputs, ActionManager.CustomNameAction))
        self.extension_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Find And Replace"), character_replacement_inputs, ActionManager.CharacterReplacementAction))
        self.extension_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Insert Characters"), character_insertion_inputs, ActionManager.CharacterInsertionAction))
        self.extension_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Delete Characters"), character_deletion_inputs, ActionManager.CharacterDeletionAction))

    def init_UI(self):
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
        self.file_box = ActionButtonGroup.ActionButtonGroup(self.tr("File"), self.all_action_descriptors, self.frame_width, self.frame_height, "file")
        self.file_box.setSizePolicy( QSizePolicy.Fixed, QSizePolicy.Fixed );
        self.file_box.setMinimumSize(self.frame_width, self.frame_height)
        self.file_box.changed.connect(self.apply_action)
        self.file_box.addedBefore.connect(self.add_prefix)
        self.file_box.addedAfter.connect(self.add_suffix)
            #---EXTENSION GROUP---
        self.extension_box = ActionButtonGroup.ActionButtonGroup(self.tr("Extension"), self.extension_action_descriptors, self.frame_width, self.frame_height, "extension")
        self.extension_box.setSizePolicy( QSizePolicy.Fixed, QSizePolicy.Fixed );
        self.extension_box.setMinimumSize(self.frame_width, self.frame_height)
        self.extension_box.changed.connect(self.apply_action)
        #Container Widget        
        widget_container = QWidget()
        #Layout of Container Widget
        self.scroll_area_layout = QHBoxLayout()
        self.scroll_area_layout.addStretch()
        self.scroll_area_layout.addWidget(self.file_box)
        self.scroll_area_layout.addWidget(self.extension_box)
        self.scroll_area_layout.addStretch()
        widget_container.setLayout(self.scroll_area_layout)
        widget_container.setStyleSheet("QWidget#widget_container{background-color: rgb(213, 213, 213)};")
        #Scroll Area Properties
        scroll = QScrollArea()
        scroll.setObjectName("scroll_area")
        scroll.setAutoFillBackground(False)
        scroll.setStyleSheet("QFrame#scroll_area{border:1px solid rgb(213, 213, 213); border-radius: 4px; padding:2px; background-color: rgb(213, 213, 213)};")
        scroll.setSizePolicy( QSizePolicy.Fixed, QSizePolicy.Fixed);
        scroll.setMinimumSize(1000, self.frame_height + 50)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QWidget#scroll_area{background-color: rgb(213, 213, 213)};")
        scroll.setWidgetResizable(True)
        scroll.setWidget(widget_container)
        #Scroll Area Layer add 
        hLayout = QHBoxLayout()
        hLayout.addWidget(scroll)
        self.main_grid.addLayout(hLayout,0,0)
        self.folder_icon = QIcon(":/folder_icon.svg")
        self.file_icon = QIcon(":/file_icon.svg")
        self.directory = os.path.join(os.path.dirname(__file__),"UnitTest")

    def add_prefix(self, widget_caller):
        self.prefix_box = ActionButtonGroup.ActionButtonGroup(self.tr("Prefix"), self.prefix_action_descriptors, self.frame_width, self.frame_height, "prefix")
        self.prefix_box.setSizePolicy( QSizePolicy.Fixed, QSizePolicy.Fixed );
        self.prefix_box.setMinimumSize(self.frame_width, self.frame_height)
        self.prefix_box.addedBefore.connect(self.add_prefix)
        self.prefix_box.removed.connect(self.remove_widget)
        self.prefix_box.changed.connect(self.apply_action)
        self.scroll_area_layout.insertWidget(self.scroll_area_layout.indexOf(widget_caller) , self.prefix_box)

    def add_suffix(self, widget_caller):
        self.suffix_box = ActionButtonGroup.ActionButtonGroup(self.tr("Suffix"), self.prefix_action_descriptors, self.frame_width, self.frame_height, "suffix")
        self.suffix_box.setSizePolicy( QSizePolicy.Fixed, QSizePolicy.Fixed );
        self.suffix_box.setMinimumSize(self.frame_width, self.frame_height)
        self.suffix_box.addedAfter.connect(self.add_suffix)
        self.suffix_box.removed.connect(self.remove_widget)
        self.suffix_box.changed.connect(self.apply_action)
        self.scroll_area_layout.insertWidget(self.scroll_area_layout.indexOf(widget_caller) + 1, self.suffix_box)

    def remove_widget(self, widget_caller):
        self.scroll_area_layout.removeWidget(widget_caller)
        widget_caller.destruct_layout()

    def on_selector_changed(self, index):
        if index == 0:
            self.file_or_folder = "file"
            self.file_box.set_label(self.tr("File"))
            self.file_box.set_frame_type("file")
            self.extension_box.show()
        elif index == 1:
            self.file_or_folder = "folder"
            self.extension_box.hide()
            self.file_box.set_label(self.tr("Folder"))
            self.file_box.set_frame_type("folder")
        self.apply_action()

    def get_action_button_group(self):
        return self.file_box

    def create_file(self, name):
        file = io.open(os.path.join(self.directory, name), 'w')
        file.write(name)
        file.close()

    def create_folder(self, name):
        os.makedirs(os.path.join(self.directory, name))
        
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
        widget_number = self.scroll_area_layout.count()
        for i in range(1, widget_number-1): #do not count the stretch widget
            action_button_group = self.scroll_area_layout.itemAt(i).widget()
            self.populate_actions(action_button_group, action_button_group.get_frame_type())
        # for prefix in self.prefix_boxes:
            # self.populate_actions(prefix, "prefix")
        # self.populate_actions(self.file_box, self.file_or_folder)
        # for suffix in self.suffix_boxes:
            # self.populate_actions(suffix, "suffix")
        # if self.file_or_folder == "file":
            # self.populate_actions(self.extension_box, "extension")
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


