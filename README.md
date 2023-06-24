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

Using the wireless sensor network (WSN) a localizing algorithm is proposed with the objective of determining the absolute global position (x, y) of all nodes. This algorithm utilizes the positions of three initial nodes that are within transmission range of each other. The primary focus is on optimizing the number of retransmissions to conserve the battery power of the nodes. Each node operates this algorithm in a distributed edge computing mode and adheres to the following rules upon receiving a packet:

Algorithm:

Initialize the status of all nodes as 0.
Set the status of nodes with known positions to 1.
Search for four nodes, where three nodes have a status of 1 and one node has a status of 0. These nodes should be within transmission range of each other.
Employ the triangulation method to estimate two sets of mirror symmetry position coordinates for the unlocalized node using two of the three known coordinate nodes.
Utilize all combinations of three known coordinate nodes to estimate six sets of coordinates for the unlocalized node.
Identify the common coordinate points among the six estimated sets and assign these coordinates to the unknown coordinate node. Update its status to 1.
Repeat the process from step 3 until it becomes impossible to find the desired set of nodes.
Localization concludes at the end of step 3.



