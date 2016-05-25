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
import sys
import os
import os.path
import subprocess
import webbrowser
import urllib.request
import whiterenamer

from PyQt5.QtCore import pyqtSlot, QSize
from PyQt5.QtWidgets import QMainWindow, QAction, QActionGroup, QLineEdit, QWidget, QSizePolicy, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon

from . import MainWidget, resource_rc
from ..model import FileSystem


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.setWindowTitle('White Renamer')
        # self.setWindowIcon(QIcon(':/white_renamer48.png'))
        self.setUnifiedTitleAndToolBarOnMac(True)
        self.directory = None
        self.use_subfolder = False
        self.filtered_collection = None
        self.files_collection = None
        self.resize(1000, 800)
        self.showMaximized()
        self.name_filter = ''
        self.files_type = ['*.*']
        self.reverse_order = False
        self.sorting_criteria = "name"

        #CREATE THE ACTIONS
        self.action_open = QAction(self.tr('&Open'), self)
        self.action_open = self.edit_action(self.action_open, self.open_directory_dialog_click, None, 'ctrl+o', "new_icon.png" ,self.tr('Open directory.'))
        self.action_exit = QAction(self.tr('&Exit'), self)
        self.action_exit = self.edit_action(self.action_exit, self.close, None,'ctrl+q', "exit_icon.png", self.tr('Exit the application.'))
        self.action_help = QAction(self.tr('&Help'), self)
        self.action_help = self.edit_action(self.action_help, self.help_click, None, 'ctrl+h', 'help_icon.png', self.tr('Show help page.'))
        self.action_about = QAction(self.tr('&About'), self)
        self.action_about = self.edit_action(self.action_about, self.about_box_click, None, None, None,self.tr('About Box.'))


        self.action_check_update = QAction(self.tr('&Check Updates'), self)
        self.action_check_update = self.edit_action(self.action_check_update, self.check_update_click, None, None, None,self.tr('Check for updates.'))

        self.action_recursion = QAction(self.tr('Show Subdirectories'), self)
        self.action_recursion = self.edit_action(self.action_recursion, self.recursion_click, bool, None, "subdirectory_icon.png",self.tr('Rename subdirectories recursively.'))
        self.action_recursion.setCheckable(True)
        self.action_hide = QAction(self.tr('Show Hidden Files'), self)
        self.action_hide = self.edit_action(self.action_hide, self.hide_files_click, bool, 'ctrl+h', "hidden_icon.png",self.tr('Show hidden files.'))
        self.action_hide.setCheckable(True)
        self.action_rename = QAction(self.tr('&Rename'), self)
        self.action_rename = self.edit_action(self.action_rename, self.rename_click, None, 'ctrl+enter', "run_icon.png",self.tr('Rename the files/folders.'))
        self.action_undo = QAction(self.tr('Undo'), self)
        self.action_undo = self.edit_action(self.action_undo, self.undo_click, None, 'ctrl+z', "undo_icon.png",self.tr('Undo the previous renaming.'))
        self.action_reverse_sorting = QAction(self.tr('Reverse'), self)
        self.action_reverse_sorting.setCheckable(True)
        self.action_reverse_sorting = self.edit_action(self.action_reverse_sorting, self.reverse_sorting_click, bool, None, "order_icon.png",self.tr('Reverse the sorting order.'))
        self.action_name_sorting = QAction(self.tr('By Name'), self)
        self.action_name_sorting.setCheckable(True)
        self.action_name_sorting = self.edit_action(self.action_name_sorting, self.name_sorting_click, None, None, None,self.tr('Sort the files/folders by name.'))
        self.action_name_sorting.setChecked(True)
        self.action_size_sorting = QAction(self.tr('By Size'), self)
        self.action_size_sorting.setCheckable(True)
        self.action_size_sorting = self.edit_action(self.action_size_sorting, self.size_sorting_click, None, None, None,self.tr('Sort the files/folders by size.'))
        self.action_modified_date_sorting = QAction(self.tr('By Modified Date'), self)
        self.action_modified_date_sorting.setCheckable(True)
        self.action_modified_date_sorting = self.edit_action(self.action_modified_date_sorting, self.modified_date_sorting_click, None, None, None,self.tr('Sort the files/folders by modified date.'))
        self.action_creation_date_sorting = QAction(self.tr('By Creation Date'), self)
        self.action_creation_date_sorting.setCheckable(True)
        self.action_creation_date_sorting = self.edit_action(self.action_creation_date_sorting, self.creation_date_sorting_click, None, None, None,self.tr('Sort the files/folders by creation date.'))
        sort_group = QActionGroup(self)
        sort_group.addAction(self.action_name_sorting)
        sort_group.addAction(self.action_size_sorting)
        sort_group.addAction(self.action_modified_date_sorting)
        sort_group.addAction(self.action_creation_date_sorting)

        filterInput = QLineEdit()
        filterInput.setPlaceholderText(self.tr("Filter Files..."))
        filterInput.setMaximumWidth(150)
        filterInput.textChanged[str].connect(self.get_name_filter)
        self.action_files_only = QAction(self.tr('Files Only'), self)
        self.action_files_only.setCheckable(True)
        self.action_files_only.setChecked(True)
        self.action_files_only = self.edit_action(self.action_files_only, self.files_only_click, None, None, "file_icon.png",self.tr('Rename only files.'))
        self.action_folders_only = QAction(self.tr('Folders Only'), self)
        self.action_folders_only.setCheckable(True)
        self.action_folders_only = self.edit_action(self.action_folders_only, self.folders_only_click, None, None, "folder_icon.png",self.tr('Rename only folders.'))

        node_type_selector = QActionGroup(self)
        node_type_selector.setObjectName('selector')
        node_type_selector.addAction(self.action_files_only)
        node_type_selector.addAction(self.action_folders_only)

        file_type = QActionGroup(self)
        self.action_all_files = QAction(self.tr("All"),self)
        self.action_all_files = self.edit_action(self.action_all_files, self.all_files_click, None, None, "all_files_icon.png",self.tr('Rename files of any kind.'))
        self.action_all_files.setCheckable(True)
        self.action_all_files.setChecked(True)
        self.action_music_files = QAction(self.tr("Music"),self)
        self.action_music_files = self.edit_action(self.action_music_files, self.music_files_click, None, None, "music_icon.png",self.tr('Rename only music files.'))
        self.action_music_files.setCheckable(True)
        self.action_image_files = QAction(self.tr("Images"),self)
        self.action_image_files = self.edit_action(self.action_image_files, self.image_files_click, None, None, "images_icon.png",self.tr('Rename only image files.'))
        self.action_image_files.setCheckable(True)
        file_type.addAction(self.action_all_files)
        file_type.addAction(self.action_image_files)
        file_type.addAction(self.action_music_files)
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
        menu_filter = menubar.addMenu(self.tr('&Filter'))
        menu_filter.addAction(self.action_files_only)
        menu_filter.addAction(self.action_folders_only)
        menu_filter.addSeparator()
        menu_filter.addAction(self.action_all_files)
        menu_filter.addAction(self.action_image_files)
        menu_filter.addAction(self.action_music_files)
        #TOOL
        menu_tool = menubar.addMenu(self.tr('&Tool'))
        menu_tool.addAction(self.action_rename)
        menu_tool.addAction(self.action_undo)
        #HELP
        menu_help = menubar.addMenu(self.tr('&Help'))
        menu_help.addAction(self.action_help)
        menu_help.addAction(self.action_about)
        menu_help.addAction(self.action_check_update)

        self.main_toolbar = self.addToolBar('main_toolbar')
        self.main_toolbar.addAction(self.action_open)
        self.main_toolbar.addSeparator()
        self.main_toolbar.addAction(self.action_hide)
        self.main_toolbar.addAction(self.action_recursion)
        self.main_toolbar.addSeparator()
        self.main_toolbar.addAction(self.action_files_only)
        self.main_toolbar.addAction(self.action_folders_only)
        self.main_toolbar.addSeparator()
        self.main_toolbar.addAction(self.action_all_files)
        self.main_toolbar.addAction(self.action_image_files)
        self.main_toolbar.addAction(self.action_music_files)
        self.main_toolbar.addWidget(filterInput)
        self.main_toolbar.addSeparator()
        self.main_toolbar.addAction(self.action_rename)
        self.main_toolbar.addAction(self.action_undo)
        self.main_toolbar.setIconSize(QSize(16,16))

        empty = QWidget();
        empty.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Preferred)
        self.main_toolbar.addWidget(empty)
        self.main_toolbar.addAction(self.action_help)
        # create the status bar
        self.statusBar()
        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)

    def get_main_widget(self):
        return self.main_widget


    def edit_action(self, action, slot=None, type=None, shortcut=None, icon=None, tip=None):
        '''This method adds to action: icon, shortcut, ToolTip,\
        StatusTip and can connect triggered action to pyqtSlot '''
        if icon is not None:
            action.setIcon(QIcon(":/{0}".format(icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            if type is not None:
                action.triggered[type].connect(slot)
            else:
                action.triggered.connect(slot)

        return action

    @pyqtSlot()
    def get_name_filter(self, value):
        self.name_filter = value
        self.reset_files_collection()

    @pyqtSlot()
    def help_click(self):
        '''Read and display a help file- currently the README.txt.'''
        if getattr(sys, 'frozen', False): # frozen
            dir_ = os.path.dirname(sys.executable)
            filepath = os.path.join(dir_, "Documentation.pdf")
        else: # unfrozen
            dir_ = os.path.dirname(os.path.realpath(__file__))
            filepath = os.path.join(dir_, "..","doc", "Documentation.pdf")

        if sys.platform.startswith('darwin'):
            subprocess.call(('open', filepath))
        elif os.name == 'nt':
            os.startfile(filepath)
        elif os.name == 'posix':
            subprocess.call(('xdg-open', filepath))

    @pyqtSlot()
    def music_files_click(self):
        self.files_type = ['.flac', '.mp3', '.m4a', '.ogg', '.wma', '.m3a', '.mp4']
        self.reset_files_collection()

    @pyqtSlot()
    def image_files_click(self):
        self.files_type = ['.jpg', '.jpeg', '.tif', '.png', '.gif', '.bmp', '.eps', '.im', '.jfif', '.j2p', '.jpx', '.pcx', '.ico', '.icns', '.psd', '.nef', 'cr2', 'pef']
        self.reset_files_collection()

    @pyqtSlot()
    def all_files_click(self):
        self.files_type = ['*.*']
        self.reset_files_collection()

    @pyqtSlot()
    def files_only_click(self):
        self.files_type = ['*.*']
        self.action_all_files.setChecked(True)
        self.action_all_files.setEnabled(True)
        self.action_image_files.setEnabled(True)
        self.action_music_files.setEnabled(True)
        self.main_widget.is_file(True)
        self.reset_files_collection()

    @pyqtSlot()
    def folders_only_click(self):
        self.files_type = ["folders"]
        self.action_all_files.setChecked(True)
        self.action_all_files.setEnabled(False)
        self.action_image_files.setEnabled(False)
        self.action_music_files.setEnabled(False)
        self.main_widget.is_file(False)
        self.reset_files_collection()


    @pyqtSlot()
    def about_box_click(self):
        '''Popup a box with about message.'''
        QMessageBox.about(self, "About WhiteRenamer",
                """<b>White Renamer</b> 
                <p>Copyright &copy; 2015 Pierre BLANC.</p>
                <p>email : <a href="mailto:pierrecnalb@mailbox.org">pierrecnalb@mailbox.org</a></p>
                <p> White Renamer is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.</p>

<p>White Renamer is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; See the GNU General Public License for more details.</p>
                 """ )
    @pyqtSlot()
    def check_update_click(self):
        try:
            code_online = urllib.request.urlopen("https://raw.githubusercontent.com/pierrecnalb/White-Renamer/master/whiterenamer/version.txt").read().splitlines()
            version_online = code_online[0].decode().split('.')
            version_online = str(whiterenamer.Version(version_online[0], version_online[1], version_online[2]))
            print(version_online)
            self.update_message(str(whiterenamer.__version__), version_online)
        except:
            raise Exception("Unable to retrieve the new software version from the server. Please try later.")

    @pyqtSlot(bool)
    def recursion_click(self, value):
        self.use_subfolder = value
        if self.directory is None:
            return
        self.reset_files_collection()

    @pyqtSlot(bool)
    def hide_files_click(self, value):
        self.show_hidden_files = value
        self.reset_files_collection()

    def are_hidden_files_shown(self):
        return self.action_hide.isChecked()

    @pyqtSlot()
    def open_directory_dialog_click(self):
        """Opens a dialog to allow user to choose a directory """
        flags = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        try:
            self.directory = QFileDialog.getExistingDirectory(self,self.tr("Select Directory"), os.getcwd(), flags)
            self.reset_files_collection()
        except Exception as e:
            print(str(e))
            msg_box = QMessageBox.warning(self, "Invalid directory", "Please select a valid directory." )

    @pyqtSlot(bool)
    def reverse_sorting_click(self, value):
        self.reverse_order = value
        self.reset_files_collection()

    @pyqtSlot()
    def name_sorting_click(self):
        self.sorting_criteria = "name"
        self.reset_files_collection()
    @pyqtSlot()
    def size_sorting_click(self):
        self.sorting_criteria = "size"
        self.reset_files_collection()
    @pyqtSlot()
    def creation_date_sorting_click(self):
        self.sorting_criteria = "creation_date"
        self.reset_files_collection()
    @pyqtSlot()
    def modified_date_sorting_click(self):
        self.sorting_criteria = "modified_date"
        self.reset_files_collection()

    def reset_files_collection(self):
        if(self.directory is None):
            return
        self.files_system = FileSystem(self.directory, self.use_subfolder)
        self.files_system_view = self.files_system.generate_files_system_view(self.are_hidden_files_shown(), self.files_type, self.name_filter, self.sorting_criteria, self.reverse_order)
        self.main_widget.set_filtered_files(self.files_system_view)

    @pyqtSlot()
    def rename_click(self):
        self.main_widget.rename()
        self.reset_files_collection()

    @pyqtSlot()
    def undo_click(self):
        self.main_widget.undo()

    def update_message(self, version, new_version):
        if(version == new_version):
            msg_box = QMessageBox.information(self, "Version", 
                """<p>Your version of whiterenamer is up to date.</p>
                """.format(version, new_version), QMessageBox.Ok)

        else:
            msg_box = QMessageBox.information(self, "Update available", 
                                              """
                <b>New version available</b> 
                <p>You are running an old version of White Renamer (v{0}).</p>
                <p>A newer version is available (v{1}). Do you want to download it ?</p>
                """.format(version, new_version), QMessageBox.No, QMessageBox.Yes)
            if msg_box == QMessageBox.No:
                pass
            if msg_box == QMessageBox.Yes:
                new = 2 # open in a new tab, if possible
                # open a public URL, in this case, the webbrowser docs
                url = "https://github.com/pierrecnalb/WhiteRenamer-builds"
                webbrowser.open(url,new=new)
                # Save was clicked
                # elif ret == QMessageBox.Discard:
                # Don't save was clicked
