"""
Streamlines fixes for taking cameras from unreal,
bringing them into Maya to have them set up and that process of the setup be automated.

If questions / issues contact: sydneyrelkin.com / https://github.com/sydrelx/UnrealCameraAlignment
"""

import maya.cmds as mc
import os

from OptionsWindow import OptionsWindow

# =============================================================================
# CameraToolGUI — subclass of OptionsWindow
# =============================================================================

class CameraToolGUI(OptionsWindow):
    """
    Camera alignment tool window.
    Inherits the OptionsWindow frame (menu bar, Apply/Close buttons).
    The 'Apply' button triggers applyAll(), running all active operations.
    The 'Apply and Close' button does the same and then closes the window.
    """

    def __init__(self):
        super(CameraToolGUI, self).__init__()
        self.window = "CameraToolWindow"
        self.title = "Unreal Camera Alignment Tools"
        self.size = (400, 680)
        self.actionName = "Apply and Close"
        self.applyName = "Apply"

    # ------------------------------------------------------------------
    # displayOptions — builds the tool UI inside self.innerColumn
    # ------------------------------------------------------------------

    def displayOptions(self):
        """Populates self.innerColumn with the camera tool sections."""
        self.displayCameraSelection()
        self.displayKeyframeMover()
        self.displayPositionOffset()
        self.displayExportSelected()

    # ------------------------------------------------------------------
    # Section builders
    # ------------------------------------------------------------------

    def displayCameraSelection(self):
        """Camera selection section."""
        labelWidth = 150
        inputWidth = 190
        halfWidth = inputWidth // 2 - 2

        mc.frameLayout(
            label="Camera Selection",
            marginWidth=10,
            parent=self.innerColumn,
        )
        mc.columnLayout(adjustableColumn=True)

        mc.rowLayout(
            numberOfColumns=2,
            columnWidth2=(labelWidth, inputWidth),
            adjustableColumn=2,
            columnAlign2=["right", "left"],
            columnAttach2=["both", "both"],
        )
        mc.text(label="Select Camera(s)", width=labelWidth)
        self.cameraList = mc.textScrollList(
            "cameraList",
            width=inputWidth,
            height=120,
            allowMultiSelection=True,
        )
        cameras = mc.listRelatives(mc.ls(type="camera"), parent=True) or []
        for cam in cameras:
            mc.textScrollList("cameraList", e=True, append=cam)
        mc.setParent("..")

        # Row: Select All | Deselect All
        mc.rowLayout(
            numberOfColumns=3,
            columnWidth3=(labelWidth, halfWidth, halfWidth),
            adjustableColumn=3,
            columnAlign3=["right", "left", "left"],
            columnAttach3=["both", "both", "both"],
        )
        mc.text(label="", width=labelWidth)
        mc.button(label="Select All",   command=self.selectAllCameras,   width=halfWidth)
        mc.button(label="Deselect All", command=self.deselectAllCameras, width=halfWidth)
        mc.setParent("..")

        # Row: Refresh
        mc.rowLayout(
            numberOfColumns=2,
            columnWidth2=(labelWidth, inputWidth),
            adjustableColumn=2,
            columnAlign2=["right", "left"],
            columnAttach2=["both", "both"],
        )
        mc.text(label="", width=labelWidth)
        mc.button(
            label="Refresh Camera List",
            command=self.refreshCameras,
            width=inputWidth,
        )
        mc.setParent("..")
        mc.setParent("..")  # columnLayout
        mc.setParent("..")  # frameLayout

    def displayKeyframeMover(self):
        """Keyframe adjustments section."""
        labelWidth = 150
        inputWidth = 190

        mc.frameLayout(
            label="Keyframe Adjustments",
            marginWidth=10,
            collapsable=True,
            parent=self.innerColumn,
        )
        mc.columnLayout(adjustableColumn=True)

        mc.rowLayout(
            numberOfColumns=2,
            columnWidth2=(labelWidth, inputWidth),
            adjustableColumn=2,
            columnAlign2=["right", "left"],
            columnAttach2=["both", "both"],
        )
        mc.text(label="Start at Frame", width=labelWidth)
        self.frameField = mc.intField("targetFrameField", value=0, width=inputWidth)
        mc.setParent("..")
        mc.setParent("..")
        mc.setParent("..")

    def displayPositionOffset(self):
        """Location offset section."""
        labelWidth = 150
        inputWidth = 190

        mc.frameLayout(
            label="Location Offset",
            marginWidth=10,
            collapsable=True,
            parent=self.innerColumn,
        )
        mc.columnLayout(adjustableColumn=True)

        mc.rowLayout(numberOfColumns=1, adjustableColumn=1, columnAlign1="left")
        mc.text(label="Adjust in Space")
        mc.setParent("..")

        for axis, default in [("X", 0.0), ("Y", 1.0), ("Z", 0.0)]:
            mc.rowLayout(
                numberOfColumns=2,
                columnWidth2=(labelWidth, inputWidth),
                adjustableColumn=2,
                columnAlign2=["right", "left"],
                columnAttach2=["both", "both"],
            )
            mc.text(label="%s Position" % axis, width=labelWidth)
            mc.floatField(
                "%sField" % axis.lower(),
                value=default,
                precision=3,
                width=inputWidth,
            )
            mc.setParent("..")

        mc.rowLayout(
            numberOfColumns=2,
            columnWidth2=(labelWidth, inputWidth),
            adjustableColumn=2,
            columnAlign2=["right", "left"],
            columnAttach2=["both", "both"],
        )
        mc.text(label="Bake Motion Before Moving", width=labelWidth)
        self.bakeCheck = mc.checkBox("bakeCheck", label="", value=True)
        mc.setParent("..")
        mc.setParent("..")
        mc.setParent("..")

    def displayExportSelected(self):
        """Export selected section."""
        labelWidth = 150
        inputWidth = 190

        mc.frameLayout(
            label="Export Selected",
            marginWidth=10,
            collapsable=True,
            parent=self.innerColumn,
        )
        mc.columnLayout(adjustableColumn=True)

        # Export folder path
        mc.rowLayout(
            numberOfColumns=2,
            columnWidth2=(labelWidth, inputWidth),
            adjustableColumn=2,
            columnAlign2=["right", "left"],
            columnAttach2=["both", "both"],
        )
        mc.text(label="Export Folder", width=labelWidth)
        self.exportPathField = mc.textField(
            "exportPathField",
            placeholderText="/path/to/export/folder",
            width=inputWidth,
        )
        mc.setParent("..")

        # Browse button — picks a folder
        mc.rowLayout(
            numberOfColumns=2,
            columnWidth2=(labelWidth, inputWidth),
            adjustableColumn=2,
            columnAlign2=["right", "left"],
            columnAttach2=["both", "both"],
        )
        mc.text(label="", width=labelWidth)
        mc.button(label="Select Filepath", command=self.browseExportPath, width=inputWidth)
        mc.setParent("..")

        # File type dropdown
        mc.rowLayout(
            numberOfColumns=2,
            columnWidth2=(labelWidth, inputWidth),
            adjustableColumn=2,
            columnAlign2=["right", "left"],
            columnAttach2=["both", "both"],
        )
        mc.text(label="File Type", width=labelWidth)
        self.exportTypeMenu = mc.optionMenu("exportTypeMenu", width=inputWidth)
        for lbl in ["Alembic (.abc)","FBX (.fbx)","Maya Binary (.mb)", "OBJ (.obj)","USD (.usd)"]:
            mc.menuItem(label=lbl)
        mc.setParent("..")

        # Optional subfolder name
        mc.rowLayout(
            numberOfColumns=2,
            columnWidth2=(labelWidth, inputWidth),
            adjustableColumn=2,
            columnAlign2=["right", "left"],
            columnAttach2=["both", "both"],
        )
        mc.text(label="Subfolder", width=labelWidth)
        self.exportSubfolderField = mc.textField(
            "exportSubfolderField",
            placeholderText="camera(s) (optional)",
            width=inputWidth,
        )
        mc.setParent("..")

        mc.setParent("..")  # columnLayout
        mc.setParent("..")  # frameLayout

    # ------------------------------------------------------------------
    # Callbacks
    # ------------------------------------------------------------------

    # --- OptionsWindow overrides ---

    def helpMenuCmd(self, *args):
        mc.launch(web="http://sydneyrelkin.com")

    def editMenuResetCmd(self, *args):
        """Reset all fields to their default values."""
        mc.intField("targetFrameField", e=True, value=0)
        mc.floatField("xField", e=True, value=0.0)
        mc.floatField("yField", e=True, value=1.0)
        mc.floatField("zField", e=True, value=0.0)
        mc.checkBox("bakeCheck", e=True, value=True)
        mc.textField("exportPathField", e=True, text="")
        mc.textField("exportSubfolderField", e=True, text="")
        mc.optionMenu("exportTypeMenu", e=True, select=1)

    def applyBtnCmd(self, *args):
        """Apply button — runs the full pipeline."""
        self.applyAll()

    def actionCmd(self, *args):
        """Apply and Close button — runs the full pipeline then closes."""
        self.applyAll()
        self.closeBtnCmd()

    # --- Camera selection ---

    def refreshCameras(self, *args):
        """Refresh the camera list with all cameras currently in the scene, preserving selection where possible."""
        previously_selected = mc.textScrollList("cameraList", q=True, selectItem=True) or []
        mc.textScrollList("cameraList", e=True, removeAll=True)
        cameras = mc.listRelatives(mc.ls(type="camera"), parent=True) or []
        for cam in cameras:
            mc.textScrollList("cameraList", e=True, append=cam)
        # Restore previous selection where cameras still exist
        for cam in previously_selected:
            if cam in cameras:
                mc.textScrollList("cameraList", e=True, selectItem=cam)

    def selectAllCameras(self, *args):
        """Select all items in the camera list."""
        all_items = mc.textScrollList("cameraList", q=True, allItems=True) or []
        for item in all_items:
            mc.textScrollList("cameraList", e=True, selectItem=item)

    def deselectAllCameras(self, *args):
        """Deselect all items in the camera list."""
        mc.textScrollList("cameraList", e=True, deselectAll=True)

    def getSelectedCameras(self):
        """Return a list of all selected cameras from the scroll list."""
        return mc.textScrollList("cameraList", q=True, selectItem=True) or []

    # --- Keyframe operations ---

    def getCameraTransform(self, obj):
        """Return the transform node for a given camera object or shape."""
        shapes = mc.listRelatives(obj, shapes=True, type="camera") or []
        if shapes or mc.nodeType(obj) == "camera":
            if mc.nodeType(obj) == "camera":
                return mc.listRelatives(obj, parent=True)[0]
            return obj
        mc.warning("%s is not a camera." % obj)
        return None

    def moveKeyframes(self, log):
        """
        Move all keyframes on the selected camera(s) so the first key lands on target_frame.
        Appends result messages to the provided log list instead of showing dialogs.
        Returns True on success, False on failure.
        """
        cameraNames = self.getSelectedCameras()
        target_frame = mc.intField("targetFrameField", q=True, value=True)

        if not cameraNames:
            log.append("  [Keyframes]  WARNING: No camera selected — skipped.")
            return False

        any_success = False
        for cameraName in cameraNames:
            transform = self.getCameraTransform(cameraName)
            if not transform:
                log.append("  [Keyframes]  WARNING: '%s' is not a valid camera — skipped." % cameraName)
                continue

            shapes = mc.listRelatives(transform, shapes=True, type="camera") or []
            attrs = mc.listAttr(transform, keyable=True) or []

            if shapes:
                camera_attrs = mc.listAttr(shapes[0], keyable=True) or []
                attrs.extend(["%s.%s" % (shapes[0], a) for a in camera_attrs])

            keyframes_moved = False
            for attr in attrs:
                full_attr = "%s.%s" % (transform, attr) if "." not in attr else attr
                keys = mc.keyframe(full_attr, q=True, timeChange=True)
                if keys:
                    offset = target_frame - min(keys)
                    mc.keyframe(full_attr, e=True, relative=True, timeChange=offset)
                    keyframes_moved = True

            if keyframes_moved:
                log.append("  [Keyframes]  '%s': Moved keyframes to frame %d." % (cameraName, target_frame))
                print("Moved keyframes on '%s' to frame %d" % (cameraName, target_frame))
                any_success = True
            else:
                log.append("  [Keyframes]  WARNING: No keyframes found on '%s'." % transform)

        return any_success

    # --- Position offset operations ---

    def offsetCameraAnimation(self, cameraName, offset):
        """Offset all translate keyframes (or static values) by the given XYZ offset."""
        for i, axis in enumerate(["X", "Y", "Z"]):
            attr = "%s.translate%s" % (cameraName, axis)
            keyCount = mc.keyframe(attr, q=True, keyframeCount=True)
            if keyCount and keyCount > 0:
                for k in range(keyCount):
                    value = mc.keyframe(attr, index=(k,), q=True, valueChange=True)[0]
                    mc.keyframe(attr, index=(k,), valueChange=value + offset[i])
            else:
                mc.setAttr(attr, mc.getAttr(attr) + offset[i])

    def bakeAnimation(self, cameraName):
        """
        Bake simulation onto the camera at only its existing keyframe times,
        preserving the original sparse keyframe count, then unparent it.
        """
        attrs = ["tx", "ty", "tz", "rx", "ry", "rz"]

        # Collect every unique keyframe time already on the camera
        key_times = set()
        for attr in attrs:
            times = mc.keyframe("%s.%s" % (cameraName, attr), q=True, timeChange=True) or []
            key_times.update(times)

        mc.select(cameraName)

        if key_times:
            # Bake only at the frames where keys already exist
            for t in sorted(key_times):
                mc.currentTime(t, update=True)
                for attr in attrs:
                    val = mc.getAttr("%s.%s" % (cameraName, attr))
                    mc.setKeyframe(cameraName, attribute=attr, time=t, value=val)
        else:
            # No keyframes found — fall back to a single static bake at current time
            t = mc.currentTime(q=True)
            for attr in attrs:
                val = mc.getAttr("%s.%s" % (cameraName, attr))
                mc.setKeyframe(cameraName, attribute=attr, time=t, value=val)

        if mc.listRelatives(cameraName, parent=True):
            mc.parent(cameraName, world=True)

    def applyPositionOffset(self, log):
        """
        Apply the XYZ position offset to the selected camera(s).
        Appends result messages to the provided log list instead of showing dialogs.
        Returns True on success, False on failure.
        """
        cameraNames = self.getSelectedCameras()
        newX = mc.floatField("xField", q=True, value=True)
        newY = mc.floatField("yField", q=True, value=True)
        newZ = mc.floatField("zField", q=True, value=True)
        shouldBake = mc.checkBox("bakeCheck", q=True, value=True)

        if not cameraNames:
            log.append("  [Offset]     WARNING: No camera selected — skipped.")
            return False

        any_success = False
        for cameraName in cameraNames:
            if shouldBake:
                self.bakeAnimation(cameraName)

            currentPos = mc.xform(cameraName, q=True, worldSpace=True, translation=True)
            offset = [newX - currentPos[0], newY - currentPos[1], newZ - currentPos[2]]
            self.offsetCameraAnimation(cameraName, offset)

            log.append(
                "  [Offset]     '%s' offset complete. "
                "Offset: [%.3f, %.3f, %.3f]" % (cameraName, offset[0], offset[1], offset[2])
            )
            print("Camera '%s' offset by %s" % (cameraName, offset))
            any_success = True

        return any_success

    # --- Export operations ---

    def browseExportPath(self, *args):
        """Open a folder browser and populate the export folder field."""
        result = mc.fileDialog2(
            fileMode=3,       # 3 = existing directory
            dialogStyle=2,
        )
        if result:
            mc.textField("exportPathField", e=True, text=result[0])

    def exportSelected(self, log):
        """
        Export each selected camera as its own file inside the specified folder.
        The folder (and optional subfolder) will be created if it does not exist.
        Each file is named after the camera: <cameraName>.<ext>
        Appends result messages to the provided log list.
        Returns True if at least one camera was exported successfully.
        """
        folder_path = mc.textField("exportPathField", q=True, text=True).strip()
        subfolder   = mc.textField("exportSubfolderField", q=True, text=True).strip()
        type_label  = mc.optionMenu("exportTypeMenu", q=True, value=True)

        if not folder_path:
            log.append("  [Export]     WARNING: No export folder specified — skipped.")
            return False

        # Build final output directory
        export_dir = os.path.join(folder_path, subfolder) if subfolder else folder_path

        # Create the directory tree if needed
        if not os.path.exists(export_dir):
            try:
                os.makedirs(export_dir)
                log.append("  [Export]     Created folder: %s" % export_dir)
            except Exception as e:
                log.append("  [Export]     ERROR: Could not create folder — %s" % str(e))
                return False

        # Resolve file extension and Maya type string from the dropdown label
        type_map = {
            "FBX (.fbx)":          (".fbx", "FBX export"),
            "Maya Binary (.mb)":   (".mb",  "mayaBinary"),
            "OBJ (.obj)":          (".obj", "OBJexport"),
            "Alembic (.abc)":      (".abc", "Alembic"),
        }
        ext, file_type = type_map.get(type_label, (".fbx", "FBX export"))

        cameraNames = self.getSelectedCameras()
        if not cameraNames:
            log.append("  [Export]     WARNING: No cameras selected — skipped.")
            return False

        any_success = False
        for cameraName in cameraNames:
            # Select just this camera for export
            mc.select(cameraName, replace=True)
            out_path = os.path.join(export_dir, cameraName + ext)
            try:
                mc.file(
                    out_path,
                    force=True,
                    options="v=0",
                    type=file_type,
                    exportSelected=True,
                )
                log.append("  [Export]     '%s' → %s" % (cameraName, out_path))
                any_success = True
            except Exception as e:
                log.append("  [Export]     ERROR: Failed to export '%s' — %s" % (cameraName, str(e)))

        return any_success

    # --- Apply all ---

    def applyAll(self, *args):
        """
        Runs all operations in order:
          1. Move keyframes to the target frame
          2. Apply the position offset (bakes first if the checkbox is set)
          3. Export each selected camera to its own file in the specified folder

        All step results are collected into a single summary dialog shown at the end.
        """
        log = []

        self.moveKeyframes(log)
        self.applyPositionOffset(log)
        self.exportSelected(log)

        # Determine overall status
        has_error = any(
            ("ERROR" in line or "WARNING" in line) for line in log
        )
        title = "Apply Complete — Review Results" if has_error else "Apply Complete"
        summary = "\n".join(log)

        mc.confirmDialog(title=title, message=summary, button=["OK"])


# =============================================================================
# Entry point  (script name must match to run from Maya's Script Editor)
# =============================================================================

def CameraAlignment():
    gui = CameraToolGUI()
    gui.create()
