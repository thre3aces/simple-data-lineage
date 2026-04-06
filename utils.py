import networkx as nx
from typing import Dict, Any, List, Set

def condense_graph(G_raw: nx.DiGraph, condense_threshold: int) -> nx.DiGraph:
    """
    Condense the nodes of a directed graph where a node has more than 
    a specified threshold of successors.

    Args:
        G_raw: The original NetworkX DiGraph.
        condense_threshold: The threshold above which successors will be condensed.

    Returns:
        A condensed NetworkX DiGraph.
    """
    G = nx.DiGraph()
    condensed_successors = set()
    
    # First pass: identify chokepoints and their condensed successors
    chokepoints = {}
    for node in G_raw.nodes():
        successors = list(G_raw.successors(node))
        if len(successors) > condense_threshold:
            condensed_node_id = f"Condensed_from_{node}"
            chokepoints[node] = {
                'id': condensed_node_id,
                'nodes': successors,
                'label': f"[{len(successors)} nodes]"
            }
            condensed_successors.update(successors)

    # Second pass: Build the condensed graph
    for u, v, data in G_raw.edges(data=True):
        if u in chokepoints:
            # u is a chokepoint, v is being condensed
            target = chokepoints[u]['id']
            G.add_node(target, label=chokepoints[u]['label'])
            G.add_edge(u, target, label=data.get('label', ''))
        elif v in condensed_successors:
            # v is condensed, but u is NOT the chokepoint that condensed it
            # (i.e. v has multiple parents)
            # Find which chokepoint(s) v belongs to
            for cp_node, cp_info in chokepoints.items():
                if v in cp_info['nodes']:
                    G.add_edge(u, cp_info['id'], label=data.get('label', ''))
        else:
            # Normal edge
            G.add_edge(u, v, label=data.get('label', ''))
            
    # Third pass: Handle edges FROM condensed nodes
    for cp_node, cp_info in chokepoints.items():
        for v in cp_info['nodes']:
            for successor in G_raw.successors(v):
                if successor not in condensed_successors:
                     G.add_edge(cp_info['id'], successor, label=G_raw[v][successor].get('label', ''))
                else:
                    # Successor is ALSO condensed (possibly by another chokepoint)
                    for cp_node_2, cp_info_2 in chokepoints.items():
                        if successor in cp_info_2['nodes']:
                             G.add_edge(cp_info['id'], cp_info_2['id'], label=G_raw[v][successor].get('label', ''))
    
    # Add labels to original nodes in G if not present
    # AND Ensure nodes that should be condensed are actually NOT in G
    nodes_to_remove = [node for node in G.nodes() if node in condensed_successors]
    for node in nodes_to_remove:
        G.remove_node(node)

    for node in G.nodes():
        if node not in [cp['id'] for cp in chokepoints.values()] and 'label' not in G.nodes[node]:
             # G.nodes[node] might have labels if it was added from edges that had them or something
             pass

    return G
