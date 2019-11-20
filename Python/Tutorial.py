#!/usr/local/bin/python3
# Assume: pip3 install python-igraph
import igraph

class Tutorial:

    def print_basic_stats ( self, graph ):
        print ( "----------------")
        print ( graph )
        # print ( dir(graph) )  # show every possible attribute
        # print ( graph["name"] )   # show one attribute
        if graph.is_directed():
            print ("Directed graph")
            print ( " in-degree: " ,end='' )
            print ( graph.indegree( [0,1,2,3] ) )
            print ( " out-degree: " ,end='' )
            print ( graph.outdegree( [0,1,2,3] ) )
            # print ( graph.betweenness(vertices=[0,1,2,3], directed=True) )
        else:
            print ("Undirected graph")
            print ( " degree: " ,end='' )
            print ( graph.degree( [0,1,2,3] ) )
        print ( " node betweenness " ,end='' )
        print ( graph.betweenness() )
        print ( " edge betweenness: " ,end='' )
        print ( graph.edge_betweenness() )
        print ( "----------------")

    def main (self):

        ug = igraph.Graph(4)
        ug.add_edges( [ (0,1), (1,2), (2,3) ] )
        ug["name"] = "Undirected Graph Tutorial"
        self.print_basic_stats (ug)
        un = None

        dg = igraph.Graph(4,directed=True)
        dg.add_edges( [ (0,1), (1,2), (2,3) ] )
        dg["name"] = "Directed Graph Tutorial"
        self.print_basic_stats (dg)
        dn = None

if __name__ == '__main__':
    instance=Tutorial()
    instance.main()

