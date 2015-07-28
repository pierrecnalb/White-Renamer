import os
import PySide
from PySide.QtCore import *
from PySide.QtGui  import *
from PySide.QtSvg  import *
import resource_rc
import MainWidget

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.setWindowTitle('Renamer')
        self.directory = None
        self.use_subfolder = False
        self.show_hidden_files = False
        self.sorting_criteria = "name"
        self.reverse_order = False
        self.showMaximized()
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
        self.main_widget = MainWidget.MainWidget()
        self.setCentralWidget(self.main_widget)

    def get_main_widget(self):
        return self.main_widget

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
        self.directory = os.path.join(os.path.dirname(__file__),"UnitTest","Test Directory")
        #self.directory ="/home/pierre/Desktop/Test"
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
