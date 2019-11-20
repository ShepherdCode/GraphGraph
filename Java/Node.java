import java.util.*;
public class Node {
    int id;
    boolean visited;
    ArrayList<Edge> edges;
    public Node (int id)     {
        this.id = id;
        edges = new ArrayList<Edge>(10);
    }
    public int getID () {
        return id;
    }
    public String toString () {
        return "Node("+id+")";
    }
    public int getDegree() {
        return edges.size();
    }
    public void setVisited (boolean state) {
        visited = state;
    }
    public boolean wasVisited () {
        return visited;
    }
    public void addEdge (Edge e) {
        edges.add(e);  // TO DO: check for redundancy
    }
    public Edge getEdge (int i) {
        return edges.get(i);
    }
    public int getNumEdges() {  // same as getNumNeighbors
        return edges.size();
    }
    public Node getNeighbor(int i) {
        Edge e = getEdge(i);
        Node neighbor = e.getOtherNode(this);
        return neighbor;
    }
        
}
