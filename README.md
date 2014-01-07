BiomeEdit
=========

An easy to use Biome Config editor for Terrain Control Biomes

Features
--------
 * In place editing of BiomeConfig files (this means comments and line spaceing are preserved)
 * Opening multiple files or whole folders
 * Saveing all open biomes
 * Saveing a particular Biome
 * Saveing a biome to another location or with a different name
 * Saveing all open biomes to another folder

Planned Features
----------------
 * Biome tabs that allow you to edit individual biomes with a nice ui
 * Fully working undo/redo functionality
 * copying data out of grid table (for what ever reason)
 * maybe pasting data into grid table
 * One current limitation is that you can only edit attributes or fields that are or were in a previously opened Biome. It will not be able to add fields that do not appear in any of the opened biomes. It would nice to improve this by adding a list of default fields and a way to add extra fields as needed.
 
Requirements
------------
 * Python 2.7 (not tested on earlier versions)
 * wxpython 2.8 (or higher)

Installation/Running
-------------------
If on Linux just make sure you have the right packages then download the repository to a directory and run the following command from inside that directory.

    python BiomeEdit.py
    
Its important to note that currently the only files needed are *BiomeEdit.py* and *BiomeEditUI.py*
The other files are important for development but not needed to run the app.


Windows Directions coming soon.


Basic Useage
------------
Most everything is pretty obvious but there are a few things to note.

 * Biome tabs are not currently implemented and only act as a placeholder
 * You can save/save as/close individual biomes when on their tab
 * Double clicking on a biome label in the 'All Biomes' tab will take you to that biomes tab
 * While you can open the same biome twice it's not recommended unless you are planing to save that biome as a different file.
 * If a Biome did not have a particular attribute or field in it before editing it will be appended to the end.
 * Its very important when saveing a biome to properly name that biome ending in BiomeConfig.ini. There may or may not be unexpected behavior if you don't.
