public class Problems {
    public Problems ()    {
    }
    
    public static void line () {
        Graph g = new Graph(false);
        g.addEdge (1,2);
        g.addEdge (2,3);
        g.addEdge (3,4);
        g.addEdge (3,5);
        printStats (g);
        int i=2;
        int j=3;
        System.out.print("Shortest path "+i+" to "+j+" :");
        System.out.println(g.shortestPath(i,j,1,100));
    }    

    public static void q1 () {
        Graph g = new Graph(false);
        g.addEdge (1,2);
        g.addEdge (1,4);
        g.addEdge (1,6);
        g.addEdge (2,3);
        g.addEdge (3,4);
        g.addEdge (3,5);
        g.addEdge (4,5);
        g.addEdge (5,6);
        g.addEdge (6,7);
        printStats (g);
        int i=1;
        int j=4;
        System.out.print("Shortest path "+i+" to "+j+" :");
        System.out.println(g.shortestPath(i,j,1,100));
    }
    
    public static void printStats (Graph g) {
        System.out.println("===Graph for Step 1===");
        System.out.printf("Graph has %d nodes, %d edges, %7.3f density \n",
            g.getNumNodes(), g.getNumEdges(), g.getDensity());
        System.out.println("* Degree and Degree Centrality");
        for (int n = 1; n <= g.getNumNodes(); n++) {
            Node node = g.getNodeByID(n); 
            System.out.printf("Node %5d : degree %7d : centrality %7.3f \n",
                n,node.getDegree(),g.getDegreeCentrality(n));
        }
        for (int n = 1; n <= g.getNumNodes(); n++) {
            Node node = g.getNodeByID(n); 
            System.out.printf("Node %5d : between centrality %7d : normalized %7.3f \n",
                n,g.getBetweenCentrality(n),g.getNormalizedBC(n));
        }
    }
} 


