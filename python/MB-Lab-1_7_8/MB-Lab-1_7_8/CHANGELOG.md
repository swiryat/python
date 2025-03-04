# CHANGE LOG

All changes will be documented here

# MB-Lab 1.7.8

## Added

- MB-Dev Character Development Framework introduced
- Hair Engine now adds hair shaders to Cycles and EEVEE

## Changed

- MBLabSkin2 uses Principled BSDF yet again
- Removed SSS scale group, replaced with Vector Math node
- Bump map added, Thickness map removed
- Modified skin oil maps
- Eyelash shader now has bump and gloss
- ExpressionEngine class now in it's own file
- Blush map converted to grayscale
- Modified Albedo maps
- Bump maps now 4k resolution
- Modified Freckle masks
- Modified Material Engine
- Changed lighting code
- MB-Lab has new version numbering scheme. Last number for dev purposes
- Sliders are now highlighted
- GUI update
- MBLab Pupil use Diffuse Node instead of Emission
- SSS Radius changed to more accurate values
- Freckles now include two colors

## Bug Fixes

- Poses don't show when user selects IK model
- Preserve Phenotype random function code fix
- Typo: Hands_Lenght, fixed in transformation and measurements JSON
- Typo: Various names in transformation files fixed
- Hair Dynamics bug fix for Nvidia GPU cards

# MB-Lab 1.7.7

## Added

- Hair System added
- Human Rotation Limits added
- New option to fit in reverse direction to convert a character-specific mesh to a generic proxy.
- New options to do more precise fitting by turning off some normally useful smoothing passes.
- New option in Preferences to remove censors

## Changed

- Blender 2.81.16 required for MB-Lab 1.7.7
- Afro Female now the default character on startup
- Updated GUI
- Removed Docs from project directory to it's own repository

## Bug Fixes

- Certain bones have to be precisely aligned to the rotation of a specific other bone, which required new code.
- Stretch to has to be applied to the muscle bones while fitting.
- B-Bone handles and certain constraints have to be fixed in the library file via a script.
- Fixed fitting of meshes that are very close to the skin.
- Replaced obj.hide_select = False with obj.hide_set(False) fixing Age update bug.
- Minor GUI edits to fix drawing issues.
- Fixed Bump and Displacement issues in MBLab_Skin2
- Fixed IK and IK/Muscle bugs
- Eye Displacement bug fixed

## Known Issues

- The Hair Engine does NOT apply a shader at this time
- Hair engine does not support shapekeys at this time


# MB-Lab 1.7.6

## Added

- New Skin Shader, MB-Lab Skin 2 added to the Realistic Humans
- New Tone maps based on character selection
- New Latino Model Type added to MB-Lab
- New South American Phenotype added
- New texture masks for skin shader
- New Nails shader added

## Changed

- Material Engine updated for new skin shader
- Alphabetized the characters list
- Modified freckle masks
- Changed structure of humanoid_library.blend
- Added model license types in character selection menu

## Bug Fixes

- Fixed MBLab_fur for EEVEE, renamed to MBLab_eyelash
- Fixed MBLab_human_eyes SSS rendering artifact in EEVEE

# MB-Lab 1.7.5

## Added

- Added icons and modified GUI
- Tongue shader added
- Improved Iris and Eyeball shaders
- Save/Load BVH Bone Config

## Changed

- Changed descriptions for male and female elf and dwarf characters
- Changed Blender minimum version to 2.80.74
- Removed Buggy message from Muscle checkbox because the Blender bug has been fixed
- Changed CREATION TOOLS in GUI to CREATION OPTIONS at startup
- Documentation updates
- Changed characters_config.json for tongue shader
- Rebuilt humanoid_library.blend file for Blender 2.80.74
- Reduced SSS value for EEVEE in human skin shader
- Edited bump maps
- Changed "Body Measures" in "Body Measures" to "Measurements" to fix confusion
- Eyes UV remapped

## Bug Fixes

