# WSN_Localizer

We assume a certain number of WSN nodes, say N, are placed randomly in a plain so that each node has at least a few say M minimum neighboring nodes within its transmitting range.
We assume that each node participates in a localization procedure (algorithm) at regular intervals to generate a list of all nodes N with their node-no, location information x and y using received signal strengths.


<img src="Readme_files/Main.png">

Figure-1 Simulation of a Wireless Sensor Network (WSN) with interactive GUI to demonstrate a new Localization algorithm. 

This Algorithm is used for a Novel Energy Efficient Routing Algorithm https://github.com/hsmazumdar/WSN_Router/tree/main . Initially populate selected number of nodes, with random placement on canvas using 'File' menu of by simply pressing (Cnt+d)

Quick Start Steps:

Download the zip file and unzip in a folder ‘WSN_Localizer’.
Select ‘WsnLocalize.py’ file and load in VS Code
Install necessary library components in VC Code
Run 'WsnLocalize.py' to popup 'WSN Localizing' application of figure-1
Open 'File' menu tab and press 'Draw Nodes (Cnt+d)' tab or press 'Control + d' to populate randomly distributed nodes as shown in figure-1. The default number of nodes are 100 and can be changed using ‘Max Nodes’ tab
