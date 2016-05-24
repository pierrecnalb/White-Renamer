#!/usr/bin/python3

# Copyright (C) 2015-2016 Pierre Blanc
#
# This file is part of WhiteRenamer.
#
# WhiteRenamer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WhiteRenamer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WhiteRenamer. If not, see <http://www.gnu.org/licenses/>.

from PyQt5.QtWidgets import QWidget, QGridLayout, QTreeView, QSizePolicy, QScrollArea, QHBoxLayout, QFrame, QLabel, QMessageBox, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QIcon, QFont, QStandardItem
from ..model import action_manager, FileSystem, Controller
from . import ActionButtonGroup, resource_rc


class MainWidget(QWidget):
    #QMainWindow does not allow any self.main_layout or boxes layout. Therefore we use a QWidget instance

    def __init__(self):
        QWidget.__init__(self)
        self.files_system_view = None
        self.all_action_descriptors = []
        self.prefix_action_descriptors = []
        self.extension_action_descriptors = []
        self.file_or_folder = "file"
        self.frame_space = 20
        self.frame_width = 260
        self.frame_height = 290
        self.button_width = 25
        self.init_actions()
        self.init_UI()
        #----------------------------------INIT UI---------------------------------------
        #---INPUTS DEFINITION---
    def init_actions(self):
        original_name_inputs = []
        case_change_inputs = []
        first_letter_inputs = []
        first_letter_inputs.append(action_manager.ActionInput(
            'first_letter', self.tr('First Letter'), "checkable", True))
        first_letter_inputs.append(action_manager.ActionInput(
            'after_symbols', self.tr('And After'), str, "- _"))
        uppercase_inputs = []
        lowercasecase_inputs = []
        character_replacement_inputs = []
        character_replacement_inputs.append(action_manager.ActionInput(
            'old_char', self.tr('Replace'), str, ""))
        character_replacement_inputs.append(action_manager.ActionInput(
            'new_char', self.tr('With'), str, ""))
        character_replacement_inputs.append(action_manager.ActionInput(
            'regex', self.tr('Regex'), "checkable", False))
        character_insertion_inputs = []
        character_insertion_inputs.append(action_manager.ActionInput(
            'new_char', self.tr('Insert'), str, ""))
        character_insertion_inputs.append(action_manager.ActionInput(
            'index', self.tr('At Position'), int, 0))
        character_deletion_inputs = []
        character_deletion_inputs.append(action_manager.ActionInput(
            'starting_position', self.tr('From'), int, 0))
        character_deletion_inputs.append(action_manager.ActionInput(
            'ending_position', self.tr('To'), int, 1))
        custom_name_inputs = []
        custom_name_inputs.append(action_manager.ActionInput(
            'new_name', self.tr('New Name'), str, ""))
        counter_inputs = []
        counter_inputs.append(action_manager.ActionInput(
            'start_index', self.tr('Start At'), int, 0))
        counter_inputs.append(action_manager.ActionInput('increment', self.tr(
            'Increment'), int, 1))
        counter_inputs.append(action_manager.ActionInput(
            'digit_number', self.tr('Number of Digit'), int, 1))
        date_inputs = []
        date_inputs.append(action_manager.ActionInput(
            'is_modified_date', self.tr('Modified'), bool, False))
        date_inputs.append(action_manager.ActionInput(
            'is_created_date', self.tr('Created'), bool, True))
        date_inputs.append(
            action_manager.ActionInput('format_display', self.tr('Format'),
                                       str, "%Y-%m-%d %H:%M:%S (%A %B)"))
        foldername_inputs = []
        image_metadata_inputs = []
        image_date_time_original = []
        image_date_time_original.append(action_manager.ActionInput(
            'time_format', self.tr('Format'), str, "%Y-%m-%d %H:%M:%S"))

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
        case_action_descriptors.append(action_manager.ActionDescriptor(
            self.tr("Titlecase"), first_letter_inputs,
            action_manager.TitleCaseAction))
        case_action_descriptors.append(action_manager.ActionDescriptor(
            self.tr("Uppercase"), uppercase_inputs,
            action_manager.UpperCaseAction))
        case_action_descriptors.append(action_manager.ActionDescriptor(
            self.tr("Lowercase"), lowercasecase_inputs,
            action_manager.LowerCaseAction))
        image_action_descriptors = []
        image_action_descriptors.append(action_manager.ActionDescriptor(
            self.tr("Original Date"), image_date_time_original,
            action_manager.ImageDateTimeOriginal))
        image_action_descriptors.append(action_manager.ActionDescriptor(
            self.tr("F Number"), image_f_number, action_manager.ImageFNumber))
        image_action_descriptors.append(action_manager.ActionDescriptor(
            self.tr("Exposure"), image_exposure_time,
            action_manager.ImageExposureTime))
        image_action_descriptors.append(action_manager.ActionDescriptor(
            self.tr("ISO"), image_iso, action_manager.ImageISO))
        image_action_descriptors.append(action_manager.ActionDescriptor(
            self.tr("Camera Model"), image_camera_model,
            action_manager.ImageCameraModel))
        image_action_descriptors.append(action_manager.ActionDescriptor(
            self.tr("X Dimension"), image_x_dimension,
            action_manager.ImageXDimension))
        image_action_descriptors.append(action_manager.ActionDescriptor(
            self.tr("Y Dimension"), image_y_dimension,
            action_manager.ImageYDimension))
        image_action_descriptors.append(action_manager.ActionDescriptor(
            self.tr("Focal Length"), image_focal_length,
            action_manager.ImageFocalLength))
        image_action_descriptors.append(action_manager.ActionDescriptor(
            self.tr("Artist"), image_artist, action_manager.ImageArtist))
        music_action_descriptors = []
        music_action_descriptors.append(action_manager.ActionDescriptor(
            self.tr("Artist"), music_artist, action_manager.MusicArtist))
        music_action_descriptors.append(action_manager.ActionDescriptor(
            self.tr("Title"), music_title, action_manager.MusicTitle))
        music_action_descriptors.append(action_manager.ActionDescriptor(
            self.tr("Year"), music_year, action_manager.MusicYear))
        music_action_descriptors.append(action_manager.ActionDescriptor(
            self.tr("Album"), music_album, action_manager.MusicAlbum))
        music_action_descriptors.append(action_manager.ActionDescriptor(
            self.tr("Genre"), music_genre, action_manager.MusicGenre))
        music_action_descriptors.append(action_manager.ActionDescriptor(
            self.tr("Track"), music_track, action_manager.MusicTrack))

        self.all_action_descriptors.append(action_manager.ActionDescriptor(
            self.tr("Original Name"), original_name_inputs,
            action_manager.OriginalNameAction))
        self.all_action_descriptors.append(
            action_manager.ActionDescriptorGroup(
                self.tr("Case"), case_action_descriptors,
                action_manager.CaseChangeAction))
        self.all_action_descriptors.append(action_manager.ActionDescriptor(
            self.tr("Custom Name"), custom_name_inputs,
            action_manager.CustomNameAction))
        self.all_action_descriptors.append(action_manager.ActionDescriptor(
            self.tr("Folder Name"), foldername_inputs,
            action_manager.FolderNameUsageAction))
        self.all_action_descriptors.append(action_manager.ActionDescriptor(
            self.tr("Find And Replace"), character_replacement_inputs,
            action_manager.CharacterReplacementAction))
        self.all_action_descriptors.append(action_manager.ActionDescriptor(
            self.tr("Insert Characters"), character_insertion_inputs,
            action_manager.CharacterInsertionAction))
        self.all_action_descriptors.append(action_manager.ActionDescriptor(
            self.tr("Delete Characters"), character_deletion_inputs,
            action_manager.CharacterDeletionAction))
        self.all_action_descriptors.append(action_manager.ActionDescriptor(
            self.tr("Counter"), counter_inputs, action_manager.Counter))
        self.all_action_descriptors.append(action_manager.ActionDescriptor(
            self.tr("Date"), date_inputs, action_manager.DateAction))
        self.all_action_descriptors.append(
            action_manager.ActionDescriptorGroup(
                self.tr("Image Metadata"), image_action_descriptors,
                action_manager.GenericImageAction))
        self.all_action_descriptors.append(
            action_manager.ActionDescriptorGroup(
                self.tr("Music Metadata"), music_action_descriptors,
                action_manager.GenericMusicAction))
        #PREFIX ACTION DESCRIPTOR
        self.prefix_action_descriptors.append(action_manager.ActionDescriptor(
            self.tr("Custom Name"), custom_name_inputs,
            action_manager.CustomNameAction))
        self.prefix_action_descriptors.append(action_manager.ActionDescriptor(
            self.tr("Folder Name"), foldername_inputs,
            action_manager.FolderNameUsageAction))
        self.prefix_action_descriptors.append(action_manager.ActionDescriptor(
            self.tr("Counter"), counter_inputs, action_manager.Counter))
        self.prefix_action_descriptors.append(action_manager.ActionDescriptor(
            self.tr("Date"), date_inputs, action_manager.DateAction))
        self.prefix_action_descriptors.append(
            action_manager.ActionDescriptorGroup(
                self.tr("Image Metadata"), image_action_descriptors,
                action_manager.GenericImageAction))
        self.prefix_action_descriptors.append(
            action_manager.ActionDescriptorGroup(
                self.tr("Music Metadata"), music_action_descriptors,
                action_manager.GenericMusicAction))

        #EXTENSION ACTION DESCRIPTOR
        self.extension_action_descriptors.append(
            action_manager.ActionDescriptor(
                self.tr("Original Name"), original_name_inputs,
                action_manager.OriginalNameAction))
        self.extension_action_descriptors.append(
            action_manager.ActionDescriptorGroup(
                self.tr("Case"), case_action_descriptors,
                action_manager.CaseChangeAction))
        self.extension_action_descriptors.append(
            action_manager.ActionDescriptor(
                self.tr("Custom Name"), custom_name_inputs,
                action_manager.CustomNameAction))
        self.extension_action_descriptors.append(
            action_manager.ActionDescriptor(
                self.tr("Find And Replace"), character_replacement_inputs,
                action_manager.CharacterReplacementAction))
        self.extension_action_descriptors.append(
            action_manager.ActionDescriptor(
                self.tr("Insert Characters"), character_insertion_inputs,
                action_manager.CharacterInsertionAction))
        self.extension_action_descriptors.append(
            action_manager.ActionDescriptor(
                self.tr("Delete Characters"), character_deletion_inputs,
                action_manager.CharacterDeletionAction))

    def init_UI(self):
        #---LAYOUT---
        self.main_grid = QGridLayout(self)
        self.main_grid.setObjectName("main_grid")
        self.setLayout(self.main_grid)
        #---TREE VIEW---
        self.treeView = QTreeView()
        self.treeView.setStyleSheet(
            "QTreeView{border:2px solid rgb(220, 220, 220); border-radius: 2px};")
        self.treeView.setObjectName("treeView")
        self.treeView.setAlternatingRowColors(True)
        self.treeView.setSortingEnabled(False)
        #self.treeView.setDragDropMode(QAbstractItemView.DropOnly)
        self.model = QStandardItemModel()
        self.model.setObjectName("model")
        self.model.setHorizontalHeaderLabels([self.tr("Original Files"),
                                              self.tr("Modified Files")])
        self.treeView.setModel(self.model)
        self.treeView.setColumnWidth(0, (
            self.treeView.columnWidth(0) + self.treeView.columnWidth(1)) / 2)
        self.main_grid.addWidget(self.treeView, 3, 0)
        self.file_box = ActionButtonGroup(
            self.tr("File"), self.all_action_descriptors, self.frame_width,
            self.frame_height, "file")
        self.file_box.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.file_box.setFixedSize(self.frame_width, self.frame_height)
        self.file_box.changed.connect(self.apply_action)
        self.file_box.addedBefore.connect(self.add_prefix)
        self.file_box.addedAfter.connect(self.add_suffix)
        #---EXTENSION GROUP---
        self.extension_box = ActionButtonGroup(
            self.tr("Extension"), self.extension_action_descriptors,
            self.frame_width, self.frame_height, "extension")
        self.extension_box.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
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
        widget_container.setStyleSheet(
            "QWidget#widget_container{background-color: rgb(226, 226, 226)};")
        #Scroll Area Properties
        scroll = QScrollArea()
        scroll.setObjectName("scroll_area")
        scroll.setAutoFillBackground(False)
        scroll.setStyleSheet(
            "QFrame#scroll_area{border:1px solid rgb(223, 223, 223); border-radius: 2px; padding:2px; background-color: rgb(226, 226, 226)};")
        scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        scroll.setMinimumSize(self.frame_width * 2, self.frame_height + 50)
        scroll.setWidgetResizable(True)
        scroll.setWidget(widget_container)
        #Scroll Area Layer add
        hLayout = QHBoxLayout()
        hLayout.addWidget(scroll)
        font = QFont()
        font.setWeight(75)
        font.setBold(True)
        pattern_label = QLabel(self.tr("Pattern"))
        pattern_label.setFont(font)
        self.main_grid.addWidget(pattern_label, 0, 0)
        self.main_grid.addLayout(hLayout, 1, 0)
        self.folder_icon = QIcon(":/folder_icon.png")
        self.file_icon = QIcon(":/file_icon.png")
        self.preview_label = QLabel(self.tr("Preview"))
        self.preview_label.setFont(font)
        self.main_grid.addWidget(self.preview_label, 2, 0)

    def add_prefix(self, widget_caller):
        self.prefix_box = ActionButtonGroup(
            self.tr("Prefix"), self.prefix_action_descriptors,
            self.frame_width, self.frame_height, "prefix")
        self.prefix_box.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.prefix_box.setMinimumSize(self.frame_width, self.frame_height)
        self.prefix_box.addedBefore.connect(self.add_prefix)
        self.prefix_box.removed.connect(self.remove_widget)
        self.prefix_box.changed.connect(self.apply_action)
        self.scroll_area_layout.insertWidget(
            self.scroll_area_layout.indexOf(widget_caller), self.prefix_box)
        self.apply_action()

    def add_suffix(self, widget_caller):
        self.suffix_box = ActionButtonGroup(
            self.tr("Suffix"), self.prefix_action_descriptors,
            self.frame_width, self.frame_height, "suffix")
        self.suffix_box.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.suffix_box.setMinimumSize(self.frame_width, self.frame_height)
        self.suffix_box.addedAfter.connect(self.add_suffix)
        self.suffix_box.removed.connect(self.remove_widget)
        self.suffix_box.changed.connect(self.apply_action)
        self.scroll_area_layout.insertWidget(
            self.scroll_area_layout.indexOf(widget_caller) + 1,
            self.suffix_box)
        self.apply_action()

    def remove_widget(self, widget_caller):
        self.scroll_area_layout.removeWidget(widget_caller)
        widget_caller.destruct_layout()
        self.apply_action()

    def is_file(self, value):
        if value is True:
            self.file_or_folder = "file"
            self.file_box.set_label(self.tr("File"))
            self.file_box.set_frame_type("file")
            self.extension_box.show()
        else:
            self.file_or_folder = "folder"
            self.extension_box.hide()
            self.file_box.set_label(self.tr("Folder"))
            self.file_box.set_frame_type("folder")
        self.apply_action()

    def get_action_button_group(self):
        return self.file_box

    def set_filtered_files(self, files_system_view):
        """Process the selected directory to create the tree and modify the files"""
        self.files_system_view = files_system_view
        self.controller = Controller(self.files_system_view)
        self.redraw_tree()
        self.apply_action()

    def redraw_tree(self):
        tree = self.main_grid.itemAtPosition(2, 0)
        self.model.clear()
        self.model.setHorizontalHeaderLabels([self.tr("Original Files"),
                                              self.tr("Modified Files")])
        root_tree_node_view = self.files_system_view.get_file_system_tree_node(
        )
        self.preview_label.setText(self.tr("Preview") + ": " +
                                   root_tree_node_view.get_original_path())
        self.populate_tree(self.model, root_tree_node_view, True)
        self.treeView.setColumnWidth(0, (
            self.treeView.columnWidth(0) + self.treeView.columnWidth(1)) / 2)
        self.treeView.expandAll()

    def populate_tree(self, parent, tree_node, reset_view):
        """Populate the tree with the selected directory. If reset_view is False, only the modified_files are updated."""
        children = tree_node.get_children()
        for i, child in enumerate(children):
            if child.original_filedescriptor.is_folder:
                icon = self.folder_icon
            else:
                icon = self.file_icon
            original_file = QStandardItem(
                icon, child.original_filedescriptor.basename)
            original_file.setEditable(False)
            modified_file = QStandardItem(
                child.modified_filedescriptor.basename)
            modified_file.setEditable(False)
            if isinstance(parent, QStandardItemModel):
                #parent.itemChanged[QStandardItem].connect(self.tree_item_changed)
                if reset_view:
                    parent.setItem(i, 0, original_file)
                parent.setItem(i, 1, modified_file)
                self.populate_tree(parent.item(i, 0), child, reset_view)
            else:
                if reset_view:
                    parent.setChild(i, 0, original_file)
                parent.setChild(i, 1, modified_file)
                self.populate_tree(parent.child(i, 0), child, reset_view)
    #@Slot()            
    #def tree_item_changed(self, selected_item):
    #    pass
    #    #print(selected_item.row())

    def rename(self):
        """Rename all the files and folders."""
        try:
            self.controller.batch_rename()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        # self.populate_tree(self.model, self.files_system_view.get_file_system_tree_node(), True)
        # self.apply_action()

    def undo(self):
        """Undo the previous renaming action."""
        self.controller.batch_undo()
        self.populate_tree(self.model,
                           self.files_system_view.get_file_system_tree_node(),
                           True)
        self.apply_action()

    def apply_action(self):
        self.actions = []
        widget_number = self.scroll_area_layout.count()
        for i in range(1, widget_number - 1):  #do not count the stretch widget
            action_button_group = self.scroll_area_layout.itemAt(i).widget()
            self.actions.append(action_button_group.get_action_with_inputs())
        if self.files_system_view is not None:
            try:
                self.controller.batch_update(self.actions, self.file_or_folder)
            except Exception as e:
                QMessageBox.warning(self, "Warning", str(e))
            #refresh tree
            self.populate_tree(
                self.model, self.files_system_view.get_file_system_tree_node(),
                False)


class SizeCalculator(object):
    def __init__(self, main_window):
        self.main_window = main_window
        main_widget = main_window.get_main_widget()
        action_button_group = main_widget.get_action_button_group()
        for i in range(len(action_button_group.get_action_descriptors())):
            action_button_group.on_selected_action_changed(i)
            self.max_height = action_button_group.get_maximum_height()
            self.max_width = action_button_group.get_maximum_width()
        return (self.max_height, self.max_width)
