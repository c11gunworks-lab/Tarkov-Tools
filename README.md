# Tarkov-Tools
Small assortment of tools to assist with SPT modding

Contains three Unity Plugins (BundleDependencyExporter, FixAnimNames and TextureAssigner), and a few Python Scripts.

Drag and drop the .cs files into your unity project in the "editor" folder

run the python programs with "python .\$pythonprogram.py"

# BundleDependencyExporter:

will dump a list of all the bundles you're building as well as their dependencies. Run the "convert_bundles.py" to take this file and have it cleaned up for use in your mod.

# FixAnimNames:

is just fixes all the errors about your animation names not matching. Just an annoyance for me personally.

# Texture Assigner:

select all the material balls you want to have textures assigned to, and then run the tool. It will look for textures with the same name as the material ball and try to add them. Currently set up for Epics Shader workflow but can be changed. 

# The Texture Tool 

Usefull for taking textures from other games or from a model that doesn't have separated textures and splitting them for use in substance. 

Also takes base Tarkov textures as exported from AssetStudioGUI, and makes the red normals blue again, and splits the diffuse texture into a base color and a specular. Again, useful for using in Substance Painter for retexturing. 


Main features:
  Convert ORM or RMA textures to separate Ambient Occlusion, Roughness and Metallic maps
  Convert DirectX normals to OpenGL
  Split Diffuse
  Change Red to Blue Normals
  Rotate all images in a directory

#SPT ID Creator
Takes all of your jsons and makes an .sptid file for those using jetbrains rider with the SPT plugin.
