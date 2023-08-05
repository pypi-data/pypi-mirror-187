import numpy as np
import anndata

from .._utils import Base

from tqdm.notebook import tqdm

from licorice_font import font_format

note = font_format("NOTE", ["BLUE"])

class kNN(Base):
    def __init__(self, adata, k=10, distances_key="X_dist", use_key="X_pca"):

        edges = set([])
        self.__parse__(locals())

    def _configure_distances(self):
        if not hasattr(self, "_distances"):
            if not self.distances_key in self.adata.obsp_keys():
                print(" - [{}] | Computing distance matrix".format(note))
                compute_distance_matrix(self.adata, use_key=self.use_key)
            self._distances = self.adata.obsp[self.distances_key]

    def _configure_indices(self):
        if not hasattr(self, "_indices"):
            print(" - [{}] | Configuring indices from distance matrix".format(note))
            self._indices = np.argpartition(self.distances, self.k, axis=1)[:, : self.k]

    def indices_from_annoy(self, graph_idx):    
        print(" - [{}] | Configuring provided graph index".format(note))
        self._indices = [graph_idx.get_nns_by_item(i, int(self.k + 1))[1:] for i in tqdm(range(len(self.adata)))]
        
    @property
    def distances(self):
        self._configure_distances()
        return self._distances

    @property
    def indices(self):
        self._configure_indices()
        return self._indices
    
    @property
    def n_cells(self):
        return self.adata.shape[0]
        
    def _add_edge(self, i, j):
        if i != j:
            self.edges.add(tuple(sorted([i, j])))

    def __call__(self, graph_idx=None):
        
        if not isinstance(graph_idx, type(None)):
            self.indices_from_annoy(graph_idx)
        
        print(" - [{}] | Generating edge list".format(note))
        for i in tqdm(range(self.n_cells)):
            for j in self.indices[i]:
                self._add_edge(i, j)

        return np.array(list(self.edges))


def construct_kNN_graph(
    adata: anndata.AnnData,
    graph_idx=None,
    k: int = 10,
    distances_key: str = "X_dist",
    key_added: str = "edges",
    use_key="X_pca",
):

    Graph = kNN(adata, k=k, distances_key=distances_key, use_key=use_key)
    adata.uns[key_added] = Graph(graph_idx)
