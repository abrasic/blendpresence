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
- **Update Every** determines how fast BlendPresence should update your presence in [x] seconds. Use small values at your own risk as this may cost you more performance.

### Large Icon Tooltip ###
- **Render Engine** displays the render engine that's currently in use by the user. This should work with most other third-party render engines such as Octane and Redshift.
- **Blender Version** displays Blender version that the addon is running in.
- **Display GPU** displays the name of the GPU Blender is using.

### Small Icon ###
- (Viewport) **Active Mode** displays the mode (Object, Edit, Pose, etc.) that the user is currently active in.
- (Rendering) **Render Stats** displays render information such as frame resolution and FPS while rendering.

### Buttons ###
- A maximum of two buttons can be displayed at the bottom of your presence and can be personalized with any label and URL of their choosing.
   - **Important: The link MUST start with a protocol (`https://`)**

### Details ###
- **Display Types**: *Literal* is filler text that changes based on what you're doing, such as if you're rendering something, it will change to "Rendering a project". Alternatively you can set your own text by changing this setting to *Custom*
- **Display File Name** overrides the setting above with the current .blend file name. This will only work if the file is saved onto your machine.

### State ###
- (Viewport) **Display Types**: There are several object types that you can display in the presence, including objects, faces, bones, materials and keyframes. It can also fetch the current frame you're viewing, or you can also set your own text in this field.
- (Rendering) **Frame Range** will display the current frame number that you're rendering. If it's an animation, it will fetch the frame range that's being rendered

### Time Elapsed ###
- **Reset on Render** will reset the timer when a render starts.

This plugin is a modified fork from [Protinon/Blender-rpc](https://github.com/Protinon/Blender-rpc)
