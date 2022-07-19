# BlendPresence
This is an addon for Blender that allows you to show off what you're doing in Discord using Rich Presence.

**BlendPresence currently supports versions 2.93 and higher.**
<p align="center">
  <img src="https://i.ibb.co/w07qJfX/Screenshot-2.png" height="300px">
</p>


# Features

<p align="center">
  <img src="https://abx.gg/i/buttons.gif" height="180px">
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
2. Open Blender, then go to `Edit > Preferences > Add-ons`. Click `Install...` and select the zipfile.

## Updating

1. Select the `BlendPresence` dropdown in the add-ons menu and click `Remove...` - repeat the steps above for the newer version.

## Troubleshooting

If the Rich Presence is not displaying, try the following:
* In Discord, go to your **User Settings > Activity Privacy > Display current activity as a status message** and make sure it's _enabled_.
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
- (Viewport) **Active Mode** displays the mode (Object, Edit, Pose, etc.) that the user is currently active in.
- (Rendering) **Render Stats** displays render information such as frame resolution and FPS while rendering.

### Buttons ###
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