- Fixed API change 'bpy.context.scene.update()' to 'bpy.context.view_layer.update()' in animationengine.py fixing BVH import bug
- Gloss fix for EEVEE in human skin shader
- Muscle FK and IK, Skeleton FK and IK roll fixes for various bones in armatures
- Registration bug that caused errors during unregistering classes
- Fix 'Bones rot. offset' in after-creation tools
- Fixed Skin complexion function related to SSS
- Toes_R connected bug fixed
- SSS scale fixed in Teeth shader

# MB-Lab 1.7.4

## Added

- New Procedural Eye shaders
- New Texture Mask for freckles

## Changed

- Deleted Principled BSDF shader networks for custom surface shaders
- Minor GUI edits
- Edited Bump and Albedo texture maps (NOT YET)
- Changed scaling of sub dermal map
- Updated Material Engine code for texture masks
- Added bug warning to Muscle checkbox
- When transferring weights for proxying, check the vertex is in the group
- Changed lighting setup using Area lights

## Bug Fixes

- Set lighting setup default to False, fixing a minor startup bug

# MB-Lab 1.7.3

## Added

 - Added Auto-Updater by CGCookie

## Bug Fixes

 - Fixed logging errors left over from original code


# MB-Lab 1.7.2

 - Changed Diffuse to Albedo in shaders and textures to reflect current shader terminology
 - New Roughness Map
 - Added Feet / Inches display in Body Measures panel
 - New Docs made with Sphinx


# MB-Lab 1.7.1b

## Changed

 - Replace algorithms.print_log_report by python standard logging
 - Use numpy to to calculate_disp_pixel
 - Code cleanup

## Bug Fixes

 - Fixed a spelling typo in facerig.populate_modifiers
 - Finalize character fix
 - Remove 'self' from args
 - Moved is_ik_armature, get_active_armature, get_deforming_armature, get_object_parent to utils.py
 - init.py uses get_active_armature and is_ik_armature from utils (previous was algorithms that wasn't imported)
 - Armature Toe Bone flipped pose bug

 ## Known Issues
 - Proxy Fitting was broken, now it is fixed
 - morphengine.py and humanoid.py reverted back to 1.7.0 version with logging added


# MB-Lab 1.7.1

## Added

 - New Facial Rig connected to shapekeys
 - EEVEE and CYCLES specific shading networks
 - New Clothes in the Assets directory ready to be added to proxies

## Known Issues

 - EEVEE Eye shader darker than normal trying to find a fix

# MB-Lab 1.7.0b

## Bug fixes

 - Fixed texture map lookup bug for Anime characters
 - Fixed a bug with unregistering the add-on

## Changed

 - Anime skin and eye shaders now grouped up
 - Moved Dermal and Displacement image import / export to File Tools
 - Changed and added missing descriptions


# MB-Lab 1.7.0

## Blender 2.80 Update!

 - Blender 2.80 Beta code port done by Amir Shehata amir.shehata@gmail.com

## Changed

 - Minor shader node edit to eyes to bring out iris more in renders
 - Changes in bump mapping, now uses both procedural and texture map
 - Removed skin age

## Added

 - New SSS Scalable vector node, brings scalable SSS to Principled BSDF
 - New bump texture map
 - New eye diffuse map for all realistic models


# MB-Lab 1.6.5

 - New shading network based on Principled BSDF for skin, eyes and teeth
 - New texture maps for specular and subdermal
 - Additional code to load new texture maps into the right image texture node
 - Added references to new texture maps for all character types
 - Changed Skin Editor values to reflect new PBR shading network

# MB-Lab 1.6.4

## Changed

 - Minor edits to skin bump mapping
 - Eye shader node tweek

## Added

 - Procedural freckle generator, basic functionality
 - Freckles editable in Skin Editor

# MB-Lab 1.6.3

## Changed

- Changed button labels to be more uniform
- Minor edits to shader networks

## Added

- Basic procedural pore and skin cell bump mapping
- Third layer of SSS added to simulate sub-dermal tissue

# MB-Lab 1.6.2

## Changed

- New layer of SSS added to skin shader
- Grouped Skin, Eye and Teeth shader networks into easy to edit nodes
- Modified Eye shader, added Diffuse and Glossy network
- Modified Eye shader to reduce red fireflies artifact
- Changed identity, version number, wiki and issue tracker URL
- Changed Blender version from 2,7,9 to 2,79,0
