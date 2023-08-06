Power-sysGraph explores relations of power in graphs.
Given a directed graph, this Python package calculates the colonization matrix and properties such as hierarchy and mutualism.
It contains only the "system" class.

x = system(n_nodes, edge, ..., edges=0, weight=0.1)
    Instantiate this way a power system. Class will automatically calculate the colonization matrix of the system.

    Arguments:

        n_nodes:    int, the number of nodes in the system (the first node will be node 0)

        edge, ...:  (optional) tuples of the form (out, in, weight) that define single edges:
                        out:    int, the out node of the edge
                        in:     int, the in node of the edge
                        weight: float between 0 and 1 (both excluded), the weight of the edge

        edges:      (optional) int, the number of random edges to add (you can use this argument
                    when the previous edge argument is empty, otherwise it will be ignored)

        weight:     (optional) float between 0 and 1 (both excluded), the weight of the random 
                    edges (default 0.1)

    Properties:

        system.graph:           networkx.DiGraph()

        system.n:               int, the number of nodes

        system.edge_list:       list of tuples of the form (out, in, weight)

        system.adjacency:       list of lists which contains the adjacency matrix

        system.colonization:    list of lists which contains the colonization matrix. 
                                The colonization of node X in node Y is system.colonization[X][Y]

        system.hierarchy:       float

        system.mutualism:       float

        system.freedom:         float

        system.cooperation:     float

    Methods:

        system.show():          It shows a figure with adjacency graph, histogram of colonizations and 
                                donut of properties.
                                layout: (optional) string. Admitted values:
                                "circular", "random", "shell", "spring", "spectral", "spiral", "tree" 
                                (default: "random")

Example:

import power_sysGraph as ps
J = ps.system(8, (0, 1, 0.5), (1, 2, 0.5))
J.show('tree')
print ('Colonization of 0 in 2: ', J.colonization[0][2])