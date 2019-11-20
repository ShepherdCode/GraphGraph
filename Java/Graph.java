import java.util.*;
public class Graph {
    boolean directedGraph;
    ArrayList<Edge> edges;
    ArrayList<Node> nodes;
    public Graph (boolean directed)    {
        edges = new ArrayList<Edge>(100);
        nodes = new ArrayList<Node>(100);
        directedGraph = directed;
    }

    public Node getNodeByID (int id) {
        for (Node n : nodes) {
            if (n.getID() == id) {
                return n;
            }
        }
        return null;
    }

    public boolean contains (int nodeID) {
        return getNodeByID(nodeID) != null;
    }

    public Node addNode (int id) {
        Node n = getNodeByID (id);
        if (n==null) {
            n = new Node (id);
            nodes.add(n);
        }
        return n;
    }

    public Edge addEdge (int i1, int i2) {
        Node n1 = addNode (i1);
        Node n2 = addNode (i2);
        Edge e = new Edge (n1,n2); // TO DO: guard for duplicate edge
        n1.addEdge(e);
        n2.addEdge(e);
        edges.add(e);
        return e;
    }

    public int getNumNodes () {
        return nodes.size();
    }

    public int getNumEdges () {
        return edges.size();
    }

    public double getDensity () {
        int actualEdges = getNumEdges();
        int actualNodes = getNumNodes();
        int possibleEdges = actualNodes * (actualNodes-1);
        if (!directedGraph) {
            possibleEdges /= 2;
        }
        return 1.0*actualEdges/possibleEdges;
    }

    public double getDegreeCentrality(int nodeID) {
        int totalNodes = getNumNodes();
        Node n = getNodeByID(nodeID); // TO DO: guard against invalid node
        int degree = n.getDegree();
        double centrality = 1.0 * degree / ( totalNodes - 1);
        return centrality;
    }

    void unsetVisitedAllNodes() {
        for (Node node : nodes) {
            node.setVisited(false);
        }
    }
    
    public int getBetweenCentrality(int nodeID) {
        unsetVisitedAllNodes();
        int totalNodes = getNumNodes();
        Node n = getNodeByID(nodeID); // TO DO: guard against invalid node
        int between=0;
        return between;
    }

    void setVisited (boolean val) {
        for (Node n : nodes) {
            n.setVisited(val);
        }
    }
    
    public int shortestPath (int start, int end, int len, int shortest){
        setVisited(false);
        return sp(start,end,len,shortest);
    }
        
    int sp (int start, int end, int len, int shortest){
        Node s = getNodeByID (start);
        s.setVisited(true);
        for (int i = 0; i< s.getNumEdges(); i++) {
            Node next = s.getNeighbor(i);
            int nextID = next.getID();
            if (nextID==end) {
                if (len < shortest) {
                    shortest = len;
                }
                return shortest;
            }
            if (!next.wasVisited()) {
                len = sp (nextID, end, len, shortest);
                if (len < shortest) {
                    shortest = len;
                }
            }
        }
        s.setVisited(false);
        return shortest;
    }
    
    public double getNormalizedBC(int nodeID) {
        return 0.0;
    }
}
