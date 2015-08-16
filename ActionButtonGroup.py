#author : pierrecnalb
#copyright pierrecnalb
import PySide
from PySide.QtCore import *
from PySide.QtGui  import *
from PySide.QtSvg  import *
import resource_rc

class ActionButtonGroup(QWidget):
    """Group the combobox with the textboxes containing the subactions"""
    changed = Signal() # get changes in order to refresh the preview
    def __init__(self, frame_name, action_descriptors, frame_width, frame_height):
        QWidget.__init__(self)
        self.maximum_height_size = frame_height
        self.maximum_width_size = frame_width
        self.frame = QFrame(self)
        self.frame.setObjectName("frame")
        if ("fix" in frame_name):
            self.frame.setStyleSheet("QFrame#frame{border:1px solid rgb(190, 190, 190); border-radius: 4px; padding:2px; background-color: rgb(230, 230, 230)};")
        else:
            self.frame.setStyleSheet("QFrame#frame{border:2px solid rgb(203, 203, 203); border-radius: 10px; padding:2px; background-color: rgb(244, 244, 244)};")
        self.frame_grid = QGridLayout(self.frame) #this is a hidden grid to handle the objects in the frame as if it was a grid.
        self.frame_grid.setObjectName("frame_grid")
        self.frame.setGeometry(QRect(0, 0, self.maximum_width_size, self.maximum_height_size))
        self.frame_name = frame_name
        self.combobox = QComboBox()
        self.combobox.setObjectName("action_selector")
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

    def set_label(self, new_label):
        self.frame_name = new_label
        self.label.setText(new_label)

    def change(self):
        ''' Change occurs on the layout. '''
        self.changed.emit()

    def get_action_descriptors(self):
        return self.action_descriptors

    def on_selected_action_changed(self, index):
        self.selected_action = self.action_descriptors[index]
        self.button_inputs_dict = {}
        self.add_sub_button()
        self.change()
        #self.frame.resize(self.frame.minimumSizeHint())

    def add_sub_button(self):
        sub_buttons = self.grid.itemAtPosition(2,0)
        if sub_buttons is not None:
            widgetToRemove = sub_buttons.widget()
            # get it out of the layout list
            self.grid.removeWidget(widgetToRemove)
            # remove it form the gui
            widgetToRemove.setParent(None)
        if self.selected_action and self.selected_action.action_inputs != []:
            subframe = QFrame(self)
            subframe.setObjectName("subframe")
            subframe.setStyleSheet("QFrame#subframe{border:2px solid rgb(210, 210, 210); border-radius:3px; padding:2px; background-color: rgb(253, 253, 253)};")
            sub_grid = QGridLayout(subframe)
            sub_grid.setObjectName("subgrid")
            sub_grid.destroyed.connect(self.isDestroyed)
            font = QFont()
            font.setWeight(55)
            font.setBold(True)
            option_label = QLabel("options :")
            option_label.setFont(font)
            sub_grid.addWidget(option_label, 0, 0, 1, 2)
            self.button_inputs_dict = {}
            for i, arguments in enumerate(self.selected_action.action_inputs):
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
                elif arguments.argument_type == "combo":
                    sub_button = QComboBox()
                    for enum in arguments.optional_argument:
                        sub_button.addItem(enum[1], enum[0])
                    sub_button.currentIndexChanged[int].connect(self.get_combobox_changed)
                sub_button.setObjectName(str(arguments.argument_name))
                if(label.text() == ""):
                    sub_grid.addWidget(sub_button, i+1, 0, 1, 2)
                else:
                    sub_grid.addWidget(label, i+1, 0, 1, 1)
                    sub_grid.addWidget(sub_button, i+1, 1, 1, 1)
                self.button_inputs_dict[arguments.argument_name] = arguments.default_value
            self.grid.addWidget(subframe,2,0,1,1)
        self.grid.addItem(self.spacerItem,3,0,1,1)

    def isDestroyed(self, *args):
        pass

    def get_maximum_height(self):
        if (self.maximum_height_size < self.frame.minimumSizeHint().height()):
            self.maximum_height_size = self.frame.minimumSizeHint().height()
        return self.maximum_height_size

    def get_maximum_width(self):
        if (self.maximum_width_size < self.frame.minimumSizeHint().width()):
            self.maximum_width_size = self.frame.minimumSizeHint().width()
        return self.maximum_width_size

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

    def get_combobox_changed(self, value):
        self.button_inputs_dict[self.sender().objectName()] = self.sender().itemData(value)
        #Hide buttons related to TitleCase
        sub_grid = self.grid.itemAtPosition(2,0)
        if self.sender().objectName() == "case_choice" and sub_grid is not None:
            if value == 0:
                sub_grid.widget().layout().itemAtPosition(2,0).widget().show()
                sub_grid.widget().layout().itemAtPosition(2,1).widget().show()
                sub_grid.widget().layout().itemAtPosition(3,0).widget().show()
                sub_grid.widget().layout().itemAtPosition(3,1).widget().show()
            else:
                sub_grid.widget().layout().itemAtPosition(2,0).widget().hide()
                sub_grid.widget().layout().itemAtPosition(2,1).widget().hide()
                sub_grid.widget().layout().itemAtPosition(3,0).widget().hide()
                sub_grid.widget().layout().itemAtPosition(3,1).widget().hide()
        self.change()

    def clearLayout(self, layout):
        """delete all children of the specified layout"""
        for i in reversed(range(layout.count())): 
                        widgetToRemove = layout.itemAt(i).widget()
                        # get it out of the layout list
                        layout.removeWidget( widgetToRemove )
                        # remove it form the gui
                        widgetToRemove.setParent( None )
        #while layout.count():
        #    child = layout.takeAt(0)
        #    if child.widget() is not None:
        #        child.widget().deleteLater()
        #    elif child.layout() is not None:
        #        self.clearLayout(child.layout())

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

