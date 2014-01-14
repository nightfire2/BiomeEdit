BiomeEdit
=========

An easy to use Biome Config editor for Terrain Control Biomes

Features
--------
 * In place editing of BiomeConfig files (this means comments and line spaceing are preserved)
 * Opening multiple files or whole folders
 * Undo Redo Functionality (NEW!)
 * Saveing all open biomes
 * Saveing a particular Biome
 * Saveing a biome to another location or with a different name
 * Saveing all open biomes to another folder

Planned Features
----------------
 * Biome tabs that allow you to edit individual biomes with a nice ui
 * Field tool tips when hovering over a field label in the All Biomes tab.
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

    ./BiomeEdit.py

If you are on windows there is a pre built package made using pyinstaller that makes things pretty straight forward.
Simply right click on [this](https://github.com/nightfire2/BiomeEdit/blob/master/packages/BiomeEditWindows.zip) link and select save as to download the packaged windows version. Then extract the contents to a folder. You can then run the BiomeEdit.exe file to run the application. You will still need to have python installed on the computer.


Basic Useage
------------
Most everything is pretty obvious but there are a few things to note.

 * Biome tabs are not currently implemented and only act as a placeholder
 * You can save/save as/close individual biomes when on their tab
 * Double clicking on a biome label in the 'All Biomes' tab will take you to that biomes tab
 * While you can open the same biome twice it's not recommended unless you are planing to save that biome as a different file.
 * If a Biome did not have a particular attribute or field in it before editing it will be appended to the end.
 * Its very important when saveing a biome to properly name that biome ending in BiomeConfig.ini. There may or may not be unexpected behavior if you don't.
 * There is a minor bug with the undo/redo functionality where if you save then undo a change you had made it will not correctly update the label of the config to show that it is different from when it was last saved. Note that if you close with out saveing all it will not ask you if you want to save those chances and will simply exit.
