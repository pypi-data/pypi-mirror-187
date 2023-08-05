
import vinplots
import numpy as np
import matplotlib.pyplot as plt


class PlotUMAP:
    def __init__(self, adata, figsize=0.8, c=None):

        self.adata = adata
        self.fig, self.axes = vinplots.quick_plot(
            nplots=1, ncols=1, figsize=figsize, rm_ticks=True, spines_to_delete="all"
        )
        self.c = c

    def _group_attributes(self, groupby, zorder_preset):

        self.grouped = self.adata.obs.groupby(groupby)

        GroupDict = {}

        for n, (group, group_df) in enumerate(self.grouped):
            GroupDict[group] = {}
            if group in zorder_preset.keys():
                GroupDict[group]["zorder"] = zorder_preset[group]
            else:
                GroupDict[group]["zorder"] = n + 1

            GroupDict[group]["c"] = self.c[group]
            xu = self.adata[group_df.index].obsm["X_umap"]
            GroupDict[group]["x"], GroupDict[group]["y"] = xu[:, 0], xu[:, 1]

        self.GroupDict = GroupDict

    def __call__(self, s=2, groupby="Annotation", zorder_preset={"undiff": 0}, c="lightgrey"):
        
        obs_cols = self.adata.obs.columns.tolist()
        
        if not isinstance(groupby, type(None)):
            self._group_attributes(groupby, zorder_preset)
        
        else:
            self.GroupDict = {"all_cells": {}}
            X_umap = self.adata.obsm['X_umap']
            self.GroupDict["all_cells"]['x'], self.GroupDict["all_cells"]['y'] = X_umap[:,0], X_umap[:,1]
            
            if c in obs_cols:
                _c = self.adata.obs[c].values
                c_idx = np.argsort(_c)
                self.GroupDict['all_cells']['c'] = _c[c_idx]
                self.GroupDict["all_cells"]['x'] = self.GroupDict["all_cells"]['x'][c_idx]
                self.GroupDict["all_cells"]['y'] = self.GroupDict["all_cells"]['y'][c_idx]

            elif not isinstance(c, type(None)):
                self.GroupDict['all_cells']['c'] = c

        for group, group_dict in self.GroupDict.items():
            img = self.axes[0].scatter(**group_dict, s=s, label=group)
        
        if not isinstance(groupby, type(None)):
            self.axes[0].legend(edgecolor="w", fontsize=8, loc=(1, 0.4), markerscale=2)
            
        if c in obs_cols:
            plt.colorbar(mappable=img, shrink=0.5)
            self.axes[0].set_title(c)
            
        
def plot_umap(
    adata, groupby: str = None, c: dict = None, figsize: float = 0.8, s: float = 2, zorder_preset = None,
):

    plot_umap = PlotUMAP(adata, figsize=figsize, c=c)

    return plot_umap(s=s, groupby=groupby, zorder_preset=zorder_preset, c=c)
