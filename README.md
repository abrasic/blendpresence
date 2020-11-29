# BlendPresence
A personalized Blender plugin fork from [Protinon/Blender-rpc](https://github.com/Protinon/Blender-rpc)

BlendPresence is a blender plugin that shows off what you're doing in blender using the power of Discord Rich Presence. It shows various statistics including app version, .blend file name and the mode you're currently using. Whilel rendering, you can also show the count of frames rendered and frame resolution if you want.

![Example 1](https://abrasic.com/assets/img/bp1.png)
![Example 2](https://abrasic.com/assets/img/bp2.png)

## Installation
0. Download Python if you haven't: https://www.python.org/
1. Download the latest version in **Releases**. DO NOT UNZIP
2. In Blender go to **Edit > Preferences > Addons > Install** and select the downloaded zip file.
3. Enable the plugin and manage settings as such.

### Not displaying?
Make sure in Discord, your **User Settings > Game Activity > Display currently running game as a status message** is enabled, otherwise it won't show in Discord. If it still doesn't show up, refresh the app by pressing Ctrl+R then re-enable the plugin in Blender.

## Customizable Options
- **Display file name**: Displays .blend file name. Disabled by default.
- **Display elapsed time**: Displays time elapsed.
- **Reset elapsed time on next action**: If enabled, the timer will reset when switching between edit/render modes.
- **Display active mode**: Displays the current mode from the 3D Viewport.
- **Display rendered frames**: Displays the current frames while rendering.
- **Display render stats**: Displays camera resolution and FPS while rendering.

