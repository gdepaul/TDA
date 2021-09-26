import networkx as nx
import itertools

import matplotlib.pyplot as plt
import plotly.graph_objects as go

def draw_2d_simplicial_complex(simplicial_complex, pos=None, return_pos=False, ax = None):
    """
    Draw a simplicial complex up to dimension 2 from a list of simplices, as in [1].
        
        Args
        ----
        simplicial_complex: a SAGE SimplicialComplex structure. (Added by Greg DePaul)
        
        pos: dict (default=None)
            If passed, this dictionary of positions d:(x,y) is used for placing the 0-simplices.
            The standard nx spring layour is used otherwise.
           
        ax: matplotlib.pyplot.axes (default=None)
        
        return_pos: dict (default=False)
            If True returns the dictionary of positions for the 0-simplices.
            
        References
        ----------    
        .. [1] I. Iacopini, G. Petri, A. Barrat & V. Latora (2019)
               "Simplicial Models of Social Contagion".
               Nature communications, 10(1), 2485.
               
        Authors: 
        .. I. Iacopini (Original Author) - github-username: iaciac
        .. G. DePaul - github-username: gdepaul
    """

    # Obtain simplices from SAGE simplicial complex
    vertices = set()
    for face in simplicial_complex.facets():
        for vertex in list(face):
            vertices.add(vertex)
    vertex_list = list(vertices)
    node_names_to_index = { vertex_list[i]:i for i in range(len(vertex_list))}

    simplices = []
    for face in simplicial_complex.facets():
        new_face = []
        for vertex in list(face):
            new_face.append(node_names_to_index[vertex])
        simplices.append(new_face)
    
    #List of 0-simplices
    nodes =list(set(itertools.chain(*simplices)))
    
    #List of 1-simplices
    edges = list(set(itertools.chain(*[[tuple(sorted((i, j))) for i, j in itertools.combinations(simplex, 2)] for simplex in simplices])))

    #List of 2-simplices
    triangles = list(set(itertools.chain(*[[tuple(sorted((i, j, k))) for i, j, k in itertools.combinations(simplex, 3)] for simplex in simplices])))
    
    if ax is None: ax = plt.gca()
    ax.set_xlim([-1.1, 1.1])      
    ax.set_ylim([-1.1, 1.1])
    ax.get_xaxis().set_ticks([])  
    ax.get_yaxis().set_ticks([])
    ax.axis('off')
       
    if pos is None:
        # Creating a networkx Graph from the edgelist
        G = nx.Graph()
        G.add_edges_from(edges)
        # Creating a dictionary for the position of the nodes
        pos = nx.spring_layout(G)
        
    # Drawing the edges
    for i, j in edges:
        (x0, y0) = pos[i]
        (x1, y1) = pos[j]
        line = plt.Line2D([ x0, x1 ], [y0, y1 ],color = 'black', zorder = 1, lw=0.7)
        ax.add_line(line);
    
    # Filling in the triangles
    for i, j, k in triangles:
        (x0, y0) = pos[i]
        (x1, y1) = pos[j]
        (x2, y2) = pos[k]
        tri = plt.Polygon([ [ x0, y0 ], [ x1, y1 ], [ x2, y2 ] ],
                          edgecolor = 'black', facecolor = plt.cm.Blues(0.6),
                          zorder = 2, alpha=0.4, lw=0.5)
        ax.add_patch(tri);

    # Drawing the nodes 
    for i in nodes:
        (x, y) = pos[i]
        circ = plt.Circle([ x, y ], radius = 0.02, zorder = 3, lw=0.5,
                          edgecolor = 'Black', facecolor = u'#ff7f0e')
        ax.add_patch(circ);

    if return_pos: return pos

