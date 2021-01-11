import bpy
import os
import sys
import time
import math
import random
from .pypresence import pypresence as rpc

bl_info = {
    "name": "BlendPresence",
    "description": "Discord Rich Presence for Blender 2.90",
    "author": "Abrasic",
    "version": (1, 3, 0),
    "blender": (2, 90, 1),
    "category": "System",
}

rpcClient = rpc.Presence("766373631424200705")
pidFilePath = os.path.join(os.path.dirname(os.path.normpath(bpy.app.tempdir)), "BlendRpcPid")
startTime = None
isRendering = False
renderedFrames = 0

def register():
    global startTime

    bpy.utils.register_class(RpcPreferences)
    startTime = time.time()
    rpcClient.connect()
    writePidFileAtomic()
    bpy.app.timers.register(updatePresenceTimer, first_interval=1.0, persistent=True)
    bpy.app.handlers.save_post.append(writePidHandler)
    
    # Rendering
    bpy.app.handlers.render_init.append(startRenderJobHandler)
    bpy.app.handlers.render_complete.append(endRenderJobHandler)
    bpy.app.handlers.render_cancel.append(endRenderJobHandler)
    bpy.app.handlers.render_post.append(postRenderHandler)

def unregister():
    global startTime

    startTime = None
    rpcClient.close()
    removePidFile()
    bpy.app.timers.unregister(updatePresenceTimer)
    bpy.app.handlers.save_post.remove(writePidHandler)
    bpy.utils.unregister_class(RpcPreferences)
    
    # Rendering
    bpy.app.handlers.render_init.remove(startRenderJobHandler)
    bpy.app.handlers.render_complete.remove(endRenderJobHandler)
    bpy.app.handlers.render_cancel.remove(endRenderJobHandler)
    bpy.app.handlers.render_post.remove(postRenderHandler)

def writePidFileAtomic():
    pid = os.getpid()
    tmpPidFilePath = f"{pidFilePath}-{pid}"
    with open(tmpPidFilePath, "w") as tmpPidFile:
        tmpPidFile.write(str(pid))
        tmpPidFile.flush()
        os.fsync(tmpPidFile.fileno())
    os.replace(tmpPidFilePath, pidFilePath)

def readPidFile():
    try:
        with open(pidFilePath, 'r') as pidFile:
            storedPid = int(pidFile.read())
    except OSError:
        return None
    except ValueError:
        return None
    return storedPid

def removePidFile():
    try:
        os.remove(pidFilePath)
    except OSError:
        pass

@bpy.app.handlers.persistent
def writePidHandler(*args):
    writePidFileAtomic()

@bpy.app.handlers.persistent
def startRenderJobHandler(*args):
    global isRendering
    global startTime
    isRendering = True
    
    if bpy.context.preferences.addons[__name__].preferences.resetTimer:
        startTime = time.time()

@bpy.app.handlers.persistent
def endRenderJobHandler(*args):
    global isRendering
    global renderedFrames
    global startTime
    isRendering = False
    renderedFrames = 0
    
    if bpy.context.preferences.addons[__name__].preferences.resetTimer:
        startTime = time.time()

@bpy.app.handlers.persistent
def postRenderHandler(*args):
    global renderedFrames
    renderedFrames += 1
    
def updatePresenceTimer():
    updatePresence()
    return 5.0

