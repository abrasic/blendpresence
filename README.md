# BlendPresence
A personalized Blender plugin fork from [Protinon/Blender-rpc](https://github.com/Protinon/Blender-rpc)

BlendPresence is a blender plugin that shows off what you're doing in blender using Discord Rich Presence. It shows various statistics including app version, .blend file name and the mode you're currently using. While rendering, it can display what frame(s) you're currently rendering.

![Example 1](https://abrasic.com/assets/img/bp1.png)
![Example 2](https://abrasic.com/assets/img/bp2.png)

## Installation
1. Download the latest version in releases. DO NOT UNZIP
2. In blender go to Edit > Preferences > Addons > Install and select the downloaded zip file.
3. Enable the plugin and manage settings as such.
Make sure in your **User Settings > Game Activity** you have *Display currently running game as a status message* enabled, otherwise it won't show in Discord.

## Customizable Options
- **Display file name**: Displays .blend file name.
- **Display elapsed time**: Displays time elapsed.
- **Reset elapsed time on next action**: If enabled, the timer will reset when switching between edit/render modes.
- **Display active mode**: Displays the current mode from the 3D Viewport.
- **Display rendered frames**: Displays the current frames while rendering.
- **Display render stats**: Displays camera resolution and FPS while rendering.

