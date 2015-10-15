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
import pdb
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
            self.frame_width = 280
            self.frame_height = 350
            self.button_width = 25
        elif sys.platform == 'win32' or sys.platform == 'win64':
            self.frame_space = 20
            self.frame_width = 174
            self.frame_height = 182
            self.button_width = 25
        elif sys.platform == 'darwin':
            self.frame_space = 20
            self.frame_width = 210
            self.frame_height = 210
            self.button_width = 25
        self.init_actions()
        self.init_UI()
        #----------------------------------INIT UI---------------------------------------
        #---INPUTS DEFINITION---
    def init_actions(self):
        original_name_inputs = []
        case_change_inputs = []
        first_letter_inputs = []
        first_letter_inputs.append(ActionManager.ActionInput('first_letter', self.tr('First Letter'), "checkable", True))
        first_letter_inputs.append(ActionManager.ActionInput('after_symbols', self.tr('And After'), str, "- _" ))
        uppercase_inputs = []
        lowercasecase_inputs = []
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
        image_metadata_inputs = []
        image_date_time_original = []
        image_date_time_original.append(ActionManager.ActionInput('time_format', self.tr('Format'), str, "%Y-%m-%d %H:%M:%S"))

        image_f_number = []
        image_exposure_time = []
        image_iso = []
        image_camera_model = []
        image_x_dimension = []
        image_y_dimension = []
        image_focal_length = []
        image_artist = []
        music_metadata_inputs = []
        music_artist = []
        music_title = []
        music_year = []
        music_album = []
        music_genre = []
        music_track = []
        case_action_descriptors = []
        case_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Titlecase"), first_letter_inputs, ActionManager.TitleCaseAction))
        case_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Uppercase"), uppercase_inputs, ActionManager.UpperCaseAction))
        case_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Lowercase"), lowercasecase_inputs, ActionManager.LowerCaseAction))
        image_action_descriptors = []
        image_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Original Date"), image_date_time_original, ActionManager.ImageDateTimeOriginal))
        image_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("F Number"), image_f_number, ActionManager.ImageFNumber))
        image_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Exposure"), image_exposure_time, ActionManager.ImageExposureTime))
        image_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("ISO"), image_iso, ActionManager.ImageISO))
        image_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Camera Model"), image_camera_model, ActionManager.ImageCameraModel))
        image_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("X Dimension"), image_x_dimension, ActionManager.ImageXDimension))
        image_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Y Dimension"), image_y_dimension, ActionManager.ImageYDimension))
        image_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Focal Length"), image_focal_length, ActionManager.ImageFocalLength))
        image_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Artist"), image_artist, ActionManager.ImageArtist))
        music_action_descriptors = []
        music_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Artist"), music_artist, ActionManager.MusicArtist))
        music_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Title"), music_title, ActionManager.MusicTitle))
        music_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Year"), music_year, ActionManager.MusicYear))
        music_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Album"), music_album, ActionManager.MusicAlbum))
        music_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Genre"), music_genre, ActionManager.MusicGenre))
        music_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Track"), music_track, ActionManager.MusicTrack))

        self.all_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Original Name"), original_name_inputs, ActionManager.OriginalNameAction))
        self.all_action_descriptors.append(ActionManager.ActionDescriptorGroup(self.tr("Case"), case_action_descriptors, ActionManager.CaseChangeAction))
        self.all_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Custom Name"), custom_name_inputs, ActionManager.CustomNameAction))
        self.all_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Folder Name"), foldername_inputs, ActionManager.FolderNameUsageAction))
        self.all_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Find And Replace"), character_replacement_inputs, ActionManager.CharacterReplacementAction))
        self.all_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Insert Characters"), character_insertion_inputs, ActionManager.CharacterInsertionAction))
        self.all_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Delete Characters"), character_deletion_inputs, ActionManager.CharacterDeletionAction))
        self.all_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Counter"), counter_inputs, ActionManager.Counter))
        self.all_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Date"), date_inputs, ActionManager.DateAction))
        self.all_action_descriptors.append(ActionManager.ActionDescriptorGroup(self.tr("Image Metadata"), image_action_descriptors, ActionManager.GenericImageAction))
        self.all_action_descriptors.append(ActionManager.ActionDescriptorGroup(self.tr("Music Metadata"), music_action_descriptors, ActionManager.GenericMusicAction))
        #PREFIX ACTION DESCRIPTOR
        self.prefix_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Custom Name"), custom_name_inputs, ActionManager.CustomNameAction))
        self.prefix_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Folder Name"), foldername_inputs, ActionManager.FolderNameUsageAction))
        self.prefix_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Counter"), counter_inputs, ActionManager.Counter))
        self.prefix_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Date"), date_inputs, ActionManager.DateAction))
        self.prefix_action_descriptors.append(ActionManager.ActionDescriptorGroup(self.tr("Image Metadata"), image_action_descriptors, ActionManager.GenericImageAction))
        self.prefix_action_descriptors.append(ActionManager.ActionDescriptorGroup(self.tr("Music Metadata"), music_action_descriptors, ActionManager.GenericMusicAction))


        #EXTENSION ACTION DESCRIPTOR
        self.extension_action_descriptors.append(ActionManager.ActionDescriptor(self.tr("Original Name"), original_name_inputs, ActionManager.OriginalNameAction))
        self.extension_action_descriptors.append(ActionManager.ActionDescriptorGroup(self.tr("Case"), case_action_descriptors, ActionManager.CaseChangeAction))
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
        self.treeView.setStyleSheet("QTreeView{border:2px solid rgb(220, 220, 220); border-radius: 2px};")
        self.treeView.setObjectName("treeView")
        self.treeView.setAlternatingRowColors(True)
        self.treeView.setSortingEnabled(False)
        #self.treeView.setDragDropMode(QAbstractItemView.DropOnly)
        self.model = QStandardItemModel()
        self.model.setObjectName("model")
        self.model.setHorizontalHeaderLabels([self.tr("Original Files"),self.tr("Modified Files")])
        self.treeView.setModel(self.model)
        self.treeView.setColumnWidth(0, (self.treeView.columnWidth(0)+self.treeView.columnWidth(1))/2)
        self.main_grid.addWidget(self.treeView, 3, 0)
        self.file_box = ActionButtonGroup.ActionButtonGroup(self.tr("File"), self.all_action_descriptors, self.frame_width, self.frame_height, "file")
        # self.file_box.setSizePolicy( QSizePolicy.Fixed, QSizePolicy.Fixed);
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
        widget_container.setObjectName("widget_container")
        #Layout of Container Widget
        self.scroll_area_layout = QHBoxLayout()
        self.scroll_area_layout.setSpacing(17)
        self.scroll_area_layout.addStretch()
        self.scroll_area_layout.addWidget(self.file_box)
        self.scroll_area_layout.addWidget(self.extension_box)
        self.scroll_area_layout.addStretch()
        widget_container.setLayout(self.scroll_area_layout)
        widget_container.setStyleSheet("QWidget#widget_container{background-color: rgb(226, 226, 226)};")
        #Scroll Area Properties
        scroll = QScrollArea()
        scroll.setObjectName("scroll_area")
        scroll.setAutoFillBackground(False)
        scroll.setStyleSheet("QFrame#scroll_area{border:1px solid rgb(223, 223, 223); border-radius: 2px; padding:2px; background-color: rgb(226, 226, 226)};")
        scroll.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Fixed);
        scroll.setMinimumSize(self.frame_width *2, self.frame_height + 50)
        scroll.setWidgetResizable(True)
        scroll.setWidget(widget_container)
        #Scroll Area Layer add 
        hLayout = QHBoxLayout()
        hLayout.addWidget(scroll)
        font = QFont()
        font.setWeight(75)
        font.setBold(True)
        pattern_label = QLabel("Pattern")
        pattern_label.setFont(font)
        self.main_grid.addWidget(pattern_label,0,0)
        self.main_grid.addLayout(hLayout,1,0)
        self.folder_icon = QIcon(":/folder_icon.svg")
        self.file_icon = QIcon(":/file_icon.svg")
        self.directory = os.path.join(os.path.dirname(__file__),"UnitTest")
        label = QLabel("Preview")
        label.setFont(font)
        self.main_grid.addWidget(label,2,0)

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
        
    def input_directory(self, directory, recursion, show_hidden_files, sorting_criteria, reverse_order, filters, type_filters):
        """Process the selected directory to create the tree and modify the files"""
        self.recursion = recursion
        self.show_hidden_files = show_hidden_files
        self.sorting_criteria = sorting_criteria
        self.reverse_order = reverse_order
        tree = self.main_grid.itemAtPosition(2,0)
        self.model.clear()
        self.model.setHorizontalHeaderLabels([self.tr("Original Files"),self.tr("Modified Files")])
        self.files_collection = FileManager.FilesCollection(directory, recursion, show_hidden_files, sorting_criteria, reverse_order, filters, type_filters)
        self.root_tree_node = self.files_collection.get_file_system_tree_node()
        self.populate_tree(self.model, self.root_tree_node, True)
        self.treeView.setColumnWidth(0, (self.treeView.columnWidth(0)+self.treeView.columnWidth(1))/2)
        self.treeView.expandAll()
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
        self.apply_action()

    def apply_action(self):
        print(self.file_box.sizeHint())
        self.actions = []
        widget_number = self.scroll_area_layout.count()
        for i in range(1, widget_number-1): #do not count the stretch widget
            action_button_group = self.scroll_area_layout.itemAt(i).widget()
            self.populate_actions(action_button_group, action_button_group.get_frame_type())
        if self.files_collection is not None:
            try:
                self.files_collection.process_file_system_tree_node(self.actions, self.file_or_folder)
            except Exception as e:
                QMessageBox.warning(self, "Warning", str(e))
            #refresh tree
            self.populate_tree(self.model, self.root_tree_node, False)

    def populate_actions(self, actiongroup, path_part):
        """populate the list of actions depending on the parameters entered in the ActionButtonGroup"""
        # print(actiongroup)
        # print(path_part)
        (action_descriptor, action_args) = actiongroup.get_inputs()
        # print(action_descriptor)
        # print(action_args)
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


