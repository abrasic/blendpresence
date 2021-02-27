### Do NOT download from the repo! Please download the latest version from Releases!

# BlendPresence
A personalized Blender plugin fork from [Protinon/Blender-rpc](https://github.com/Protinon/Blender-rpc)

BlendPresence is an addon for Blender 2.9x that shows off what you're doing in blender using the power of Discord's Rich Presence. It can display various statistics including the .blend file name, render engine, and what mode you're currently using in the 3D Viewport. While rendering, you can also display the count of frames rendered and frame resolution. It is completely customizable too!

![Example 1](https://i.imgur.com/7iU1VcC_d.png?maxwidth=437)

## Installation
1. Download Python if you haven't: https://www.python.org/
2. Download the latest version in **Releases**. DO NOT UNZIP
3. In Blender go to **Edit > Preferences > Addons > Install** and select the downloaded zip file.
4. Enable the plugin and manage settings as such.

### Not displaying?
Make sure in Discord, your **User Settings > Game Activity > Display currently running game as a status message** is enabled. If it still doesn't show up, refresh the app by pressing Ctrl+R then re-enable the plugin in Blender.

## Customizable Features
### Large Icon Tooltip ###
**Render Engine** displays the render engine that's currently in use by the user. This should work with most other third-party render engines such as Octane and Redshift.

**Blender Version**: Displays Blender version that the addon is running in.

### Small Icon ###
- (Viewport) **Active Mode** displays the mode (Object, Edit, Pose, etc.) that the user is currently active in.
- (Rendering) **Render Stats** displays render information such as frame resolution and FPS while rendering.

### Details ###
- **Display Types**: *Literal* is filler text that changes based on what you're doing, such as if you're rendering something, it will change to "Rendering a project". Alternatively you can set your own text by changing this setting to *Custom*
- **Display File Name** overrides the setting above with the current .blend file name. This will only work if the file is saved onto your machine.

### State ###
- **Viewport Information**
   - There are several object types that you can display in the presence, including objects, faces, bones, materials and keyframes. Can't choose your favotite? Enable **Randomize** and BlendPresence will cycle through your chosen stats at random. It can also fetch the current frame you're viewing, or you can also set your own text in this field.
   - **WARNING:** Enabling *keyframe count* can cause Blender to lag spike every time the presence updates if too many keyframes are in a scene. It's recommended to only enable this for smaller animation projects.

- (Rendering) **Frame Range** will display the current frame number that you're rendering. If it's an animation, it will fetch the frame range that's being rendered

### Time Elapsed ###
- **Reset on Render** will reset the timer when a render starts.
