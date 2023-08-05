
import numpy as np
import pandas as pd
from autodevice import AutoDevice
from licorice_font import font_format
import time
import torch


from .._utils import Base


note = font_format("NOTE", ["BLUE"])

class Potential(Base):
    def __init__(self, adata):

        self.__parse__(locals())

    def _to_torch(self, X):
        if isinstance(X, np.ndarray):
            return torch.from_numpy(X).to(AutoDevice())
        elif isinstance(X, pd.Series):
            return torch.from_numpy(X.values).to(AutoDevice())
        else:
            raise ValueError("Non-recognizable input passed")

    def _configure_Laplacian(self):
        if not hasattr(self, "_L"):
            self._L = self.adata.obsp["Laplacian"]

    def _configure_R(self):
        if not hasattr(self, "_R"):
            self._R = self.adata.obs["R"]

    @property
    def R(self):
        self._configure_R()
        return self._R

    @property
    def L(self):
        self._configure_Laplacian()
        return self._L

    def _compute_L_inverse(self):
        
        """
        func source: https://pytorch.org/docs/stable/generated/torch.linalg.pinv.html
        """
        if not hasattr(self, "_L_inv"):
            print(" - [{}] | Computing pseudo-inverse of the Laplacian".format(note))
            # self.adata.obsp['L_inv'] = self._L_inv.detach().cpu().numpy()
            try:
                self.pinv_engine = "torch"
                t0 = time.time()
                self._L_inv = torch.linalg.pinv(self._to_torch(self.L).to(torch.float32))
                t1 = time.time()
            except:
                self.pinv_engine = "numpy"
                t0 = time.time()
                self._L_inv = self._to_torch(np.linalg.pinv(self.L))
                t1 = time.time()
            self.pinv_time = t1 - t0
            
            print(" - [{}] | Pseudo-inversion computed over {:.3f}s with {}".format(note, self.pinv_time, self.pinv_engine))
            
    @property
    def L_inverse(self):
        self._compute_L_inverse()
        return self._L_inv

    def _compute_potential(self):
        """
        func source: 
        """
        if not hasattr(self, "_V"):
            L_inv = self.L_inverse.to(torch.float32)
            print(" - [{}] | Computing dot product w.r.t. R to obtain potential".format(note))
            self._V = torch.matmul(L_inv, self._to_torch(self.R).to(torch.float32))

    @property
    def V(self):
        self._compute_potential()
        return self._V
    
def compute_potential(adata, key_added="V"):
    
    potential = Potential(adata, )
    adata.obs["V"] = potential.V.detach().cpu().numpy()
