# Unreal Camera Alignment Tool for Maya
A tool to prep Unreal cameras that are not easily transferred between softwares

Originally created for SCAD VFX Senior Project, https://linktr.ee/metamorphosis_vfxthesis



### To run:

Download files and place them in a folder that Maya has access to.

In the `userSetup.py` file, the user will have to change line 14 to where the scripts are located. 


____

## **User Guide** 

### **Brief & Purpose for Tool**
Unreal Cameras that are tracked using RedSpy infrared technology are not typically exported out of unreal with settings that allow it to be easily transferred between softwares. Because of this abnormality, the camera keyframes when exported are at around 800,000 frames and the space of where the camera is in space is largely away from the center axis of any 3d scene when brought into a 3d program. Additionally sometimes the export from Unreal is not recognized by Houdini. Maya is the best program to fix these problems, as it can be not only manually fixed here, but also automated to be fixed with this tool. This documentation is going to go over how to use the tool, and to fix the problems automatically.


### **Camera Selection**

For this tool to work you have to have a camera selected by selecting the camera(s) in the tools GUI. The dropdown menu gives you the option to refresh and select the camera that is chosen to be moved. To select the camera(s), click on the camera(s) in the GUI. If it is not visible, click the “Refresh Camera List” button and the list of cameras will refresh

### **Keyframe adjustments**

Once the Camera(s) is selected, the keyframe adjustment section allows for the user to move the keyframes to start at any keyframe given. The default is at 0.

### **Location Offset**

This gives the ability for the user to move the camera to a specific area in space based upon X,Y,Z Coordinates. Additionally there is an option to bake the motion before moving. This allows for the motion of the camera to stay the same, just the location of the motion being different making it easier to use between 3D softwares. It is automatically selected as being checked, as there will be very rare instances of motion not wanting to be baked before moving, but the user has the option. 

### **Export Selected**

Once all of the adjustments are set up, the filepath to export the camera(s) are in the tool as well. Export Folder is where the user can write the file path for where the user wants the cameras to go. Additionally there is an option to manually select the folder using the “Select Filepath” button. “File Type” allows for the user to select the kind of file the camera(s) will be exported as. The options to export is .abc .fbx .mb .obj and .usd
Additionally, there is an option to make a subfolder for where the user selects for the cameras to be exported to.


Link to Guide in google doc format: https://docs.google.com/document/d/1cRKXsq4xGX7Xpe11cT13N9pD3eVhxhDkCCKm41UjWzU/edit?usp=sharing


____

