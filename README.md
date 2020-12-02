# BlendPresence
A personalized Blender plugin fork from [Protinon/Blender-rpc](https://github.com/Protinon/Blender-rpc)

BlendPresence is a blender plugin that shows off what you're doing in blender using the power of Discord Rich Presence. It shows various statistics including the .blend file name, render engine, and what mode you're currently using in the 3D Viewport. While rendering, you can also display the count of frames rendered and frame resolution.

![Example 1](https://i.imgur.com/7iU1VcC_d.png?maxwidth=437)

## Installation
1. Download Python if you haven't: https://www.python.org/
2. Download the latest version in **Releases**. DO NOT UNZIP
3. In Blender go to **Edit > Preferences > Addons > Install** and select the downloaded zip file.
4. Enable the plugin and manage settings as such.

### Not displaying?
Make sure in Discord, your **User Settings > Game Activity > Display currently running game as a status message** is enabled. If it still doesn't show up, refresh the app by pressing Ctrl+R then re-enable the plugin in Blender.

## Customizable Features
- **File name**: Displays .blend file name. Disabled by default.
- **Custom text**: A piece of text customizable to the user. Minimum two characters.
- **Elapsed time**: Displays time elapsed.
- **Reset elapsed time on next action**: If enabled, the timer will reset when switching between edit/render modes.
- **Active mode**: Displays the current mode from the 3D Viewport.
- **Frame information**: Displays frame count while rendering.
- **Render stats**: Displays information such as camera resolution and FPS while rendering.
- **Render engine**: Displays current render engine in use.
- **Blender version**: Displays current version of Blender.

