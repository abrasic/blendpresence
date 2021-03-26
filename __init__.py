import bpy
import os
import sys
import time
import math
import random
from .pypresence import pypresence as rpc

bl_info = {
    "name": "BlendPresence",
    "description": "Discord Rich Presence for Blender 2.9x",
    "author": "Abrasic",
    "version": (1, 4, 0),
    "blender": (2, 90, 1),
    "category": "System",
}

rpcClient = rpc.Presence("766373631424200705")
pidFilePath = os.path.join(os.path.dirname(os.path.normpath(bpy.app.tempdir)), "BlendRpcPid")
startTime = None
isRendering = False
renderedFrames = 0
timer = 5

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
    return timer

def updatePresence():
    global timer
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
    
    if prefs.generalEnable:
        timer = prefs.generalUpdate

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
        if prefs.displayMode and bpy.context.mode:
        
            modes = {
                "OBJECT": ["Object Mode", "object"],
                "EDIT_": ["Edit Mode", "edit"],
                "POSE": ["Pose Mode", "pose"],
                "SCULPT": ["Sculpt Mode", "sculpt"],
                "PAINT_GPENCIL": ["Draw Mode", "paint_gpencil"],
                "PAINT_TEXTURE": ["Texture Paint", "texture_paint"],
                "PAINT_VERTEX": ["Vertex Paint", "vertex_paint"],
                "PAINT_WEIGHT": ["Weight Paint", "weight_paint"],
            }
            
            activeMode = bpy.context.mode
            
            for i in modes:
                if i in activeMode:
                    smallIconText = modes[i][0]
                    smallIcon = modes[i][1]
                
        ## DETAILS AND STATE
        if isRendering:
            smallIcon = "render"
            if prefs.displayRenderStats:
                smallIconText = f"Rendering | {bpy.context.scene.render.resolution_x}x{bpy.context.scene.render.resolution_y}"
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
                    smallIconText = f"Rendering | {bpy.context.scene.render.resolution_x}x{bpy.context.scene.render.resolution_y}@{bpy.context.scene.render.fps}fps"
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
              
            
            # GET COUNTS      
            if prefs.stateType == "custom":
                if len(prefs.stateCustomText) > 1:
                    stateText = str(prefs.stateCustomText)
                else:
                    stateText = "  "
            if prefs.stateType == "obj":
                stateText = getObjectCount()
            if prefs.stateType == "poly":
                stateText = getPolyCount()
            if prefs.stateType == "bone":
                stateText = getBoneCount()
            if prefs.stateType == "mat":
                stateText = getMatCount()
            if prefs.stateType == "frame":
                stateText = getCurrentFrame()
            if prefs.stateType == "anim":
                stateText = getFramesAnimated()
            if prefs.stateType == "active":
                stateText = getActiveObject()
                    
        # Start Time (prefs)
        if prefs.enableTime and not isRendering:
            fStartTime = startTime
        elif prefs.enableTime and isRendering:
            fStartTime = startTime
        else:
            fStartTime = None

        # Push to RPC
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

    else:
        rpcClient.clear()

def getFileName():
    name = bpy.path.display_name_from_filepath(bpy.data.filepath)
    if name == "":
        return None
    else:
        return name

def getObjectCount():
    return f"{len(bpy.context.selectable_objects):,d} total objects"
    
def getPolyCount():
    count = 0
    for element in bpy.context.scene.objects:
        if element.type == "MESH":
            count += len(element.data.polygons)
    return f"{count:,d} total polys"

def getBoneCount():
    count = 0
    for element in bpy.context.scene.objects:
        if element.type == "ARMATURE":
            count += len(element.data.bones)
    return f"Working with {count:,d} bones"
    
def getMatCount():
    return f"{len(bpy.data.materials):,d} total materials"
    
def getFramesAnimated():
    if bpy.data.actions:
        ac = [action.frame_range for action in bpy.data.actions]
        k = (sorted(set([item for sublist in ac for item in sublist])))
        return f"{math.floor(k[-1]):,d} frames animated"
    else:
        return "  "
        
def getCurrentFrame():
    i = "Viewing frame"
    if bpy.context.screen.is_animation_playing:
       i = "Playing animation |"
       
    return f"{i} {bpy.context.scene.frame_current:,d}"
    
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
    
def getActiveObject():
    if bpy.context.active_object:
        return bpy.context.active_object.name
    else:
        return ""

class RpcPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    ## GENERAL SETTINGS
    generalEnable: bpy.props.BoolProperty(
        name = "Enabled",
        description = "Enable Discord Rich Presence",
        default = True,
    )
    
    generalUpdate: bpy.props.IntProperty(
        name = "Update Every",
        description = "How long the presence will update in seconds. A value of 5 is recommended",
        default = 5,
        min = 1,
        max = 60
    )
    
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
        description = "Enables 'state' property. This is the middle piece of text shown in the presence",
        default = True,
    )
    
    stateType: bpy.props.EnumProperty(
        name = "Display",
        items = (
            ("anim", "Frames Animated", "Displays the frame number that holds the last keyframe from all given actions."),
            ("poly", "Polygon Count", "Display the total amount of objects in the current scene"),
            ("bone", "Bone Count", "Display the total amount of armature bones in the current scene"),
            ("mat", "Material Count", "Display the total amount of materials in the current scene"),
            ("obj", "Object Count", "Display the total amount of objects in the current scene"),
            ("active", "Active Object", "Display the name of the curent active object selected. If none is seleced then this will return nothing."),
            ("frame", "Current Frame", "Display the current frame being viewed in the timeline. The text will also change if you are playing back an animation."),
            ("custom", "Custom", "A string that will display in the 'details' property. Two characters or longer"),
        ),
        default = "custom",
    )

    stateCustomText: bpy.props.StringProperty(
        name = "Custom",
        description = "Your custom text goes here. Two characters or longer",
        default = "",
    )

    stateDisplayObjects: bpy.props.BoolProperty(
        name = "Object Count",
        description = "Displays the number of all objects in the scene",
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

        layoutTop = self.layout.row()
        layout = self.layout.row()
        colLeft = layout.column()
        colRight = layout.column()
        
        # Core
        layoutTop.prop(self, "generalEnable")
        
        if prefs.generalEnable:
            layoutTop.prop(self, "generalUpdate")
            
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
                boxStViewSettings.prop(self, "stateType")
                
                if prefs.stateType == "custom":
                    boxStViewSettings.prop(self, "stateCustomText")

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
