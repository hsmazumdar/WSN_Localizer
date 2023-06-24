# WSN_Localizer

We assume a certain number of WSN nodes, say N, are placed randomly in a plain so that each node has at least a few say M minimum neighboring nodes within its transmitting range.
We assume that each node participates in a localization procedure (algorithm) at regular intervals to generate a list of all nodes N with their node-no, location information x and y using received signal strengths.

<img src="Readme_files/Main.png">

Figure-1 Simulation of a Wireless Sensor Network (WSN) with interactive GUI to demonstrate a new Localization algorithm. 

This Algorithm is used for a Novel Energy Efficient Routing Algorithm https://github.com/hsmazumdar/WSN_Router/tree/main . Initially populate selected number of nodes, with random placement on canvas using 'File' menu of by simply pressing (Cnt+d)

Quick Start Steps:

1. Download the zip file and unzip in a folder ‘WSN_Localizer’.
2. Select ‘WsnLocalize.py’ file and load in VS Code
3. Install necessary library components in VC Code
4. Run 'WsnLocalize.py' to popup 'WSN Localizing' application of figure-1
5. Open 'File' menu tab and press 'Draw Nodes (Cnt+d)' tab or press 'Control + d' to populate randomly distributed nodes as shown in figure-1. The default number of nodes are 100 and can be changed using ‘Max Nodes’ tab
6. Press 'File->Localize' tab or press Cnt+z to localize all nodes as shown in figure-2
7. You may set 'Slow' checked using 'Tool->Slow' to new slow animation of localization 
8. Press 'File->Save' tab to open save file dialog box, select save file path and enter save file name. Press 'Save' button to save localize list of nodes.
9. Press 'File->Load' tab to open load file dialog box, select load file path and enter load file name. Press 'Load' button to load localize list of nodes as shown below.

LocalizeHsm.txt,100  =>File Name, Number of nodes

0,16,257,100,0       =>Serial no, x, y, state  

1,20,290,100,0

2,21,231,100,0

.........

<img src="Readme_files/Localize.png">

Figure-2 Simulation demonstrates WSN nodes Localization from initial three nodes of known coordinates connected using red lines. 

The proposed localizing algorithm for the wireless sensor network (WSN), the aim is to estimate the absolute global position (x,y) of all nodes from given position of three initial nodes which are within transmission range to each other. 
optimize the number of retransmissions in order to save the battery power of the nodes. Each node runs this algorithm in distributed edge computing mode and follows the following rules when receives a packet:

Algorithm:

1. Set the status all all the nodes to 0
2. Set the status of known position nodes to 1
3. Search 4 nodes such that 3 nodes are with status 1 and 1 node is with status 0, each node being in transmission range of other 3 nodes.
4. Estimate the 2 set of mirror symetry position coordinates of un-localized node using 2 of the 3 nodes of known coordinates using traingulation method.
5. Estimate 6 sets of th oordinates of un-localized node using all combination of 3 known coordinate nodes.
6. Locate common cordinate points in above 6 estimated coordinates and assigne this coordinate to unknown coordinate node. Set its status to 1.
7. Repeat the process from step 3 until step 3 is unable to find desired set of nodes.
