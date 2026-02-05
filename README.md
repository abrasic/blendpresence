# BlendPresence
This is an addon for Blender that allows you to show off what you're doing in Discord using Rich Presence.

**BlendPresence currently supports versions 2.93 and higher.**
<p align="center">
 <img width="314" height="128" alt="image" src="https://github.com/user-attachments/assets/b3e587d5-642a-432c-8bcc-c03b0a085974" />

  <img width="258" height="116" alt="image" src="https://github.com/user-attachments/assets/c80116c4-7f42-4ef1-8ac2-da349a894a9c" />
</p>


# Features

<p align="center">
  <img width="570" height="201" alt="image" src="https://github.com/user-attachments/assets/1161a231-8a4c-4302-b781-c9a6c0e7209c" />
</p>


* Up to two customizable buttons, redirecting to a link of your choice (portfolio, website, etc)
* Current Blender version
* Active render engine name
* Name of current GPU in use
* Current mode (object, edit, pose, etc)
* Render stats while rendering (current frame and percentage complete)
* Other context-sensitive features like:
   - Number of current frame
   - Name of current scene
   - Name of current object selected
   - Number of bones/polys/materials in the scene
   - And more
   
## Installation

1. Go to the [Latest Release](../../releases/latest) and download the blendpresence.zip file. DON'T UNZIP IT!
2. Open Blender, then go to `Edit > Preferences > Add-ons`. Click `Install from Disk...` in the dropdown at the top right and select the zipfile.

## Updating

1. Select the `BlendPresence` dropdown in the add-ons menu and click `Uninstall` - repeat the steps above for the newer version.

## Troubleshooting

If the Rich Presence is not displaying, try the following:
* In Discord, go to your **User Settings > Activity Privacy > Share my activity** and make sure it's _enabled_.
* It could be a display bug. Refresh the Discord client by pressing `Ctrl+R`
* It could be a bug with the addon. Try re-enabling it or go to `Window > Toggle System Console` and ensure no errors from BlendPresence appear.

## Customizable Features
### Core ###
- **Enabled** determines if your rich presence will be shown on Discord.
- **Update Every** determines how fast BlendPresence will update your presence in [x] seconds. Lower is faster.
   * Faster update rates may affect performance on lower-end machines. A recommended value is 5 seconds.
   
### Large Icon Tooltip ###
- **Render Engine** displays the render engine (Cycles, EEVEE, etc.) that's currently in use.
  * Some third-party render engines like Octane or Redshift will show their unique logo aside the blender logo while used.
- **Blender Version** displays Blender version that the addon is running in.
- **Display GPU** displays the name of the GPU Blender is using.
  * Currently, only NVIDIA cards are supported. Support for AMD, Intel and Apple cards may happen in the future.

### Small Icon ###
- (Viewport) **Icon Set**: Icon sets dynamically change based on what you're doing inside of Blender.
  * Active Mode: Displays the icon of the current mode in use (i.e. Object, Edit, Pose)
  * Active Workspace: Displays the relevant icon of your active workspace. For this to work, your current workspace name needs to be exactly one of the following: `Modeling`, `Sculpting`, `UV Editing`, `Texture Paint`, `Shading`, `Animation`, `Rendering`, `Compositing`, `Geometry Nodes`, `Scripting`
- (Rendering) **Render Stats** displays render information such as frame resolution and FPS while rendering.

### Buttons ###
> [!NOTE]
> You cannot see your own RPC buttons. This is a Discord-related issue. To see your buttons, view them on another account.
- A maximum of two buttons can be displayed at the bottom of your presence and can be personalized with any label and URL of their choosing.
   - **IMPORTANT!** The link MUST start with a protocol (`https://`)!

### Details ###
- **Display Types**: *Literal* is filler text that changes based on what you're doing, such as if you're rendering something, it will change to "Rendering a project". Alternatively you can set your own text by changing this setting to *Custom*
- **Display File Name** overrides the setting above with the current .blend file name. 
  * This will only work on saved files. If nothing shows up, you need to save your .blend file first.

### State ###
- (Viewport) **Display Types**: There are several object types that you can display in the presence, such as:
    * **File Size**: Displays the formatted file size of the current file.
    * **Current Frame**: Returns the frame number currently on the playhead.
    * **Active Object**: Returns the name of the active object.
    * **Current Scecne**: Returns the name of the current scene.
    * **Active Object**: Returns the name of the active object.
    * **Object/Bone/Material/Polygon Count**: Returns the number of specified objects in the current scene.
    * **Custom**: Allows the user to input their custom text.
- (Rendering) **Frame Range** will display the current frame number that you're rendering. If it's an animation, it will fetch the frame range that's being rendered

### Time Elapsed ###
- **Enabled** will show the amount of time elapsed upon the addon being enabled. If you restart the addon, this timer resets.
- **Reset on Render** will reset the timer when a render starts.

This plugin is a modified fork from [Protinon/Blender-rpc](https://github.com/Protinon/Blender-rpc)