def updatePresence():
    stateText = None
    detailsText = None
    smallIcon = None
    smallIconText = None
    
    # Pre-Checks
    readPid = readPidFile()
    if readPid is None:
        writePidFileAtomic()
    elif readPid != os.getpid():
        rpcClient.clear()
        return
    
    # Addon Preferences
    prefs = bpy.context.preferences.addons[__name__].preferences

    ## LARGE ICON
    if prefs.displayVersion:
        if prefs.displayEngine:
            largeIconText = getRenderEngineStr() + " in " + getVersionStr()
        else:
            largeIconText = getVersionStr()
    else:
        if prefs.displayEngine:
            largeIconText = getRenderEngineStr()
        else:
            largeIconText = None

    ## SMALL ICON
    activeMode = bpy.context.object.mode
    if prefs.displayMode and activeMode:
        smallIcon = activeMode.lower()
        smallIconText = activeMode.replace("_", " ").title()
        
        if "MODE" in activeMode:
            smallIconText = activeMode.replace("_", " ").title()
        else:
            smallIconText = f'{activeMode.replace("_", " ").title()} Mode' 
            
    ## DETAILS AND STATE
    if isRendering:
        smallIcon = "render"
        if prefs.displayRenderStats:
            smallIconText = f"{bpy.context.scene.render.resolution_x}x{bpy.context.scene.render.resolution_y}"
        else:
            smallIconText = None
        # Rendering Details (prefs)

        if prefs.enableDetails:
            if prefs.detailsType == "literal":
                if prefs.displayFileName and getFileName():
                    detailsText = f"Rendering {getFileName()}.blend"
                else:
                    detailsText = f"Rendering a project"
            else:
                detailsText = str(prefs.detailsCustomText)
            
        # Rendering State
        if renderedFrames > 0:
            frameRange = getFrameRange()
            if prefs.displayRenderStats:
                smallIconText = f"{bpy.context.scene.render.resolution_x}x{bpy.context.scene.render.resolution_y}@{bpy.context.scene.render.fps}fps"
            else:
                smallIconText = None
            if prefs.displayFrames:
                stateText = f"Frame {frameRange[0]} of {frameRange[1]}"
        else:
            if prefs.enableState and prefs.displayFrames:
                stateText = f"Frame {bpy.context.scene.frame_current}"
    else: ## NOT RENDERING
        if prefs.enableDetails:
            if prefs.detailsType == "literal":
                if prefs.displayFileName and getFileName():
                    detailsText = f"{getFileName()}.blend"
                else:
                    detailsText = "Working on a project"
            else:
                if prefs.detailsCustomText and len(prefs.detailsCustomText) > 1:
                    detailsText = str(prefs.detailsCustomText)
                else: # Details cannot be empty or less than 2 chars but for some reason this works too
                    detailsText = "  "
        else:
            detailsText = "  "
            
        if len(prefs.stateCustomText) > 1:
            stateText = str(prefs.stateCustomText)
        
        # GET COUNTS      
        if prefs.enableState:
            if prefs.stateRandomize:
                textCycles = []
                if prefs.stateCustomText:
                    textCycles.append(prefs.stateCustomText)
                if prefs.stateDisplayObjects:
                    textCycles.append(getObjectCount())
                if prefs.stateDisplayFaces:
                    textCycles.append(getFaceCount())
                if prefs.stateDisplayBones:
                    textCycles.append(getBoneCount())
                if prefs.stateDisplayMats:
                    textCycles.append(getMatCount())
                if prefs.stateDisplayKeys:
                    textCycles.append(getKeyCount())
                if prefs.stateDisplayFrame:
                    textCycles.append(getCurrentFrame())
                    
                if textCycles:
                    stateText = random.choice(textCycles)
                else:
                    stateText = "  "

            else:
                if prefs.stateCustomText:
                    stateText = prefs.stateCustomText
                if prefs.stateDisplayObjects:
                    stateText = getObjectCount()
                if prefs.stateDisplayFaces:
                    stateText = getFaceCount()
                if prefs.stateDisplayBones:
                    stateText = getBoneCount()
                if prefs.stateDisplayMats:
                    stateText = getMatCount()
                if prefs.stateDisplayKeys:
                    stateText = getKeyCount()
                if prefs.stateDisplayFrame:
                    stateText = getCurrentFrame()
                
    # Start Time (prefs)
    if prefs.enableTime and not isRendering:
        fStartTime = startTime
    elif prefs.enableTime and isRendering:
        fStartTime = startTime
    else:
        fStartTime = None

    rpcClient.update(
        pid=os.getpid(),
        start=fStartTime,
        state=stateText,
        details=detailsText,
        small_image=smallIcon,
        small_text=smallIconText,
        large_image='blenderlogo',
        large_text=largeIconText,
    )

def getFileName():
    name = bpy.path.display_name_from_filepath(bpy.data.filepath)
    if name == "":
        return None
    else:
        return name

def getObjectCount():
    return f"{len(bpy.context.selectable_objects):,d} total objects"
    
def getFaceCount():
    count = 0
    for element in bpy.context.scene.objects:
        if element.type == "MESH":
            count += len(element.data.polygons)
    return f"{count:,d} total faces"

def getBoneCount():
    count = 0
    for element in bpy.context.scene.objects:
        if element.type == "ARMATURE":
            count += len(element.data.bones)
    return f"Working with {count:,d} bones"
    
