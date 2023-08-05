
import seaborn as sns
import numpy as np
import vinplots


class FateBiasClusterMap:
    
    def __init__(self, adata):
        
        self.adata = adata
        
    @property
    def fates(self):
        return self.adata.uns['fates']
        
    @property
    def fate_bias(self):
        return self.adata.obsm["fate_bias"]
    
    @property
    def S(self):
        return self.adata.obsm['S']
    
    @property
    def fate_bias(self):
        return self.adata.obsm['fate_bias']
    
    @property
    def sorted_fate_idx(self):
        
        if not hasattr(self, "_sorted_fate_idx"):
    
            self._sorted_fate_idx = np.array([])
            df = self.adata.obs.copy()

            for fate in self.fates:
                idx = df.loc[df["Annotation"] == fate].index.to_numpy()
                self._sorted_fate_idx = np.append(self._sorted_fate_idx, idx)

        return self._sorted_fate_idx
    
    @property
    def color_palette(self):
        cp = vinplots.colors.LARRY_in_vitro
        cp["undiff"] = "#f0efeb"
        return cp
    
    @property
    def row_colors(self):
        return self.adata[self.sorted_fate_idx].obs["Annotation"].map(self.color_palette).to_numpy()
    
    @property
    def column_colors(self):
        return [self.color_palette[fate] for fate in self.fates]
        
    def __call__(self, subset: tuple = None, title=None):
        
        if not isinstance(subset, type(None)):
            key, val = subset
            df = self.adata.obs.copy()
            _adata = self.adata[df.loc[df[key] == val].index]
            self.__init__(_adata)
                
        cg = sns.clustermap(
            self.fate_bias,
            figsize=(3, 6),
            cmap="Blues",
            xticklabels=self.fates,
            yticklabels=False,
            row_cluster=True,
            row_colors=self.row_colors,
            col_colors=self.column_colors,
            cbar_pos=(1, 0.4, 0.05, 0.2),
            vmin=0,
            vmax=1,
        )
        cg.ax_row_dendrogram.set_visible(False)
        if isinstance(title, type(None)):
            title = "{} cells".format(self.fate_bias.shape[0])
        cg.ax_col_dendrogram.set_title(title, fontsize=10)
        
def plot_fate_bias_clustermap(adata, subset=("Time point", 2), title=None):
    
    fatebias_clustermap = FateBiasClusterMap(adata)
    fatebias_clustermap(subset=subset)
