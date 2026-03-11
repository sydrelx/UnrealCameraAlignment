
"""
Built on the OptionsWindow base class template.

"""

import maya.cmds as mc
import os


class OptionsWindow(object):
    """
    OptionsWindow() base class definition creates a window with
    three buttons on the bottom. Users should subclass OptionsWindow()
    and implement callback functions and the displayOptions() method
    to display custom GUI controls.
    """

    def __init__(self):
        self.window = "optionsWindow"
        self.title = "OptionsWindow"
        self.size = (546, 350)
        self.actionName = "Apply and Close"
        self.applyName = "Apply"

    def create(self):
        if mc.window(self.window, exists=True):
            mc.deleteUI(self.window, window=True)

        self.window = mc.window(
            self.window, title=self.title, widthHeight=self.size, menuBar=True
        )
        self.mainForm = mc.formLayout(nd=100)
        self.commandMenu()
        self.optionsForm = mc.formLayout(nd=100, parent=self.mainForm)

        mc.formLayout(
            self.mainForm,
            e=True,
            attachForm=(
                [self.optionsForm, "top", 0],
                [self.optionsForm, "left", 2],
                [self.optionsForm, "right", 2],
                [self.optionsForm, "bottom", 0],
            ),
        )

        self.scrollLayout = mc.scrollLayout(
            parent=self.optionsForm,
            horizontalScrollBarThickness=0,
            verticalScrollBarThickness=16,
            childResizable=True,
        )
        self.innerColumn = mc.columnLayout(
            adjustableColumn=True, parent=self.scrollLayout
        )

        self.displayOptions()
        self.commonButtons()

        mc.formLayout(
            self.optionsForm,
            e=True,
            attachForm=(
                [self.scrollLayout, "top", 0],
                [self.scrollLayout, "left", 2],
                [self.scrollLayout, "right", 2],
                [self.acctionBtn, "left", 5],
                [self.acctionBtn, "bottom", 5],
                [self.applyBtn, "bottom", 5],
                [self.closeBtn, "bottom", 5],
                [self.closeBtn, "right", 5],
            ),
            attachControl=([self.scrollLayout, "bottom", 5, self.applyBtn]),
            attachPosition=(
                [self.acctionBtn, "right", 1, 33],
                [self.closeBtn, "left", 0, 67],
            ),
            attachNone=(
                [self.acctionBtn, "top"],
                [self.applyBtn, "top"],
                [self.closeBtn, "top"],
            ),
        )
        mc.formLayout(
            self.optionsForm,
            e=True,
            attachControl=(
                [self.applyBtn, "left", 4, self.acctionBtn],
                [self.applyBtn, "right", 4, self.closeBtn],
            ),
        )

        mc.showWindow()

    def commandMenu(self):
        """Adds a pull-down menu to the main window menu bar."""
        self.editMenu = mc.menu(label="Edit")
        self.editMenuSave = mc.menuItem(
            label="Save Settings", command=self.editMenuSaveCmd
        )
        self.editMenuReset = mc.menuItem(
            label="Reset Settings", command=self.editMenuResetCmd
        )
        self.helpMenu = mc.menu(label="Help")
        self.helpMenuItem = mc.menuItem(
            label="Help on %s" % self.title, command=self.helpMenuCmd
        )

    def helpMenuCmd(self, *args):
        mc.launch(web="http://maya-python.com")

    def editMenuSaveCmd(self, *args):
        pass

    def editMenuResetCmd(self, *args):
        pass

    def actionCmd(self, *args):
        """Apply-and-Close callback — override in subclass."""
        print("ACTION")

    def applyBtnCmd(self, *args):
        """Apply callback — override in subclass."""
        print("APPLY")

    def closeBtnCmd(self, *args):
        mc.deleteUI(self.window, window=True)

    def commonButtons(self):
        """Adds three buttons (Action, Apply, Close) to the bottom of optionsForm."""
        self.commonBtnSize = (self.size[0] - 18 / 3, 26)
        self.acctionBtn = mc.button(
            label=self.actionName,
            height=self.commonBtnSize[1],
            command=self.actionCmd,
            parent=self.optionsForm,
        )
        self.applyBtn = mc.button(
            label=self.applyName,
            height=self.commonBtnSize[1],
            command=self.applyBtnCmd,
            parent=self.optionsForm,
        )
        self.closeBtn = mc.button(
            label="Close",
            height=self.commonBtnSize[1],
            command=self.closeBtnCmd,
            parent=self.optionsForm,
        )

    def displayOptions(self):
        """
        All custom UI controls should be added here.
        Controls will be children of self.innerColumn.
        """
        pass