def draw_3d_simplicial_complex(simplicial_complex):
    """
    Draw a simplicial complex up to dimension 2 from a list of simplices, as in [1].
        
        Args
        ----
        simplicial_complex: a SAGE SimplicialComplex structure. (Added by Greg DePaul)
        
        pos: dict (default=None)
            If passed, this dictionary of positions d:(x,y) is used for placing the 0-simplices.
            The standard nx spring layour is used otherwise.
           
        ax: matplotlib.pyplot.axes (default=None)
        
        return_pos: dict (default=False)
            If True returns the dictionary of positions for the 0-simplices.
            
        References
        ----------    
        .. [1] I. Iacopini, G. Petri, A. Barrat & V. Latora (2019)
               "Simplicial Models of Social Contagion".
               Nature communications, 10(1), 2485.
               
        Authors: 
        .. I. Iacopini (Original Author) - github-username: iaciac
        .. G. DePaul - github-username: gdepaul
    """

    # Obtain simplices from SAGE simplicial complex
    vertices = set()
    for face in simplicial_complex.facets():
        for vertex in list(face):
            vertices.add(vertex)
    vertex_list = list(vertices)
    node_names_to_index = { vertex_list[i]:i for i in range(len(vertex_list))}

    simplices = []
    for face in simplicial_complex.facets():
        new_face = []
        for vertex in list(face):
            new_face.append(node_names_to_index[vertex])
        simplices.append(new_face)
    
    #List of 0-simplices
    nodes =list(set(itertools.chain(*simplices)))
    
    #List of 1-simplices
    edges = list(set(itertools.chain(*[[tuple(sorted((i, j))) for i, j in itertools.combinations(simplex, 2)] for simplex in simplices])))

    #List of 2-simplices
    triangles = list(set(itertools.chain(*[[tuple(sorted((i, j, k))) for i, j, k in itertools.combinations(simplex, 3)] for simplex in simplices])))
    
    # Credit: Much of this code was lift from the site: https://deepnote.com/@deepnote/3D-network-visualisations-using-plotly-oYxeN6UXSye_3h_ulKV2Dw
       
    G = nx.Graph()
    G.add_edges_from(edges)
    Num_nodes = len(nodes)
     
    spring_3D = nx.spring_layout(G,dim=3, seed=18)

    #we need to seperate the X,Y,Z coordinates for Plotly
    x_nodes = [spring_3D[i][0] for i in range(Num_nodes)]# x-coordinates of nodes
    y_nodes = [spring_3D[i][1] for i in range(Num_nodes)]# y-coordinates
    z_nodes = [spring_3D[i][2] for i in range(Num_nodes)]# z-coordinates
    
    #We also need a list of edges to include in the plot
    edge_list = G.edges()
    
    #we  need to create lists that contain the starting and ending coordinates of each edge.
    x_edges=[]
    y_edges=[]
    z_edges=[]

    #need to fill these with all of the coordiates
    for edge in edge_list:
        #format: [beginning,ending,None]
        x_coords = [spring_3D[edge[0]][0],spring_3D[edge[1]][0],None]
        x_edges += x_coords

        y_coords = [spring_3D[edge[0]][1],spring_3D[edge[1]][1],None]
        y_edges += y_coords

        z_coords = [spring_3D[edge[0]][2],spring_3D[edge[1]][2],None]
        z_edges += z_coords
        
    #create a trace for the edges
    trace_edges = go.Scatter3d(x=x_edges,
                        y=y_edges,
                        z=z_edges,
                        mode='lines',
                        line=dict(color='black', width=2),
                        hoverinfo='none')
    #create a trace for the nodes
    trace_nodes = go.Scatter3d(x=x_nodes,
                             y=y_nodes,
                            z=z_nodes,
                            mode='markers',
                            marker=dict(symbol='circle',
                                        size=4,
                                        colorscale=['lightgreen','magenta'], #either green or mageneta
                                        line=dict(color='black', width=0.5)))

    #we need to set the axis for the plot 
    axis = dict(showbackground=False,
                showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title='')
    
    #also need to create the layout for our plot
    layout = go.Layout(width=800,
                    height=800,
                    showlegend=False,
                    scene=dict(xaxis=dict(axis),
                            yaxis=dict(axis),
                            zaxis=dict(axis),
                            ),
                    margin=dict(t=100),
                    hovermode='closest')
    
    #Include the traces we want to plot and create a figure
    data = [trace_edges, trace_nodes]
    fig = go.Figure(data=data, layout=layout)

    fig.show()