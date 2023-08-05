
import numpy as np
from licorice_font import font_format

note = font_format("NOTE", ["BLUE"])

def compute_adjacency_matrix(adata, edges_key="edges"):

    edges = adata.uns[edges_key]
    
    print(" - [{}] | Computing adjacency matrix".format(note))

    i, j = edges[:, 0], edges[:, 1]
    N = np.max([i, j]) + 1
    A = np.zeros((N, N))
    A[i, j] = 1
    A[j, i] = 1
    
    adata.obsp['adjacency'] = A