import numpy as np
from .._utils import Base

from licorice_font import font_format
note = font_format("NOTE", ["BLUE"])

class Laplacian(Base):
    def __init__(self, adata, adjacency_key="adjacency"):

        n_cells = adata.shape[0]
        A = adata.obsp[adjacency_key]

        self.__parse__(locals(), private=["adjacency_key", "n_cells"])

    def _configure_identity_matrix(self):
        if not hasattr(self, "_identity_matrix"):
            print(" - [{}] | Configuring identity matrix".format(note))
            self._identity_matrix = np.identity(self._n_cells)

    @property
    def identity_matrix(self):
        self._configure_identity_matrix()
        return self._identity_matrix

    def row_sum_normalize(self, A):

        print(" - [{}] | Computing row sum normalization of adjacency matrix".format(note))
        return A / A.sum(axis=1, keepdims=True)
    
    def __call__(self):
        return self.identity_matrix - self.row_sum_normalize(self.A)
    
def compute_Laplacian(adata, adjacency_key="adjacency", key_added="Laplacian"):
    
    L = Laplacian(adata)
    adata.obsp['Laplacian'] = L()