def getMatCount():
    return f"{len(bpy.data.materials):,d} total materials"
    
def getKeyCount():
    keyframes = []
    if bpy.context.scene.objects:
        for obj in bpy.context.scene.objects:
            anim = obj.animation_data
            if anim is not None and anim.action is not None:
                for fcu in anim.action.fcurves:
                    for keyframe in fcu.keyframe_points:
                        x, y = keyframe.co
                        if x not in keyframes:
                            keyframes.append((math.ceil(x)))
    return f"{len(keyframes):,d} frames animated"
        
def getCurrentFrame():
    return f"Viewing frame {bpy.context.scene.frame_current:,d}"
    
def getVersionStr():
    verTup = bpy.app.version
    verChar = bpy.app.version_char
    return f"{verTup[0]}.{verTup[1]}.{verTup[2]}{verChar}"

def getRenderEngineStr():
    internalName = bpy.context.engine
    internalNameStripped = internalName.replace("BLENDER_", "").replace("_", " ")
    return internalNameStripped.title() + " Engine"

def getFrameRange():
    start = bpy.context.scene.frame_start
    end = bpy.context.scene.frame_end
    cursor = bpy.context.scene.frame_current
    return (cursor - start + 1, end - start + 1)


class RpcPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    ## LARGE ICON TOOLTIP
    displayEngine: bpy.props.BoolProperty(
        name = "Render Engine",
        description = "Displays the current render engine",
        default = True,
    )

    displayVersion: bpy.props.BoolProperty(
        name = "Blender Version",
        description = "Displays the version of Blender software",
        default = True,
    )
    
    ## SMALL ICON TOOLTIP
    displayMode: bpy.props.BoolProperty(
        name = "Active Mode",
        description = "Displays the current mode (Object, Edit, Pose, etc.) from the 3D Viewport",
        default = True,
    )
    
    displayRenderStats: bpy.props.BoolProperty(
        name = "Render Stats",
        description = "Displays render information such as camera resolution and FPS where applicable",
        default = True,
    )
    
    ## DETAILS
    enableDetails: bpy.props.BoolProperty(
        name = "Enabled",
        description = "Enables 'details' property. This is the top-most piece of text shown in the presence",
        default = True,
    )
    
    detailsType: bpy.props.EnumProperty(
        name = "Display",
        items = (
            ("literal", "Literal", "Changes depending on what you're doing (ex. while rendering it will display 'Rendering a project'"),
            ("custom", "Custom", "A string that will display in the 'details' property. Two characters or longer"),
        ),
        default = "literal",
    )
    
    displayFileName: bpy.props.BoolProperty(
        name = "Display File Name",
        description = "Replace literal string to your .blend file name (ex. 'project.blend')",
        default = False,
    )
    
    detailsCustomText: bpy.props.StringProperty(
        name = "Custom",
        description = "Your custom text goes here. Two characters or longer",
        default = "",
    )
    
    displayFrames: bpy.props.BoolProperty(
        name = "Frame Range",
        description = "Displays range of currently rendering frames (ex. 'Frame 1 of 100')",
        default = True,
    )

    
    ## STATE
    enableState: bpy.props.BoolProperty(
        name = "Enabled",
        description = "Enables 'state' property. This text is shown right under the 'Details' in the presence",
        default = False,
    )
    
    stateRandomize: bpy.props.BoolProperty(
        name = "Randomize",
        description = "Allows you to select multiple options. Randomly picks a stat to display every few seconds.",
        default = False,
    )

    stateCustomText: bpy.props.StringProperty(
        name = "Custom",
        description = "Your custom text goes here. Two characters or longer",
        default = "",
    )

    stateDisplayObjects: bpy.props.BoolProperty(
        name = "Object Count",
        description = "Displays the number of all objects in the scene.",
        default = False,
    )
    
    stateDisplayFaces: bpy.props.BoolProperty(
        name = "Face Count",
        description = "Displays the sum of all faces on all meshes in the scene.",
        default = False,
    )
    
    stateDisplayBones: bpy.props.BoolProperty(
        name = "Bone Count",
        description = "Displays the sum of all bones on all armatures in the scene.",
        default = False,
    )
    
    stateDisplayMats: bpy.props.BoolProperty(
        name = "Material Count",
        description = "Displays the number of all materials in the scene.",
        default = False,
    )
    
    stateDisplayKeys: bpy.props.BoolProperty(
        name = "Keyframe Count",
        description = "Displays the number of frames that have atleast one keyframe on the currently selected object.",
        default = False,
    )
    
    stateDisplayFrame: bpy.props.BoolProperty(
        name = "Current Frame",
        description = "Displays the number of the current frame you're viewing.",
        default = False,
    )
    
    
    ## TIME ELAPSED
    enableTime: bpy.props.BoolProperty(
        name = "Enabled",
        description = "Displays the total amount of time elapsed since the plugin was enabled",
        default = True,
    )
    
    resetTimer: bpy.props.BoolProperty(
        name = "Reset On Render",
        description = "While enabled, the elapsed time will reset when a render begins",
        default = True,
    )

    def draw(self, context):
        prefs = bpy.context.preferences.addons[__name__].preferences
        cyclers = [prefs.stateCustomText, prefs.stateDisplayObjects, prefs.stateDisplayFaces, prefs.stateDisplayBones, prefs.stateDisplayMats, prefs.stateDisplayKeys, prefs.stateDisplayFrame]
        cyclStr = ["stateCustomText", "stateDisplayObjects", "stateDisplayFaces", "stateDisplayBones", "stateDisplayMats", "stateDisplayKeys", "stateDisplayFrame"]

        layout = self.layout.row()
        colLeft = layout.column()
        colRight = layout.column()
        
        # Large Icon Tooltip
        boxLrg = colLeft.box()
        boxLrg.label(text="Large Icon Tooltip", icon="BLENDER")
        boxLrg.prop(self, "displayEngine")
        boxLrg.prop(self, "displayVersion")

        # Small Icon Tooltip
        boxSml = boxLrg.box()
        boxSml.label(text="Small Icon", icon="PROP_CON")
        boxSmlView = boxSml.row().box()
        boxSmlView.label(text="Viewport", icon="VIEW3D")
        boxSmlView.prop(self, "displayMode")
        boxSmlRender = boxSml.row().box()
        boxSmlRender.label(text="Rendering", icon="RENDER_STILL")
        boxSmlRender.prop(self, "displayRenderStats")
        
        # Details Text (Top)
        boxDts = colRight.box()
        boxDts.label(text="Details", icon="ALIGN_TOP")
        boxDts.prop(self, "enableDetails")
        if prefs.enableDetails:
            boxDtsSettings = boxDts.row().box()
            boxDtsSettings.prop(self, "detailsType")
            if prefs.detailsType == "custom":
                boxDtsSettings.prop(self, "detailsCustomText")
            if prefs.detailsType == "literal":
                boxDtsSettings.prop(self, "displayFileName")
        
        # State Text (Middle)
        boxSt = colRight.box()
        boxSt.label(text="State", icon="ALIGN_MIDDLE")
        boxSt.prop(self, "enableState")
        
        if prefs.enableState:
            boxStViewSettings = boxSt.row().box()
            boxStViewSettings.label(text="Viewport", icon="VIEW3D")
            boxStViewSettings.prop(self, "stateRandomize")
            boxStViewCyclers = boxStViewSettings.row().box()
            
            if not prefs.stateRandomize:
                boxStViewSettings.label(text="'Randomize' is not enabled. Only one option can be enabled at a time.")
            
            boxStViewSettings.separator(factor=0.5)
            
            e = False
            d = False
            if not prefs.stateRandomize:
                i = 0
                for value in cyclers:
                    if d:
                        prefs[cyclStr[i]] = False
                    if value and not d:
                        e = True
                        d = True
                        boxStViewCyclers.prop(self, cyclStr[i])
                    i += 1

            if not e:
                for value in cyclStr:
                    boxStViewCyclers.prop(self, value)

            
            boxStViewSettings = boxSt.row().box()
            boxStViewSettings.label(text="Rendering", icon="RENDER_STILL")
            boxStViewSettings.prop(self, "displayFrames")

        # Time Elapsed (Bottom)
        boxTm = colRight.box()
        boxTm.label(text="Time Elapsed", icon="ALIGN_BOTTOM")
        boxTm.prop(self, "enableTime")

        if prefs.enableTime:
            boxTmSettings = boxTm.column()
            boxTmSettings.prop(self, "resetTimer")
