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

from PyQt5.QtCore import pyqtSignal, QRect, Qt, QSize
from PyQt5.QtWidgets import QWidget, QFrame, QGridLayout, QLabel, QPushButton, QComboBox, QCheckBox, QLineEdit, QSpinBox, QRadioButton
from PyQt5.QtGui import QFont, QIcon
from ..model import action_manager
from . import resource_rc


class ActionButton(QWidget):
    action_changed = pyqtSignal(object, object)  # get changes in order to refresh the preview.

    def __init__(self, action_descriptors, are_sub_buttons):
        QWidget.__init__(self)
        self.grid = QGridLayout(self)
        self.are_sub_buttons = are_sub_buttons
        self.button_inputs_dict = {}
        self.combobox = QComboBox()
        self.combobox.setObjectName("action_selector")
        self.action_descriptors = action_descriptors
        for element in self.action_descriptors:
            self.combobox.addItem(str(element))
        self.grid.addWidget(self.combobox, 0, 0, 1, 1)
        self.combobox.currentIndexChanged[int].connect(self.on_combobox_changed)
        self.grid.setRowStretch(2,1)
        self.populate_widget(self.action_descriptors[0])
        self.store_inputs()

    def change(self):
        ''' Change occurs on the layout. '''
        self.store_inputs()
        self.action_changed.emit(self.selected_action, self.action_inputs)

    def on_combobox_changed(self, index):
        self.button_inputs_dict = {}
        self.populate_widget(self.action_descriptors[index])
        self.change()

    def populate_widget(self, current_combo_selection):
        sub_buttons = self.grid.itemAtPosition(1,0)
        if sub_buttons is not None:
            widgetToRemove = sub_buttons.widget()
            # get it out of the layout list
            self.grid.removeWidget(widgetToRemove)
            # remove it form the gui
            widgetToRemove.setParent(None)

        if isinstance(current_combo_selection, action_manager.ActionDescriptorGroup):
            subframe = QFrame(self)
            subframe.setObjectName("subframe")
            subframe.setStyleSheet("QFrame#subframe{border:2px solid rgb(220, 220, 220); border-radius:3px; padding:0px; background-color: rgb(253, 253, 253)};")
            sub_grid = QGridLayout(subframe)
            sub_grid.setObjectName("subgrid")
            font = QFont()
            font.setWeight(55)
            font.setBold(True)
            option_label = QLabel("options :")
            option_label.setFont(font)
            sub_grid.addWidget(option_label, 0, 0, 1, 1)
            self.sub_action_group = ActionButton(current_combo_selection.action_descriptors, True)
            self.sub_action_group.action_changed.connect(self.change)
            sub_grid.addWidget(self.sub_action_group, 1, 0, 1, 1)
            self.grid.addWidget(subframe,1,0,1,1)
            return
        if current_combo_selection.action_inputs != []:
            subframe = QFrame(self)
            subframe.setObjectName("subframe")
            sub_grid = QGridLayout(subframe)
            sub_grid.setObjectName("subgrid")
            if self.are_sub_buttons is False:
                subframe.setStyleSheet("QFrame#subframe{border:2px solid rgb(220, 220, 220); border-radius:3px; padding:0px; background-color: rgb(253, 253, 253)};")
                font = QFont()
                font.setWeight(55)
                font.setBold(True)
                option_label = QLabel("options :")
                option_label.setFont(font)
                sub_grid.addWidget(option_label, 0, 0, 1, 1)
            for i, arguments in enumerate(current_combo_selection.action_inputs):
                label = QLabel()
                label.setObjectName("label")
                label.setText(str(arguments.argument_caption))
                if arguments.argument_type == str:
                    sub_button = QLineEdit()
                    sub_button.setText(arguments.default_value)
                    sub_button.textChanged[str].connect(self.get_text_changed)
                elif arguments.argument_type == "checkable":
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
                if(label.text() == ""):
                    sub_grid.addWidget(sub_button, i+1, 0, 1, 2)
                else:
                    sub_grid.addWidget(label, i+1, 0, 1, 1)
                    sub_grid.addWidget(sub_button, i+1, 1, 1, 1)
                self.button_inputs_dict[arguments.argument_name] = arguments.default_value
            self.grid.addWidget(subframe,1,0,1,1)

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
        self.button_inputs_dict[self.sender().objectName()] = value
        self.change()

    def get_inputs(self):
        return self.selected_action, self.action_inputs

    def store_inputs(self):
        if isinstance(self.action_descriptors[self.combobox.currentIndex()], action_manager.ActionDescriptorGroup):
            (self.selected_action, self.action_inputs) = self.sub_action_group.get_inputs()
        else:
            self.selected_action = self.action_descriptors[self.combobox.currentIndex()]
            self.action_inputs = self.button_inputs_dict

