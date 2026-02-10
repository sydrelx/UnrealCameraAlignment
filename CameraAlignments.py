"""

Streamlines fixes for taking cameras from unreal, 
bringing them into Maya to have them set up and that process of the setup be automated


If questions / issues contact: sydneyrelkin.com
"""

import maya.cmds as mc

class CameraToolGUI:
    def __init__(self):
        self.window = "CameraToolWindow"
        self.title = "Unreal Camera Alignment Tools"
        self.size = (400, 500)
        
    def create(self):
        """Creates the main window"""
        # Delete window if it exists
        if mc.window(self.window, exists=True):
            mc.deleteUI(self.window, window=True)
        
        # Create new window
        self.window = mc.window(self.window, title=self.title, widthHeight=self.size)
        
        # Main layout
        self.mainLayout = mc.columnLayout(adjustableColumn=True)
        
        # Display camera selection
        self.displayCameraSelection()
        
        # Display keyframe mover
        self.displayKeyframeMover()
        
        # Display position offset
        self.displayPositionOffset()
        
        # Show window
        mc.showWindow(self.window)
    
    def displayCameraSelection(self):
        """Creates the camera selection GUI"""
        labelWidth = 150
        inputWidth = 190
        
        # Camera selection section
        self.cameraLayout = mc.frameLayout(
            label="Camera Selection", 
            marginWidth=10, 
            
        )
        
        self.cameraColumn = mc.columnLayout(adjustableColumn=True)
        
        # Camera dropdown
        self.cameraRow = mc.rowLayout(
            numberOfColumns=2,
            columnWidth2=(labelWidth, inputWidth),
            adjustableColumn=2,
            columnAlign2=["right", "left"],
            columnAttach2=["both", "both"]
        )
        
        mc.text(label="Select Camera", width=labelWidth)
        self.cameraDropdown = mc.optionMenu("cameraDropdown", width=inputWidth)
        
        # Populate camera dropdown
        cameras = mc.listRelatives(mc.ls(type="camera"), parent=True)
        if cameras:
            for cam in cameras:
                mc.menuItem(label=cam)
        
        mc.setParent('..')
        
        # Refresh button
        self.refreshRow = mc.rowLayout(
            numberOfColumns=2,
            columnWidth2=(labelWidth, inputWidth),
            adjustableColumn=2,
            columnAlign2=["right", "left"],
            columnAttach2=["both", "both"]
        )
        
        mc.text(label="", width=labelWidth)
        mc.button(label="Refresh Camera List", command=self.refreshCameras, width=inputWidth)
        
        mc.setParent('..')
        mc.setParent('..')
        mc.setParent('..')
    
    def displayKeyframeMover(self):
        """Creates the keyframe mover GUI"""
        labelWidth = 150
        inputWidth = 190
        
        # Keyframe mover section
        self.keyframeLayout = mc.frameLayout(
            label="Keyframe Adjustments", 
            marginWidth=10, 
            collapsable=True
        )
        
        self.keyframeColumn = mc.columnLayout(adjustableColumn=True)
        
        # Target frame input
        self.frameRow = mc.rowLayout(
            numberOfColumns=2,
            columnWidth2=(labelWidth, inputWidth),
            adjustableColumn=2,
            columnAlign2=["right", "left"],
            columnAttach2=["both", "both"]
        )
        
        mc.text(label="Start at Frame", width=labelWidth)
        self.frameField = mc.intField("targetFrameField", value=0, width=inputWidth)
        
        mc.setParent('..')
        
        # Move keyframes button
        self.moveButtonRow = mc.rowLayout(
            numberOfColumns=2,
            columnWidth2=(labelWidth, inputWidth),
            adjustableColumn=2,
            columnAlign2=["right", "left"],
            columnAttach2=["both", "both"]
        )
        
        mc.text(label="", width=labelWidth)
        mc.button(label="Move to Frame", command=self.moveKeyframes, width=inputWidth, backgroundColor=(0.4, 0.6, 0.4))
        
        mc.setParent('..')
        mc.setParent('..')
        mc.setParent('..')
    
    def displayPositionOffset(self):
        """Creates the position offset GUI"""
        labelWidth = 150
        inputWidth = 190
        
        # Position offset section
        self.offsetLayout = mc.frameLayout(
            label="Location Offset", 
            marginWidth=10, 
            collapsable=True
        )
        
        self.offsetColumn = mc.columnLayout(adjustableColumn=True)
        self.textRow = mc.rowLayout(
            numberOfColumns=1,
            adjustableColumn=1,
            columnAlign1="left"
        )
        
        mc.text(label="Adjust in Space")
        
        mc.setParent('..')
        # X Position
        self.xRow = mc.rowLayout(
            numberOfColumns=2,
            columnWidth2=(labelWidth, inputWidth),
            adjustableColumn=2,
            columnAlign2=["right", "left"],
            columnAttach2=["both", "both"]
        )
        
        mc.text(label="X Position", width=labelWidth)
        self.xField = mc.floatField("xField", value=0.0, precision=3, width=inputWidth)
        
        mc.setParent('..')
        
        # Y Position
        self.yRow = mc.rowLayout(
            numberOfColumns=2,
            columnWidth2=(labelWidth, inputWidth),
            adjustableColumn=2,
            columnAlign2=["right", "left"],
            columnAttach2=["both", "both"]
        )
        
        mc.text(label="Y Position", width=labelWidth)
        self.yField = mc.floatField("yField", value=1.0, precision=3, width=inputWidth)
        
        mc.setParent('..')
        
        # Z Position
        self.zRow = mc.rowLayout(
            numberOfColumns=2,
            columnWidth2=(labelWidth, inputWidth),
            adjustableColumn=2,
            columnAlign2=["right", "left"],
            columnAttach2=["both", "both"]
        )
        
        mc.text(label="Z Position", width=labelWidth)
        self.zField = mc.floatField("zField", value=0.0, precision=3, width=inputWidth)
        
        mc.setParent('..')
        
        # Bake animation option
        self.bakeRow = mc.rowLayout(
            numberOfColumns=2,
            columnWidth2=(labelWidth, inputWidth),
            adjustableColumn=2,
            columnAlign2=["right", "left"],
            columnAttach2=["both", "both"]
        )
        
        mc.text(label="Bake Motion Before Moving", width=labelWidth)
        self.bakeCheck = mc.checkBox("bakeCheck", label="", value=True)
        
        mc.setParent('..')
        
        # Apply offset button
        self.applyOffsetRow = mc.rowLayout(
            numberOfColumns=2,
            columnWidth2=(labelWidth, inputWidth),
            adjustableColumn=2,
            columnAlign2=["right", "left"],
            columnAttach2=["both", "both"]
        )
        
        mc.text(label="", width=labelWidth)
        mc.button(label="Move Camera", command=self.applyPositionOffset, width=inputWidth, backgroundColor=(0.1, 0.6, 0.6))
        
        mc.setParent('..')
        mc.setParent('..')
        mc.setParent('..')
    
    def refreshCameras(self, *args):
        """Refreshes the camera dropdown list"""
        # Clear existing items
        menuItems = mc.optionMenu("cameraDropdown", query=True, itemListLong=True)
        if menuItems:
            mc.deleteUI(menuItems)
        
        # Repopulate
        cameras = mc.listRelatives(mc.ls(type="camera"), parent=True)
        if cameras:
            for cam in cameras:
                mc.menuItem(label=cam, parent="cameraDropdown")
    
    def getCameraTransform(self, obj):
        """Get camera transform from object"""
        shapes = mc.listRelatives(obj, shapes=True, type='camera') or []
        
        if shapes or mc.nodeType(obj) == 'camera':
            if mc.nodeType(obj) == 'camera':
                return mc.listRelatives(obj, parent=True)[0]
            else:
                return obj
        else:
            mc.warning(f"{obj} is not a camera.")
            return None
    
    def moveKeyframes(self, *args):
        """Move keyframes from selected camera to target frame (with relative timing maintained)"""
        # Get selected camera from dropdown
        cameraName = mc.optionMenu("cameraDropdown", query=True, value=True)
        target_frame = mc.intField("targetFrameField", query=True, value=True)
        
        if not cameraName:
            mc.warning("Please select a camera from the dropdown.")
            return
        
        transform = self.getCameraTransform(cameraName)
        
        if not transform:
            return
        
        shapes = mc.listRelatives(transform, shapes=True, type='camera') or []
        attrs = mc.listAttr(transform, keyable=True) or []
        
        if shapes:
            camera_shape = shapes[0]
            camera_attrs = mc.listAttr(camera_shape, keyable=True) or []
            attrs.extend([f"{camera_shape}.{attr}" for attr in camera_attrs])
        
        keyframes_moved = False
        
        for attr in attrs:
            full_attr = f"{transform}.{attr}" if '.' not in attr else attr
            keys = mc.keyframe(full_attr, query=True, timeChange=True)
            
            if keys:
                # Always maintain relative timing
                first_key = min(keys)
                offset = target_frame - first_key
                mc.keyframe(full_attr, edit=True, relative=True, timeChange=offset)
                keyframes_moved = True
        
        if keyframes_moved:
            result_msg = f"Moved keyframes to frame {target_frame}"
            print(result_msg)
            mc.confirmDialog(
                title='Success',
                message=result_msg,
                button=['OK']
            )
        else:
            mc.warning(f"No keyframes found on {transform}")
    
    def offsetCameraAnimation(self, cameraName, offset):
        """Offsets all keyframes on the camera's translate channels to specific location"""
        
        for axis in ['X', 'Y', 'Z']:
            transAttr = f"{cameraName}.translate{axis}"
            
            # Check if attribute has keyframes
            keyCount = mc.keyframe(transAttr, query=True, keyframeCount=True)
            
            if keyCount and keyCount > 0:
                # Offset each keyframe
                for key in range(keyCount):
                    value = mc.keyframe(transAttr, index=(key,), query=True, valueChange=True)[0]
                    axisIndex = ['X', 'Y', 'Z'].index(axis)
                    newValue = value + offset[axisIndex]
                    mc.keyframe(transAttr, index=(key,), valueChange=newValue)
            else:
                # No animation, just set the value
                currentValue = mc.getAttr(transAttr)
                axisIndex = ['X', 'Y', 'Z'].index(axis)
                mc.setAttr(transAttr, currentValue + offset[axisIndex])
    
    def bakeAnimation(self, cameraName):
        """Bakes the animation on the camera"""
        mc.select(cameraName)
        
        start = mc.playbackOptions(q=True, min=True)
        end = mc.playbackOptions(q=True, max=True)
        
        mc.bakeResults(
            cameraName, 
            t=(start, end),
            simulation=True,
            attribute=['tx', 'ty', 'tz', 'rx', 'ry', 'rz']
        )
        
        # Unparent if needed
        parentCheck = mc.listRelatives(cameraName, parent=True)
        if parentCheck:
            mc.parent(cameraName, world=True)
    
    def applyPositionOffset(self, *args):
        """Apply position offset to camera"""
        # Get inputs
        cameraName = mc.optionMenu("cameraDropdown", query=True, value=True)
        newX = mc.floatField("xField", query=True, value=True)
        newY = mc.floatField("yField", query=True, value=True)
        newZ = mc.floatField("zField", query=True, value=True)
        shouldBake = mc.checkBox("bakeCheck", query=True, value=True)
        
        if not cameraName:
            mc.warning("Please select a camera")
            return
        
        # Bake if requested
        if shouldBake:
            self.bakeAnimation(cameraName)
        
        # Calculate offset based on absolute position
        currentPos = mc.xform(cameraName, query=True, worldSpace=True, translation=True)
        offset = [newX - currentPos[0], newY - currentPos[1], newZ - currentPos[2]]
        
        # Apply offset
        self.offsetCameraAnimation(cameraName, offset)
        
        print(f"Camera '{cameraName}' offset by {offset}")
        mc.confirmDialog(
            title='Success',
            message=f'Camera motion offset complete!\nOffset Moved from: [{offset[0]:.3f}, {offset[1]:.3f}, {offset[2]:.3f}]',
            button=['OK']
        )


# Create and show the tool 
"Needs to be the same name as file to run in scrip gui"
def CameraAlignments():
    setGUI= CameraToolGUI()
    setGUI.create()
