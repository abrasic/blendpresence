### Do NOT download from the repo! Please download the latest version from Releases!

# BlendPresence
A personalized Blender plugin fork from [Protinon/Blender-rpc](https://github.com/Protinon/Blender-rpc)
**This addon supports 2.9x branches and 3.0.0 (for some reason)**

BlendPresence is an addon for Blender 2.9x that shows off what you're doing in blender using the power of Discord's Rich Presence. It can display various statistics including the .blend file name, render engine, and what mode you're currently using in the 3D Viewport. While rendering, you can also display the count of frames rendered and frame resolution. It is completely customizable too!

![Example 1](https://i.imgur.com/7iU1VcC_d.png?maxwidth=437)

## Installation
1. Download Python if you haven't yet: https://www.python.org/.
2. Download the [latest version](https://github.com/abrasic/blendpresence/releases). DO NOT UNZIP THE FILE!
3. In Blender go to **Edit > Preferences > Addons > Install** and select the downloaded zip file.
4. Enable the plugin and customize settings via add-on preferences.

## Troubleshooting

If the Rich Presence is not displaying, try the following:
* In Discord, go to your **User Settings > Activity Status > Display current activity as a status message** and make sure it's _enabled_.
* It could be a display bug. Refresh the Discord client by pressing `Ctrl+R`
   * **At this time, BlendPresence will not automatically re-connect if you refresh your Discord client. You will need to re-enable the addon if you want to make it reappear after a Discord update or refresh.**
* It could be a bug with the addon. Try re-enabling it or go to `Window > Toggle System Console` and ensure no errors from BlendPresence appear.

BlendPresence lagspikes every [x] seconds:
* There is a known issue with the **Frames Animated** display feature that can lag Blender every time BlendPresence is executed if you have too many keyframes (roughly one thousand or higher).

## Customizable Features
### Core ###
- **Update Every** determines how fast BlendPresence should update your presence in [x] seconds. Use small values at your own risk!

### Large Icon Tooltip ###
- **Render Engine** displays the render engine that's currently in use by the user. This should work with most other third-party render engines such as Octane and Redshift.
- **Blender Version** displays Blender version that the addon is running in.

### Small Icon ###
- (Viewport) **Active Mode** displays the mode (Object, Edit, Pose, etc.) that the user is currently active in.
- (Rendering) **Render Stats** displays render information such as frame resolution and FPS while rendering.

### Details ###
- **Display Types**: *Literal* is filler text that changes based on what you're doing, such as if you're rendering something, it will change to "Rendering a project". Alternatively you can set your own text by changing this setting to *Custom*
- **Display File Name** overrides the setting above with the current .blend file name. This will only work if the file is saved onto your machine.

### State ###
- (Viewport) **Display Types**: There are several object types that you can display in the presence, including objects, faces, bones, materials and keyframes. It can also fetch the current frame you're viewing, or you can also set your own text in this field.
- (Rendering) **Frame Range** will display the current frame number that you're rendering. If it's an animation, it will fetch the frame range that's being rendered

### Time Elapsed ###
- **Reset on Render** will reset the timer when a render starts.
