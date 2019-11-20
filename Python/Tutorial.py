# pip3 install python-igraph
# python3
import igraph

ug = igraph.Graph(4)
ug.add_edges( [ (0,1), (1,2), (2,3) ] )
ug["name"] = "Demo Undirected Graph"

print ( ug )
# print ( dir(ug) )  # show every possible attribute
# print ( ug["name"] )   # show one attribute
print ( " degree: " ,end='' )
print ( ug.degree( [0,1,2,3] ) )
print ( " edge betweenness: " ,end='' )
print ( ug.edge_betweenness())
print ( " node betweenness " ,end='' )
print (ug.betweenness())
ug = None

dg = igraph.Graph(4)
dg["name"] = "Demo Directed Graph"
dg.add_edges( [ (0,1), (1,2), (2,3) ] )

print ( dg )
print ( " degree: " ,end='' )
print ( dg.degree( [0,1,2,3] ) )
print ( " edge betweenness: " ,end='' )
print ( dg.edge_betweenness())
print ( " node betweenness " ,end='' )
print ( dg.betweenness())
dg = None
