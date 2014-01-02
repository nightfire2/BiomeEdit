BiomeEdit
=========

An easy to use Biome Config editor for Terrain Control Biomes

Features
--------
 * In place editing of BiomeConfig files (this means comments and line spaceing are presereved)
 * Opening multiple files or whole folders
 * Saveing all open biomes
 * Saveing a particular Biome
 * Saveing a biome to another location or with a different name
 * Saveing all open biomes to another folder

Planned Features
----------------
 * Biome tabs that allow you to edit individual biomes with a nice ui
 
Requirements
------------
 * Python 2.7 (not tested on earlier versions)
 * wxpython 2.8 (or higher)

Instalation/Running
-------------------
If on Linux just make sure you have the right packages then download the repository to a directory and run the following command from inside that directory.

    python BiomeEdit.py
    
Its important to note that currently the only files needed are BiomeEdit.py and BiomeEditContainer.py 
The other files are important but not needed to run the app.


Windows Directions coming soon.


Basic Useage
------------
Most everything is pretty obvious but there are a few things to note.

 * Biome tabs are not currently implemented and only act as a placeholder
 * You can save/save as/close individual biomes when on their tab
 * Double clicking on a biome label in the 'All Biomes' tab will take you to that biomes tab
 * While you can open the same biome twice it's not recommended unless you are planing to save that biome 
 * If a Biome did not have a particular attribute or field in it before editing it will be appended to the end.
 * Its very important when saveing a biome to properly name that biome ending in BiomeConfig.ini. There may or may not be unexpected behavior if you don't.
