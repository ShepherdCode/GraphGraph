public class Edge {
    Node node1, node2;
    public Edge (Node n1, Node n2)    {
        node1 = n1; node2 = n2; // TO DO: guard against n1==n2
    }
    public Node getOtherNode (Node one) {
        if (node1==one) {
            return node2;
        }
        return node1; // TO DO: make sure n1 != one
    }
}