class ActionButtonGroup(QWidget):
    changed = pyqtSignal() # get changes in order to refresh the preview.
    """Group the combobox with the textboxes containing the subactions"""
    removed = pyqtSignal(QWidget) # emit a signal when the widget is removed.
    addedBefore = pyqtSignal(QWidget) 
    addedAfter = pyqtSignal(QWidget)
    button_stylesheet = """
    QPushButton {
         border: none;
         border-radius: 6px;
         min-width: 25px;
     }

    QPushButton:hover {
        border: 1px solid rgb(180,180,180);
        background-color: rgb(210, 210, 210);
        border-radius: 6px;
    }
    """

    def __init__(self, frame_name, action_descriptors, frame_width, frame_height, frame_type):
        QWidget.__init__(self)
        self.maximum_height_size = frame_height
        self.maximum_width_size = frame_width
        self.frame_type = frame_type
        self.frame = QFrame(self)
        self.frame.setObjectName("frame")
        if ("fix" in frame_type):
            self.frame.setStyleSheet("QFrame#frame{border:2px solid rgb(210, 210, 210); border-radius: 7px; padding:0px; background-color: rgb(230, 230, 230)};")
        else:
            self.frame.setStyleSheet("QFrame#frame{border:2px solid rgb(220, 220, 220); border-radius: 7px; padding:0px; background-color: rgb(244, 244, 244)};")
        self.frame_grid = QGridLayout(self.frame) #this is a hidden grid to handle the objects in the frame as if it was a grid.
        self.frame_grid.setObjectName("frame_grid")
        self.frame.setGeometry(QRect(0, 0, self.maximum_width_size, self.maximum_height_size))
        self.frame_name = frame_name
        self.label = QLabel(self.frame_name)
        self.label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        remove_widget = QPushButton()
        remove_widget.setFixedSize(25,25)
        remove_widget.setIcon(QIcon(":/delete_icon.png"))
        remove_widget.setIconSize(QSize(16,16))
        remove_widget.setFlat(True)
        remove_widget.setStyleSheet(self.button_stylesheet)
        remove_widget.pressed.connect(self.on_remove_widget)
        add_prefix = QPushButton()
        add_prefix.setFixedSize(25,25)
        add_prefix.setIcon(QIcon(":/add_icon.png"))
        add_prefix.setFlat(True)
        add_prefix.setStyleSheet(self.button_stylesheet)
        add_prefix.setIconSize(QSize(16,16))
        add_prefix.pressed.connect(self.on_add_prefix)
        add_suffix = QPushButton()
        add_suffix.setFixedSize(25,25)
        add_suffix.setIcon(QIcon(":/add_icon.png"))
        add_suffix.setIconSize(QSize(16,16))
        add_suffix.setFlat(True)
        add_suffix.setStyleSheet(self.button_stylesheet)
        add_suffix.pressed.connect(self.on_add_suffix)
        self.grid = QGridLayout()
        self.grid.setObjectName("grid")
 
        self.grid.addWidget(self.label, 0, 1, 1, 1)
        if (self.frame_type == "prefix"):
            self.grid.addWidget(add_prefix, 0, 0 ,1 ,1)
            self.grid.addWidget(remove_widget, 0 ,2 ,1 ,1)
        if (self.frame_type == "suffix"):
            self.grid.addWidget(add_suffix, 0 ,2 ,1 ,1)
            self.grid.addWidget(remove_widget, 0 ,0 ,1 ,1)
        if (self.frame_type == "file" or frame_type == "folder"):
            self.grid.addWidget(add_prefix, 0 ,0 ,1 ,1)
            self.grid.addWidget(add_suffix, 0 ,2 ,1 ,1)
        if (self.frame_type =="extension"):
            empty = QWidget();
            empty.setMinimumSize(add_suffix.size())
            self.grid.addWidget(empty, 0 ,0 ,1 ,1)
            self.grid.addWidget(empty, 0 ,2 ,1 ,1)
        self.action_group = ActionButton(action_descriptors, False)
        self.action_group.action_changed.connect(self.change)
        self.grid.addWidget(self.action_group, 1, 0, 1, 3)
        self.frame_grid.addLayout(self.grid, 0, 0, 1, 1)

    def get_action_with_inputs(self):
        (selected_action_descriptor, action_args) = self.action_group.get_inputs()
        action_class = selected_action_descriptor.action_class
        action_instance = action_class(self.frame_type, **action_args)
        return action_instance


    def change(self, selected_action, button_inputs):
        '''Emit signal when added.'''
        self.selected_action = selected_action
        self.action_inputs = button_inputs
        self.changed.emit()

    def on_add_prefix(self):
        '''Emit signal when added.'''
        self.addedBefore.emit(self)

    def on_add_suffix(self):
        '''Emit signal when added.'''
        self.addedAfter.emit(self)

    def on_remove_widget(self):
        '''Emit signal when removed.'''
        self.removed.emit(self)

    def set_label(self, new_label):
        self.frame_name = new_label
        self.label.setText(new_label)

    def get_action_descriptors(self):
        return self.action_descriptors

    def get_frame_type(self):
        return self.frame_type

    def get_frame_name(self):
        return self.frame_name

    def set_frame_type(self, value):
        self.frame_type = value


    def get_maximum_height(self):
        if (self.maximum_height_size < self.frame.minimumSizeHint().height()):
            self.maximum_height_size = self.frame.minimumSizeHint().height()
        return self.maximum_height_size

    def get_maximum_width(self):
        if (self.maximum_width_size < self.frame.minimumSizeHint().width()):
            self.maximum_width_size = self.frame.minimumSizeHint().width()
        return self.maximum_width_size


    def clearLayout(self, layout):
        """delete all children of the specified layout"""
        for i in reversed(range(layout.count())): 
                        widgetToRemove = layout.itemAt(i).widget()
                        # get it out of the layout list
                        layout.removeWidget( widgetToRemove )
                        # remove it form the gui
                        widgetToRemove.setParent( None )

    def destruct_layout(self):
        """Delete entire layout."""
        while self.grid.count():
            child = self.grid.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clearLayout(child.layout())
        self.deleteLater()

    def on_show_information(self, warning_message):
        """Show the information message"""
        QMessageBox.information(self, "Information", warning_message)

